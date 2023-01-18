#import necessary libraries
import pandas as pd
import numpy as np

#create the dataframe
data = {'Stock Price': [20, 15, 10, 5],
        'PE Ratio': [15, 12, 10, 8],
        'Dividend Yield': [4, 3, 2, 1]}

df = pd.DataFrame(data)

#calculate the intrinsic value
intrinsic_values = df['Stock Price']/df['PE Ratio'] + df['Dividend Yield']

#calculate the margin of safety
margin_of_safety = intrinsic_values - df['Stock Price']

#print the results
print("Intrinsic Values: ", intrinsic_values)
print("Margin of Safety: ", margin_of_safety)

#determine the best investment
max_margin = margin_of_safety.max()
best_investment = df.loc[margin_of_safety == max_margin]

print("The best investment is: \n", best_investment)
