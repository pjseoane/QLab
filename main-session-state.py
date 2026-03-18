import streamlit as st

# initialise screen state
if "screen" not in st.session_state:
    st.session_state["screen"] = "welcome"

# ── Welcome screen ─────────────────────────────────────────────────────────────
if st.session_state["screen"] == "welcome":
    st.title("👋 Welcome to Stock Dashboard")
    st.write("Configure your settings to get started")

    with st.form("setup"):
        ticker   = st.text_input("First ticker", "AAPL")
        period   = st.selectbox("Period", ["1mo", "3mo", "1y"])
        submitted = st.form_submit_button("Get Started →")

    if submitted:
        st.session_state["ticker"] = ticker
        st.session_state["period"] = period
        st.session_state["screen"] = "dashboard"   # switch screen
        st.rerun()

# ── Dashboard screen ───────────────────────────────────────────────────────────
elif st.session_state["screen"] == "dashboard":
    st.title("📊 Dashboard")
    st.write(f"Showing: {st.session_state['ticker']}")

    if st.button("← Back to Welcome"):
        st.session_state["screen"] = "welcome"
        st.rerun()