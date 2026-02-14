import streamlit as st
import requests

st.set_page_config(page_title="Earnings Decoder", layout="wide")

st.title("AI Earnings Call Decoder")
st.markdown("Summarize lengthy corporate earnings calls into actionable investment insights.")

tab1, tab2 = st.tabs(["📡 Live API Mode", "📝 Manual Paste Mode"])

with tab1:
    st.info("Fetches data from Financial Modeling Prep (Requires Paid Key for some dates)")
    col1, col2, col3 = st.columns(3)
    with col1:
        ticker = st.text_input("Stock Ticker", "AAPL")
    with col2:
        year = st.number_input("Year", min_value=2020, max_value=2026, value=2024)
    with col3:
        quarter = st.selectbox("Quarter", [1, 2, 3, 4], index=2)
    
    if st.button("Decode with API"):
        with st.spinner("Listening to the CFO..."):
            try:
                # Call backend
                response = requests.get(f"http://1271.0.0.1:8090/decode/{ticker}?year={year}&quarter={quarter}")
                if response.status_code == 200:
                    data = response.json()
                    st.divider()
                    st.subheader(f"📊 {data['ticker']} - Q{quarter} {year} Report")
                    st.markdown(data['analysis'])
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Connection Error: {e}")

with tab2:
    st.info("Paste any financial text below (News, Transcript, or Report) to test the AI.")

    raw_text = st.text_area("Paste Transcript Here:", height=300)
    
    if st.button("Analyze Text"):
        if raw_text:
            with st.spinner("Analyzing your text..."):
                try:
                    response = requests.post("http://1271.0.0.1:8090/decode-manual", json={"text": raw_text})
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.divider()
                        st.subheader("📊 Analysis Result")
                        st.markdown(result['analysis'])
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Connection Error: {e}")
        else:
            st.warning("Please paste some text first!")
