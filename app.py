from tavily import TavilyClient
from ics import Calendar, Event
from datetime import datetime, timedelta
import yagmail
from groq import Groq
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import streamlit as st
import os

def web_information_retrieval(user_query):
  tavily_client = TavilyClient(api_key=os.environ.get('TAVILY_API_KEY'))

  response = tavily_client.search(user_query,search_depth="basic",include_answer=True)

  return response['answer']


def information_retrieval(user_query):
    client = Groq(api_key=os.environ.get('GROQ_API_KEY'))
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": user_query}
        ],
        model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content

def e_commerce_search(user_query):
  tavily_client= TavilyClient(api_key=os.environ.get('TAVILY_API_KEY'))
  response = tavily_client.search(user_query,search_depth="advanced", include_domains=['http://amazon.in','http://flipkart.com','https://www.myntra.com/','https://www.nykaa.com/','http://ajio.com'],include_images=True)
  return response

def travel_and_navigation(user_query):
  tavily_client= TavilyClient(api_key=os.environ.get('TAVILY_API_KEY'))
  response = tavily_client.search(user_query,search_depth="advanced", include_domains=['https://delhimetrorail.info/','http://goibibo.com','http://makemytrip.com'],include_images=True)
  return response

def send_calendar_invite(title, description, location, start_time, end_time, attendee_emails, sender_email='manaslucifercr7@gmail.com', sender_password='wdpv atip epfw tksx'):
    cal = Calendar()
    event = Event()
    event.name = title
    event.description = description
    event.location = location
    event.begin = start_time
    event.end = end_time
    for email in attendee_emails:
        event.add_attendee(email)
    cal.events.add(event)

    ics_content = str(cal)

    subject = f'Calendar Invite: {title}'
    body = f'Please find attached the calendar invite for the event: {title}'

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ', '.join(attendee_emails)
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(ics_content)
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename=invite.ics')
    msg.attach(part)

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print(f'Calendar invite sent successfully to: {", ".join(attendee_emails)}')
    except Exception as e:
        print(f'Failed to send calendar invite: {e}')

from openai import OpenAI
import json

client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

def run_conversation(user_query):
    messages = [{"role": "user", "content": user_query}]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "web_information_retrieval",
                "description": "Retrieve web information based on user query",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_query": {
                            "type": "string",
                            "description": "User query to search web information",
                        },
                    },
                    "required": ["user_query"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "information_retrieval",
                "description": "Retrieve general information based on user query without internet",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_query": {
                            "type": "string",
                            "description": "User query to retrieve information",
                        },
                    },
                    "required": ["user_query"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "e_commerce_search",
                "description": "Search e-commerce sites based on user query",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_query": {
                            "type": "string",
                            "description": "User query to search e-commerce sites",
                        },
                    },
                    "required": ["user_query"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "travel_and_navigation",
                "description": "Search travel and navigation sites based on user query",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_query": {
                            "type": "string",
                            "description": "User query to search travel and navigation sites",
                        },
                    },
                    "required": ["user_query"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "send_calendar_invite",
                "description": "Send a calendar invite for an event",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Title of the event",
                        },
                        "description": {
                            "type": "string",
                            "description": "Description of the event",
                        },
                        "location": {
                            "type": "string",
                            "description": "Location of the event",
                        },
                        "start_time": {
                            "type": "string",
                            "description": "Start time of the event",
                        },
                        "end_time": {
                            "type": "string",
                            "description": "End time of the event",
                        },
                        "attendee_emails": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "description": "Emails of attendees",
                            },
                        },
                        "sender_email": {
                            "type": "string",
                            "description": "Sender's email address",
                        },
                        "sender_password": {
                            "type": "string",
                            "description": "Sender's email password",
                        },
                    },
                    "required": ["title", "location", "start_time", "end_time", "attendee_emails"],
                },
            },
        },
    ]
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    if tool_calls:
        available_functions = {
            "web_information_retrieval": web_information_retrieval,
            "information_retrieval": information_retrieval,
            "e_commerce_search": e_commerce_search,
            "travel_and_navigation": travel_and_navigation,
            "send_calendar_invite": send_calendar_invite,
        }

        messages.append(response_message)
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            if function_name == "send_calendar_invite":
                function_response = function_to_call(
                    title=function_args.get("title"),
                    description=function_args.get("description"),
                    location=function_args.get("location"),
                    start_time=function_args.get("start_time"),
                    end_time=function_args.get("end_time"),
                    attendee_emails=function_args.get("attendee_emails"),
                )
            else:
                function_response = function_to_call(
                    user_query=function_args.get("user_query"),
                )

            if function_name in ["e_commerce_search", "travel_and_navigation"]:
                for i, result in enumerate(function_response['results']):
                    st.write(f"### [{result['title']}]({result['url']})")
                    st.write(result['content'])
                    if i < len(function_response['images']):
                        st.image(function_response['images'][i])

            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )
            return function_response

    else:
        return response_message.content

st.title("Glucon_D Chatbot")
user_query = st.text_input("Enter your query")
if st.button("Run"):
    if user_query:
        response = run_conversation(user_query)


