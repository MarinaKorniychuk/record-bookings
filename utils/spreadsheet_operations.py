import logging

import pygsheets

from pygsheets.datarange import DataRange
from pygsheets.cell import Cell

from constants import TEMPLATE_WORKSHEETS
from data.days import DAYS_TO_COLUMNS_MAPPING
from data.months import MONTHS_TO_NAME_MAPPING


logger = logging.getLogger('record.bookings')

def get_worksheet_name_by_month(date):
    """Return name of worksheet combining month mapped to russian equivalent with a year

    example: for `date` 2022.12.28
             return: 'Декабрь 2022'
    """
    worksheet = f'{MONTHS_TO_NAME_MAPPING[date.month]} {date.year}'
    return worksheet


def get_cell_address_by_date(date, record):
    """Return tuple of two cell addresses for a provided date
    by mapping `date.day` to according column and adding line numbers from the record to it

    First cell is from total price line, second is a daily price line

    example: for `date` 2022.12.28 and `record.category` 'СтудСад'
             return: (AD55, AD56)
    """
    cell_1 = DAYS_TO_COLUMNS_MAPPING[date.day] + str(record['line1'])
    cell_2 = DAYS_TO_COLUMNS_MAPPING[date.day] + str(record['line2'])
    return cell_1, cell_2


def open_or_create_worksheet(worksheet_name, spreadsheet, worksheets):
    """Open specified worksheet in spreadsheet by its title
    and save it in worksheets dict for a later use

    If worksheet doesn't exist in spreadsheet, create new one using an empty template from TEMPLATE_WORKSHEETS"""
    # do nothing and return if specified worksheet is already opened and saved in worksheets dict
    if worksheets.get(worksheet_name):
        return

    try:
        worksheet = spreadsheet.worksheet('title', worksheet_name)
    except pygsheets.WorksheetNotFound:
        # open template and copy it to create a new worksheet
        template = spreadsheet.worksheet('title', TEMPLATE_WORKSHEETS[spreadsheet.id])
        worksheet = spreadsheet.add_worksheet(worksheet_name, src_worksheet=template)

        logger.info(f'NEW WORKSHEET {worksheet_name} IS CREATED IN {spreadsheet.title}.\n')

    worksheets[worksheet_name] = worksheet


def update_range_with_values(start, end, worksheet, values, update_borders):
    """Call Google API to update range of cells [start - end] with specified values and borders"""
    cell_range = DataRange(start=start, end=end, worksheet=worksheet)
    cell_range.update_values(values)
    cell_range.update_borders(
        top=update_borders[0], right=update_borders[1], bottom=update_borders[2], left=update_borders[3], style='SOLID_THICK'
    )


def update_cell_with_value(address, value, worksheet):
    """Call Google API to update specified cell value"""
    final_amount_cell = Cell(address, worksheet=worksheet)
    final_amount_cell.set_value(value)
