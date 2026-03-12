# Derivatives Analytics Toolkit

A collection of **Streamlit utilities** for quantitative finance, focused on derivatives valuation, risk management, and hedging analysis. This workspace includes interactive applications for bond pricing, Value at Risk (VaR) calculation, minimum-variance hedging, and geometric Brownian motion simulations.

## 📁 Project Structure

```
.
├── bond_valuation.py                      # Interactive bond pricing and duration calculator
├── VaR.py                                 # Portfolio Value at Risk (VaR) calculator
├── minimum_variance_hedge_ratio_5.py      # Minimum-variance hedge ratio and optimal contracts
├── gbm_fast.py                            # GPU-accelerated GBM simulation (CuPy)
├── geometricbrownianmotion.py             # CPU-based GBM simulation (NumPy)
├── tests/
│   └── test_var_portfolio.py              # Unit tests for VaR module
└── README.md (this file)
```

## 🎯 Applications

### 1. **Value at Risk (VaR) Calculator** (`VaR.py`)

Interactive Streamlit app for computing **Value at Risk** for portfolios and individual assets using historical market data.

**Features:**
- Single or multi-asset portfolio support (comma-separated tickers)
- Configurable confidence levels (90%, 95%, 99%)
- N-day Value at Risk horizons (1-20 days)
- Automatic data fetching via Yahoo Finance (`yfinance`)
- Historical returns visualization

**Key Inputs:**
- **Tickers:** Asset symbols (e.g., AAPL, MSFT)
- **Values:** Weights for each asset in the portfolio
- **Confidence Level:** VaR confidence threshold
- **Date Range:** Historical period for calculation

**Run:**
```powershell
streamlit run VaR.py
```

---

### 2. **Bond Valuation Tool** (`bond_valuation.py`)

Streamlit app for **bond pricing and duration analysis** using continuous compounding.

**Calculations:**
- Bond price: $B = \sum_{i=1}^n c_i e^{-yt_i}$
- Macaulay duration: $D = \sum_{i=1}^n t_i c_i e^{-yt_i} B^{-1}$

**Features:**
- Flexible coupon frequency (Monthly, Quarterly, Semi-annual, Yearly)
- Continuous compounding yield calculations
- Price sensitivity analysis (ΔB vs. Δy)
- Cashflow visualization and preview
- Modified duration and convexity metrics

**Key Inputs:**
- Face value and coupon percentage
- Bond yield (continuous compounding)
- Maturity term in years
- Coupon payment frequency

**Run:**
```powershell
streamlit run bond_valuation.py
```

---

### 3. **Minimum Variance Hedge Ratio Calculator** (`minimum_variance_hedge_ratio_5.py`)

Streamlit app for computing **optimal hedging ratios** and the **number of futures contracts** required.

**Calculations:**
- Hedge ratio: $\hat{h} = \hat{\rho} \times (\hat{\sigma}_S / \hat{\sigma}_F)$
- Optimal contracts: $N^* = (\hat{h} \times V_A) / V_F$

**Features:**
- Automatic correlation and volatility estimation from historical data
- Scatter plot with fitted hedge line
- Optional calculation of N* (optimal number of futures contracts)
- Daily percentage returns analysis

**Key Inputs:**
- Spot asset ticker (e.g., PSX)
- Futures contract or correlated asset ticker (e.g., CL=F)
- Position value and futures contract specifications (for N* calculation)

**Run:**
```powershell
streamlit run minimum_variance_hedge_ratio_5.py
```

---

## 📊 Utility Modules

### **GBM Simulations**

#### `gbm_fast.py` — GPU-Accelerated (CuPy)
Fast geometric Brownian motion simulation using NVIDIA GPUs for handling large path counts.

```python
gpu_paths = simulate_gbm_gpu(mu=0.1, sigma=0.2, S0=100.0, dt=0.01, n=1000, M=100000)
```

**Requirements:** CUDA-capable GPU and CuPy library.

