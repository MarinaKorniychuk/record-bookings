from constants import CONFIG_WORKSHEET, RADIK_SPREADSHEET_ID


def get_config_spreadsheet(gc):
    spreadsheet = gc.open_by_key(RADIK_SPREADSHEET_ID)
    worksheet = spreadsheet.worksheet('title', CONFIG_WORKSHEET)
    column_names = ['category', 'spreadsheet', 'line1', 'line2']
    config = worksheet.get_as_df(has_header=False, start='C4')
    config = config.set_axis(column_names, axis=1, copy=False)

    # drop empty lines
    config = config[config.category != '']

    return config
