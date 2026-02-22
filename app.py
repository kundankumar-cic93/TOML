import streamlit as st
import ollama

st.title("Chat with different AI Model of your choice from the selectBox")

# Set up model selection (optional, can be hardcoded)
# Ensure the model is downloaded locally using `ollama run <model_name>`
model = st.selectbox("Choose an Ollama model:", ["llama3", "gemma3:4b", "mistral", "phi3", "qwen2.5:7b-instruct"])

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from the Ollama model
    with st.chat_message("assistant"):
        # Use ollama.chat for multi-turn conversations
        response = ollama.chat(model=model, messages=st.session_state.messages, stream=True)
        # Stream the response in real-time
        full_response = ""
        placeholder = st.empty()
        for chunk in response:
            full_response += chunk['message']['content']
            placeholder.markdown(full_response + "▌") # optional: a blinking cursor effect
        placeholder.markdown(full_response)
        
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

