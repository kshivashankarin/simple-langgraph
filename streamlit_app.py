import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/ask"

st.set_page_config(page_title="LangGraph Chat", page_icon="💬")

st.title("💬 LangGraph Chat")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask a question..."):

    # Show user message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Call API
    try:
        payload = {
            "question": prompt,
            "thread_id": st.session_state.thread_id
        }

        response = requests.post(API_URL, json=payload)
        response.raise_for_status()

        data = response.json()

        # Save thread_id for conversation continuity
        st.session_state.thread_id = data["thread_id"]

        answer = data["answer"]
        route = data.get("route", "")
        sql_query = data.get("sql_query")

        assistant_response = answer

        if route:
            assistant_response += f"\n\n**Route:** `{route}`"

        if sql_query:
            assistant_response += f"\n\n**SQL Query:**\n```sql\n{sql_query}\n```"

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": assistant_response
            }
        )

        with st.chat_message("assistant"):
            st.markdown(assistant_response)

    except Exception as e:
        st.error(f"Error: {e}")

# Sidebar
with st.sidebar:
    st.subheader("Session")
    st.write(
        f"Thread ID: `{st.session_state.thread_id}`"
        if st.session_state.thread_id
        else "No active thread"
    )

    if st.button("New Chat"):
        st.session_state.messages = []
        st.session_state.thread_id = None
        st.rerun()
