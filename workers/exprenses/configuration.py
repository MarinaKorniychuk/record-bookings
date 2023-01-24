from constants import EXPENSES_SPREADSHEET_ID, CONFIG_WORKSHEET


def get_config_spreadsheet(gc):
    spreadsheet = gc.open_by_key(EXPENSES_SPREADSHEET_ID)
    worksheet = spreadsheet.worksheet('title', CONFIG_WORKSHEET)
    column_names = ['datetime', 'name', 'sheet', 'category', 'apartment/rent', 'apartment/internet', 'employee', 'comment', 'amount', 'receipt', 'recorded']
    config = worksheet.get_as_df(has_header=False, start='A2', empty_value=None)
    config = config.set_axis(column_names, axis=1, copy=False)

    config = config[config.category != '']
    return config
