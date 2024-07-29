import streamlit as st
from groq import Groq
import random

from langchain.chains import ConversationChain, LLMChain # ConversationChain is a specific type of chain that is designed for managing conversations. It typically involves a sequence of interactions where the AI model processes and responds to user inputs in a coherent manner. It represents a chain that involves the use of large language models to process and generate text.

from langchain_core.prompts import(
    ChatPromptTemplate,
    HumanMessagePromptTemplate, 
    MessagesPlaceholder,
) # HumanMessagePromptTemplate is a sepcific type of template designed to handle messages from the human user. It ensures that the human input is formatted and integrated properly within the overall prompt template.
#MessagesPlaceholder is another specific type of template that can be used to insert messages into the prompt(can be both human and system-generated). It helps in maintaining the context of the conversation by ensuring the past messages are included in the current prompt.

from langchain_core.messages import SystemMessage #SystemMessage is class used within LangChain framework to represent the output or response generated by the AI model or system. Used to distinguish between human and system

from langchain.chains.conversation.memory import ConversationBufferMemory #ConversationBufferMemory is a class in langchain to manage and store the conversation history in memory.

from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv() #loading the dotenv. Used to load the environment variables.

def main():
    #Get the groq api key
    GROQ_API_KEY = "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"

    #The title and greeting message
    st.title("Personal Chatbot")
    st.write("Hey there! I'm your personal chatbot. I can help answer your questions, provide information or just chat with you. Let's start conversing :)")

    #Adding the customization options to the sidebar. Will include the previous chats
    st.sidebar.title('Customization')

    conversational_memory_length = st.sidebar.slider('Conversational memory length:', 1, 10,value = 5) #range is from 1 to 10. Default value is 5

    memory = ConversationBufferMemory(k = conversational_memory_length, memory_key = "chat_history", return_messages = True) #k is a paramerter that specifier how many previous messages to retain in the memory buffer. Here it is based on the value given by the user using the slider. memory_key sets the key used to store the memory buffer in a dictionary or other data structure. It's a way to identify and access the stored chat history.return_messages when it is set to true will return the actual content of the messages, otherwise it will return some other messages like message IDs etc.

    user_question = st.text_input("Ask a question: ")

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    else:
        for message in st.session_state.chat_history:
            memory.save_context(
                {'input':message['human']},
                {'output':message['AI']}
            )

    groq_chat = ChatGroq(
        groq_api_key = GROQ_API_KEY,
        model_name = 'mixtral-8x7b-32768'
    )

    if user_question:
        #using from_messages class method that allows you to create a ChatPromptTemplate by specifying a list of message objects. Each message object represents a part of the conversation, such as system messages or user messages.
        prompt = ChatPromptTemplate.from_messages(
            [
                #MessagesPlaceholder is a class used as a placeholder within a prompt template to dynamically insert the conversation history or other contextual information. variable_name specifies the name of the variable that will be used to insert the conversation history into the prompt
                MessagesPlaceholder(
                    variable_name = "chat_history"
                ),

                #HumanMessagePromptTemplate is a class used to define the format of messages coming from the human user within a prompt template. It helps structure how user inputs should be formatted. human_input is a placeholder that will get replaced with the actual content of the user input.
                HumanMessagePromptTemplate.from_template(
                    "{human_input}"
                ),
            ]
        )

        conversation = LLMChain(
            llm = groq_chat,
            prompt = prompt,
            verbose = True, #when verbose is set to True, additional details about the process, such as debug information or internal state changes.
            memory = memory,
        )

        response = conversation.predict(human_input = user_question)
        message = {'human':user_question,'AI':response} #since i have save message as dictionary above with human and AI as keys
        st.session_state.chat_history.append(message)
        st.write("Chatbot:", response)




if __name__ == "__main__":
    main()