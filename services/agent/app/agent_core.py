import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def recommend_problem(summary_text: str):
    prompt = f"""You are a logistics solutions architect. Based on these dataset summaries:
{summary_text}

Suggest one high-impact problem to solve for the company.
Explain briefly why, list required components, and outline a short plan."""
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    text = response.text.strip() if hasattr(response, 'text') else str(response)
    return {'recommendation': text}

if __name__ == '__main__':
    sample = 'Orders data, delivery performance metrics, and vehicle routes available.'
    print(recommend_problem(sample))
