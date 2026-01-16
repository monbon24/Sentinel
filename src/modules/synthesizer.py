"""
Sentinel Intelligence System - The Synthesis Core
LLM-powered intelligence analysis and report generation.
"""

import os
import re
import json
from datetime import datetime
from typing import Optional
from dataclasses import asdict

# Gemini API
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("[!] google-generativeai not installed. AI synthesis disabled.")

# Import configuration
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.config import GEMINI_MODEL, OUTPUT_DIR, REPORT_FILENAME_TEMPLATE


# Synthesis prompt template
SYNTHESIS_PROMPT = """You are an AI intelligence analyst for "Project Sentinel". 

Analyze the following raw intelligence data and produce a structured intelligence report.

## Your Objectives:

1. **Deduplicate**: Identify stories that appear in multiple sources and merge them.
2. **Filter Noise**: Aggressively remove:
   - Marketing fluff and promotional announcements
   - Partnership announcements without technical details
   - Opinion pieces without data
3. **Extract Value**: For each remaining item, identify:
   - **Customer Name** (if mentioned)
   - **Quantifiable Metrics** (e.g., "40% faster", "$2M saved", "50ms latency reduction")
   - **Technical Details** (models, architectures, techniques)
4. **Categorize**: Group findings into:
   - **Breakthroughs**: Novel research, SOTA results, first-of-their-kind capabilities
   - **Use Cases**: Practical implementations and tutorials
   - **Customer Improvements**: Real-world deployments with metrics
   - **White Papers**: Research reports and technical deep dives

## Output Format:

Generate a Markdown report with the following structure:

```markdown
# Sentinel Intelligence Report
**Date**: [Today's date]
**Items Analyzed**: [Number]

## Executive Summary
[2-3 sentence overview of the most significant findings]

## Breakthroughs
[List of breakthrough items with bullet points]

## Customer Improvements
[List with company names and metrics]

## Use Cases
[Practical implementations]

## White Papers
[Research summaries]

## Raw Signal Count
- Total items processed: X
- Items after deduplication: Y
- High-value items: Z
```

## Raw Intelligence Data:

{intelligence_data}

---

Now generate the intelligence report:
"""


