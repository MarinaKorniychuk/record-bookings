import pandas

from utils.configuration import get_form_responses_worksheet


def get_expenses_data(gc):
    worksheet= get_form_responses_worksheet(gc)

    column_names = ['datetime',	'spreadsheet', 'name', 'cat1', 'com1', 'am1', 'ch1', 'cat2', 'com2', 'am2', 'ch2', 'cat3', 'com3', 'am3', 'ch3', 'recorded']
    df = worksheet.get_as_df(has_header=False, start='A2', empty_value=None)
    df = df.set_axis(column_names, axis=1, copy=False)

    df[['cat1', 'com1', 'cat2', 'com2', 'cat3', 'com3']] = df[['cat1', 'com1', 'cat2', 'com2', 'cat3', 'com3']].fillna(value='')
    df[['am1', 'am2', 'am3']] = df[['am1', 'am2', 'am3']].fillna(value=0)

    return df


def get_processed_expenses_data(spreadsheets_config, expenses_config, gc):
    expense_df = get_expenses_data(gc)

    expense_df['category'] = expense_df[['cat1', 'cat2', 'cat3']].astype(str).apply(''.join, axis=1)
    expense_df['note'] = expense_df[['com1', 'com2', 'com3']].astype(str).apply(''.join, axis=1)
    expense_df['amount'] = expense_df[['am1', 'am2', 'am3']].astype(float).sum(axis=1)

    expense_df['rec_line'] = expense_df.index + 2
    expense_df = expense_df.drop(columns=['cat1', 'com1', 'am1', 'ch1', 'cat2', 'com2', 'am2', 'ch2', 'cat3', 'com3', 'am3', 'ch3'])

    expense_df['recorded'] = expense_df['recorded'].fillna(0)
    expense_df = expense_df[expense_df.recorded.isin([0.0])]

    data = dict()
    for _, record in spreadsheets_config.iterrows():
        spreadsheet_id = record['spreadsheet_id']
        expenses_sub_df = expense_df.query("spreadsheet == @spreadsheet_id")
        expenses_sub_df.set_index('category')
        categories_set = expenses_config.query("spreadsheet_id == @spreadsheet_id")

        data[record['spreadsheet_title']] = expenses_sub_df.join(categories_set.set_index('category'), on='category')

    return data


