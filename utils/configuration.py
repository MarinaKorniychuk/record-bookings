from pygsheets import Cell

from constants import CONFIG_SPREADSHEET, BOOKINGS_CONFIG_WORKSHEET, SPREADSHEET_CONFIG_WORKSHEET, EXPENSES_CONFIG_WORKSHEET


def get_spreadsheets_config(gc):
    spreadsheet = gc.open(CONFIG_SPREADSHEET)

    spreadsheet_config_worksheet = spreadsheet.worksheet('title', SPREADSHEET_CONFIG_WORKSHEET)
    column_names = ['spreadsheet_id', 'spreadsheet_title']
    spreadsheets_config = spreadsheet_config_worksheet.get_as_df(has_header=False, start='C4')
    spreadsheets_config = spreadsheets_config.set_axis(column_names, axis=1, copy=False)

    return spreadsheets_config

def get_bookings_config(gc):
    spreadsheet = gc.open(CONFIG_SPREADSHEET)

    bookings_config_worksheet = spreadsheet.worksheet('title', BOOKINGS_CONFIG_WORKSHEET)
    column_names = ['category', 'spreadsheet', 'line1', 'line2']
    bookings_config = bookings_config_worksheet.get_as_df(has_header=False, start='C4')
    bookings_config = bookings_config.set_axis(column_names, axis=1, copy=False)

    # drop empty lines
    bookings_config = bookings_config[bookings_config.category != '']

    return bookings_config

def get_expenses_config(gc):
    spreadsheet = gc.open(CONFIG_SPREADSHEET)

    expenses_config_worksheet = spreadsheet.worksheet('title', EXPENSES_CONFIG_WORKSHEET)
    column_names = ['category', 'spreadsheet', 'line']
    expenses_config = expenses_config_worksheet.get_as_df(has_header=False, start='C7')
    expenses_config = expenses_config_worksheet.set_axis(column_names, axis=1, copy=False)

    # drop empty lines
    expenses_config = expenses_config[expenses_config.category != '']

    return expenses_config

def get_form_responses_spreadsheet_data(gc):
    spreadsheet = gc.open(CONFIG_SPREADSHEET)

    expenses_config_worksheet = spreadsheet.worksheet('title', EXPENSES_CONFIG_WORKSHEET)
    title_cell = Cell('D3', worksheet=expenses_config_worksheet)
    sheet_cell = Cell('D4', worksheet=expenses_config_worksheet)

    spreadsheet_data = {
        'title': title_cell.value,
        'sheet': sheet_cell.value,
    }

    return spreadsheet_data
