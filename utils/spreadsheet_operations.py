import math

from pygsheets.datarange import DataRange
from pygsheets.cell import Cell

from data.apartments import APARTMENTS_LINES_MAPPING
from data.days import DAYS_TO_COLUMNS_MAPPING
from data.months import MONTHS_TO_NAME_MAPPING
from utils.date_helper import get_date


def get_worksheets_to_update(start_d, end_d):
    if (end_d.month - start_d.month) > 1:
        print('Long bookings record, skip')
        raise

    start_worksheet = f'{MONTHS_TO_NAME_MAPPING[start_d.month]} {start_d.year}'
    end_worksheet = f'{MONTHS_TO_NAME_MAPPING[end_d.month]} {end_d.year}'
    return start_worksheet, end_worksheet


def get_cells_range_to_update(start_d, end_d, record):
    range_line_number = APARTMENTS_LINES_MAPPING[record['category']][1]
    start_cell = DAYS_TO_COLUMNS_MAPPING[start_d.day] + range_line_number
    end_cell = DAYS_TO_COLUMNS_MAPPING[end_d.day - 1] + range_line_number
    return start_cell, end_cell


def get_final_amount_cell_address(start_d, record):
    line_number = APARTMENTS_LINES_MAPPING[record['category']][0]
    cell = DAYS_TO_COLUMNS_MAPPING[start_d.day] + line_number
    return cell


def open_or_create_worksheet(worksheet_name, spreadsheet, worksheets):
    # разные таблицы, одинаковые листы!
    if not worksheets.get(worksheet_name):
        worksheets[worksheet_name] = spreadsheet.worksheet('title', worksheet_name)

    # создать новый, если такого нет


def record_booking_records(spreadsheet, records):
    worksheets = {}
    for _, record in records.iterrows():
        start_d = get_date(record['arrival_date'])
        end_d = get_date(record['leaving_date'])
        record['days'] = (end_d - start_d).days
        record['daily_amount'] = math.floor(record['final_amount'] / record['days'])

        if record['daily_amount'] == 0:
            continue

        start_worksheet, end_worksheet = get_worksheets_to_update(start_d, end_d)

        if end_worksheet == start_worksheet:
            open_or_create_worksheet(start_worksheet, spreadsheet, worksheets)
            start_cell, end_cell = get_cells_range_to_update(start_d, end_d, record)

            values = [[record['daily_amount']] * record['days']]
            cell_range = DataRange(start=start_cell, end=end_cell, worksheet=worksheets[start_worksheet])
            cell_range.update_values(values)
            cell_range.update_borders(top=False, right=True, bottom=False, left=True, style='SOLID_THICK')

            final_amount_cell_address = get_final_amount_cell_address(start_d, record)
            final_amount_cell = Cell(final_amount_cell_address, worksheet=worksheets[start_worksheet])
            final_amount_cell.set_value(math.floor(record['final_amount']))
        else:
            pass

