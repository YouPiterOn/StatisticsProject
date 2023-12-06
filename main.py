import pandas as pd
import matplotlib.pyplot as plt
#import seaborn as sns

types = ['Coffee', 'Bakery', 'Tea', 'Drinking Chocolate']


def tables_for_product(product: str):
    df = pd.read_csv("statistic_project.csv", sep=';')
    df = df[df['product_category'] == product]
    timeFrame = pd.DataFrame(columns=['time', 'qty'])
    timeFrame['time'] = pd.to_timedelta(df['transaction_time']).dt.components['hours'].astype(int)
    timeFrame['qty'] = df['transaction_qty']
    timeFrame = timeFrame.groupby('time')['qty'].sum().reset_index()
    timePlt = plt.subplot(2, 1, 1)
    cont = timePlt.bar(timeFrame['time'], timeFrame['qty'])
    timePlt.bar_label(cont)
    plt.title(product)

    dayFrame = pd.DataFrame(columns=['day', 'qty'])
    dayFrame['day'] = pd.to_datetime(df['transaction_date'], format='%d.%m.%Y').dt.day.astype(int)
    dayFrame['qty'] = df['transaction_qty']
    dayFrame = dayFrame.groupby('day')['qty'].sum().reset_index()
    dayPlt = plt.subplot(2, 1, 2)
    cont = dayPlt.bar(dayFrame['day'], dayFrame['qty'])
    dayPlt.bar_label(cont)
    plt.show()


"""
for type in types:
    tables_for_product(type)
"""


def tables_for_all_products():
    df = pd.read_csv("statistic_project.csv", sep=';')
    timeFrame = pd.DataFrame(columns=['time', 'qty'])
    timeFrame['time'] = pd.to_timedelta(df['transaction_time']).dt.components['hours'].astype(int)
    timeFrame['qty'] = df['transaction_qty']
    timeFrame = timeFrame.groupby('time')['qty'].sum().reset_index()
    timePlt = plt.subplot(2, 1, 1)
    cont = timePlt.bar(timeFrame['time'], timeFrame['qty'])
    timePlt.bar_label(cont)
    plt.title('All products')

    dayFrame = pd.DataFrame(columns=['day', 'qty'])
    dayFrame['day'] = pd.to_datetime(df['transaction_date'], format='%d.%m.%Y').dt.day.astype(int)
    dayFrame['qty'] = df['transaction_qty']
    dayFrame = dayFrame.groupby('day')['qty'].sum().reset_index()
    dayPlt = plt.subplot(2, 1, 2)
    cont = dayPlt.bar(dayFrame['day'], dayFrame['qty'])
    dayPlt.bar_label(cont)
    plt.show()


tables_for_all_products()


def price_from_place():
    df = pd.read_csv("statistic_project.csv", sep=';')
    df = df.drop_duplicates(subset=['product_type', 'store_location'])
    locationFrame = pd.DataFrame(columns=['product', 'location', 'price', 'type'])
    locationFrame['product'] = df['product_type']
    locationFrame['location'] = df['store_location']
    locationFrame['price'] = df['unit_price']
    locationFrame['type'] = df['product_category']
    products = locationFrame['product'].drop_duplicates()
    locationFrame['price'] = locationFrame['price'].apply(lambda x: float(x.replace(',', '.')))
    for type in types:
        typeFrame = locationFrame[locationFrame['type'] == type]
        typeFrame = typeFrame.groupby('location')['price'].mean().reset_index()
        plt.plot(typeFrame['location'], typeFrame['price'])
    plt.legend(types)
    plt.show()
    print(locationFrame)


price_from_place()
