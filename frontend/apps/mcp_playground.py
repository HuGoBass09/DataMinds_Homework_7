"""Main chat playground application for the Azercell Knowledge Base."""

import traceback
import requests
import streamlit as st

import ui_components.sidebar_components as sd_compents
from services.chat_service import _append_message_to_session, get_current_chat


def request_stream(prompt: str, modelName: str, api_url: str):
    """Send request to FastAPI backend and stream the response."""
    try:
        data = {"prompt": prompt, "modelName": modelName}
        print(f"Sending request to API: {api_url} with data: {data}", flush=True)
        
        with requests.post(api_url, json=data, stream=True) as resp:
            if resp.status_code != 200:
                detail = resp.text if hasattr(resp, 'text') else str(resp.status_code)
                st.error(f"API Error {resp.status_code}: {detail}")
                return
            
            # Stream the response line by line
            for line in resp.iter_lines(decode_unicode=True):
                if line:  # Filter out empty lines
                    yield line
                    
    except requests.exceptions.RequestException as e:
        st.error(f"Network error while calling API: {e}")
        return


def main():
    """Main application entry point."""
    with st.sidebar:
        st.subheader("Chat History")
    sd_compents.create_history_chat_container()
    st.header("Chat with Agent")
    messages_container = st.container(border=True, height=600)
    
    if st.session_state.get("current_chat_id"):
        st.session_state["messages"] = get_current_chat(
            st.session_state["current_chat_id"]
        )
        for m in st.session_state["messages"]:
            with messages_container.chat_message(m["role"]):
                if "tool" in m and m["tool"]:
                    st.code(m["tool"], language="yaml")
                if "content" in m and m["content"]:
                    st.markdown(m["content"])

    user_text = st.chat_input("Ask a question about Azercell.")

    sd_compents.create_sidebar_chat_buttons()
    sd_compents.create_provider_select_widget()

    if user_text is None:
        st.stop()

    api_url = "http://backend:8000/generate"
    if user_text:
        user_text_dct = {"role": "user", "content": user_text}
        _append_message_to_session(user_text_dct)
        with messages_container.chat_message("user"):
            st.markdown(user_text)

        with st.spinner("Thinking…", show_time=True):
            print(
                "Running agent with user input:",
                user_text,
                "and model: ",
                st.session_state["params"]["model_id"],
                flush=True,
            )
            try:
                print(
                    "temperature:",
                    st.session_state["params"].get("temperature"),
                    flush=True,
                )
                print(
                    "max_tokens:",
                    st.session_state["params"].get("max_tokens"),
                    flush=True,
                )

                response_stream = request_stream(
                    prompt=user_text,
                    modelName=st.session_state["params"]["model_name"],
                    api_url=api_url,
                )
                print("Response stream received:", response_stream, flush=True)
                with messages_container.chat_message("assistant"):
                    response = st.write_stream(response_stream)
                    response_dct = {"role": "assistant", "content": response}
            except Exception as e:
                response = f"⚠️ Something went wrong: {str(e)}"
                st.error(response)
                st.code(traceback.format_exc(), language="python")
                st.stop()
        
        _append_message_to_session(response_dct)
