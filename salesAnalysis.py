import os
import pandas as pd
import matplotlib.pyplot as plt
from itertools import combinations
from collections import Counter

#Create dataframe for 2019 sales data
annual_df = pd.DataFrame()

#Add each month's sales data to dataframe
path = "filepath"
files = [file for file in os.listdir(path) if not file.startswith('.')] # Ignore hidden files

for file in files:
   current_data = pd.read_csv(path+"/"+file)
   annual_df = pd.concat([annual_df, current_data])

#Create new csv for entire year
annual_df.to_csv("annual_data_2019.csv", index=False)

#Read in entire year csv as dataframe
df = pd.read_csv("annual_data_2019.csv")

#Drop null values
df = df[df['Order Date'].str[0:2] != 'Or']
df.dropna(how='any', inplace=True)

#Assign correct data types to columns
df['Quantity Ordered'] = pd.to_numeric(df['Quantity Ordered'])
df['Price Each'] = pd.to_numeric(df['Price Each'])

#Add month column
df['Month'] = df['Order Date'].str[0:2]
df['Month'] = df['Month'].astype('int32')

#Add city column
def getCity(address):
    return address.split(",")[1].strip(" ")

def getState(address):
    return address.split(",")[2].split(" ")[1]

df['City'] = df['Purchase Address'].apply(lambda x: getCity(x) + ' ' + getState(x))

#Best sales month
def bestMonth():
    df['Sales'] = df['Quantity Ordered'].astype('int') * df['Price Each'].astype('float')
    df.groupby(['Month']).sum()

    #Graph results
    months = range(1,13)

    plt.bar(months,df.groupby(['Month']).sum()['Sales'])
    plt.xticks(months)
    plt.ylabel('Sales in USD ($)')
    plt.xlabel('Month number')
    plt.show()

def bestCity():
    df.groupby(['City']).sum()

    #Graph results
    keys = [city for city, data in df.groupby(['City'])]

    plt.bar(keys,df.groupby(['City']).sum()['Sales'])
    plt.ylabel('Sales in USD ($)')
    plt.xlabel('Month number')
    plt.xticks(keys, rotation='vertical', size=8)
    plt.show()

def bestAdTime():
    df['Hour'] = pd.to_datetime(df['Order Date']).dt.hour
    df['Minute'] = pd.to_datetime(df['Order Date']).dt.minute
    df['Count'] = 1

    #Graph results
    keys = [pair for pair, data in df.groupby(['Hour'])]

    plt.plot(keys, df.groupby(['Hour']).count()['Count'])
    plt.xticks(keys)
    plt.grid()
    plt.show()

def productCombinations():
    order_df = df[df['Order ID'].duplicated(keep=False)]

    order_df['Grouped'] = order_df.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))
    df2 = order_df[['Order ID', 'Grouped']].drop_duplicates()

    count = Counter()

    for row in df2['Grouped']:
        row_list = row.split(',')
        count.update(Counter(combinations(row_list, 2)))

    for key,value in count.most_common(10):
        print(key, value)

def bestSellers():
    #Most units sold
    product_group = df.groupby('Product')
    quantity_ordered = product_group.sum()['Quantity Ordered']

    #Graph results
    keys = [pair for pair, data in product_group]
    plt.bar(keys, quantity_ordered)
    plt.xticks(keys, rotation='vertical', size=8)
    plt.show()

    #Set up price to units sold correlation
    prices = df.groupby('Product').mean()['Price Each']

    #Graph results
    fig, ax1 = plt.subplots()

    ax2 = ax1.twinx()
    ax1.bar(keys, quantity_ordered, color='g')
    ax2.plot(keys, prices, color='b')

    ax1.set_xlabel('Product Name')
    ax1.set_ylabel('Quantity Ordered', color='g')
    ax2.set_ylabel('Price ($)', color='b')
    ax1.set_xticklabels(keys, rotation='vertical', size=8)

    fig.show()

print("Choose month, city, ad time, product combinations, or best sellers.")
selection = input("What would you like to know? ")
if selection == "month":
    bestMonth()
    selection = input("Is there anything else you would like to know? ")
elif selection == "city":
    bestCity()
    selection = input("Is there anything else you would like to know? ")
elif selection == "ad time":
    bestCity()
    selection = input("Is there anything else you would like to know? ")
elif selection == "product combinations":
    bestCity()
    selection = input("Is there anything else you would like to know? ")
elif selection == "best sellers":
    bestCity()
    selection = input("Is there anything else you would like to know? ")
else:
    selection = input("Please enter a valid input: ")
