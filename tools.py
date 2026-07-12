# tools.py
import json
from datetime import datetime, timedelta
import pandas_ta as ta
import yfinance as yf
from langchain_core.tools import tool
from tavily import TavilyClient
tavily = TavilyClient()

# @tool
# def get_stock_financials(ticker: str) -> str:
    
#     """
#     Fetch key fundamental financial metrics for a stock ticker.
#     Returns P/E ratio, forward P/E, revenue growth (YoY), EPS (TTM),
#     profit margin, debt-to-equity ratio, and free cash flow yield.
#     Use this tool first to understand whether a company's fundamentals
#     are strong before diving into price-based analysis.
#     Works for both NSE tickers (e.g. RELIANCE.NS) and US tickers (e.g. AAPL).
#     """
#     try:
#         stock = yf.Ticker(ticker)  # [4]
#         info = stock.info
#         financials = stock.financials
#         balance_sheet = stock.balance_sheet
#         cashflow = stock.cashflow
        
#         fundamentals = {
#             "company_name": info.get("longName", ticker),
#             "sector": info.get("sector", "N/A"),
#             "market_cap_b": round(info.get("marketCap", 0) / 1e9, 2),
#             "pe_ratio_ttm": info.get("trailingPE"),
#             "pe_ratio_forward": info.get("forwardPE"),
#             "eps_ttm": info.get("trailingEps"),
#             "revenue_growth_yoy": info.get("revenueGrowth"),
#             "earnings_growth_yoy": info.get("earningsGrowth"),
#             "profit_margin": info.get("profitMargins"),
#             "operating_margin": info.get("operatingMargins"),
#             "debt_to_equity": debt_equity,
#             try:
#                total_debt = balance_sheet.loc["Total Debt"].iloc[0]
#                equity = balance_sheet.loc["Stockholders Equity"].iloc[0]

#                debt_equity = round(total_debt / equity, 2)
#             except:
#                debt_equity = None 
#             "current_ratio": info.get("currentRatio"),
#             "return_on_equity_pct": roe,
#             try:
#                net_income = financials.loc["Net Income"].iloc[0]
#                shareholder_equity = balance_sheet.loc["Stockholders Equity"].iloc[0]

#                roe = round(net_income / shareholder_equity * 100, 2)
#             except:
#                roe = None. 
#             "free_cash_flow_b": round(free_cash_flow/1e9,2),
#             try:
#                operating_cf = cashflow.loc["Operating Cash Flow"].iloc[0]
#                capex = abs(cashflow.loc["Capital Expenditure"].iloc[0])

#                free_cash_flow = operating_cf - capex
#             except:
#                free_cash_flow = None
#             "dividend_yield": info.get("dividendYield"),
#             "52_week_high": info.get("fiftyTwoWeekHigh"),
#             "52_week_low": info.get("fiftyTwoWeekLow"),
#             "current_price": info.get("currentPrice"),
#         }
#         # Flag key concerns automatically
#         concerns = []
#         if fundamentals["debt_to_equity"] and fundamentals["debt_to_equity"] > 200:
#             concerns.append("High debt-to-equity ratio - leverage risk")
#         if fundamentals["profit_margin"] and fundamentals["profit_margin"] < 0:
#             concerns.append("Negative profit margin - company is unprofitable")
#         if fundamentals["revenue_growth_yoy"] and fundamentals["revenue_growth_yoy"] < -0.05:
#             concerns.append("Revenue declining year-over-year")
#         fundamentals["flagged_concerns"] = concerns
#         return json.dumps(fundamentals, indent=2)
#     except Exception as e:
#         return json.dumps({"error": str(e), "ticker": ticker})