#### `geometricbrownianmotion.py` — CPU-Based (NumPy)
Standard GBM simulation using NumPy, suitable for exploratory analysis and smaller datasets.

```python
St = np.exp((mu - sigma**2 / 2) * dt + sigma * np.random.normal(...)).cumprod(axis=0)
```

**Both modules generate:**
- Multiple price paths following GBM dynamics
- Time-indexed visualization
- Configurable drift ($\mu$), volatility ($\sigma$), and horizons

---

## 🔧 Installation & Dependencies

### Requirements
```
streamlit
pandas
numpy
matplotlib
yfinance
pytest (for testing)
```

**Optional:** CuPy (for GPU acceleration in `gbm_fast.py`)

### Setup

1. **Clone or navigate to the workspace:**
   ```powershell
   cd "c:\Users\nahue\OneDrive\Desktop\Options, futures, and other derivatives\Coding projects"
   ```

2. **Create a virtual environment (recommended):**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```
   Or install manually:
   ```powershell
   pip install streamlit pandas numpy matplotlib yfinance pytest
   ```

---

## 📊 Running the Applications

Start any Streamlit app from the workspace root:

```powershell
# Value at Risk Calculator
streamlit run VaR.py

# Bond Valuation Tool
streamlit run bond_valuation.py

# Minimum Variance Hedge Ratio
streamlit run minimum_variance_hedge_ratio_5.py
```

Streamlit will open in your default browser at `http://localhost:8501`

---

## ✅ Testing

Run the test suite:

```powershell
pytest tests/ -v
```

### Test Coverage
- **test_var_portfolio.py:** VaR calculation validation, portfolio weighting, input parsing
  - `test_parse_list()` — CSV parsing correctness
  - `test_weights_and_var()` — Portfolio VaR computation
  - `test_build_price_dataframe_scalars()` — Data structure handling

---

## 🎨 Code Patterns & Conventions

### Streamlit UI Design
- Single-file apps with `st.button()` for triggering calculations
- Input validation with `st.error()` for missing or invalid data
- Metrics display via `st.metric()` and charts via `st.pyplot()`
- Math rendering in `st.markdown()` using LaTeX: `$...$` for inline, `$$...$$` for blocks

### Data Fetching
```python
def fetch_price(ticker):
    """Download price series using yfinance."""
    df = yf.download(ticker, start=start_date, end=end_date)
    if df.empty:
        return None
    return df["Adj Close"] if "Adj Close" in df.columns else df["Close"]
```

### Error Handling
```python
try:
    # calculation logic
except Exception as e:
    st.error(f"Error: {str(e)}")
```

### Numeric Inputs
```python
st.number_input("Face Value", value=100.0, placeholder="e.g. 1,000")
```

---

## 📝 Notes

- **Data Source:** All applications use Yahoo Finance (`yfinance`) for historical market data
- **Continuous Compounding:** Bond valuation uses continuous compounding formulas
- **Percentage Returns:** Hedge ratio calculations work with daily percentage changes (%)
- **N-Day VaR:** Value at Risk is scaled to the specified horizon using volatility scaling

---

## 🚀 Next Steps & Future Enhancements

- Add **Greeks calculations** (Delta, Gamma, Vega, Rho) for option pricing
- Implement **Monte Carlo simulations** for exotic derivatives
- Extend **portfolio optimization** with constraints (diversification, sector limits)
- Add **stress testing** and **scenario analysis** frameworks
- Performance improvements for large portfolios (parallel computation)
- Unit tests for bond valuation and hedge ratio modules

---

## 📄 License & Attribution

This workspace is for educational purposes in derivatives and quantitative finance.

For questions or contributions, ensure changes:
1. Maintain Streamlit UX and simple dataflow patterns
2. Include appropriate error handling and input validation
3. Include unit tests for new computational helpers
4. Preserve LaTeX math formatting in documentation

---

**Created:** March 2026  
**Python Version:** 3.8+  
**Last Updated:** March 12, 2026
