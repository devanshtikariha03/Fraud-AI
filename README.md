# FraudGuard AI

A powerful fraud detection system using Groq LLM.

## Setup

1. Clone the repository:
```bash
git clone https://github.com/devanshtikariha03/Fraud-AI.git
cd Fraud-AI
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
   - Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
   - Edit `.env` and add your Groq API key:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

4. Run the application:
```bash
python main.py
```

5. Access the application at http://localhost:8001

## Features

- Advanced fraud detection using Groq LLM
- Rate limiting to prevent API abuse
- Comprehensive analysis of messages and URLs
- Detailed fraud risk assessment
- User-friendly web interface

## API Endpoints

- `GET /`: Homepage with the fraud detection form
- `POST /analyze`: Analyze content for fraud
- `GET /healthz`: Health check endpoint

## Configuration

You can modify the following settings in your `.env` file:
- `GROQ_API_KEY`: Your Groq API key
- `PORT`: Server port (default: 8001)
- `HOST`: Server host (default: 0.0.0.0)

## Security

- API keys are stored in environment variables
- Rate limiting is implemented to prevent abuse
- Input validation for all endpoints
- Error handling and logging

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Project Structure

```
project/
├── main.py              # FastAPI application
├── fraud_detection.py   # Fraud detection logic
├── requirements.txt     # Project dependencies
└── templates/
    └── index.html      # Web interface template
```

## Development

To extend the fraud detection capabilities, modify the `process_fraud_query_realtime` function in `main.py` or create a separate module in `fraud_detection.py`. 