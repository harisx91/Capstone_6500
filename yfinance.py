import sqlite3
import yfinance as yf

# create a connection to the database
conn = sqlite3.connect('portfolio.db')

# create a cursor object
c = conn.cursor()

# create a table to store stock data
c.execute('''CREATE TABLE IF NOT EXISTS stocks
             (symbol TEXT, name TEXT, shares INTEGER, purchase_price REAL, current_price REAL)''')

# function to add a new stock to the portfolio
def add_stock(symbol, shares, purchase_price):
    stock = yf.Ticker(symbol)
    name = stock.info['shortName']
    current_price = stock.info['regularMarketPrice']
    c.execute('''INSERT INTO stocks (symbol, name, shares, purchase_price, current_price)
                 VALUES (?, ?, ?, ?, ?)''', (symbol, name, shares, purchase_price, current_price))
    conn.commit()
    print('Stock added successfully')

# function to update a stock in the portfolio
def update_stock(symbol, shares, purchase_price):
    stock = yf.Ticker(symbol)
    name = stock.info['shortName']
    current_price = stock.info['regularMarketPrice']
    c.execute('''UPDATE stocks
                 SET name = ?, shares = ?, purchase_price = ?, current_price = ?
                 WHERE symbol = ?''', (name, shares, purchase_price, current_price, symbol))
    conn.commit()
    print('Stock updated successfully')

# function to delete a stock from the portfolio
def delete_stock(symbol):
    c.execute('''DELETE FROM stocks WHERE symbol = ?''', (symbol,))
    conn.commit()
    print('Stock deleted successfully')

# function to get the current value of the portfolio
def get_portfolio_value():
    total_value = 0
    for row in c.execute('SELECT * FROM stocks'):
        total_value += row[2] * row[4]
    return total_value

# sample usage
add_stock('AAPL', 100, 150)
update_stock('AAPL', 150, 170)
delete_stock('AAPL')
print('Portfolio value:', get_portfolio_value())
