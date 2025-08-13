import streamlit as st
import requests
import time
import uuid

# --- Streamlit app configuration ---
st.set_page_config(page_title="Streaming bot", page_icon="❔")
# --- Page title ---
st.title("AI Chat Assistant")

# --- Initialize session_id in Streamlit state ---
# This ensures all messages in the same session share the same ID
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4()) # Generate a unique session ID

# --- Store chat history in session state ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display previous chat messages ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Chat input box for user query ---
if user_input := st.chat_input("Ask anything..."):
    
    # Backend API endpoint configuration
    API_URL = "http://localhost:8000/stream"
    data = {
            "query": user_input,
            "session_id": st.session_state.session_id
        }
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Create an empty placeholder for streaming the assistant's response 
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # --- Send the request and stream the response ---
        with requests.post(API_URL, json=data, stream=True) as r:
            for chunk in r.iter_content(chunk_size=None):
                if chunk:
                    # Decode each chunk from bytes to string
                    text_chunk = chunk.decode("utf-8")
                    # Append chunk to the ongoing response
                    full_response += text_chunk
                    # Update the Streamlit placeholder in real-time with partial response
                    message_placeholder.markdown(full_response + "▌")
                    time.sleep(0.02) # Small delay for smoother streaming effect
                    
        # Replace with the final response
        message_placeholder.markdown(full_response)
        
    # Add assistant's final message to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})