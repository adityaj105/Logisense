import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Disable warnings for better UI
import warnings
warnings.filterwarnings("ignore")

def show_eda(datasets: dict):
    """Display simple exploratory data analysis for each dataset."""
    if not datasets:
        st.info("No datasets loaded for EDA.")
        return

    for name, df in datasets.items():
        if df is None or df.empty:
            st.warning(f"Dataset '{name}' is empty or invalid.")
            continue

        st.subheader(f"📊 EDA for {name}")

        # Show basic statistics
        st.write("**Dataset Shape:**", df.shape)
        st.write("**Column Overview:**")
        st.dataframe(pd.DataFrame({
            "Column": df.columns,
            "Type": df.dtypes.astype(str),
            "Missing Values": df.isnull().sum(),
            "Unique Values": df.nunique()
        }).reset_index(drop=True))

        # Correlation heatmap for numeric columns
        numeric_df = df.select_dtypes(include=['int64', 'float64'])
        if not numeric_df.empty:
            st.write("**Correlation Heatmap:**")
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
            st.pyplot(fig)
        else:
            st.info("No numeric columns available for correlation heatmap.")

        # Show value counts for categorical columns
        cat_cols = df.select_dtypes(include=['object']).columns
        if len(cat_cols) > 0:
            st.write("**Categorical Distribution (Top 3 columns):**")
            for col in cat_cols[:3]:
                st.write(f"**{col}**")
                fig, ax = plt.subplots(figsize=(6, 3))
                df[col].value_counts().head(10).plot(kind='bar', ax=ax)
                ax.set_title(f"Distribution of {col}")
                st.pyplot(fig)

        # Spacer between datasets
        st.markdown("---")
