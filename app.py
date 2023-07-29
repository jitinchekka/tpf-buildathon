import streamlit as st
import requests

def chatbot_response(input_text):
    url = 'https://avid-infinity-386618.el.r.appspot.com/api'
    payload = {'userPrompt': input_text}
    try:
        with requests.post(url, json=payload) as response:
            response.raise_for_status()  # Check for any HTTP errors
            data = response.json()
            print(data)
            return data
    except requests.exceptions.RequestException as e:
        return f'Error: {e}'
     

def main():
    # Initialize SessionState to store chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.title("Simple Chatbot")

    # Sidebar with settings
    st.sidebar.title("Settings")
    email = st.sidebar.text_input("Email ID", "")
    # Add more settings as needed

    # Apply custom CSS to change the background color
    background_color = "#444654"
    st.markdown(
        f"""
        <style>
        body {{
            background-color: {background_color};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Main chat section
    user_input = st.text_input("You:", "")

    if st.button("Send"):
        response = chatbot_response(user_input)
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("PrivateGPT", response["privatePrompt"]))
        st.session_state.chat_history.append(("Chatbot", response["response"]))
        user_input = ""  # Clear the user input after sending

    # Display previous chats in a chat-style layout
    st.subheader("Chat")
    chat_container = st.empty()

    chat_log = ""
    for sender, message in st.session_state.chat_history:
        if sender == "You":
            chat_log += f'<div style="text-align: left; padding-left: 20px; padding: 1.5rem; color:#fff; background-color: #333;">{message}</div>'
        elif  sender == "PrivateGPT":
            chat_log += f'<div style="text-align: left; padding-left: 20px; padding: 1.5rem; color:#fff; background-color: #555;">{message}</div>'
        else:
            chat_log += f'<div style="text-align: left; padding-right: 20px; padding: 1.5rem; color:#fff; background-color: #444;">{message}</div>'

    chat_container.write(chat_log, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
