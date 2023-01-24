from constants import EXPENSES_SPREADSHEET_ID, RADIK_SPREADSHEET_ID, DINARA_SPREADSHEET_ID, \
    SEREBRYANICHESKIY_SPREADSHEET_ID

def get_expenses_data(gc):
    spreadsheet = gc.open_by_key(EXPENSES_SPREADSHEET_ID)

    # start_cell = 'A2' or make it configurable

    worksheet = spreadsheet.worksheet('title', 'Sheet1')
    dataframe = worksheet.get_as_df(has_header=False, start='A2', empty_value=None)
    column_names = ['datetime', 'name', 'sheet', 'apartment', 'apartment/rent', 'apartment/internet', 'employee',
                    'comment', 'amount', 'receipt', 'recorded']
    dataframe = dataframe.set_axis(column_names, axis=1, copy=False)

    return dataframe


def get_category_from_record(record):
    # concatenate some columns to get unique expense category
    pass


def process_expenses_data(expense_df, config):
    """"""
    expense_df['recorded'] = expense_df['recorded'].fillna(0)
    expense_df = expense_df[expense_df.recorded.isin([0.0])]

    # expense_df['category'] = expense_df.apply(lambda row: get_category_from_record(row), axis=1)

    cols = ['category']
    expense_df = expense_df.join(config.set_index(cols), on=cols)

    data = {
        SEREBRYANICHESKIY_SPREADSHEET_ID: expense_df.query("spreadsheet == @SEREBRYANICHESKIY"),
        DINARA_SPREADSHEET_ID: expense_df.query("spreadsheet == @DINARA"),
        RADIK_SPREADSHEET_ID: expense_df.query("spreadsheet == @RADIK"),
    }

    return data


