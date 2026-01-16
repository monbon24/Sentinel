# 🛡️ Project Sentinel

**The AI Intelligence Gathering Engine**

An autonomous system that aggregates competitive intelligence from the open web and private communication channels, synthesizing it into actionable reports.

---

## 🎯 What Sentinel Does

1. **🌐 The Watchtower (Web Scraper)**
   - Scrapes AI news sources for developments, use cases, and customer improvements
   - Monitors RSS feeds (TechCrunch, arXiv, VentureBeat, OpenAI Blog)
   - Uses Playwright for dynamic content that requires JavaScript rendering

2. **📧 The Mailroom (Gmail Bridge)**
   - Authenticates via OAuth 2.0 to access Gmail
   - Searches for white papers, research reports, and technical deep dives
   - Extracts PDF attachments for analysis

3. **🧠 The Synthesis Core (LLM Brain)**
   - Powered by Gemini 3 Flash
   - Deduplicates and filters noise ("workslop")
   - Extracts customer names and quantifiable improvement metrics
   - Generates structured Markdown intelligence reports

---

## 📁 Project Structure

```
Sentinel/
├── src/
│   ├── modules/
│   │   ├── watchtower.py      # Web scraping module
│   │   ├── mailroom.py        # Gmail API integration
│   │   └── synthesizer.py     # LLM synthesis core
│   ├── config.py              # Configuration and targets
│   └── main.py                # Orchestration script
├── output/                    # Generated reports
├── docs/                      # Downloaded white papers
├── credentials.json           # Google OAuth credentials (DO NOT COMMIT)
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

---

## 🚀 Quick Start

### 1. Set Up Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### 2. Configure Google OAuth

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project and enable Gmail API
3. Create OAuth 2.0 credentials
4. Download `credentials.json` to the project root

### 3. Run Sentinel

```bash
python src/main.py
```

---

## ⚙️ Configuration

Edit `src/config.py` to customize:

- **RSS_FEEDS**: News sources to monitor
- **SCRAPE_TARGETS**: Websites for deep scraping (customer stories)
- **GMAIL_QUERY**: Search operators for finding white papers
- **LLM_MODEL**: Which Gemini model to use

---

## 📊 Output

Sentinel generates a `Sentinel_Report_YYYY-MM-DD.md` file in the `output/` folder containing:

- **🔬 Breakthroughs**: Major AI developments
- **💼 Use Cases**: Real customer implementations
- **📈 Customer Improvements**: Quantifiable metrics (X% faster, Y% savings)
- **📄 White Papers**: Summaries from email subscriptions

---

## 🔐 Security Notes

⚠️ **NEVER commit these files:**

- `credentials.json` (OAuth secrets)
- `token.json` (Access tokens)
- Any files in `docs/` (private content)

These are included in `.gitignore`.

---

## 🛠️ Debug/Reset

- **Clear token**: Delete `token.json` to re-authenticate Gmail
- **Reset output**: Clear the `output/` folder
- **Verbose mode**: Run with `python src/main.py --verbose`

---

Built with 🧠 for autonomous intelligence gathering.
