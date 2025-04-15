from groq import AsyncGroq
import json
from typing import Dict, Optional
import os
import httpx

# Initialize GROQ client with environment variable
# Set the API key as an environment variable instead of hardcoding it
os.environ["GROQ_API_KEY"] = "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"

# Create a custom httpx client without proxies
http_client = httpx.AsyncClient()
client = AsyncGroq(http_client=http_client)

async def analyze_with_groq(message: Optional[str] = None, url: Optional[str] = None) -> Dict:
    """
    Analyze text or URL using GROQ for fraud detection
    """
    # Construct the prompt based on what's available
    if message and url:
        prompt = f"""Analyze the following message and URL for potential fraud. Consider these aspects:

1. Sender Information:
   - Email/phone details and authenticity
   - Potential spoofing indicators
   - Known fraudulent sources

2. Technical Metadata:
   - Email headers (if applicable)
   - HTTP headers and SSL certificates
   - Authentication results (DKIM, SPF, DMARC)

3. Domain and URL Analysis:
   - WHOIS data (registration date, registrar, owner)
   - URL reputation and history
   - Suspicious patterns or redirections

4. Behavioral and Contextual Data:
   - Timing and frequency patterns
   - Unusual communication patterns
   - Context of the message

5. Content Analysis:
   - Urgency and pressure tactics
   - Suspicious financial requests
   - Unusual language patterns
   - Grammar and spelling inconsistencies
   - Visual inconsistencies (if mentioned)

6. Financial Indicators:
   - Unusual payment requests
   - Unexpected fees
   - Requests for upfront payments
   - Suspicious transaction patterns

Message: {message}
URL: {url}

Provide a detailed analysis in JSON format with the following structure:
{{
    "aggregated_analysis": {{
        "heuristic_score": <score from 1-10>,
        "content_analysis": {{
            "label": "fraud" or "legitimate",
            "explanation": "detailed explanation"
        }},
        "financial_risk": {{
            "financial_risk": true/false,
            "details": "explanation"
        }},
        "domain_verification": {{
            "verified": true/false,
            "details": "explanation"
        }},
        "sender_verification": {{
            "verified": true/false,
            "details": "explanation of sender authenticity"
        }},
        "technical_analysis": {{
            "secure": true/false,
            "details": "explanation of technical security indicators"
        }},
        "behavioral_analysis": {{
            "suspicious": true/false,
            "details": "explanation of behavioral patterns"
        }}
    }},
    "final_decision": {{
        "final_label": "fraud" or "legitimate",
        "final_explanation": "comprehensive explanation"
    }}
}}"""
    elif message:
        prompt = f"""Analyze the following message for potential fraud. Consider these aspects:

1. Sender Information:
   - Email/phone details and authenticity
   - Potential spoofing indicators
   - Known fraudulent sources

2. Technical Metadata:
   - Email headers (if applicable)
   - Authentication results (DKIM, SPF, DMARC)

3. Behavioral and Contextual Data:
   - Timing and frequency patterns
   - Unusual communication patterns
   - Context of the message

4. Content Analysis:
   - Urgency and pressure tactics
   - Suspicious financial requests
   - Unusual language patterns
   - Grammar and spelling inconsistencies
   - Visual inconsistencies (if mentioned)

5. Financial Indicators:
   - Unusual payment requests
   - Unexpected fees
   - Requests for upfront payments
   - Suspicious transaction patterns

Message: {message}

Provide a detailed analysis in JSON format with the following structure:
{{
    "aggregated_analysis": {{
        "heuristic_score": <score from 1-10>,
        "content_analysis": {{
            "label": "fraud" or "legitimate",
            "explanation": "detailed explanation"
        }},
        "financial_risk": {{
            "financial_risk": true/false,
            "details": "explanation"
        }},
        "domain_verification": {{
            "verified": true/false,
            "details": "No URL provided for verification"
        }},
        "sender_verification": {{
            "verified": true/false,
            "details": "explanation of sender authenticity"
        }},
        "technical_analysis": {{
            "secure": true/false,
            "details": "explanation of technical security indicators"
        }},
        "behavioral_analysis": {{
            "suspicious": true/false,
            "details": "explanation of behavioral patterns"
        }}
    }},
    "final_decision": {{
        "final_label": "fraud" or "legitimate",
        "final_explanation": "comprehensive explanation"
    }}
}}"""
    elif url:
        prompt = f"""Analyze the following URL for potential fraud. Consider these aspects:

1. Domain and URL Analysis:
   - WHOIS data (registration date, registrar, owner)
   - URL reputation and history
   - Suspicious patterns or redirections
   - Domain age and legitimacy

2. Technical Metadata:
   - HTTP headers and SSL certificates
   - Authentication results
   - Security protocols

3. Content Analysis:
   - Visual inconsistencies
   - Design quality and consistency
   - Logo usage and branding
   - Language and grammar patterns

4. Behavioral Indicators:
   - Known phishing patterns
   - Suspicious redirects
   - Malware hosting indicators

URL: {url}

Provide a detailed analysis in JSON format with the following structure:
{{
    "aggregated_analysis": {{
        "heuristic_score": <score from 1-10>,
        "content_analysis": {{
            "label": "fraud" or "legitimate",
            "explanation": "No message content provided for analysis"
        }},
        "financial_risk": {{
            "financial_risk": true/false,
            "details": "explanation based on URL analysis"
        }},
        "domain_verification": {{
            "verified": true/false,
            "details": "detailed domain analysis"
        }},
        "sender_verification": {{
            "verified": true/false,
            "details": "No sender information provided"
        }},
        "technical_analysis": {{
            "secure": true/false,
            "details": "explanation of technical security indicators"
        }},
        "behavioral_analysis": {{
            "suspicious": true/false,
            "details": "explanation of behavioral patterns"
        }}
    }},
    "final_decision": {{
        "final_label": "fraud" or "legitimate",
        "final_explanation": "comprehensive explanation"
    }}
}}"""
    else:
        # This should never happen due to validation in the API endpoint
        return {
            "error": "At least one of message or URL must be provided"
        }

    try:
        # Call GROQ API with the updated model
        completion = await client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a definitive fraud detection expert with extensive knowledge of phishing, scams, and online fraud patterns."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=1000,
            top_p=1
        )

        # Parse the response
        response_text = completion.choices[0].message.content
        # Extract JSON from the response (in case there's additional text)
        json_str = response_text[response_text.find("{"):response_text.rfind("}")+1]
        result = json.loads(json_str)
        
        return result

    except Exception as e:
        # Return a safe fallback response in case of errors
        return {
            "aggregated_analysis": {
                "heuristic_score": 5,
                "content_analysis": {
                    "label": "error",
                    "explanation": f"Error during analysis: {str(e)}"
                },
                "financial_risk": {
                    "financial_risk": False,
                    "details": "Analysis failed"
                },
                "domain_verification": {
                    "verified": False,
                    "details": "Analysis failed"
                },
                "sender_verification": {
                    "verified": False,
                    "details": "Analysis failed"
                },
                "technical_analysis": {
                    "secure": False,
                    "details": "Analysis failed"
                },
                "behavioral_analysis": {
                    "suspicious": False,
                    "details": "Analysis failed"
                }
            },
            "final_decision": {
                "final_label": "error",
                "final_explanation": "An error occurred during the analysis. Please try again."
            }
        } 