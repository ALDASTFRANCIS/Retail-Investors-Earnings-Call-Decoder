import os
import requests
from fastapi import FastAPI, HTTPException
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel

app = FastAPI(title="Earnings Call Decoder")

# Configuration
FMP_API_KEY = "asdfghjklqwertyuiop"
LLM_MODEL = "llama3" 

# Initialize the local AI model via Ollama
llm = Ollama(model=LLM_MODEL)

# Add this class for data validation
class ManualText(BaseModel):
    text: str

# Add this new endpoint
@app.post("/decode-manual")
async def decode_manual(input_data: ManualText):
    try:
        summary = summarize_financial_text(input_data.text)
        return {"analysis": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_mock_transcript() -> str:
    """Returns a fake transcript so you can test the AI without an API Key."""
    return """
    Operator: Good day everyone and welcome to the Apple Inc. Third Quarter Fiscal Year 2024 Earnings Conference Call.
    
    Tim Cook (CEO): Thank you. We are pleased to report record revenue of $85 billion, up 5% year over year. 
    Our services segment hit an all-time high. We are investing heavily in Generative AI and expect to integrate it across all devices by late 2025.
    However, we see headwinds in the China market due to local competition. Supply chain constraints remain a risk for the iPhone 16 rollout.
    We plan to remain cash neutral and continue our share buyback program.
    """

def fetch_transcript(ticker: str, year: int, quarter: int) -> str:
    url = f"https://financialmodelingprep.com/api/v3/earning_call_transcript/{ticker}?year={year}&quarter={quarter}&apikey={FMP_API_KEY}"
    
    response = requests.get(url)

    if response.status_code != 200:
        print("API failed or is restricted. Using MOCK data for testing.")
        return get_mock_transcript()
        
    data = response.json()
    if not data:
        print("Transcript not found. Using MOCK data for testing.")
        return get_mock_transcript()
        
    return data[0]['content']

def summarize_financial_text(text: str) -> str:

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=200)
    chunks = text_splitter.split_text(text)

    primary_text = chunks[0] + chunks[1] if len(chunks) > 1 else chunks[0]

    prompt_template = """
    You are an expert financial analyst focusing on long-term value investing (3+ year hold).
    Read the following excerpt from a company's earnings call transcript and extract the following:
    
    1. The Moat & Strategy: What is their long-term growth strategy?
    2. Forward Guidance: What are their financial predictions for the next year?
    3. Risk Factors: What headwinds or dangers did management mention?
    
    Transcript Excerpt:
    {text}
    
    Provide the response in a clean, bulleted format.
    """
    
    prompt = PromptTemplate(template=prompt_template, input_variables=["text"])
    final_prompt = prompt.format(text=primary_text)

    return llm.invoke(final_prompt)


@app.get("/decode/{ticker}")
async def decode_earnings(ticker: str, year: int, quarter: int):

    try:

        raw_text = fetch_transcript(ticker.upper(), year, quarter)

        summary = summarize_financial_text(raw_text)

        return {
            "ticker": ticker.upper(),
            "period": f"Q{quarter} {year}",
            "analysis": summary
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
