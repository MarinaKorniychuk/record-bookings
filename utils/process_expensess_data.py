import pandas

from constants import EXPENSES_SPREADSHEET_ID

def get_expenses_data(spreadsheet_data, gc):
    spreadsheet = gc.open(spreadsheet_data['title'])

    # start_cell = 'A2' or make it configurable

    worksheet = spreadsheet.worksheet('title', spreadsheet_data['sheet'])
    dataframe = worksheet.get_as_df(has_header=False, start='A2', empty_value=None)
    column_names = ['datetime',	'spreadsheet', 'name', 'cat1', 'com1', 'am1', 'ch1', 'cat2', 'com2', 'am2', 'ch2', 'cat3', 'com3', 'am3', 'ch3', 'recorded']
    df = dataframe.set_axis(column_names, axis=1, copy=False)
    df['category'] = df['cat1'] + df['cat2'] + df['cat3']
    df['comment'] = df['com1'] + df['com2'] + df['com3']
    df['line'] = df.index + 2

    df.drop(columns=['cat1', 'com1', 'am1', 'ch1', 'cat2', 'com2', 'am2', 'ch2', 'cat3', 'com3', 'am3', 'ch3'])
    print(df.head())

    return dataframe


def get_category_from_record(record):
    # concatenate some columns to get unique expense category
    pass


def process_expenses_data(expense_df, spreadsheets_config, expenses_config):
    """"""
    expense_df['recorded'] = expense_df['recorded'].fillna(0)
    expense_df = expense_df[expense_df.recorded.isin([0.0])]

    # expense_df['category'] = expense_df.apply(lambda row: get_category_from_record(row), axis=1)

    cols = ['category']
    expense_df = expense_df.join(expenses_config.set_index(cols), on=cols)

    data = dict()

    for _, record in spreadsheets_config.iterrows():
        spreadsheet_id = record['spreadsheet_id']
        data[record['spreadsheet_title']] = expense_df.query("spreadsheet == @spreadsheet_id")

    return data


