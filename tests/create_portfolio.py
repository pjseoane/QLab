# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import streamlit as st
import utils.data_fetching as data_fetching

st.title("Define Your Portfolio")

if "tickers" not in st.session_state:
    st.session_state.tickers = ["AAPL.US", "MSFT.US"]

new_ticker = st.text_input("Add new ticker:")

col1, col2 = st.columns([1, 3])

with col1:
    if st.button("Add"):
        if new_ticker and new_ticker.upper() not in st.session_state.tickers:
            st.session_state.tickers.append(new_ticker.upper())

with col2:
    for t in st.session_state.tickers:
        if st.button(f"Remove {t}", key=f"remove_{t}"):
            st.session_state.tickers.remove(t)
            st.experimental_rerun()

st.write("### Current Tickers")
st.write(st.session_state.tickers)
