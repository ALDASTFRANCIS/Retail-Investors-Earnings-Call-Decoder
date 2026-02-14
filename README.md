# Retail-Investors-Earnings-Call-Decoder

This tool automates the analysis of corporate earnings call transcripts. It uses a locally running Large Language Model (LLM) to extract long-term investment insights—specifically focusing on company strategy, forward guidance, and risk factors—so you don't have to read the entire 30-page document.

Features

    Local AI Processing: Uses Ollama (Llama 3) to process text locally for free.

    Live Data Fetching: Connects to the Financial Modeling Prep (FMP) API to get real-time transcripts.

    Manual Mode: Paste any text (news, reports, or transcripts) to analyze it without an API key.

    Interactive Dashboard: A simple Streamlit interface to search for stocks or paste text.

Architecture

    Frontend: Streamlit (Web Interface)

    Backend: FastAPI (Python API)

    AI Engine: Ollama (Local Llama 3 Model)

    Orchestration: LangChain (Text chunking and prompting)
