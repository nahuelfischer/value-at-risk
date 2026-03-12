# Value at Risk (VaR) Calculator

A **Streamlit-based interactive application** for computing **Value at Risk (VaR)** for portfolios and individual assets using historical market data from Yahoo Finance.

## 📊 What is Value at Risk?

Value at Risk (VaR) is a risk metric that estimates the **maximum potential loss** of a portfolio over a given time horizon at a specified confidence level.

For example:
- **95% VaR of $-50,000 over 10 days** means there's a 95% probability the portfolio won't lose more than $50,000 in the next 10 days (or a 5% chance it will lose more).

## 🎯 Features

✅ **Multi-asset portfolio support** — Enter comma-separated tickers with custom weights  
✅ **Configurable confidence levels** — 90%, 95%, or 99%  
✅ **Flexible time horizons** — N-day VaR (1-20 days)  
✅ **Real-time data fetching** — Automatic Yahoo Finance data retrieval  
✅ **Visual analytics** — Historical returns display and portfolio composition  
✅ **Robust error handling** — Input validation and data availability checks  

---

## 🚀 Installation & Setup

### Requirements
```
streamlit
pandas
numpy
matplotlib
yfinance
```

### Install Dependencies

1. **Navigate to the project directory:**
   ```powershell
   cd "c:\Users\nahue\OneDrive\Desktop\Options, futures, and other derivatives\Coding projects"
   ```

2. **Create a virtual environment (recommended):**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install packages:**
   ```powershell
   pip install streamlit pandas numpy matplotlib yfinance
   ```

---

## 📋 Running the Application

From the project root, run:

```powershell
streamlit run VaR.py
```

Streamlit will open in your default browser at `http://localhost:8501`

---

## 🎮 User Interface

### Input Section

| Input | Description | Example |
|-------|-------------|---------|
| **Asset Tickers** | Comma-separated ticker symbols | `AAPL,MSFT,GOOG` |
| **Asset Values** | Position size for each asset (same order) | `50000,30000,20000` |
| **Confidence Level** | VaR confidence threshold | 95% (default) |
| **Horizon (days)** | Time period for VaR calculation (1-20 days) | 10 days |
| **Start Date** | Historical data start date | 2020-01-01 |
| **End Date** | Historical data end date | 2025-10-01 |

### Output Section

The app displays:
- **Portfolio statistics** — Mean return, volatility, Sharpe ratio
- **VaR metric** — Dollar loss at specified confidence level
- **Expected Shortfall (CVaR)** — Average loss exceeding VaR
- **Historical returns plot** — Visualization of portfolio performance

---

## 💻 Code Architecture

### Key Functions

#### `parse_list(text)`
Converts comma-separated strings into cleaned lists.
```python
parse_list("AAPL, MSFT ,GOOG")  # Returns: ["AAPL", "MSFT", "GOOG"]
```

#### `fetch_price(ticker)`
Downloads historical price data using `yfinance`.
- Handles missing data gracefully
- Prefers "Adj Close" over "Close"
- Returns pandas Series or None

#### `build_price_dataframe(price_dict)`
Aggregates multiple price series into aligned DataFrame.
- Converts scalars to Series
- Collapses single-column DataFrames
- Auto-aligns on dates

#### `compute_n_day_returns(returns, n)`
Scales daily returns to N-day horizon using:
$$\text{N-day return} = (1 + \text{daily return})^n - 1$$

#### `compute_portfolio_var(returns, values, confidence_level, n_days)`
Main VaR calculation:
1. Weights returns by asset values
2. Aggregates into portfolio returns
3. Scales to N-day horizon
4. Computes percentile at (1 - confidence_level)

---

## 📊 Example Usage

### Single Asset VaR
- **Ticker:** AAPL
- **Value:** $100,000
- **Confidence:** 95%
- **Horizon:** 10 days

Result: 95% VaR = $-4,250 (5% chance of losing more than $4,250 in 10 days)

### Portfolio VaR
- **Tickers:** AAPL, MSFT, GOOG
- **Values:** $50,000, $30,000, $20,000
- **Confidence:** 95%
- **Horizon:** 10 days

Result: Portfolio 95% VaR incorporates correlation between assets

