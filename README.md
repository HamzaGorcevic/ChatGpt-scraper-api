# ChatGPT Scraper API

A FastAPI project for sending prompts to ChatGPT and retrieving responses. Each request starts a new chat session.

## Features
- **POST Endpoint**: Send a prompt and get ChatGPT's response.
- **Easy Setup**: Built with FastAPI and `requests`.

## Installation
1. Clone the repository:  
   `git clone https://github.com/yourusername/chatgpt-scraper-api.git && cd chatgpt-scraper-api`
2. Install dependencies:  
   `pip install -r requirements.txt`
3. Run the server:  
   `uvicorn main:app --reload`

## Usage
### Example Request
Send a POST request to `/chatgpt` with a JSON body:
```json
{
  "message": "Your prompt here"
}
Response
{
  "response": "ChatGPT's reply"
}
Curl Example
curl -X POST https://chatgpt-scraper-api.onrender.com/chatgpt \
-H "Content-Type: application/json" \
-d '{"message": "Hello, ChatGPT!"}'
Hosted API
Live at: https://chatgpt-scraper-api.onrender.com

License
This project is licensed under the MIT License.

