# IM-ONE

Welcome to the **IM-ONE** repository, a chatbot platform designed to handle a wide range of tasks such as information retrieval, e-commerce search, travel and navigation queries, and calendar invite scheduling. This project leverages multiple service APIs, including **Tavily** and **Groq**, to provide rich, diverse, and accurate responses to user queries.

## Features

- **Web Information Retrieval**: Perform web searches and retrieve relevant articles and summaries.
- **E-commerce Search**: Retrieve product information from popular shopping platforms.
- **Travel and Navigation**: Get travel-related information from travel and transportation platforms.
- **Calendar Invite**: Schedule and send calendar invites with details to the desired attendees.
- **Information Retrieval**: Use Groq's LLM to generate conversational responses.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/manas95826/IM-ONE.git
   cd IM-ONE
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables. You will need API keys for **Tavily** and **Groq**. Add these to your environment:

   ```bash
   export TAVILY_API_KEY='your-tavily-api-key'
   export GROQ_API_KEY='your-groq-api-key'
   ```

4. (Optional) For calendar invites, you may need Gmail credentials for sending invites:

   ```bash
   export EMAIL_USER='youremail@gmail.com'
   export EMAIL_PASS='yourpassword'
   ```

## Usage

Run the chatbot using **Streamlit**:

```bash
streamlit run main.py
```

### Example

Once the app is running, input a query such as:

- **"Find the latest news on AI technology"** for web information retrieval.
- **"Search for Nike shoes"** for e-commerce queries.
- **"Find train routes in Delhi"** for travel and navigation information.

The chatbot will respond accordingly with relevant data.

## File Structure

- **main.py**: Contains the main Streamlit app code.
- **service_factory.py**: Implements the `ServiceFactory` class responsible for creating the different services based on the user's query type.
- **service.py**: Defines individual service classes like `TavilySearchService`, `GroqSearchService`, and `CalendarInviteService` that handle specific functionalities.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.
