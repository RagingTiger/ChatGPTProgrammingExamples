#import necessary libraries
import pandas as pd
import numpy as np

#read in data and store in pandas dataframe
df = pd.read_csv("stock_data.csv")

#initialize variables
cash = 10000 #initial amount of cash
stocks = [] #list to store stocks purchased

#loop through dataframe, find stocks with low PE ratios
for index, row in df.iterrows():
    if row['PE'] < 20:
        #find amount of stock we can buy with available cash
        num_shares = int(cash/row['Price'])
        #subtract cost of stock from cash
        cash -= num_shares*row['Price']
        #add stock to list
        stocks.append((row['Stock'], num_shares))

#print out stocks purchased and remaining cash
print("Stocks purchased:")
for stock in stocks:
    print("{} shares of {}".format(stock[1], stock[0]))

print("Remaining cash: ${:.2f}".format(cash))

# Calculate the total value of the portfolio
total_value = cash

for stock in stocks:
    total_value += stock[1] * df[df['Stock'] == stock[0]]['Price'].iloc[0]

print("Total portfolio value: ${:.2f}".format(total_value))

# Calculate the return on investment
initial_investment = 10000
roi = (total_value - initial_investment) / initial_investment

print("Return on investment: {:.2f}%".format(roi*100))
