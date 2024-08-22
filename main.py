import streamlit as st
from service_factory import ServiceFactory
import json

def run_conversation(user_query):
    service_factory = ServiceFactory()
    messages = [{"role": "user", "content": user_query}]

    response_message = None
    function_response = None

    tools = [
        {"type": "web_information_retrieval", "name": "web_information_retrieval"},
        {"type": "information_retrieval", "name": "information_retrieval"},
        {"type": "e_commerce_search", "name": "e_commerce_search"},
        {"type": "travel_and_navigation", "name": "travel_and_navigation"},
        {"type": "send_calendar_invite", "name": "send_calendar_invite"},
    ]

    tool_choice = tools[0] 

    service_type = tool_choice["type"]
    service = service_factory.create_service(service_type)

    if service_type in ["web_information_retrieval", "e_commerce_search", "travel_and_navigation"]:
        function_response = service.web_information_retrieval(user_query) if service_type == "web_information_retrieval" else service.e_commerce_search(user_query)
        for i, result in enumerate(function_response['results']):
            st.write(f"### [{result['title']}]({result['url']})")
            st.write(result['content'])
            if i < len(function_response['images']):
                st.image(function_response['images'][i])

    elif service_type == "information_retrieval":
        function_response = service.information_retrieval(user_query)
    elif service_type == "send_calendar_invite":
        pass

    return function_response or response_message

st.title("Glucon_D Chatbot")
user_query = st.text_input("Enter your query")
if st.button("Run"):
    if user_query:
        response = run_conversation(user_query)
