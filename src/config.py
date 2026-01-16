"""
Sentinel Intelligence System - Configuration
Centralized settings for RSS feeds, target URLs, and synthesis prompts.
"""

# ================================================================================
# RSS INTELLIGENCE FEEDS
# Low-friction, structured sources for AI developments
# ================================================================================

RSS_FEEDS = [
    # AI News
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://venturebeat.com/category/ai/feed/",
    "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml",
    "https://www.wired.com/feed/tag/ai/latest/rss",
    
    # Academic / Research
    "https://arxiv.org/rss/cs.AI",
    "https://arxiv.org/rss/cs.LG",  # Machine Learning
    
    # Company Blogs
    "https://openai.com/blog/rss/",
    "https://blog.google/technology/ai/rss/",
    "https://www.anthropic.com/news/feed.xml",
    
    # Developer News
    "https://developers.googleblog.com/feeds/posts/default",
    "https://news.ycombinator.com/rss",
]

# ================================================================================
# DEEP WEB SCRAPING TARGETS
# Dynamic JavaScript sites requiring Playwright (Customer Success pages)
# ================================================================================

SCRAPE_TARGETS = [
    # Customer Story Pages (High-value use cases and metrics)
    "https://cloud.google.com/customers",
    "https://openai.com/customer-stories",
    "https://www.microsoft.com/en-us/ai/ai-customer-stories",
    "https://aws.amazon.com/solutions/case-studies/",
    
    # AI News Sites (fallback if RSS fails)
    "https://www.theguardian.com/technology/artificialintelligenceai",
]

# ================================================================================
# GMAIL SEARCH QUERIES
# Advanced operators to find white papers and research reports
# ================================================================================

GMAIL_QUERIES = [
    # White papers with PDF attachments
    'newer_than:2d has:attachment filename:pdf subject:(whitepaper OR "white paper")',
    'newer_than:2d has:attachment filename:pdf subject:("research report" OR "technical report")',
    'newer_than:2d has:attachment filename:pdf subject:("technical deep dive" OR "case study")',
    
    # Newsletter labels (user-configurable)
    'newer_than:7d label:newsletters has:attachment filename:pdf',
    
    # AI-specific newsletters
    'newer_than:3d from:(newsletter OR digest) subject:(AI OR "artificial intelligence" OR "machine learning")',
]

# ================================================================================
# CONTENT CLASSIFICATION KEYWORDS
# Used by both Watchtower and Synthesis Core for categorization
# ================================================================================

CATEGORY_KEYWORDS = {
    "customer_improvement": [
        "customer", "case study", "success story", "testimonial", 
        "implementation", "deployed", "adopted", "integrated",
        "saved", "reduced", "improved", "increased", "roi"
    ],
    "breakthrough": [
        "breakthrough", "novel", "first", "revolutionary", "discovery",
        "state-of-the-art", "sota", "unprecedented", "groundbreaking"
    ],
    "use_case": [
        "how to", "tutorial", "implementation", "use case", "guide",
        "example", "demo", "showcase", "practical"
    ],
    "white_paper": [
        "paper", "research", "study", "arxiv", "journal", "pdf",
        "preprint", "publication", "technical report"
    ]
}

# ================================================================================
# METRICS EXTRACTION PATTERNS (Regex)
# Used to identify quantifiable improvements in text
# ================================================================================

METRIC_PATTERNS = {
    "percentage": r'(?:increased?|improved?|reduced?|saved?|grew?|boost(?:ed)?)\s+(?:by\s+)?(\d+(?:\.\d+)?)\s*%',
    "multiplier": r'(\d+(?:\.\d+)?)\s*x\s+(?:faster|better|more efficient|improvement)',
    "time_savings": r'(?:saved?|reduced?)\s+(\d+(?:\.\d+)?)\s*(?:hours?|days?|weeks?|minutes?|ms|milliseconds?)',
    "cost_savings": r'(?:saved?|reduced?)\s+\$?(\d+(?:,\d{3})*(?:\.\d+)?)\s*(?:million|billion|k|thousand)?',
}

# ================================================================================
# SYNTHESIS CORE SETTINGS
# ================================================================================

GEMINI_MODEL = "gemini-2.0-flash"  # Default model for synthesis

# Maximum items to process per run (to control costs)
MAX_RSS_ITEMS_PER_FEED = 10
MAX_DEEP_WEB_PAGES = 5
MAX_EMAIL_RESULTS = 20

# ================================================================================
# OUTPUT CONFIGURATION
# ================================================================================

OUTPUT_DIR = "./output"
DOCS_DIR = "./docs"  # For downloaded PDFs
REPORT_FILENAME_TEMPLATE = "Sentinel_Report_{date}.md"

# ================================================================================
# USER AGENT
# ================================================================================

USER_AGENT = "Sentinel-Bot/2.0 (Research; github.com/monbon24/Sentinel)"
