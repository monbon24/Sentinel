"""
Sentinel Intelligence System - The Mailroom
Gmail API integration for private context intelligence.
Extracts white papers and research reports from email subscriptions.
"""

import os
import base64
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field

# Google API imports
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    GMAIL_API_AVAILABLE = True
except ImportError:
    GMAIL_API_AVAILABLE = False
    print("[!] Google API libraries not installed. Gmail integration disabled.")

# PDF processing
try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    print("[!] PyPDF2 not installed. PDF extraction disabled.")

# Import configuration
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.config import GMAIL_QUERIES, MAX_EMAIL_RESULTS, DOCS_DIR


# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


@dataclass
class EmailIntelligence:
    """Represents intelligence extracted from an email."""
    subject: str
    sender: str
    snippet: str
    gmail_link: str
    timestamp: str
    attachments: list = field(default_factory=list)
    pdf_content: Optional[str] = None


class Mailroom:
    """
    The Mailroom - Private context intelligence bridge.
    Authenticates to Gmail and extracts white papers from subscriptions.
    """
    
    def __init__(self, credentials_path: str = "credentials.json", 
                 token_path: str = "token.json",
                 verbose: bool = False):
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.verbose = verbose
        self.service = None
        self.items_collected = []
        
        # Ensure docs directory exists
        os.makedirs(DOCS_DIR, exist_ok=True)
    
    def log(self, message: str):
        """Print log message if verbose mode is enabled."""
        if self.verbose:
            print(message)
    
    def authenticate(self) -> bool:
        """
        Authenticate with Gmail API using OAuth 2.0.
        Creates token.json on first run (requires browser interaction).
        """
        if not GMAIL_API_AVAILABLE:
            print("[!] Gmail API libraries not available")
            return False
        
        if not os.path.exists(self.credentials_path):
            print(f"[!] credentials.json not found at {self.credentials_path}")
            print("    Please download OAuth credentials from Google Cloud Console")
            return False
        
        print("\n[MAILROOM] Authenticating with Gmail API...")
        
        creds = None
        
        # Load existing token
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
        
        # Refresh or create new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                self.log("   [>] Refreshing expired token...")
                creds.refresh(Request())
            else:
                self.log("   [>] Starting OAuth flow (browser will open)...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES
                )
                creds = flow.run_local_server(port=0)
            
            # Save token for future runs
            with open(self.token_path, 'w') as token:
                token.write(creds.to_json())
            self.log("   [OK] Token saved")
        
        self.service = build('gmail', 'v1', credentials=creds)
        print("   [OK] Gmail authentication successful")
        return True
    
    def extract_pdf_text(self, pdf_path: str) -> str:
        """Extract text content from a PDF file."""
        if not PDF_AVAILABLE:
            return "[PDF extraction unavailable]"
        
        try:
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page in reader.pages[:10]:  # First 10 pages only
                    text += page.extract_text() + "\n"
                return text[:5000]  # Limit to 5000 chars
        except Exception as e:
            return f"[PDF extraction error: {e}]"
    
    def download_attachment(self, message_id: str, attachment_id: str, 
                           filename: str) -> Optional[str]:
        """Download an email attachment and save to docs directory."""
        try:
            attachment = self.service.users().messages().attachments().get(
                userId='me', messageId=message_id, id=attachment_id
            ).execute()
            
            file_data = base64.urlsafe_b64decode(attachment['data'].encode('UTF-8'))
            
            # Save to docs directory
            filepath = os.path.join(DOCS_DIR, filename)
            with open(filepath, 'wb') as f:
                f.write(file_data)
            
            self.log(f"   [OK] Downloaded: {filename}")
            return filepath
            
        except Exception as e:
            self.log(f"   [!] Attachment download error: {e}")
            return None
    
    def search_whitepapers(self) -> list:
        """
        Search Gmail for white papers and research reports.
        Executes multiple queries to maximize coverage.
        """
        if not self.service:
            print("[!] Gmail not authenticated. Call authenticate() first.")
            return []
        
        print("\n[MAILROOM] Searching for White Papers & Research")
        print("=" * 60)
        
        items = []
        seen_ids = set()
        
        for query in GMAIL_QUERIES:
            try:
                self.log(f"[>] Query: {query[:50]}...")
                
                results = self.service.users().messages().list(
                    userId='me', q=query, maxResults=MAX_EMAIL_RESULTS
                ).execute()
                
                messages = results.get('messages', [])
                
                for msg_info in messages:
                    # Skip duplicates across queries
                    if msg_info['id'] in seen_ids:
                        continue
                    seen_ids.add(msg_info['id'])
                    
                    # Fetch full message
                    msg = self.service.users().messages().get(
                        userId='me', id=msg_info['id']
                    ).execute()
                    
                    # Extract headers
                    headers = {h['name']: h['value'] for h in msg['payload']['headers']}
                    subject = headers.get('Subject', 'No Subject')
                    sender = headers.get('From', 'Unknown')
                    date = headers.get('Date', datetime.now().isoformat())
                    
                    # Check for attachments
                    attachments = []
                    pdf_content = None
                    
                    parts = msg['payload'].get('parts', [])
                    for part in parts:
                        if part.get('filename', '').endswith('.pdf'):
                            attachment_id = part['body'].get('attachmentId')
                            if attachment_id:
                                filepath = self.download_attachment(
                                    msg_info['id'], attachment_id, part['filename']
                                )
                                if filepath:
                                    attachments.append(part['filename'])
                                    pdf_content = self.extract_pdf_text(filepath)
                    
                    item = EmailIntelligence(
                        subject=subject,
                        sender=sender,
                        snippet=msg.get('snippet', ''),
                        gmail_link=f"https://mail.google.com/mail/u/0/#inbox/{msg_info['id']}",
                        timestamp=date,
                        attachments=attachments,
                        pdf_content=pdf_content
                    )
                    items.append(item)
                
                print(f"   [OK] Found {len(messages)} matches")
                
            except Exception as e:
                print(f"   [!] Query error: {e}")
        
        print(f"\n[#] Mailroom Total: {len(items)} email intelligence items")
        self.items_collected = items
        return items
    
    def run(self) -> list:
        """
        Execute full Gmail intelligence gathering.
        
        Returns:
            List of EmailIntelligence objects
        """
        print("\n" + "=" * 60)
        print("   SENTINEL MAILROOM - Private Context Scan Initiated")
        print("=" * 60)
        
        if not self.authenticate():
            print("[!] Gmail authentication failed. Skipping email intelligence.")
            return []
        
        self.search_whitepapers()
        
        print(f"\n[MAILROOM COMPLETE] Total items: {len(self.items_collected)}")
        return self.items_collected


# For standalone testing
if __name__ == "__main__":
    mailroom = Mailroom(verbose=True)
    items = mailroom.run()
    
    print("\n--- Sample Items ---")
    for item in items[:3]:
        print(f"\nSubject: {item.subject}")
        print(f"From: {item.sender}")
        print(f"Attachments: {item.attachments}")
