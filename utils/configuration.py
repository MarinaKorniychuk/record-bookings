from constants import CONFIG_SPREADSHEET, BOOKINGS_CONFIG_WORKSHEET, SPREADSHEET_CONFIG_WORKSHEET, EXPENSES_CONFIG_WORKSHEET


def get_spreadsheets_config(gc):
    """Get config from worksheet 'Таблицы' (spreadsheet 'Подсчеты / Конфиг')
    Read dataframe from C4 cell
    """
    spreadsheet = gc.open(CONFIG_SPREADSHEET)

    spreadsheet_config_worksheet = spreadsheet.worksheet('title', SPREADSHEET_CONFIG_WORKSHEET)
    column_names = ['spreadsheet_id', 'spreadsheet_title']
    spreadsheets_config = spreadsheet_config_worksheet.get_as_df(has_header=False, start='C4')
    spreadsheets_config = spreadsheets_config.set_axis(column_names, axis=1, copy=False)

    return spreadsheets_config

def get_bookings_config(gc):
    """Get config from worksheet 'Приходы' (spreadsheet 'Подсчеты / Конфиг')
    Read dataframe from C4 cell, remove empty lines
    """
    spreadsheet = gc.open(CONFIG_SPREADSHEET)

    bookings_config_worksheet = spreadsheet.worksheet('title', BOOKINGS_CONFIG_WORKSHEET)
    column_names = ['category', 'spreadsheet', 'line1', 'line2']
    bookings_config = bookings_config_worksheet.get_as_df(has_header=False, start='C4')
    bookings_config = bookings_config.set_axis(column_names, axis=1, copy=False)

    # drop empty lines
    bookings_config = bookings_config[bookings_config.category != '']

    return bookings_config

def get_expenses_config(gc):
    """Get config from worksheet 'Расходы' (spreadsheet 'Подсчеты / Конфиг')
    Read dataframe from C7 cell, remove empty lines
    """
    spreadsheet = gc.open(CONFIG_SPREADSHEET)

    expenses_config_worksheet = spreadsheet.worksheet('title', EXPENSES_CONFIG_WORKSHEET)
    column_names = ['category', 'spreadsheet_id', 'line']
    expenses_config = expenses_config_worksheet.get_as_df(has_header=False, start='C7')
    expenses_config = expenses_config.set_axis(column_names, axis=1, copy=False)

    # drop empty lines
    expenses_config = expenses_config[expenses_config.category != '']

    return expenses_config

def get_form_responses_spreadsheet_data(gc):
    """Get names of expenses spreadsheet and worksheet from worksheet 'Расходы', cells D3, D4"""
    spreadsheet = gc.open(CONFIG_SPREADSHEET)

    expenses_config_worksheet = spreadsheet.worksheet('title', EXPENSES_CONFIG_WORKSHEET)

    title = expenses_config_worksheet.get_value('D3')
    sheet = expenses_config_worksheet.get_value('D4')

    spreadsheet_data = {
        'title': title,
        'sheet': sheet,
    }

    return spreadsheet_data

def get_form_responses_worksheet(gc):
    """Open and return worksheet with expenses (form responses)"""
    spreadsheet_data= get_form_responses_spreadsheet_data(gc)

    spreadsheet = gc.open(spreadsheet_data['title'])
    worksheet = spreadsheet.worksheet('title', spreadsheet_data['sheet'])

    return worksheet
