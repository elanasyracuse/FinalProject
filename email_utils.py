import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict
from email.header import Header
import re # <-- NEW IMPORT

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587

def clean_string(text: str) -> str:
    """
    Cleans a string by replacing non-breaking spaces (\xa0) and
    ensuring it is decoded and re-encoded safely.
    """
    if not isinstance(text, str):
        return text
    
    # 1. Replace the common non-breaking space character with a standard space
    cleaned_text = text.replace('\xa0', ' ')
    
    # 2. Use the 'unicode-escape' and 'ascii' codecs to identify and remove
    # any other non-standard characters that can't be encoded as ASCII,
    # replacing them with a question mark.
    # This is a fallback to ensure 100% ASCII-safety for transmission headers.
    cleaned_text = cleaned_text.encode('ascii', 'ignore').decode('ascii')
    
    return cleaned_text

def send_papers_email(
    smtp_user: str,
    smtp_password: str,
    to_address: str,
    query: str,
    papers: List[Dict]
) -> None:
    """
    Send an email with a list of research papers.
    """
    
    # 1. Scrub the query before using it in the subject
    clean_query = clean_string(query)
    
    # Properly encode the subject for non-ASCII characters
    subject_text = f"RAG Bot - Top research papers for: {clean_query}"
    subject = Header(subject_text, 'utf-8').encode()

    # Build email body
    lines = [
        f"Here are the top {len(papers)} papers for your query: {clean_query}",
        "",
    ]
    
    for i, paper in enumerate(papers, start=1):
        # 2. Scrub the paper title before using it in the body
        title = clean_string(paper.get("title", "Untitled"))
        arxiv_id = paper.get("arxiv_id", "N/A")
        url = f"https://arxiv.org/abs/{arxiv_id}"
        lines.append(f"{i}. {title}")
        lines.append(f"   {url}")
        lines.append("")
    
    lines.append("Sent via RAG Research Bot.")
    body = "\n".join(lines)

    # Create and send email
    msg = MIMEMultipart(_charset="utf-8")
    msg["From"] = smtp_user
    msg["To"] = to_address
    msg["Subject"] = subject
    
    # Attach the body using UTF-8 encoding
    msg.attach(MIMEText(body, "plain", "utf-8")) 

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        
        # Use msg.as_string() to send the fully formatted message
        server.sendmail(smtp_user, to_address, msg.as_string())