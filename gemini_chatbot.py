import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Gemini ChatBot", layout="centered")

st.title("Gemini ChatBot")
st.write("Powered by Google Generative AI")

if "history" not in st.session_state:
    st.session_state["history"] = []

# Sidebar for API Key input
st.sidebar.title("API Key Configuration")
api_key_input = st.sidebar.text_input("Enter your Gemini API key", type="password")

# Store API key in session state
if api_key_input:
    st.session_state["api_key"] = api_key_input

def model_response(user_input):
    # Retrieve the API key from session state
    api_key = st.session_state.get("api_key", None)
    if not api_key:
        return "API key is missing. Please enter it in the sidebar."
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(user_input)
    return response.text

# Display chat history
for user_message, bot_message in st.session_state.history:
    st.markdown(f"""
    <div style="
        background-color: #d1d3e0;
        border-radius: 15px;
        padding: 10px 15px;
        margin: 5px 0;
        max-width: 70%;
        text-align: left;
        display: inline-block;
    ">
        <p style="margin: 0; font-size: 16px; line-height: 1.5;"><b>You:</b> {user_message} </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="
        background-color: #e1ffc7;
        border-radius: 15px;
        padding: 10px 15px;
        margin: 5px 0;
        max-width: 70%;
        text-align: left;
        display: inline-block;
    ">
        <p style="margin: 0; font-size: 16px; line-height: 1.5;"><b>Bot:</b> {bot_message} </p>
    </div>
    """, unsafe_allow_html=True)

# Form for user input
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Enter your text", value="", max_chars=2000)
    submit_button = st.form_submit_button("Send")

    if submit_button:
        if user_input:
            response = model_response(user_input)
            st.session_state.history.append((user_input, response))
            st.rerun()
        else:
            st.warning("Please Enter A Prompt")
