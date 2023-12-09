import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats

types = ['Coffee', 'Bakery', 'Tea', 'Drinking Chocolate']


def tables_for_product(product: str):
    df = pd.read_csv("statistic_project.csv", sep=';')
    df = df[df['product_category'] == product]
    df['unit_price'] = df['unit_price'].apply(lambda x: float(x.replace(',', '.')))

    timeFrame = pd.DataFrame(columns=['time', 'revenue'])
    timeFrame['time'] = pd.to_timedelta(df['transaction_time']).dt.components['hours'].astype(int)
    timeFrame['revenue'] = df['transaction_qty']*df['unit_price']
    timeFrame = timeFrame.groupby('time')['revenue'].sum().reset_index()
    timePlt = plt.subplot(2, 1, 1)
    cont = timePlt.bar(timeFrame['time'], timeFrame['revenue'])
    timePlt.bar_label(cont)
    plt.title(product)

    dayFrame = pd.DataFrame(columns=['day', 'revenue'])
    dayFrame['day'] = pd.to_datetime(df['transaction_date'], format='%d.%m.%Y').dt.day.astype(int)
    dayFrame['revenue'] = df['transaction_qty']*df['unit_price']
    dayFrame = dayFrame.groupby('day')['revenue'].sum().reset_index()
    dayPlt = plt.subplot(2, 1, 2)
    cont = dayPlt.bar(dayFrame['day'], dayFrame['revenue'])
    dayPlt.bar_label(cont)
    plt.show()


"""
for type in types:
    tables_for_product(type)
"""


def tables_for_all_products():
    df = pd.read_csv("statistic_project.csv", sep=';')
    df['unit_price'] = df['unit_price'].apply(lambda x: float(x.replace(',', '.')))

    timeFrame = pd.DataFrame(columns=['time', 'revenue'])
    timeFrame['time'] = pd.to_timedelta(df['transaction_time']).dt.components['hours'].astype(int)
    timeFrame['revenue'] = df['transaction_qty']*df['unit_price']
    timeFrame = timeFrame.groupby('time')['revenue'].sum().reset_index()
    timePlt = plt.subplot(2, 1, 1)
    cont = timePlt.bar(timeFrame['time'], timeFrame['revenue'])
    timePlt.bar_label(cont)
    plt.title('All products')

    dayFrame = pd.DataFrame(columns=['day', 'revenue'])
    dayFrame['day'] = pd.to_datetime(df['transaction_date'], format='%d.%m.%Y').dt.day.astype(int)
    dayFrame['revenue'] = df['transaction_qty']*df['unit_price']
    dayFrame = dayFrame.groupby('day')['revenue'].sum().reset_index()
    dayPlt = plt.subplot(2, 1, 2)
    cont = dayPlt.bar(dayFrame['day'], dayFrame['revenue'])
    dayPlt.bar_label(cont)
    plt.show()


# tables_for_all_products()


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


# price_from_place()


def calculate_amount_of_product(mean: float, std: float):
    confidence_level = 0.5

    z_score = stats.norm.ppf((1 + confidence_level) / 2)
    amount_needed = mean + z_score * std

    return amount_needed


def bakery_percents(df):
    percent_frame = pd.DataFrame(columns=['transaction_qty', 'product_type'])
    percent_frame['transaction_qty'] = df['transaction_qty'].astype(int)
    percent_frame['product_type'] = df['product_type']
    result_sum = percent_frame.groupby(['product_type'])['transaction_qty'].sum().reset_index()
    total = result_sum['transaction_qty'].sum()
    print(total)
    result_sum['percent'] = result_sum['transaction_qty'] / total * 100
    print(result_sum, '\n')


def bakery_analysis():
    df = pd.read_csv("year_data.csv", sep=';')
    df = df[df['product_category'] == 'Bakery']

    bakery_percents(df)

    stores = ['Lower Manhattan', 'Hell\'s Kitchen', 'Astoria']
    for store in stores:
        store_f = df[df['store_location'] == store]

        store_frame = pd.DataFrame(columns=['transaction_qty', 'date', 'hours'])
        store_frame['hours'] = pd.to_timedelta(store_f['transaction_time']).dt.components['hours'].astype(int)
        store_frame['transaction_qty'] = store_f['transaction_qty'].astype(int)
        store_frame['date'] = pd.to_datetime(store_f['transaction_date'], format='%d.%m.%Y').dt.day.astype(int)
        result_sum = store_frame.groupby(['date', 'hours'])['transaction_qty'].sum().reset_index()
        # print(result_sum['transaction_qty'].sum())

        result_std = result_sum.groupby('hours')['transaction_qty'].std().reset_index()
        result_mean = result_sum.groupby('hours')['transaction_qty'].mean().reset_index()

        result = pd.DataFrame(columns=['hours', 'mean', 'std', 'to_produce'])

        result['hours'] = result_std['hours']
        result['mean'] = result_mean['transaction_qty']
        result['std'] = result_std['transaction_qty']

        print(store)
        bakery_percents(store_f)
        # print('STD:')
        # print(result_std, '\n')
        # print('Mean:')
        # print(result_mean, '\n')
        # print('\n')

        for index, row in result.iterrows():
            result.loc[index, 'to_produce'] = calculate_amount_of_product(row['mean'], row['std'])
        print(result, '\n')


# bakery_analysis()


def quarters():
    df = pd.read_csv("year_data.csv", sep=';')
    df = df[df['product_category'] == 'Bakery']

    df['date'] = pd.to_datetime(df['transaction_date'], format='%d.%m.%Y')
    split_date = '2023-03-31 00:00:00'
    q1 = df[df['date'] <= split_date].copy()
    q2 = df[df['date'] > split_date].copy()
    bakery_percents(q1)
    bakery_percents(q2)

    stores = ['Lower Manhattan', 'Hell\'s Kitchen', 'Astoria']
    for store in stores:
        store_df = df[df['store_location'] == store].reset_index(drop=True)
        q1_store = store_df[store_df['date'] <= split_date].copy()
        q2_store = store_df[store_df['date'] > split_date].copy()

        print(store)
        bakery_percents(q1_store)
        bakery_percents(q2_store)


quarters()
