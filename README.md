# Financial Reporting Agent

An AI-assisted equity research platform that combines financial statement analysis, valuation methodologies, technical indicators, and market sentiment to generate institutional-style investment reports for Indian and global equities.

Unlike generic LLM stock summarizers, this project performs actual financial computations such as ROE, ROCE, Free Cash Flow, leverage analysis, and sector-relative valuation before generating recommendations.

---

## Features

### Financial Statement Analysis

* Revenue Growth Analysis
* Earnings Growth Analysis
* Operating Margin Analysis
* Net Margin Analysis
* Debt-to-Equity Analysis
* Free Cash Flow Analysis
* Dividend Yield Analysis

### Business Quality Assessment

* Return on Equity (ROE)
* Return on Capital Employed (ROCE)
* Quality Score Generation
* Capital Efficiency Analysis
* Leverage Risk Assessment

### Valuation Engine

* Sector-relative P/E Analysis
* Premium / Discount Calculation
* PEG Ratio Analysis
* Price-to-Book Analysis
* Market Expectation Inference
* Valuation Reliability Assessment

### Technical Analysis

* RSI (14)
* MACD
* SMA50 / SMA200 Analysis
* Golden Cross / Death Cross Detection
* Volume Participation Analysis
* Trend Strength Assessment

### News Intelligence

* Recent News Aggregation
* Bullish/Bearish Signal Extraction
* Narrative Detection
* Market Sentiment Scoring

### Recommendation Engine

Combines:

* Business Quality
* Valuation
* Technical Momentum
* Market Sentiment

to generate:

* STRONG BUY
* BUY
* HOLD
* SELL
* STRONG SELL

recommendations with confidence levels.

---

## Example Output

```text
## Investment Brief: RELIANCE - Reliance Industries Ltd.

Recommendation: HOLD
Conviction: MEDIUM

Business Quality Score: 25/100

### Fundamental Snapshot
- Revenue Growth: 12.5%
- ROE: 8.9%
- ROCE: 11.3%
- Debt/Equity: 0.44
- Free Cash Flow: ₹692B

### Technical Picture
- RSI: 49.6
- MACD: Bearish
- Death Cross Active
- Volume: 56% of average

### News Sentiment
- Bullish (19 bullish vs 11 bearish signals)

### Valuation Analysis
- P/E: 21.9x
- Sector P/E: 7.4x
- PEG Ratio: 0.82
- Valuation: Fairly Valued

Final Recommendation: HOLD
```

---

## Research Workflow

```text
Ticker
│
├── Financial Statement Engine
│   ├── ROE
│   ├── ROCE
│   ├── Free Cash Flow
│   ├── Margins
│   └── Leverage Analysis
│
├── Business Quality Engine
│   └── Quality Score Generation
│
├── Valuation Engine
│   ├── Relative P/E Analysis
│   ├── PEG Ratio
│   ├── Price-to-Book Ratio
│   └── Market Growth Expectations
│
├── Technical Analysis Engine
│
├── News Intelligence Engine
│
└── LLM Investment Brief Generator
```

---

## Tech Stack

* Python
* LangChain
* LangGraph
* Groq LLM API
* yFinance
* Pandas TA
* Tavily Search
* Python Dotenv

---

## Project Structure

```text
financial_reporting_agent/
│
├── agent.py
├── graph.py
├── main.py
├── state.py
├── tools.py
├── requirements.txt
│
├── reports/
│   ├── Reliance_report.txt
│   ├── TCS_report.txt
│   └── ...
│
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/MananAgrawal176/financial_reporting_agent.git
cd financial_reporting_agent
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key
TAVILY_API_KEY=your_api_key
```

---

## Usage

Generate a report for a single stock:

```python
from main import research_stock

report = research_stock(
    "RELIANCE",
    stream=False
)

print(report)
```

Generate reports for multiple companies:

```python
from main import research_stock

tickers = [
    "RELIANCE",
    "TCS",
    "HDFCBANK",
    "INFY"
]

for ticker in tickers:
    report = research_stock(
        ticker,
        stream=False
    )

    with open(
        f"{ticker}_report.txt",
        "w",
        encoding="utf-8"
    ) as f:
        f.write(report)
```

---

## Philosophy

Most LLM stock agents simply summarize publicly available information.

This project follows a structured equity research workflow:

1. Understand business quality through financial statements.
2. Evaluate valuation relative to peers and growth expectations.
3. Assess technical momentum.
4. Analyze market sentiment.
5. Generate an evidence-backed investment recommendation.

The LLM acts as an explanation layer rather than the source of investment decisions.

---

## Future Improvements

* Discounted Cash Flow (DCF) Valuation
* Reverse DCF
* Piotroski F-Score
* Altman Z-Score
* Beneish M-Score
* Three Statement Forecasting
* Sector-Specific KPIs
* Portfolio Optimization
* Factor Investing Framework

---

## Author

**Manan Agrawal**
Chemical Engineering Undergraduate, IIT Bombay

Interests:

* Quantitative Finance
* Equity Research
* Financial Modelling
* AI Agents
* Financial Engineering

---

## License

This project is licensed under the MIT License.
