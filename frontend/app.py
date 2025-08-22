"""Main Streamlit application for the Azercell Knowledge Base chatbot."""

import asyncio
import atexit
import os

import nest_asyncio
import streamlit as st

from apps import mcp_playground
from services.chat_service import init_session
from utils.async_helpers import on_shutdown

nest_asyncio.apply()

page_icon_path = os.path.join(".", "icons", "playground.png")

st.set_page_config(
    page_title="Azercell Knowledge Base",
    page_icon=(page_icon_path),
    layout="wide",
    initial_sidebar_state="expanded",
)

with open(os.path.join(".", ".streamlit", "style.css")) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def main():
    """Initialize and run the main application."""
    if "loop" not in st.session_state:
        st.session_state.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(st.session_state.loop)

    atexit.register(on_shutdown)
    init_session()
    mcp_playground.main()


if __name__ == "__main__":
    main()
