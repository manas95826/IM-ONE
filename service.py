from tavily import TavilyClient
from groq import Groq
from ics import Calendar, Event
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

class TavilySearchService:
    def web_information_retrieval(self, user_query):
        tavily_client = TavilyClient(api_key=os.environ.get('TAVILY_API_KEY'))
        response = tavily_client.search(user_query, search_depth="basic", include_answer=True)
        return response['answer']

    def e_commerce_search(self, user_query):
        tavily_client = TavilyClient(api_key=os.environ.get('TAVILY_API_KEY'))
        response = tavily_client.search(user_query, search_depth="advanced", include_domains=[
            'http://amazon.in', 'http://flipkart.com', 'https://www.myntra.com/', 'https://www.nykaa.com/', 'http://ajio.com'
        ], include_images=True)
        return response

    def travel_and_navigation(self, user_query):
        tavily_client = TavilyClient(api_key=os.environ.get('TAVILY_API_KEY'))
        response = tavily_client.search(user_query, search_depth="advanced", include_domains=[
            'https://delhimetrorail.info/', 'http://goibibo.com', 'http://makemytrip.com'
        ], include_images=True)
        return response

class GroqSearchService:
    def information_retrieval(self, user_query):
        client = Groq(api_key=os.environ.get('GROQ_API_KEY'))
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": user_query}
            ],
            model="llama3-8b-8192",
        )
        return chat_completion.choices[0].message.content

class CalendarInviteService:
    def send_calendar_invite(self, title, description, location, start_time, end_time, attendee_emails, sender_email='youremail@gmail.com', sender_password='yourpassword'):
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