@tool
def get_stock_financials(ticker: str) -> str:
    """
    Fetch and compute key financial metrics for a stock.

    Computes:
    - ROE
    - ROCE
    - Debt to Equity
    - Free Cash Flow
    - Quality Score

    Works for both Indian (.NS) and US tickers.
    """

    try:
        # Automatically assume NSE ticker if no exchange suffix provided
        if "." not in ticker:
            ticker = ticker.upper() + ".NS"

        stock = yf.Ticker(ticker)

        info = stock.info
        financials = stock.financials
        balance_sheet = stock.balance_sheet
        cashflow = stock.cashflow

        # -------------------------------------------------------
        # Raw Financial Statement Calculations
        # -------------------------------------------------------

        try:
            net_income = financials.loc["Net Income"].iloc[0]
        except:
            net_income = None

        try:
            shareholder_equity = balance_sheet.loc[
                "Stockholders Equity"
            ].iloc[0]
        except:
            shareholder_equity = None

        try:
            total_debt = balance_sheet.loc[
                "Total Debt"
            ].iloc[0]
        except:
            total_debt = None

        try:
            operating_cf = cashflow.loc[
                "Operating Cash Flow"
            ].iloc[0]
        except:
            operating_cf = None

        try:
            capex = abs(
                cashflow.loc[
                    "Capital Expenditure"
                ].iloc[0]
            )
        except:
            capex = None

        try:
            ebit = financials.loc["EBIT"].iloc[0]
        except:
            ebit = None

        # -------------------------------------------------------
        # Financial Ratios
        # -------------------------------------------------------

        roe = None
        if net_income and shareholder_equity:
            roe = round(
                net_income / shareholder_equity * 100,
                2
            )

        debt_equity = None
        if total_debt and shareholder_equity:
            debt_equity = round(
                total_debt / shareholder_equity,
                2
            )

        free_cash_flow = None
        if operating_cf and capex:
            free_cash_flow = operating_cf - capex

        roce = None
        if ebit and total_debt and shareholder_equity:
            capital_employed = (
                total_debt +
                shareholder_equity
            )

            roce = round(
                ebit /
                capital_employed *
                100,
                2
            )

        # -------------------------------------------------------
        # Quality Score
        # -------------------------------------------------------

        quality_score = 0

        if roe and roe > 15:
            quality_score += 25

        if roce and roce > 15:
            quality_score += 25

        if debt_equity is not None and debt_equity < 0.5:
            quality_score += 25

        profit_margin = info.get("profitMargins")

        if profit_margin and profit_margin > 0.10:
            quality_score += 25

        # -------------------------------------------------------
        # Flag Concerns
        # -------------------------------------------------------

        concerns = []

        if debt_equity and debt_equity > 2:
            concerns.append(
                "High leverage risk"
            )

        if profit_margin and profit_margin < 0:
            concerns.append(
                "Company currently unprofitable"
            )

        if info.get("revenueGrowth") and \
           info["revenueGrowth"] < -0.05:
            concerns.append(
                "Revenue declining YoY"
            )

        # -------------------------------------------------------
        # Final Output
        # -------------------------------------------------------

        fundamentals = {
            "company_name":
                info.get("longName", ticker),

            "sector":
                info.get("sector", "N/A"),

            "market_cap_b":
                round(
                    info.get("marketCap", 0) / 1e9,
                    2
                ),

            "current_price":
                info.get("currentPrice"),

            "trailing_pe":
                info.get("trailingPE"),

            "forward_pe":
                info.get("forwardPE"),

            "eps":
                info.get("trailingEps"),

            "revenue_growth":
                info.get("revenueGrowth"),

            "profit_margin":
                profit_margin,

            "operating_margin":
                info.get("operatingMargins"),

            "roe_pct":
                roe,

            "roce_pct":
                roce,

            "debt_to_equity":
                debt_equity,

            "free_cash_flow_b":
                round(
                    free_cash_flow / 1e9,
                    2
                ) if free_cash_flow else None,

            "dividend_yield":
                info.get("dividendYield"),

            "52_week_high":
                info.get("fiftyTwoWeekHigh"),

            "52_week_low":
                info.get("fiftyTwoWeekLow"),

            "quality_score":
                quality_score,

            "flagged_concerns":
                concerns
        }

        return json.dumps(
            fundamentals,
            indent=2
        )

    except Exception as e:
        return json.dumps({
            "error": str(e),
            "ticker": ticker
        })

