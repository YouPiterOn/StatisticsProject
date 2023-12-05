import pandas as pd
import matplotlib.pyplot as plt
#import seaborn as sns


def tables_for_product(product: str):
    df = pd.read_csv("statistic_project.csv", sep=';')
    df = df[df['product_category'] == product]
    timeFrame = pd.DataFrame(columns=['time', 'qty'])
    timeFrame['time'] = pd.to_timedelta(df['transaction_time']).dt.components['hours'].astype(int)
    timeFrame['qty'] = df['transaction_qty']
    timeFrame = timeFrame.groupby('time')['qty'].sum().reset_index()
    plt.subplot(2, 1, 1)
    plt.bar(timeFrame['time'], timeFrame['qty'])
    plt.title(product)

    dayFrame = pd.DataFrame(columns=['day', 'qty'])
    dayFrame['day'] = pd.to_datetime(df['transaction_date'], format='%d.%m.%Y').dt.day.astype(int)
    dayFrame['qty'] = df['transaction_qty']
    dayFrame = dayFrame.groupby('day')['qty'].sum().reset_index()
    plt.subplot(2, 1, 2)
    plt.bar(dayFrame['day'], dayFrame['qty'])
    plt.show()


tables_for_product('Bakery')
tables_for_product('Drinking Chocolate')
tables_for_product('Tea')
tables_for_product('Coffee')


def qty_for_each_day():
    df = pd.read_csv("statistic_project.csv", sep=';')
    localFrame1 = pd.DataFrame(columns=['day', 'qty'])
    localFrame2 = pd.DataFrame(columns=['day', 'qty', 'type'])

    localFrame1['day'] = pd.to_datetime(df['transaction_date'], format='%d.%m.%Y').dt.day.astype(int)
    localFrame1['qty'] = df['transaction_qty']

    localFrame2['day'] = localFrame1['day']
    localFrame2['qty'] = df['transaction_qty']

    result = localFrame1.groupby('day')['qty'].sum().reset_index()
    print(result)

    localFrame2['type'] = df['product_category']
    result = localFrame2.groupby(['day', 'type'])['qty'].sum().reset_index()
    print(result)
