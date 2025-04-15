# Fraud Detection Web Application

A real-time fraud detection system built with FastAPI and modern web technologies.

## Features

- Real-time message analysis for fraud detection
- Optional URL analysis
- Detailed fraud analysis results
- Modern, responsive web interface
- Asynchronous processing

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

4. Open your browser and navigate to:
```
http://localhost:8000
```

## Usage

1. Enter the message you want to analyze in the text area
2. Optionally, provide a URL to analyze
3. Click "Analyze" to get the fraud detection results
4. View the detailed analysis including:
   - Final decision
   - Heuristic score
   - Content analysis
   - Financial risk assessment
   - Domain verification

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