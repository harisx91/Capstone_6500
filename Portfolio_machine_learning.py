import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
import matplotlib.pyplot as plt

# Define the set of tickers we want to consider
TICKERS = ['AAPL', 'GOOGL', 'TSLA', 'MSFT', 'AMZN']

def plot_predicted_returns(predicted_returns):
    plt.figure(figsize=(10, 6))
    plt.bar(predicted_returns.index, predicted_returns.values)
    plt.xlabel('Stock')
    plt.ylabel('Predicted Return')
    plt.title('Predicted Returns for Each Stock')
    plt.show()

def main():

    st.title('Stock Portfolio Optimization App')
    
    # Allow the user to select tickers
    selected_tickers = st.multiselect('Select your stocks:', TICKERS, default=TICKERS)

    # Fetch the historical price data
    data = yf.download(selected_tickers, period='30y')['Adj Close']
    
    # Use a linear regression model to predict future returns
    model = LinearRegression()
    returns = data.pct_change().dropna()
    X = returns.index.factorize()[0].reshape(-1, 1)  # Use dates as features
    predicted_returns = {}
    for ticker in selected_tickers:
        y = returns[ticker].values
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model.fit(X_train, y_train)
        predicted_returns[ticker] = model.predict(X_test)[-1]  # Predict the last return
    
    predicted_returns = pd.Series(predicted_returns)

    # Plot the predicted returns
    plot_predicted_returns(predicted_returns)

    # Calculate the covariance matrix of returns
    S = risk_models.sample_cov(data)
    
    # Convert predictions into expected returns
    mu = expected_returns.mean_historical_return(data)
    for ticker in selected_tickers:
        mu[ticker] = predicted_returns[ticker]

    # Set an arbitrary risk-free rate
    risk_free_rate = 0.01  # Adjust this value as needed
    
    # Ensure that at least one asset has an expected return exceeding the risk-free rate
    mu[selected_tickers[0]] = risk_free_rate + 0.001

    # Optimize for the maximal Sharpe ratio
    ef = EfficientFrontier(mu, S)
    weights = ef.max_sharpe(risk_free_rate=risk_free_rate)
    cleaned_weights = ef.clean_weights()
    
    st.subheader('Optimized Weights')
    st.write(cleaned_weights)
    
    ef.portfolio_performance(verbose=True)
    
if __name__ == '__main__':
    main()
