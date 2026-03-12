import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Value at Risk (VaR) Calculator", layout="centered")

st.title("📊 Value at Risk (VaR) Calculator")

st.markdown("""This tool computes the **Value at Risk (VaR)** for a given portfolio or individual asset using historical data.

You can enter a single ticker/value pair, or supply a comma-separated list of tickers and corresponding values to calculate the VaR of a portfolio. Values are used to weight each asset's returns in the aggregation.
""")

# --- User Inputs ---
col1, col2 = st.columns(2)
# allow comma-separated tickers and values for portfolio
tickers_input = col1.text_input(
    "Asset Tickers (comma-separated, e.g. AAPL,MSFT)",
    value="AAPL",
    placeholder="e.g. AAPL,MSFT,GOOG"
)
values_input = col2.text_input(
    "Asset values (comma-separated, same order)",
    value="1000",
    placeholder="e.g. 5000,3000,2000"
)
confidence_level = st.selectbox("Confidence Level", options=[0.90, 0.95, 0.99], index=1)
# n-day horizon slider, limit to 20
n_days = st.slider("Horizon (days)", min_value=1, max_value=20, value=10, help="Number of days for VaR calculation (n-day VaR). Typically 10.")
col3, col4 = st.columns(2)
start_date = col3.date_input("Start Date", pd.to_datetime("2020-01-01"))
end_date = col4.date_input("End Date", pd.to_datetime("2025-10-01"))
st.divider()

# --- Helper functions ---

def parse_list(text):
    """Convert a comma-separated string into a list of stripped items."""
    return [item.strip() for item in text.split(",") if item.strip()]


def fetch_price(ticker):
    """Download a price series for a single ticker.

    Returns a pandas Series or None if no data.  YFinance sometimes returns a
    DataFrame when a comma-separated string is accidentally passed; this helper
    collapses that to a Series as long as there is only one column.  It never
    returns a bare scalar.
    """
    df = yf.download(ticker, start=start_date, end=end_date)
    if df.empty:
        return None

    # pick the adjusted close if available
    if "Adj Close" in df.columns:
        ser = df["Adj Close"]
    elif "Close" in df.columns:
        ser = df["Close"]
    else:
        # unexpected format
        return None

    # if yfinance returned a DataFrame (e.g. ticker string contained commas)
    if isinstance(ser, pd.DataFrame):
        if ser.shape[1] == 1:
            ser = ser.iloc[:, 0]
        else:
            # give up, caller will report missing data
            return None

    # ensure the return type is always a Series (not a scalar or numpy array)
    if not isinstance(ser, pd.Series):
        ser = pd.Series(ser)
    return ser


def build_price_dataframe(price_dict):
    """Convert a dict of ticker->series (or scalars) into a clean DataFrame.

    - Scalars are wrapped in a one‑element Series.
    - DataFrames with a single column are collapsed.
    - Raises ValueError if a value cannot be converted.
    The result is concatenated along columns so that dates align automatically.
    """
    cleaned = {}
    for t, ser in price_dict.items():
        if ser is None:
            continue
        if isinstance(ser, (int, float, np.number)):
            cleaned[t] = pd.Series([ser])
        elif isinstance(ser, pd.DataFrame):
            if ser.shape[1] == 1:
                cleaned[t] = ser.iloc[:, 0]
            else:
                raise ValueError(f"Cannot convert DataFrame with multiple columns for {t}")
        elif isinstance(ser, pd.Series):
            cleaned[t] = ser
        else:
            cleaned[t] = pd.Series(ser)
    if not cleaned:
        return pd.DataFrame()
    # use concat so that differing indexes are aligned automatically
    return pd.concat(cleaned, axis=1)


# helper for tests and reuse

def n_day_returns(series: pd.Series, n: int) -> pd.Series:
    """Return the same series; scaling is done in var calculation.

    We no longer build multi‑day returns; the n‑day VaR is estimated by
    scaling 1‑day VaR with sqrt(n)."""
    return series


