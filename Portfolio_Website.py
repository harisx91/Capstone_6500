import streamlit as st
import yfinance as yf
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns

# Define the set of tickers we want to consider
TICKERS = ['AAPL', 'GOOGL', 'TSLA', 'MSFT', 'AMZN']

def main():

    st.title('Stock Portfolio Optimization App')
    
    # Allow user to select tickers
    selected_tickers = st.multiselect('Select your stocks:', TICKERS, default=TICKERS)

    # Fetch the historical price data
    data = yf.download(selected_tickers, period='10y')['Adj Close']
    
    # Calculate expected returns and the covariance matrix of returns
    mu = expected_returns.mean_historical_return(data)
    S = risk_models.sample_cov(data)
    
    # Optimize for the maximal Sharpe ratio
    ef = EfficientFrontier(mu, S)
    weights = ef.max_sharpe()
    cleaned_weights = ef.clean_weights()
    
    st.subheader('Optimized Weights')
    st.write(cleaned_weights)
    
    ef.portfolio_performance(verbose=True)
    
if __name__ == '__main__':
    main()

