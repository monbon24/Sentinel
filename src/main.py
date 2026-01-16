"""
Sentinel Intelligence System - Master Orchestrator
Main entry point that coordinates Watchtower, Mailroom, and Synthesis Core.
"""

import argparse
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.watchtower import Watchtower
from modules.mailroom import Mailroom
from modules.synthesizer import SynthesisCore


def print_banner():
    """Print Sentinel startup banner."""
    print("""
================================================================================
   ____            _   _            _ 
  / ___|  ___ _ __ | |_(_)_ __   ___| |
  \\___ \\ / _ \\ '_ \\| __| | '_ \\ / _ \\ |
   ___) |  __/ | | | |_| | | | |  __/ |
  |____/ \\___|_| |_|\\__|_|_| |_|\\___|_|
  
  AI Intelligence Gathering Engine v2.0
  
================================================================================
    """)


def main():
    """Main orchestration function."""
    parser = argparse.ArgumentParser(
        description="Sentinel Intelligence System - AI news aggregator and analyzer"
    )
    parser.add_argument(
        "--quick", action="store_true",
        help="Quick scan: RSS feeds only, no deep web or email"
    )
    parser.add_argument(
        "--no-email", action="store_true",
        help="Skip Gmail integration (public sources only)"
    )
    parser.add_argument(
        "--no-deep-web", action="store_true",
        help="Skip Playwright-based deep web scraping"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Enable verbose output"
    )
    parser.add_argument(
        "--credentials", type=str, default="credentials.json",
        help="Path to Gmail OAuth credentials file"
    )
    
    args = parser.parse_args()
    
    print_banner()
    print(f"Run started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Mode: {'Quick' if args.quick else 'Full'}")
    print(f"Email: {'Disabled' if args.no_email or args.quick else 'Enabled'}")
    print(f"Deep Web: {'Disabled' if args.no_deep_web or args.quick else 'Enabled'}")
    print()
    
    # ========================================
    # PHASE 1: The Watchtower (Web Intelligence)
    # ========================================
    watchtower = Watchtower(verbose=args.verbose)
    
    if args.quick:
        # Quick mode: RSS only
        web_items = watchtower.fetch_rss_intelligence()
    else:
        # Full mode: RSS + optional deep web
        web_items = watchtower.run(include_deep_web=not args.no_deep_web)
    
    # ========================================
    # PHASE 2: The Mailroom (Email Intelligence)
    # ========================================
    email_items = []
    
    if not args.no_email and not args.quick:
        mailroom = Mailroom(
            credentials_path=args.credentials,
            verbose=args.verbose
        )
        email_items = mailroom.run()
    else:
        print("\n[MAILROOM] Skipped (disabled via flags)")
    
    # ========================================
    # PHASE 3: The Synthesis Core (Analysis)
    # ========================================
    api_key = os.getenv("GEMINI_API_KEY")
    synthesizer = SynthesisCore(api_key=api_key, verbose=args.verbose)
    
    report = synthesizer.run(web_items, email_items)
    
    # ========================================
    # Summary
    # ========================================
    print("\n" + "=" * 60)
    print("   SENTINEL RUN COMPLETE")
    print("=" * 60)
    print(f"   Web items collected: {len(web_items)}")
    print(f"   Email items collected: {len(email_items)}")
    print(f"   Report generated: ./output/")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
