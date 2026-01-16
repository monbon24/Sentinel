"""
Sentinel Intelligence System - The Watchtower
Web scraping module for public intelligence gathering.
Handles RSS feeds and dynamic JavaScript sites.
"""

import feedparser
import time
import random
import re
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field

# Try to import Playwright (optional for deep web)
try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("[!] Playwright not installed. Deep web scraping disabled.")

# Try to import playwright-stealth
try:
    from playwright_stealth import stealth_sync
    STEALTH_AVAILABLE = True
except ImportError:
    STEALTH_AVAILABLE = False
    print("[!] playwright-stealth not installed. Stealth mode disabled.")

from bs4 import BeautifulSoup
import html2text

# Import configuration
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.config import (
    RSS_FEEDS, SCRAPE_TARGETS, CATEGORY_KEYWORDS, 
    METRIC_PATTERNS, MAX_RSS_ITEMS_PER_FEED, MAX_DEEP_WEB_PAGES, USER_AGENT
)


@dataclass
class IntelligenceItem:
    """Represents a single piece of gathered intelligence."""
    title: str
    source: str
    link: str
    summary: str
    timestamp: str
    category: str = "uncategorized"
    metrics: list = field(default_factory=list)
    raw_content: Optional[str] = None


class Watchtower:
    """
    The Watchtower - Primary intelligence gathering module.
    Scans RSS feeds and dynamic web pages for AI developments.
    """
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.html_converter = html2text.HTML2Text()
        self.html_converter.ignore_links = False
        self.html_converter.ignore_images = True
        self.items_collected = []
    
    def log(self, message: str):
        """Print log message if verbose mode is enabled."""
        if self.verbose:
            print(message)
    
    def categorize_content(self, text: str) -> str:
        """Categorize content based on keyword matching."""
        text_lower = text.lower()
        
        for category, keywords in CATEGORY_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return category
        
        return "general"
    
    def extract_metrics(self, text: str) -> list:
        """Extract quantifiable metrics from text using regex patterns."""
        metrics = []
        
        for metric_type, pattern in METRIC_PATTERNS.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                metrics.append({
                    "type": metric_type,
                    "value": match,
                    "context": text[:200]  # First 200 chars for context
                })
        
        return metrics
    
    def fetch_rss_intelligence(self) -> list:
        """
        Fetch intelligence from RSS feeds.
        Low-friction, structured sources.
        """
        print("\n[WATCHTOWER] Scanning RSS Intelligence Feeds")
        print("=" * 60)
        
        items = []
        
        for feed_url in RSS_FEEDS:
            try:
                self.log(f"[>] Scanning: {feed_url[:60]}...")
                feed = feedparser.parse(feed_url)
                
                if feed.bozo:
                    self.log(f"   [!] Feed error: {feed.bozo_exception}")
                    continue
                
                feed_title = feed.feed.get('title', 'Unknown Feed')
                entries = feed.entries[:MAX_RSS_ITEMS_PER_FEED]
                
                for entry in entries:
                    # Extract and clean content
                    summary = entry.get('summary', entry.get('description', ''))
                    if summary:
                        summary = BeautifulSoup(summary, 'html.parser').get_text()[:500]
                    
                    combined_text = f"{entry.get('title', '')} {summary}"
                    
                    item = IntelligenceItem(
                        title=entry.get('title', 'Untitled'),
                        source=feed_title,
                        link=entry.get('link', ''),
                        summary=summary,
                        timestamp=entry.get('published', datetime.now().isoformat()),
                        category=self.categorize_content(combined_text),
                        metrics=self.extract_metrics(combined_text)
                    )
                    items.append(item)
                
                print(f"   [OK] Extracted {len(entries)} items from {feed_title}")
                
            except Exception as e:
                print(f"   [!] Error scanning {feed_url[:40]}: {e}")
        
        print(f"\n[#] RSS Total: {len(items)} intelligence items collected")
        self.items_collected.extend(items)
        return items
    
    def fetch_deep_web_intelligence(self) -> list:
        """
        Fetch intelligence from dynamic JavaScript sites.
        Uses Playwright for rendering.
        """
        if not PLAYWRIGHT_AVAILABLE:
            print("\n[WATCHTOWER] Deep Web scanning skipped (Playwright not installed)")
            return []
        
        print("\n[WATCHTOWER] Deep Web Intelligence Scan")
        print("=" * 60)
        
        items = []
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent=USER_AGENT)
            
            # Apply stealth if available
            page = context.new_page()
            if STEALTH_AVAILABLE:
                stealth_sync(page)
            
            for url in SCRAPE_TARGETS[:MAX_DEEP_WEB_PAGES]:
                try:
                    self.log(f"[>] Deep scanning: {url[:50]}...")
                    
                    # Randomized delay to mimic human behavior
                    time.sleep(random.uniform(2, 5))
                    
                    page.goto(url, wait_until="networkidle", timeout=30000)
                    content = page.content()
                    
                    soup = BeautifulSoup(content, 'html.parser')
                    
                    # Extract article/card elements (generic selectors)
                    articles = soup.select('article, .card, .case-study, .customer-story')
                    
                    for article in articles[:10]:  # Limit per page
                        title_el = article.select_one('h2, h3, .title')
                        link_el = article.select_one('a')
                        summary_el = article.select_one('p, .description, .excerpt')
                        
                        if title_el:
                            title = title_el.get_text(strip=True)
                            link = link_el.get('href', '') if link_el else url
                            summary = summary_el.get_text(strip=True)[:500] if summary_el else ''
                            
                            combined_text = f"{title} {summary}"
                            
                            item = IntelligenceItem(
                                title=title,
                                source=f"Deep Web: {url[:30]}",
                                link=link if link.startswith('http') else url + link,
                                summary=summary,
                                timestamp=datetime.now().isoformat(),
                                category=self.categorize_content(combined_text),
                                metrics=self.extract_metrics(combined_text)
                            )
                            items.append(item)
                    
                    print(f"   [OK] Extracted {len(articles[:10])} items from {url[:40]}")
                    
                except Exception as e:
                    print(f"   [!] Error scanning {url[:40]}: {e}")
            
            browser.close()
        
        print(f"\n[#] Deep Web Total: {len(items)} intelligence items collected")
        self.items_collected.extend(items)
        return items
    
    def run(self, include_deep_web: bool = True) -> list:
        """
        Execute full intelligence gathering sweep.
        
        Args:
            include_deep_web: Whether to include Playwright-based scraping
        
        Returns:
            List of IntelligenceItem objects
        """
        print("\n" + "=" * 60)
        print("   SENTINEL WATCHTOWER - Intelligence Sweep Initiated")
        print("=" * 60)
        
        # Always run RSS (fast, reliable)
        self.fetch_rss_intelligence()
        
        # Optionally run deep web
        if include_deep_web:
            self.fetch_deep_web_intelligence()
        
        print(f"\n[WATCHTOWER COMPLETE] Total items: {len(self.items_collected)}")
        return self.items_collected


# For standalone testing
if __name__ == "__main__":
    watchtower = Watchtower(verbose=True)
    items = watchtower.run(include_deep_web=False)  # RSS only for quick test
    
    print("\n--- Sample Items ---")
    for item in items[:3]:
        print(f"\nTitle: {item.title}")
        print(f"Source: {item.source}")
        print(f"Category: {item.category}")
        print(f"Metrics: {item.metrics}")
