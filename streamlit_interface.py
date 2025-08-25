import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from scipy import stats
from streamlit_option_menu import option_menu
from statistics import mean
import math

# Set the page config
st.set_page_config(page_title="My App", layout="centered")

# Sidebar for navigation
st.sidebar.title("Navigation")

with st.sidebar:
    page = option_menu(
        "Navigation",
        ["Home", "Value investing", "equal weight investing" , "dividend based investing"],
        icons=["house", "bar-chart", "envelope"],
        menu_icon="cast",
        default_index=0,
    )

tickers = pd.read_csv(r"C:\Users\KIIT\Desktop\Code\top_50_indian_stocks.csv")

# ---- CACHE ALL YAHOO DATA ----
@st.cache_data(show_spinner="Downloading all Yahoo Finance data...")
def get_all_yahoo_data(ticker_list):
    price_data = yf.download(ticker_list, period='1d', group_by='ticker', auto_adjust=False, threads=True)
    info_data = {}
    for ticker in ticker_list:
        try:
            info_data[ticker] = yf.Ticker(ticker).info
        except Exception:
            info_data[ticker] = {}
    return price_data, info_data

ticker_list = tickers["Ticker"].dropna().astype(str).tolist()
price_data, info_data = get_all_yahoo_data(ticker_list)

# ---- DEFINE PAGES ----

def home_page():
    st.title("🏠 Home")
    st.write("Welcome to the home page of your app.")

def Value_investing_stratergy_page():
    st.title("VALUE INVESTING STRATERGY")
    st.write("Value investing is an investment philosophy that involves purchasing assets at a discount to their intrinsic value. This is also known as a security’s margin of safety. The principle behind value investing is – purchase stocks when they are undervalued or on sale, and sell them when they reach their true or intrinsic value, or rise above it.")

    st.subheader(" ANALYSING THE NIFTY50 STOCKS ")

    value_cols = [
        "TICKERS",
        "PRICE",
        'PE-RATIO',
        'PB-RATIO',
        'PS-RATIO',
        'EV/EBITA',
        'EV/GP'
    ]

    value_df = pd.DataFrame(columns=value_cols)
    for ticker in ticker_list:

        price = price_data[ticker]['Close'].iloc[-1] if not price_data[ticker]['Close'].empty else np.nan
        info = info_data.get(ticker, {})
        PE_RATIO = info.get("forwardPE", np.nan)
        PB_RATIO = info.get("priceToBook", np.nan)
        PS_RATIO = info.get("priceToSalesTrailing12Months", np.nan)
        EV = info.get("enterpriseValue", np.nan)
        EBITA = info.get("ebitda", np.nan)
        evEbita = EV / EBITA if EV and EBITA else np.nan
        grossProfit = info.get("grossMargins", np.nan) * info.get("totalRevenue", np.nan) if info.get("grossMargins") and info.get("totalRevenue") else np.nan
        evGrossProfit = EV / grossProfit if EV and grossProfit else np.nan

        value_df.loc[len(value_df)] = [
            ticker,
            price,
            PE_RATIO,
            PB_RATIO,
            PS_RATIO,
            evEbita,
            evGrossProfit
        ]

    # HANDLING MISSING VALUES
    value_cols=[
        'PE-RATIO',
        'PB-RATIO',
        'PS-RATIO',
        'EV/EBITA',
        'EV/GP'
    ]
    for col in value_cols:
        value_df[col] = value_df[col].fillna(value_df[col].mean())

    st.dataframe(value_df, width=700, height=300) #displaying NIFTY50 STOCS ALONG WITH THEIR STATS.

    # CALCULATING VALUE_SCORE
    st.subheader("VALUE SCORES OF EACH COMPANY")

    percentile_metrics = {
        "PE-RATIO": "PE RATIO PERCENTILE",
        "PB-RATIO": "PB RATIO PERCENTILE",
        "PS-RATIO": "PS RATIO PERCENTILE",
        "EV/EBITA": "EV/EBITA PERCENTILE",
        "EV/GP": "EV/GP"
    }

    for metrics, percentile in percentile_metrics.items():
        value_df[percentile] = value_df[metrics].apply(lambda x: stats.percentileofscore(value_df[metrics], x) / 100)

    value_df['VALUE_SCORE'] = value_df[[value for value in percentile_metrics.values()]].mean(axis=1)

    # DISPLAYING THE FINAL DATAFRAME ALONG WITH VALUE SCORE OF EACH COMPANY
    value_df = value_df.sort_values(by='VALUE_SCORE', ascending=False)
    st.dataframe(value_df, width=700, height=300)