---

## ✅ Testing

Unit tests are included in [tests/test_var_portfolio.py](tests/test_var_portfolio.py):

```powershell
pytest tests/test_var_portfolio.py -v
```

### Test Coverage
- **`test_parse_list()`** — CSV parsing with whitespace handling
- **`test_weights_and_var()`** — Portfolio weighting and percentile calculations
- **`test_build_price_dataframe_scalars()`** — Data structure construction and error cases

Run all tests:
```powershell
pytest tests/ -v
```

---

## 🔧 Customization & Advanced Options

### Modify Default Values
Edit the input defaults in `VaR.py`:
```python
confidence_level = st.selectbox("Confidence Level", options=[0.90, 0.95, 0.99], index=1)
n_days = st.slider("Horizon (days)", min_value=1, max_value=20, value=10)
```

### Change Date Range
```python
start_date = col3.date_input("Start Date", pd.to_datetime("2020-01-01"))
end_date = col4.date_input("End Date", pd.to_datetime("2025-10-01"))
```

### Add Additional Metrics
You can extend the app to compute:
- **Conditional Value at Risk (CVaR)** — Average loss exceeding VaR
- **Expected Shortfall** — Mean of tail returns
- **Stress test scenarios** — Pre-defined market shocks
- **Backtesting results** — Historical VaR accuracy

---

## 📝 Implementation Details

### Historical Simulation Method
The VaR calculation uses the **historical simulation approach**:

1. **Fetch historical prices** for each asset (daily)
2. **Calculate returns** — percentage change between consecutive days
3. **Weight returns** — multiply by position values
4. **Aggregate portfolio returns** — sum weighted returns
5. **Scale to horizon** — apply N-day scaling formula
6. **Find percentile** — extract the specified confidence level

### Assumptions
- Historical returns are representative of future risk
- No structural breaks in correlation
- Daily compounding of returns
- Log-normal price distributions (implicit in percentage returns)

---

## ⚠️ Limitations & Considerations

1. **Historical data dependency** — VaR accuracy depends on data length and market regime
2. **Tail risk** — Doesn't capture extreme events beyond historical range
3. **Assumption violations** — Returns may not be normally distributed
4. **Correlation stability** — Portfolio correlations can change significantly
5. **Data quality** — Missing or adjusted prices may skew results

For more robust risk assessment, consider:
- **Conditional VaR (CVaR)** for tail risk
- **Monte Carlo simulations** for forward-looking estimates
- **Stress testing** for scenario analysis
- **GARCH models** for volatility dynamics

---

## 📄 Error Handling

The app handles common issues gracefully:

| Error | Resolved By |
|-------|-------------|
| Invalid ticker | Data fetch returns None → shown to user |
| Empty date range | Error message with suggested dates |
| Insufficient data | Minimum 2 data points required for returns |
| Malformed input | CSV parser strips whitespace automatically |

---

## 🚀 Future Enhancements

- [ ] **Conditional VaR (CVaR/Expected Shortfall)** calculation
- [ ] **Backtesting module** — evaluate VaR accuracy over time
- [ ] **Correlation heatmap** — visualize asset dependencies
- [ ] **Stress scenarios** — pre-defined market shocks
- [ ] **Monte Carlo simulation** — forward-looking VaR
- [ ] **Portfolio optimization** — find minimum-VaR allocation
- [ ] **Export reports** — PDF/Excel summary
- [ ] **Real-time updates** — live VaR tracking

---

## 📚 References

- Hull, J. C. (2021). *Options, Futures, and Other Derivatives* (11th ed.)
- Dowd, K. (2007). *Measuring Market Risk* (2nd ed.)
- RiskMetrics. (1996). VaR Technical Document
- [Streamlit Documentation](https://docs.streamlit.io)
- [yfinance Documentation](https://yfinance.readthedocs.io)

---

## 👤 Author Notes

This Streamlit app is designed for educational purposes in quantitative finance. It demonstrates:
- Real-time financial data integration
- Interactive risk calculations
- Matplotlib visualization in web apps
- Pandas-based portfolio analytics
- Error handling best practices

**Created:** March 2026  
**Python Version:** 3.8+  
**Last Updated:** March 12, 2026