@tool
def get_news_sentiment(ticker: str) -> str:
    """
    Search for recent news about a stock ticker and analyse overall sentiment.
    Returns the top 5 recent headlines with publication dates and URLs,
    a sentiment classification (BULLISH / BEARISH / NEUTRAL), and
    a brief reasoning for the sentiment call.
    Use this tool to understand current market narrative and any recent
    events (earnings, regulatory issues, product launches, macro exposure)
    that could affect the stock's near-term trajectory.
    """
    try:
        stock = yf.Ticker(ticker)
        company_name = stock.info.get("longName", ticker)
        # Search for recent news via Tavily [6]
        results = tavily.search(
            query=f"{company_name} {ticker} stock news analysis 2025 2026",
            max_results=5,
            search_depth="advanced",
        )
        headlines = []
        content_for_sentiment = []
        for r in results.get("results", []):
            headlines.append({
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "published_date": r.get("published_date", ""),
                "snippet": r.get("content", "")[:300],
            })
            content_for_sentiment.append(r.get("content", ""))
        # Simple keyword-based sentiment scoring
        combined_text = " ".join(content_for_sentiment).lower()
        bullish_keywords = [
            "beat", "exceeded", "strong", "growth", "upgrade", "buy",
            "outperform", "record", "surge", "rally", "positive", "robust"
        ]
        bearish_keywords = [
            "miss", "disappointed", "weak", "decline", "downgrade", "sell",
            "underperform", "concern", "risk", "drop", "fell", "negative",
            "lawsuit", "investigation", "layoff"
        ]
        bullish_score = sum(combined_text.count(kw) for kw in bullish_keywords)
        bearish_score = sum(combined_text.count(kw) for kw in bearish_keywords)
        if bullish_score > bearish_score * 1.5:
            sentiment = "BULLISH"
            sentiment_reasoning = f"News skews positive ({bullish_score} bullish signals vs {bearish_score} bearish)"
        elif bearish_score > bullish_score * 1.5:
            sentiment = "BEARISH"
            sentiment_reasoning = f"News skews negative ({bearish_score} bearish signals vs {bullish_score} bullish)"
        else:
            sentiment = "NEUTRAL"
            sentiment_reasoning = f"Mixed signals ({bullish_score} bullish, {bearish_score} bearish)"
        output = {
            "ticker": ticker,
            "company": company_name,
            "headlines": headlines,
            "overall_sentiment": sentiment,
            "sentiment_reasoning": sentiment_reasoning,
            "bullish_signal_count": bullish_score,
            "bearish_signal_count": bearish_score,
        }
        return json.dumps(output, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e), "ticker": ticker})