class SynthesisCore:
    """
    The Synthesis Core - LLM-powered intelligence synthesis.
    Transforms raw data into structured reports using Gemini.
    """
    
    def __init__(self, api_key: Optional[str] = None, verbose: bool = False):
        self.verbose = verbose
        self.model = None
        
        # Ensure output directory exists
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        # Initialize Gemini
        if GEMINI_AVAILABLE:
            key = api_key or os.getenv("GEMINI_API_KEY")
            if key:
                genai.configure(api_key=key)
                self.model = genai.GenerativeModel(GEMINI_MODEL)
                print(f"[SYNTHESIS CORE] Initialized with {GEMINI_MODEL}")
            else:
                print("[!] GEMINI_API_KEY not found. Using fallback synthesizer.")
        else:
            print("[!] Gemini libraries not available. Using fallback synthesizer.")
    
    def log(self, message: str):
        """Print log message if verbose mode is enabled."""
        if self.verbose:
            print(message)
    
    def prepare_intelligence_data(self, web_items: list, email_items: list) -> str:
        """
        Convert intelligence items to JSON string for LLM processing.
        """
        data = {
            "web_intelligence": [],
            "email_intelligence": []
        }
        
        for item in web_items:
            data["web_intelligence"].append({
                "title": item.title,
                "source": item.source,
                "summary": item.summary[:500],
                "category": item.category,
                "metrics": item.metrics,
                "link": item.link
            })
        
        for item in email_items:
            data["email_intelligence"].append({
                "subject": item.subject,
                "sender": item.sender,
                "snippet": item.snippet,
                "attachments": item.attachments,
                "pdf_excerpt": item.pdf_content[:1000] if item.pdf_content else None
            })
        
        return json.dumps(data, indent=2)
    
    def synthesize_with_gemini(self, intelligence_data: str) -> str:
        """
        Use Gemini to synthesize intelligence into a report.
        """
        if not self.model:
            return self.fallback_synthesize(intelligence_data)
        
        print("\n[SYNTHESIS CORE] Generating AI-powered intelligence report...")
        
        try:
            prompt = SYNTHESIS_PROMPT.format(intelligence_data=intelligence_data)
            response = self.model.generate_content(prompt)
            
            if response.text:
                print("   [OK] AI synthesis complete")
                return response.text
            else:
                print("   [!] Empty response from Gemini, using fallback")
                return self.fallback_synthesize(intelligence_data)
                
        except Exception as e:
            print(f"   [!] Gemini API error: {e}")
            return self.fallback_synthesize(intelligence_data)
    
    def fallback_synthesize(self, intelligence_data: str) -> str:
        """
        Rule-based fallback synthesizer when AI is unavailable.
        """
        print("\n[SYNTHESIS CORE] Using rule-based fallback synthesizer...")
        
        try:
            data = json.loads(intelligence_data)
        except:
            data = {"web_intelligence": [], "email_intelligence": []}
        
        web_items = data.get("web_intelligence", [])
        email_items = data.get("email_intelligence", [])
        
        # Group by category
        breakthroughs = [i for i in web_items if i.get("category") == "breakthrough"]
        use_cases = [i for i in web_items if i.get("category") == "use_case"]
        customer_items = [i for i in web_items if i.get("category") == "customer_improvement"]
        white_papers = [i for i in web_items if i.get("category") == "white_paper"]
        
        # Build report
        report = f"""# Sentinel Intelligence Report
**Date**: {datetime.now().strftime("%Y-%m-%d %H:%M")}
**Items Analyzed**: {len(web_items) + len(email_items)}
**Mode**: Rule-Based Fallback (AI unavailable)

## Executive Summary
Processed {len(web_items)} web intelligence items and {len(email_items)} email items. 
This report was generated using keyword-based categorization.

## Breakthroughs ({len(breakthroughs)} items)
"""
        for item in breakthroughs[:10]:
            report += f"- **{item['title']}** ({item['source']})\n"
            if item.get('metrics'):
                report += f"  - Metrics: {item['metrics']}\n"
        
        report += f"\n## Customer Improvements ({len(customer_items)} items)\n"
        for item in customer_items[:10]:
            report += f"- **{item['title']}** ({item['source']})\n"
            report += f"  - {item['summary'][:150]}...\n"
        
        report += f"\n## Use Cases ({len(use_cases)} items)\n"
        for item in use_cases[:10]:
            report += f"- [{item['title']}]({item['link']})\n"
        
        report += f"\n## White Papers ({len(white_papers) + len(email_items)} items)\n"
        for item in white_papers[:5]:
            report += f"- **{item['title']}**\n"
        for item in email_items[:5]:
            report += f"- **{item['subject']}** (from: {item['sender'][:30]})\n"
            if item.get('attachments'):
                report += f"  - Attachments: {', '.join(item['attachments'])}\n"
        
        report += f"""
## Raw Signal Count
- Total web items: {len(web_items)}
- Total email items: {len(email_items)}
- Breakthroughs: {len(breakthroughs)}
- Customer Improvements: {len(customer_items)}
- Use Cases: {len(use_cases)}
- White Papers: {len(white_papers)}
"""
        
        return report
    
    def save_report(self, report: str) -> str:
        """Save report to output directory."""
        filename = REPORT_FILENAME_TEMPLATE.format(
            date=datetime.now().strftime("%Y-%m-%d")
        )
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n[SYNTHESIS CORE] Report saved: {filepath}")
        return filepath
    
    def run(self, web_items: list, email_items: list) -> str:
        """
        Execute full synthesis pipeline.
        
        Args:
            web_items: List of IntelligenceItem from Watchtower
            email_items: List of EmailIntelligence from Mailroom
        
        Returns:
            Generated report as string
        """
        print("\n" + "=" * 60)
        print("   SENTINEL SYNTHESIS CORE - Intelligence Analysis")
        print("=" * 60)
        
        # Prepare data
        intelligence_data = self.prepare_intelligence_data(web_items, email_items)
        self.log(f"   Prepared {len(web_items)} web + {len(email_items)} email items")
        
        # Synthesize
        report = self.synthesize_with_gemini(intelligence_data)
        
        # Save
        filepath = self.save_report(report)
        
        print(f"\n[SYNTHESIS COMPLETE]")
        return report


# For standalone testing
if __name__ == "__main__":
    # Test with mock data
    from dataclasses import dataclass
    
    @dataclass
    class MockItem:
        title: str = "Test AI Breakthrough"
        source: str = "TechCrunch"
        summary: str = "A new model achieves 40% better performance."
        category: str = "breakthrough"
        metrics: list = None
        link: str = "https://example.com"
    
    core = SynthesisCore(verbose=True)
    report = core.run([MockItem()], [])
    print("\n--- Report Preview ---")
    print(report[:1000])
