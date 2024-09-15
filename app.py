import replicate
import streamlit as st
import requests as res
from pathlib import Path
import os
st.set_page_config(page_title="AI Chatbot",page_icon="🤖")

llm=""
st.title("Chatbot")
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file =current_dir/"styles"/"main.css"
with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()),unsafe_allow_html=True)

with st.sidebar:
    st.write('This chatbot is created using the open-source Llama 2 LLM model from Meta.')
    if 'REPLICATE_API_TOKEN' in st.secrets:
        st.success('API key already provided!', icon='✅')
        replicate_api = st.secrets['REPLICATE_API_TOKEN']
    else:
        replicate_api = st.text_input('Enter Replicate API token:', type='password')
        if not (replicate_api.startswith('r8_')):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')
    os.environ['REPLICATE_API_TOKEN'] = replicate_api
    st.subheader('Models')
    selected_model = st.sidebar.selectbox('Choose a Llama2 model', ['Llama2-7B', 'Llama2-13B','Llama2-70b','Llama3-8b'], key='selected_model')
    if selected_model == 'Llama2-7B':
        llm = 'a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea'
    elif selected_model == 'Llama2-13B':
        llm = 'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5'
    elif selected_model=='Llama2-70b':
        llm = "meta/codellama-70b-instruct:a279116fe47a0f65701a8817188601e2fe8f4b9e04a518789655ea7b995851bf"
    elif selected_model=='Llama3-8b':
        llm = "meta/meta-llama-3-8b-instruct"

    #clear CHAT history button on slider
    def clear_chat_history():
      if replicate_api:
        st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
      else :
          st.session_state.messages=[{"role": "assistant", "content": "HI, I Will Copy YOU."}]
    st.button('Clear Chat History', on_click=clear_chat_history)
if replicate_api:
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hi, How May I Help You."}]
    st.session_state.messages[0]={"role": "assistant", "content": "Hi, How May I Help You."}
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])



    #for generating LLaMA2 response.
    def generate_llama2_response(prompt_input):
     string_dialogue = "Instruction based agent to response the book or student question related for topic from student and able to answers and support following things suggest answers for question based asked from LLM agent Suggest or recommend book or paper, articles  based on student query using contextual data  "
     for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
     output = replicate.run(
        llm,
        input={"prompt": f"{string_dialogue} {prompt_input} Assistant: ",
               "temperature": 0.1, "top_p": 0.01,"max_length":128, "repetition_penalty": 1})
     return output
    prompt = st.chat_input("AI CHAT BOT")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
    if st.session_state.messages[-1]["role"] != "assistant":

        with st.chat_message("assistant"):
          full_response = ''
          placeholder = st.empty()
          try:
            with st.spinner("Thinking..."):
                response = generate_llama2_response(prompt)
                for item in response:
                    full_response += item
                    placeholder.markdown(full_response)
                placeholder.markdown(full_response)
          except:
            with st.spinner("Thinking..."):
              st.warning("There is some issue with chatbot.It is working as Copybot.")
              full_response=st.session_state.messages[-1]["content"]
              placeholder.markdown(full_response)
          st.session_state.messages.append({"role": "assistant", "content": full_response})
else:
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hi , I Will Copy YOU."}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    prompt = st.chat_input("COPYBOT")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            full_response += st.session_state.messages[-1]["content"]
            message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})



