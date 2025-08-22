
"""Sidebar UI components for the Streamlit application."""

import streamlit as st

from config import MODEL_OPTIONS
from services.chat_service import create_chat, delete_chat
from utils.async_helpers import reset_connection_state


def create_history_chat_container():
    """Create a container for chat history selection."""
    history_container = st.sidebar.container(height=200, border=None)
    with history_container:
        chat_history_menu = [
            f"{chat['chat_name']}_::_{chat['chat_id']}"
            for chat in st.session_state["history_chats"]
        ]
        chat_history_menu = chat_history_menu[:50][::-1]

        if chat_history_menu:
            current_chat = st.radio(
                label="History Chats",
                format_func=lambda x: x.split("_::_")[0] + "..." if "_::_" in x else x,
                options=chat_history_menu,
                label_visibility="collapsed",
                index=st.session_state["current_chat_index"],
                key="current_chat",
            )

            if current_chat:
                st.session_state["current_chat_id"] = current_chat.split("_::_")[1]


def create_sidebar_chat_buttons():
    """Create new chat and delete chat buttons."""
    with st.sidebar:
        c1, c2 = st.columns(2)
        create_chat_button = c1.button(
            "New Chat", use_container_width=True, key="create_chat_button"
        )
        if create_chat_button:
            create_chat()
            st.rerun()

        delete_chat_button = c2.button(
            "Delete Chat", use_container_width=True, key="delete_chat_button"
        )
        if delete_chat_button and st.session_state.get("current_chat_id"):
            delete_chat(st.session_state["current_chat_id"])
            st.rerun()


def create_model_select_widget():
    """Simple model selection widget."""
    params = st.session_state["params"]
    params["model_id"] = st.sidebar.selectbox(
        "🔎 Choose model", options=MODEL_OPTIONS.keys(), index=0
    )


def create_provider_select_widget():
    """Create provider selection widget with state management."""
    params = st.session_state.setdefault("params", {})
    default_provider = params.get("model_id", list(MODEL_OPTIONS.keys())[0])
    default_index = list(MODEL_OPTIONS.keys()).index(default_provider)
    
    selected_provider = st.sidebar.selectbox(
        "🔎 Choose Model",
        options=list(MODEL_OPTIONS.keys()),
        index=default_index,
        key="provider_selection",
        on_change=reset_connection_state,
    )
    params["model_id"] = selected_provider
    params["model_name"] = MODEL_OPTIONS[selected_provider]
    params["provider_index"] = list(MODEL_OPTIONS.keys()).index(selected_provider)


def create_advanced_configuration_widget():
    """Create advanced configuration options for the model."""
    params = st.session_state["params"]
    with st.sidebar.expander("⚙️  Basic config", expanded=False):
        params["max_tokens"] = st.number_input(
            "Max tokens",
            min_value=1024,
            max_value=10240,
            value=4096,
            step=512,
        )
        params["temperature"] = st.slider("Temperature", 0.0, 1.0, step=0.05, value=1.0)
