from groq import Groq
import json
from typing import Dict, Optional, Any
import os
import httpx
import re
from urllib.parse import urlparse
from config import GROQ_API_KEY

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

def extract_urls(text: str) -> list:
    """Extract URLs from text using regex."""
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    return re.findall(url_pattern, text)

def analyze_with_groq(message: Optional[str] = None, url: Optional[str] = None) -> Dict[str, Any]:
    """
    Analyze content for fraud using Groq LLM with enhanced detection capabilities.
    
    Args:
        message: Optional text message to analyze
        url: Optional URL to analyze
        
    Returns:
        Dict containing analysis results
    """
    if not message and not url:
        return {
            "error": "At least one of message or URL must be provided",
            "is_fraudulent": False,
            "confidence": 0.0
        }

    # Construct specialized prompt based on available information
    if message and url:
        prompt = f"""Analyze the following message and URL for potential fraud:

MESSAGE:
{message}

URL:
{url}

Consider the following aspects in your analysis:

1. Content Analysis:
- Language patterns and inconsistencies
- Urgency or pressure tactics
- Grammatical errors or unusual formatting
- Suspicious keywords or phrases
- Request for sensitive information
- Impersonation attempts

2. URL Analysis:
- Domain age and reputation
- SSL certificate validity
- Suspicious URL patterns
- Known malicious indicators
- Redirect chains
- URL encoding tricks

3. Technical Indicators:
- Email header analysis (if present)
- IP reputation
- Domain WHOIS data
- SSL/TLS configuration
- Authentication mechanisms
- Known blacklist matches

4. Behavioral Patterns:
- Timing of communication
- User interaction history
- Click-through patterns
- Session behavior
- Device fingerprinting
- Geographic anomalies

5. Financial Risk Assessment:
- Payment method requests
- Unusual transaction patterns
- Currency inconsistencies
- Bank account information requests
- Cryptocurrency mentions
- Investment scheme indicators

6. Contextual Analysis:
- Industry-specific red flags
- Known scam patterns
- Historical fraud cases
- Geographic risk factors
- Time-based patterns
- Target audience analysis

Provide a detailed analysis in the following JSON format:
{{
    "is_fraudulent": boolean,
    "confidence": float (0.0 to 1.0),
    "risk_level": "LOW" | "MEDIUM" | "HIGH" | "CRITICAL",
    "content_analysis": {{
        "suspicious_patterns": [string],
        "language_analysis": {{
            "urgency_level": "LOW" | "MEDIUM" | "HIGH",
            "grammar_issues": boolean,
            "suspicious_phrases": [string]
        }},
        "impersonation_risk": boolean,
        "sensitive_info_request": boolean
    }},
    "url_analysis": {{
        "domain_reputation": "SAFE" | "SUSPICIOUS" | "MALICIOUS",
        "ssl_valid": boolean,
        "redirect_chain": [string],
        "known_malicious": boolean
    }},
    "technical_analysis": {{
        "header_analysis": {{
            "spf_valid": boolean,
            "dkim_valid": boolean,
            "dmarc_valid": boolean
        }},
        "ip_reputation": "GOOD" | "NEUTRAL" | "BAD",
        "domain_age_days": integer,
        "blacklist_matches": [string]
    }},
    "behavioral_analysis": {{
        "timing_suspicious": boolean,
        "interaction_pattern": "NORMAL" | "SUSPICIOUS",
        "geographic_anomaly": boolean,
        "device_risk": "LOW" | "MEDIUM" | "HIGH"
    }},
    "financial_risk": {{
        "payment_method_mentioned": boolean,
        "cryptocurrency_mentioned": boolean,
        "unusual_amounts": boolean,
        "bank_info_requested": boolean
    }},
    "contextual_analysis": {{
        "industry_red_flags": [string],
        "known_scam_match": boolean,
        "geographic_risk": "LOW" | "MEDIUM" | "HIGH",
        "target_audience_risk": "LOW" | "MEDIUM" | "HIGH"
    }},
    "recommendations": [string],
    "explanation": string
}}"""
    elif message:
        prompt = f"""Analyze the following message for potential fraud:

MESSAGE:
{message}

[Same analysis criteria as above, focusing on message content]"""
    else:
        prompt = f"""Analyze the following URL for potential fraud:

URL:
{url}

[Same analysis criteria as above, focusing on URL analysis]"""

    try:
        # Get completion from Groq
        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {"role": "system", "content": "You are an expert fraud detection system. Analyze the provided content for potential fraud indicators and provide detailed analysis."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=4000
        )
        
        # Parse the response
        response_text = completion.choices[0].message.content
        try:
            # Extract JSON from the response
            json_str = response_text[response_text.find("{"):response_text.rfind("}")+1]
            result = json.loads(json_str)
            return result
        except json.JSONDecodeError:
            return {
                "error": "Failed to parse analysis results",
                "is_fraudulent": False,
                "confidence": 0.0
            }
            
    except Exception as e:
        return {
            "error": f"Analysis failed: {str(e)}",
            "is_fraudulent": False,
            "confidence": 0.0
        }