@tool
def get_technical_indicators(ticker: str) -> str:
    """
    Calculate technical analysis indicators for a stock using the last
    200 days of price data. Returns RSI (14-day), MACD and signal line,
    50-day and 200-day SMAs, Golden/Death Cross status, and volume analysis.
    Use this tool to assess whether the stock is in a technically
    favourable or unfavourable position for entry.
    RSI above 70 = overbought. RSI below 30 = oversold.
    Golden cross (SMA50 > SMA200) is bullish; death cross is bearish.
    """
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period="200d")  # [4]
        if df.empty or len(df) < 50:
            return json.dumps({"error": "Insufficient price history", "ticker": ticker})
        # RSI [5]
        df.ta.rsi(length=14, append=True)
        rsi = round(df["RSI_14"].iloc[-1], 2)
        # MACD [5]
        df.ta.macd(fast=12, slow=26, signal=9, append=True)
        macd_val = round(df["MACD_12_26_9"].iloc[-1], 4)
        macd_signal = round(df["MACDs_12_26_9"].iloc[-1], 4)
        macd_histogram = round(df["MACDh_12_26_9"].iloc[-1], 4)
        # SMAs [5]
        df.ta.sma(length=50, append=True)
        df.ta.sma(length=200, append=True)
        sma_50 = round(df["SMA_50"].iloc[-1], 2)
        sma_200 = round(df["SMA_200"].iloc[-1], 2) if len(df) >= 200 else None
        current_price = round(df["Close"].iloc[-1], 2)
        # Golden/Death Cross
        if sma_200:
            cross_status = (
                "GOLDEN CROSS (bullish - SMA50 above SMA200)"
                if sma_50 > sma_200
                else "DEATH CROSS (bearish - SMA50 below SMA200)"
            )
        else:
            cross_status = "N/A (insufficient data for SMA200)"
        # Volume
        avg_volume_30d = int(df["Volume"].tail(30).mean())
        current_volume = int(df["Volume"].iloc[-1])
        volume_ratio = round(current_volume / avg_volume_30d, 2)
        rsi_signal = (
            "OVERBOUGHT - potential reversal ahead" if rsi > 70
            else "OVERSOLD - potential buying opportunity" if rsi < 30
            else f"NEUTRAL ({rsi})"
        )
        macd_signal_str = (
            "BULLISH - MACD above signal line"
            if macd_val > macd_signal
            else "BEARISH - MACD below signal line"
        )
        technicals = {
            "ticker": ticker,
            "current_price": current_price,
            "rsi_14": rsi,
            "rsi_signal": rsi_signal,
            "macd": macd_val,
            "macd_signal_line": macd_signal,
            "macd_histogram": macd_histogram,
            "macd_interpretation": macd_signal_str,
            "sma_50": sma_50,
            "sma_200": sma_200,
            "cross_status": cross_status,
            "price_vs_sma50_pct": round((current_price - sma_50) / sma_50 * 100, 2),
            "volume_30d_avg": avg_volume_30d,
            "volume_today": current_volume,
            "volume_ratio_vs_avg": volume_ratio,
            "volume_note": (
                "Above average" if volume_ratio > 1.2
                else "Below average" if volume_ratio < 0.8
                else "In line with average"
            ),
        }
        return json.dumps(technicals, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e), "ticker": ticker})

# Nifty 500 sector representative tickers
# These are liquid, well-covered stocks whose PE is reliable
SECTOR_REPRESENTATIVES = {
    "Energy": ["ONGC.NS", "IOC.NS", "BPCL.NS"],
    "Technology": ["TCS.NS", "INFY.NS", "WIPRO.NS"],
    "Financial Services": ["HDFCBANK.NS", "ICICIBANK.NS", "KOTAKBANK.NS"],
    "Banks": ["HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS"],
    "Healthcare": ["SUNPHARMA.NS", "DRREDDY.NS", "CIPLA.NS"],
    "Consumer Defensive": ["HINDUNILVR.NS", "NESTLEIND.NS", "BRITANNIA.NS"],
    "Consumer Cyclical": ["TITAN.NS", "MARUTI.NS", "BAJAJ-AUTO.NS"],
    "Industrials": ["LT.NS", "SIEMENS.NS", "ABB.NS"],
    "Basic Materials": ["JSWSTEEL.NS", "TATASTEEL.NS", "HINDALCO.NS"],
    "Communication Services": ["BHARTIARTL.NS", "IDEA.NS"],
    "Utilities": ["NTPC.NS", "POWERGRID.NS", "TATAPOWER.NS"],
}

def get_sector_pe(sector: str, exclude_ticker: str = None) -> float | None:
    """
    Compute median PE from representative peers in the same sector.
    Excludes the stock being analysed to avoid circular comparison.
    Returns None if data is insufficient.
    """
    peers = SECTOR_REPRESENTATIVES.get(sector, [])
    pe_values = []

    for peer_ticker in peers:
        if peer_ticker == exclude_ticker:
            continue
        try:
            peer_info = yf.Ticker(peer_ticker).info
            pe = peer_info.get("trailingPE")
            # Sanity filter: ignore negative or absurdly high PE
            if pe and 7 < pe < 200:  # change 3 → 7
               pe_values.append(pe)
        except:
            continue

    if not pe_values:
        return None

    # Median is more robust than mean — one outlier won't skew it
    pe_values.sort()
    mid = len(pe_values) // 2
    return round(pe_values[mid], 1)

