import os
import sys
from pathlib import Path
import importlib.util

THIS_FILE = Path(__file__).resolve()
ROOT = THIS_FILE.parents[3]
ROOT_STR = str(ROOT)
if ROOT_STR not in sys.path:
    sys.path.insert(0, ROOT_STR)

import streamlit as st
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

try:
    from services.streamlit_app.app.utils.ingest import load_all, profile_df
except Exception:
    try:
        from utils.ingest import load_all, profile_df
    except Exception as e:
        st.set_page_config(layout="wide")
        st.title("LogiSense — import error")
        st.error("Failed to import ingestion utilities.")
        st.code(str(e))
        st.stop()

show_eda = None
try:
    from components.edas import show_eda
except Exception:
    try:
        from services.streamlit_app.app.components.edas import show_eda
    except Exception:
        edas_path = ROOT / "services" / "streamlit_app" / "app" / "components" / "edas.py"
        if edas_path.exists():
            spec = importlib.util.spec_from_file_location("components.edas", edas_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules["components.edas"] = module
            spec.loader.exec_module(module)
            show_eda = getattr(module, "show_eda", None)

if show_eda is None:
    st.set_page_config(layout="wide")
    st.title("LogiSense — missing EDA")
    st.error("EDA component not found. Ensure components/edas.py exists.")
    st.stop()

st.set_page_config(page_title="LogiSense — Logistics Analyst Assistant", layout="wide")
st.title("🚛 LogiSense — Logistics Analyst Assistant")

st.sidebar.header("Configuration")
data_folder = st.sidebar.text_input("Data folder", "data")
api_key_input = st.sidebar.text_input("Gemini API Key (optional)", type="password")
api_key = api_key_input or os.getenv("GEMINI_API_KEY", "")

if api_key:
    try:
        genai.configure(api_key=api_key)
    except Exception as e:
        st.sidebar.error(f"Gemini configuration failed: {e}")
else:
    st.sidebar.info("Provide GEMINI_API_KEY in sidebar or .env to enable the Agent.")

if "datasets" not in st.session_state:
    st.session_state["datasets"] = {}

if st.sidebar.button("Load Data"):
    with st.spinner("Loading datasets..."):
        ds = load_all(data_folder)
        st.session_state["datasets"] = ds
        st.success("Data loaded.")

datasets = st.session_state.get("datasets", {})

tabs = st.tabs(["Dataset Summary", "EDA", "Agent"])

with tabs[0]:
    st.header("Dataset Summary")
    if not datasets:
        st.info("No datasets loaded. Use sidebar → Load Data.")
    else:
        for name, df in datasets.items():
            st.subheader(name)
            if df is None:
                st.warning(f"{name} not found or failed to read.")
                continue
            p = profile_df(df)
            st.write(f"Rows: {p['rows']} • Columns: {len(p['cols'])}")
            st.dataframe(pd.DataFrame(p["missing_perc"], index=[0]).T.rename(columns={0: "missing_pct"}))
            st.write("Sample rows:")
            st.dataframe(pd.DataFrame(p["sample"]).head(5))

with tabs[1]:
    st.header("Exploratory Data Analysis")
    if not datasets:
        st.info("Load data first to run EDA.")
    else:
        try:
            show_eda(datasets)
        except Exception as e:
            st.error("EDA failed.")
            st.code(str(e))

with tabs[2]:
    st.header("Agent Recommendation")
    if not datasets:
        st.info("Load data to enable the agent.")
    else:
        summary = "\n".join(
            f"{k}: {v.shape[0]} rows, {v.shape[1]} cols"
            for k, v in datasets.items() if v is not None
        )
        st.text_area("Summary sent to AI", summary, height=200)
        prompt = st.text_area("Optional instruction for the agent", value="Suggest one high-impact logistics problem and a short plan.")
        if st.button("Ask Agent"):
            if not api_key:
                st.error("No Gemini API key configured.")
            else:
                model = None
                model_name = None
                for candidate in ("gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.0-flash", "gemini-flash-latest"):
                    try:
                        model = genai.GenerativeModel(candidate)
                        model_name = candidate
                        break
                    except Exception:
                        model = None
                if model is None:
                    st.error("No compatible Gemini model available for this API key.")
                else:
                    full_prompt = f"You are a logistics analyst. Based on these dataset summaries:\n{summary}\nInstruction: {prompt}"
                    try:
                        response = model.generate_content(full_prompt)
                        text = getattr(response, "text", None) or str(response)
                        st.success("Agent Recommendation")
                        st.write(text)
                        st.caption(f"Model used: {model_name}")
                    except Exception as e:
                        st.error("LLM call failed.")
                        st.code(str(e))
