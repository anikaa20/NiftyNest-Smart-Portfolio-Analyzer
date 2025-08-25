# NiftyNest: Smart Portfolio Analyzer

## Overview

**NiftyNest** is a Streamlit-based web application for analyzing and constructing portfolios from the top 50 Indian stocks. It provides three investment strategies:
- **Value Investing**
- **Equal Weight Investing**
- **Dividend-Based Investing**

All stock data is fetched from Yahoo Finance and cached for fast, interactive analysis.

---

## Features

- **Value Investing:**  
  Ranks stocks based on valuation metrics and calculates a value score for each company.

- **Equal Weight Investing:**  
  Lets users select companies, enter an investment amount, and calculates how many shares to buy for each selected stock. Displays the remaining cash after allocation.

- **Dividend-Based Investing:**  
  Shows dividend metrics and scores for each stock, helping users identify strong dividend payers.

- **Fast Performance:**  
  All Yahoo Finance data is downloaded and cached at startup for instant page loads.

---

## Installation

1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd <your-repo-folder>
   ```

2. **Install dependencies:**
   ```sh
   pip install streamlit pandas numpy yfinance scipy streamlit-option-menu
   ```

3. **Download the stock list:**
   - Place your `top_50_indian_stocks.csv` file in the project folder.
   - The CSV should have a column named `Ticker` with stock symbols.

---

## Usage

1. **Run the app:**
   ```sh
   streamlit run streamlit_interface.py
   ```

2. **Navigate using the sidebar:**
   - Home
   - Value investing
   - Equal weight investing
   - Dividend based investing

3. **Interact with the pages:**
   - Select companies, enter investment amounts, and view analytics.

---

## File Structure

- `streamlit_interface.py` — Main Streamlit app
- `top_50_indian_stocks.csv` — List of stock tickers

---

## Customization

- Update `top_50_indian_stocks.csv` to change the universe of stocks.
- Modify weights and metrics in the code to suit your strategy.

---

## License

This project is for educational and personal use.  
Stock data is fetched from Yahoo Finance.

---

## Credits

Developed using:
- [Streamlit](https://streamlit.io/)
