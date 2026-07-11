# Financial Reporting Agent

An AI-powered financial research agent that autonomously performs multi-dimensional equity analysis and generates institutional-style investment briefs.

Built using **LangGraph**, **LangChain**, and **LLMs**, the agent combines:

- Fundamental Analysis
- Technical Analysis
- News & Market Sentiment
- Analyst Consensus

to produce a single comprehensive investment report for any stock ticker.

---

## Features

- Multi-agent research workflow using LangGraph
- Automated tool calling for financial data retrieval
- Structured investment recommendations
- Institutional-style investment brief generation
- Modular architecture for easy extension
- Supports multiple LLM providers (OpenAI, Groq, etc.)

---

## Research Pipeline

The agent follows the same workflow used by professional equity analysts:

```text
Stock Ticker
     │
     ▼
Fundamental Analysis
     │
     ▼
News Sentiment Analysis
     │
     ▼
Technical Analysis
     │
     ▼
Analyst Consensus
     │
     ▼
Investment Brief Generation
```

---

## Example Output

```text
## Investment Brief: NVDA - NVIDIA Corporation

Recommendation: BUY
Conviction: HIGH

Bull Case:
- Strong AI infrastructure demand continues to drive growth.
- Industry-leading margins and dominant market position.

Bear Case:
- Valuation remains significantly above historical averages.
- AI spending slowdown could compress multiples.

Fundamental Snapshot:
- Revenue Growth: 69%
- Gross Margin: 75%
- P/E Ratio: 48x
- Debt/Equity: 0.14

Technical Picture:
- RSI: 61
- Price above 50DMA and 200DMA
- Positive MACD crossover

News Sentiment:
- Positive AI demand narrative continues.
- Strong data-center spending outlook.

Analyst Consensus:
- Majority Buy rating.
- Average target price implies upside potential.

Final Verdict:
Strong business fundamentals combined with favourable momentum
support a BUY recommendation despite elevated valuation.
```

---

## Project Structure

```text
financial_reporting_agent/
│
├── agent.py          # LLM configuration and tool binding
├── graph.py          # LangGraph workflow definition
├── state.py          # Shared graph state management
├── tools.py          # Financial research tools
├── main.py           # Entry point
│
├── demo_reports_generated/
│   └── Sample generated reports
│
└── README.md
```

---

## Technology Stack

- Python
- LangChain
- LangGraph
- OpenAI / Groq LLMs
- Financial APIs
- News APIs

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

Set environment variables:

```bash
OPENAI_API_KEY=your_key_here
GROQ_API_KEY=your_key_here
```

---

## Usage

Run the agent:

```bash
python main.py
```

Example:

```text
Enter ticker: AAPL
```

The agent will automatically:

1. Retrieve financial fundamentals
2. Analyse recent news sentiment
3. Perform technical analysis
4. Check analyst expectations
5. Generate an investment brief

---

## Sample Use Cases

- Equity research automation
- Investment screening
- Personal portfolio research
- Financial education
- Analyst productivity tools

---

## Future Improvements

- Portfolio-level analysis
- Valuation models (DCF, Comparable Multiples)
- Earnings call transcript analysis
- SEC filing summarisation
- Risk scoring framework
- Backtesting recommendations

---

## Author

**Manan Agrawal**

Chemical Engineering Undergraduate, IIT Bombay

Interested in:
- Quantitative Finance
- AI Agents
- Financial Modelling
- Applied Machine Learning

---

## License

This project is licensed under the MIT License.