@tool
def get_valuation_analysis(ticker: str) -> str:
    """
    Perform relative valuation analysis for a stock.

    Computes:
    - P/E premium or discount relative to sector
    - Valuation classification
    - Market growth expectations
    """
    # Conglomerate heuristic: if a company operates across 3+ industries,
    # the sector PE comparison may be misleading
    
    try:
        # Assume NSE ticker if no suffix provided
        if "." not in ticker:
            ticker = ticker.upper() + ".NS"

        stock = yf.Ticker(ticker)
        info = stock.info

        company_name = info.get("longName", ticker)
        sector = info.get("sector", "Unknown")

        pe_ratio = info.get("trailingPE")
        pb_ratio = info.get("priceToBook")
        peg_ratio = info.get("pegRatio")

        # Approximate Indian sector averages
        SECTOR_PE = {
            "Technology": 28,
            "Banks": 15,
            "Financial Services": 18,
            "Consumer Defensive": 55,
            "Healthcare": 35,
            "Energy": 12,
            "Industrials": 25,
            "Basic Materials": 18,
            "Communication Services": 20,
            "Utilities": 16,
            "Consumer Cyclical": 30,
        }

        sector_pe = get_sector_pe(sector, exclude_ticker=ticker)
        sector_pe_source = "computed from sector peers" if sector_pe else "unavailable"

        premium_discount = None
        valuation_label = "Unavailable"

        if pe_ratio and sector_pe:
            premium_discount = round(
                (pe_ratio - sector_pe) / sector_pe * 100,
                2
            )

            if premium_discount < -20:
                valuation_label = "Significantly Undervalued"

            elif premium_discount < -5:
                valuation_label = "Undervalued"

            elif premium_discount <= 10:
                valuation_label = "Fairly Valued"

            elif premium_discount <= 30:
                valuation_label = "Expensive"

            else:
                valuation_label = "Highly Expensive"

        # Reverse DCF Lite
        if pe_ratio is None:
            market_expectation = "Unavailable"

        elif pe_ratio < 15:
            market_expectation = (
                "Market expects low growth or cyclicality."
            )

        elif pe_ratio < 25:
            market_expectation = (
                "Market expects moderate long-term growth."
            )

        elif pe_ratio < 40:
            market_expectation = (
                "Market expects strong earnings growth."
            )

        else:
            market_expectation = (
                "Market pricing in very aggressive future growth assumptions."
            )

        output = {
            "ticker": ticker,
            "company_name": company_name,
            "sector": sector,

            "pe_ratio": pe_ratio,
            "sector_average_pe": sector_pe,
            "pe_premium_discount_pct": premium_discount,

            "price_to_book": pb_ratio,
            "peg_ratio": peg_ratio,

            "valuation_label": valuation_label,
            "market_expectation": market_expectation,
        }
        CONGLOMERATE_KEYWORDS = [
            "industries", "enterprises", "group", "holdings", "ventures"
        ]
        is_likely_conglomerate = any(
            kw in company_name.lower() for kw in CONGLOMERATE_KEYWORDS
        )

        if is_likely_conglomerate:
            output["sector_pe_reliability"] = (
                "LOW - company name suggests conglomerate; "
                "sector PE benchmark may not reflect true peer set"
            )
            output["valuation_label"] = (
                "Unreliable - conglomerate; no valid sector benchmark"
            )
            output["pe_premium_discount_pct"] = None
        else:
            output["sector_pe_reliability"] = "HIGH"

        return json.dumps(output, indent=2)

    except Exception as e:
        return json.dumps({
            "ticker": ticker,
            "error": str(e)
        })

# Register all tools for the agent
TOOLS = [
    get_stock_financials,
    get_news_sentiment,
    get_sector_pe,
    get_technical_indicators,
    get_valuation_analysis,   
]