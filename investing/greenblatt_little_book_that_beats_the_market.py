#import necessary libraries
import pandas as pd
import numpy as np

#function to calculate the Magic Formula
def magic_formula(df):
    #calculate the enterprise multiple
    df['EV/EBIT'] = df['Enterprise Value']/df['EBIT']

    #calculate the ROC
    df['ROC'] = df['Net Income']/df['Total Assets']

    #calculate the Magic Formula score
    df['Magic Formula'] = df['ROC']/df['EV/EBIT']

    #sort the Magic Formula scores in descending order
    df = df.sort_values(by=['Magic Formula'], ascending = False)

    return df

#function to print the top 10 stocks
def top_ten_stocks(df):
    #select the top 10 stocks
    df = df.head(10)

    #print out the top 10 stocks
    print('The top 10 stocks according to the Magic Formula are:')
    print(df[['Name', 'Magic Formula']])

#main code
if __name__ == '__main__':
    #read in the data
    df = pd.read_csv('stock_data.csv')

    #call the magic_formula function
    df = magic_formula(df)

    #call the top_ten_stocks function
    top_ten_stocks(df)
