# Ask AI

Ask AI is a simple, polished chatbot built with Flask and the Groq API. It provides a clean chat experience with a few thoughtful UX touches such as quick prompt suggestions and short conversational memory.

## Features

- Simple chat interface with a modern layout
- Groq-powered responses
- Lightweight conversational context for more coherent replies
- Easy local setup

## Tech Stack

- Python
- Flask
- Groq API
- HTML/CSS/JavaScript

## Project Structure

- `app.py` — Flask server and chat endpoint
- `templates/index.html` — frontend chat UI
- `requirements.txt` — Python dependencies
- `tests/test_app.py` — basic endpoint test

## Setup Locally

1. Clone the repository
   ```bash
   git clone https://github.com/srishtipandey1/api-based-chatbot.git
   cd api-based-chatbot
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Set your Groq API key
   ```bash
   set GROQ_API_KEY=your_groq_api_key
   ```

4. Run the app
   ```bash
   python app.py
   ```

5. Open your browser at
   ```text
   http://127.0.0.1:5000
   ```

## Run Tests

```bash
pytest -q
```

## License

This project is open for learning and personal use.