def equal_weights_stratergy_page():
    st.title("EQUAL WEIGHTS STRATERGY")
    st.write("Equal weight is a type of proportional measuring method that gives the same importance to each stock in a portfolio, index, or index fund. So stocks of the smallest companies are given equal statistical significance, or weight, to the largest companies when it comes to evaluating the overall group's performance.")
    st.subheader("ANALYSING NIFTY50 STOCKS")

    all_tickers = tickers["Ticker"].dropna().astype(str).tolist()
    selected_tickers = st.multiselect(
        "Select companies to invest in:",
        options=all_tickers,
        default=all_tickers[:10]
    )

    if not selected_tickers:
        st.warning("Please select at least one company.")
        return

    # Use cached data for selected tickers
    stocks_data = []
    for ticker in selected_tickers:
        try:
            latest_price = price_data[ticker]['Close'].iloc[-1] if not price_data[ticker]['Close'].empty else np.nan
        except Exception:
            latest_price = np.nan
        market_cap = info_data.get(ticker, {}).get("marketCap", np.nan)
        stocks_data.append({
            "Ticker": ticker,
            "Market Cap": market_cap,
            "Latest Price": latest_price,
        })
    df_equal_weights = pd.DataFrame(stocks_data)

    portfolio_size = st.number_input("ENTER THE AMOUNT YOU WANT TO INVEST", min_value=1, value=10000)
    position_size = portfolio_size / len(df_equal_weights.index) if len(df_equal_weights.index) > 0 else 0

    df_equal_weights['No. of shares to buy'] = df_equal_weights['Latest Price'].apply(
        lambda price: math.floor(position_size / price) if price and price > 0 else 0
    )

    # Calculate total invested and remaining cash
    df_equal_weights['Invested Amount'] = df_equal_weights['No. of shares to buy'] * df_equal_weights['Latest Price']
    total_invested = df_equal_weights['Invested Amount'].sum()
    remaining_cash = portfolio_size - total_invested

    st.dataframe(df_equal_weights[['Ticker', 'Latest Price', 'No. of shares to buy']], width=700, height=300)
    st.info(f"Remaining amount after investing: ₹{remaining_cash:,.2f}")

def dividend_stratergy_page():
    st.title('DIVIDEND BASED INVESTING STRATEERGY')
    st.write("The dividend capture strategy is a timing-oriented investment strategy involving purchasing and later selling dividend-paying stocks. The method calls for buying a stock just before the ex-dividend date to receive the dividend and then selling it once it has been paid. The purpose of the two trades is to receive the dividend instead of investing for the longer term.")
    st.subheader("ANALYSING NIFTY50 STOCKS")

    columns = [
        "Ticker",
        'Dividend Yield(%)',
        'Dividend Rate',
        'Payout Ratio(%)',
        '5 Year Avg Dividend Yield(%)',
        'Earning Growth(%)'
    ]

    dividend_df = pd.DataFrame(columns=columns)

    for stock in ticker_list:
        info = info_data.get(stock, {})
        dividend_yield = info.get("dividendYield", np.nan) * 100 if info.get("dividendYield") else np.nan
        dividend_rate = info.get("dividendRate", np.nan)
        payout_ratio = info.get("payoutRatio", np.nan) * 100 if info.get("payoutRatio") else np.nan
        five_year_avg_dividend_yield = info.get("fiveYearAvgDividendYield", np.nan) * 100 if info.get("fiveYearAvgDividendYield") else np.nan
        earning_growth = info.get("earningsGrowth", np.nan) * 100 if info.get("earningsGrowth") else np.nan

        dividend_df.loc[len(dividend_df)] = [stock, dividend_yield, dividend_rate, payout_ratio, five_year_avg_dividend_yield, earning_growth]

    numeric_cols = [
        "Dividend Yield(%)",
        "Dividend Rate",
        'Payout Ratio(%)',
        '5 Year Avg Dividend Yield(%)',
        'Earning Growth(%)'
    ]

    for col in numeric_cols:
        if col == 'Payout Ratio(%)':
            dividend_df[col + " Normalised"] = 1 - ((dividend_df[col] - dividend_df[col].min()) / (dividend_df[col].max() - dividend_df[col].min()))
        else:
            dividend_df[col + " Normalised"] = (dividend_df[col] - dividend_df[col].min()) / (dividend_df[col].max() - dividend_df[col].min())

    st.dataframe(dividend_df, width=700, height=700)

    # CALCULATING THE DIVIDEND SCORE
    st.subheader("NIFTY50 STOCKS ALONG WITH THEIR DIVIDEND SCORE")
    weights = {
        "Dividend Yield(%) Normalised": 0.3,
        "Dividend Rate Normalised": 0.2,
        "Payout Ratio(%) Normalised": 0.2,
        "5 Year Avg Dividend Yield(%) Normalised": 0.2,
        "Earning Growth(%) Normalised": 0.1
    }
    dividend_df['Dividend score'] = dividend_df[[col for col in weights.keys()]].mul(list(weights.values())).sum(axis=1)
    dividend_df = dividend_df.sort_values(by="Dividend score", ascending=False)

    st.dataframe(dividend_df[['Ticker', 'Dividend Yield(%)', 'Dividend Rate', 'Dividend score']], width=700, height=700)

# ---- PAGE ROUTING ----
if page == "Home":
    home_page()
elif page == "Value investing":
    Value_investing_stratergy_page()
elif page == "equal weight investing":
    equal_weights_stratergy_page()
elif page == "dividend based investing":
    dividend_stratergy_page()