def portfolio_var(returns_df: pd.DataFrame, weights: np.ndarray, confidence: float, n: int) -> float:
    """Compute portfolio VaR using sqrt(n) scaling.

    Raises ValueError if there is no data to compute 1-day VaR.
    """
    port = returns_df.dot(weights)
    if port.empty:
        raise ValueError("No return data available")
    var1 = np.percentile(port.dropna(), (1 - confidence) * 100)
    return var1 * np.sqrt(n) if n > 1 else var1

# --- Main Calculation ---
if st.button("Calculate VaR"):
    try:
        tickers = [t.upper() for t in parse_list(tickers_input)]
        values = parse_list(values_input)
        try:
            values = [float(v.replace("$", "")) for v in values]
        except ValueError:
            st.error("Could not parse values. Ensure they are numbers separated by commas.")
            values = []

        if len(tickers) != len(values):
            st.error("The number of tickers and values must match.")
        elif not tickers:
            st.error("Please enter at least one ticker.")
        elif not values:
            # parsing error already reported
            pass
        else:
            total_value = sum(values)
            weights = np.array(values) / total_value

            # collect price series for each ticker
            price_dict = {}
            for t in tickers:
                series = fetch_price(t)
                if series is None or series.empty:
                    st.error(f"No data found for {t}. Check spelling or date range.")
                    price_dict = {}
                    break
                price_dict[t] = series

            if price_dict:
                try:
                    prices_df = build_price_dataframe(price_dict)
                except Exception as ve:
                    st.error(f"Error processing price data: {ve}")
                    prices_df = pd.DataFrame()

                if prices_df.empty:
                    st.error("Unable to construct a valid price table from the downloaded data.")
                else:
                    # align on dates (inner join)
                    prices_df = prices_df.dropna(how="all")
                    returns_df = prices_df.pct_change().dropna()

                    if returns_df.empty:
                        st.error("Not enough price history to compute returns. Try a longer date range.")
                    else:
                        # compute portfolio returns
                        portfolio_returns = returns_df.dot(weights)

                        # 1-day VaR and scaling to n-day via sqrt(n)
                        var1 = np.percentile(portfolio_returns, (1 - confidence_level) * 100)
                        if n_days > 1:
                            var = var1 * np.sqrt(n_days)
                            horizon_returns = portfolio_returns  # keep original for distribution plot
                        else:
                            var = var1
                            horizon_returns = portfolio_returns

                    # display results
                    st.write(f"Portfolio VaR at {confidence_level*100:.0f}% confidence level ({n_days}-day): {var:.4%}")
                    st.write(f"Total portfolio value: ${total_value:,.2f}")
                    abs_loss = -var * total_value
                    st.write(f"Estimated {n_days}-day loss at VaR: {abs_loss:,.2f}")

                    # plot distribution and mark VaR (using daily returns)
                    fig, ax = plt.subplots(figsize=(7,5))
                    ax.hist(horizon_returns, bins=50, color="skyblue", edgecolor="k")
                    ax.axvline(var, color="red", linestyle="--", label=f"VaR ({var:.2%})")
                    ax.set_title("Distribution of 1-day returns")
                    ax.set_xlabel("Return")
                    ax.set_ylabel("Frequency")
                    ax.legend()
                    st.pyplot(fig)

                    # optional display individual assets (scaled with sqrt rule)
                    if len(tickers) > 1:
                        asset_vars = {}
                        for t in tickers:
                            v1 = np.percentile(returns_df[t], (1 - confidence_level) * 100)
                            if n_days > 1:
                                asset_vars[t] = v1 * np.sqrt(n_days)
                            else:
                                asset_vars[t] = v1
                        st.write("Individual asset VaRs:")
                        for t, v in asset_vars.items():
                            st.write(f" - {t}: {v:.4%}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
