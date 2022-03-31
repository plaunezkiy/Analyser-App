import pandas as pd


def read_data(file_name):
    data = pd.read_excel(file_name)
    df = pd.DataFrame(data)
    # df.columns = [
    #     'Товар',
    #     'средний запас',
    #     '1 квартал',
    #     '2 квартал',
    #     '3 квартал',
    #     '4 квартал',
    #     'квартальное среднее'
    # ]
    df.columns = [
        'Product',
        'Avg stockpile',
        '1 Q',
        '2 Q',
        '3 Q',
        '4 Q',
        'Quarterly Avg'
    ]
    return df


def add_proportions(df):
    total_average_stock = df['Avg stockpile'].sum()

    df['Share'] = df.apply(
        lambda row: round(row['Avg stockpile']/total_average_stock, 4),
        axis=1
    )
    return df


def get_abc(df):
    df = df.sort_values(by=['Share'], ascending=False)
    total = 0

    def get_rank(item):
        nonlocal total
        total += item['Share']
        if total < 0.75:
            return 'A'
        elif total < 0.95:
            return 'B'
        return 'C'

    df['abc'] = df.apply(lambda row: get_rank(row), axis=1)
    return df


def get_xyz(df):
    def get_v(row):
        sd = row[2:6].std(ddof=0)
        mean = row[2:6].mean()
        v = 100 * sd/mean
        return round(v, 1)

    def get_rank(row):
        if row['v'] < 10:
            return 'X'
        elif row['v'] < 25:
            return 'Y'
        return 'Z'

    df['v'] = df.apply(lambda row: get_v(row), axis=1)
    df = df.sort_values(by=['v'])
    df['xyz'] = df.apply(lambda row: get_rank(row), axis=1)
    return df


def get_abc_xyz_matrix(df):
    data = add_proportions(df)

    matrix = get_xyz(get_abc(data))
    matrix = matrix.drop(columns=[
        'Avg stockpile',
        '1 Q',
        '2 Q',
        '3 Q',
        '4 Q',
        'Quarterly Avg',
        'Share',
        'v',
    ])

    # matrix = matrix.pivot_table(index='xyz', columns='abc',
    #                             values='index', aggfunc=list)
    return matrix


def get_bcg_matrix(df):
    def get_growth(row):
        growth = (row['3-4 Qs'] - row['1-2 Qs']) \
                 / row['1-2 Qs']
        if growth > 10:
            return 'HIGH'
        return 'LOW'

    def get_share(row):
        nonlocal leader, matrix
        b = row['3-4 Qs']
        share = b/leader
        if row['Product'] == matrix.iloc[0]['Product']:
            leader = b
        if share > 1:
            return 'HIGH'
        return 'LOW'

    matrix = pd.DataFrame()
    matrix['Product'] = df['Product']

    matrix['1-2 Qs'] = df['1 Q'] + df['2 Q']
    matrix['3-4 Qs'] = df['3 Q'] + df['4 Q']

    matrix['Growth'] = matrix.apply(lambda row: get_growth(row), axis=1)

    # Дополнительная возможность отсортировать по реализации за 3-4 кварталы, чтобы найти лидера
    # matrix = matrix.sort_values(by=['3-4 quarters'], ascending=False)
    leader = matrix.iloc[1]['3-4 Qs']
    matrix['Share'] = matrix.apply(lambda row: get_share(row), axis=1)

    matrix = matrix.drop(columns=['1-2 Qs', '3-4 Qs'])

    # matrix = matrix.pivot_table(index='market growth', columns='market share',
    #                             values='index', aggfunc=list)
    return matrix


def reorder_data(abc_xyz, bcg):
    df = abc_xyz.set_index('Product').join(bcg.set_index('Product'))

    matrix = df[(df['abc'] == 'C') & (df['xyz'] == 'Z')]
    
    matrix = pd.concat([matrix, df[(df['abc'] == 'C') & (df['xyz'] == 'Y')].sort_values(by=['Growth'])])
    
    matrix = pd.concat([matrix, df[(df['abc'] == 'A') & (df['xyz'] == 'Z')].sort_values(by=['Growth'])])
    
    matrix = pd.concat([matrix, df[(df['abc'] == 'A') & (df['xyz'] == 'Y')]])
    
    matrix = pd.concat([matrix, df[(df['abc'] == 'B') & (df['xyz'] == 'Y')]])
    
    # stars matrix = pd.concat([matrix, df[(df['abc'] == 'C') & (df['xyz'] == 'Y')]])

    matrix = pd.concat([matrix, df[(df['abc'] == 'C') & (df['xyz'] == 'X')]])
    matrix = pd.concat([matrix, df[(df['abc'] == 'B') & (df['xyz'] == 'X')]])
    matrix = pd.concat([matrix, df[(df['abc'] == 'A') & (df['xyz'] == 'X')]])
    
    # dno
    df = df.reset_index()
    matrix = matrix.reset_index()

    items = matrix['Product'].to_list()
    matrix = matrix.append(df.query('Product not in @items'))

    return matrix


if __name__ == '__main__':
    fn = 'test.xlsx'
    clean_data = read_data(fn)
    processed_matrix = get_abc_xyz_matrix(clean_data)
    bcg_mat = get_bcg_matrix(clean_data)
    reordered = reorder_data(processed_matrix, bcg_mat)
    print(reordered)
    # print(bcg_mat)
