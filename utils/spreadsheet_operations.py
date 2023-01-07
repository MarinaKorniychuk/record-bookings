import datetime
import calendar
import math

from datetime import timedelta
from dateutil import rrule

import pygsheets

from pygsheets.datarange import DataRange
from pygsheets.cell import Cell

from constants import TEMPLATE_WORKSHEETS
from data.apartments import APARTMENTS_LINES_MAPPING
from data.days import DAYS_TO_COLUMNS_MAPPING
from data.months import MONTHS_TO_NAME_MAPPING
from utils.date_helper import get_date


def get_worksheet_name_by_month(date):
    worksheet = f'{MONTHS_TO_NAME_MAPPING[date.month]} {date.year}'
    # print(f'worksheet by month: {date} -- {worksheet}')
    return worksheet


def get_cells_range_to_update(start_d, end_d, record):
    range_line_number = APARTMENTS_LINES_MAPPING[record['category']][1]
    start_cell = DAYS_TO_COLUMNS_MAPPING[start_d.day] + range_line_number
    end_cell = DAYS_TO_COLUMNS_MAPPING[end_d.day] + range_line_number
    # print(start_cell, end_cell)
    return start_cell, end_cell


def get_cell_address_by_date(date, record):
    # return tuple of total price and daily price cells addresses.
    line_1_number = APARTMENTS_LINES_MAPPING[record['category']][0]
    line_2_number = APARTMENTS_LINES_MAPPING[record['category']][1]
    cell_1 = DAYS_TO_COLUMNS_MAPPING[date.day] + line_1_number
    cell_2 = DAYS_TO_COLUMNS_MAPPING[date.day] + line_2_number
    return cell_1, cell_2


def open_or_create_worksheet(worksheet_name, spreadsheet, worksheets):
    # do nothing and return if specified worksheet is already opened and saved in worksheets dict
    if worksheets.get(worksheet_name):
        return

    try:
        worksheet = spreadsheet.worksheet('title', worksheet_name)
    except pygsheets.WorksheetNotFound:
        # if worksheet for specified month does not exist
        # open template and copy it to create a new worksheet
        template = spreadsheet.worksheet('title', TEMPLATE_WORKSHEETS[spreadsheet.id])
        worksheet = spreadsheet.add_worksheet(worksheet_name, src_worksheet=template)
        print(f'NEW WORKSHEET {worksheet_name} CREATED.')

    worksheets[worksheet_name] = worksheet


def update_range_with_values(start, end, worksheet, values, update_borders):
    cell_range = DataRange(start=start, end=end, worksheet=worksheet)
    cell_range.update_values(values)
    cell_range.update_borders(
        top=update_borders[0], right=update_borders[1], bottom=update_borders[2], left=update_borders[3], style='SOLID_THICK'
    )


def update_cell_with_value(address, value, worksheet):
    final_amount_cell = Cell(address, worksheet=worksheet)
    final_amount_cell.set_value(math.floor(value))


def record_booking_records(spreadsheet, records):
    worksheets = {}  # dict to store opened worksheets for different months (worksheet's name is a key)

    for _, record in records.iterrows():
        start_date = get_date(record['arrival_date'])
        end_date = get_date(record['leaving_date']) - timedelta(days=1)  # date of last staying day

        for month_date in rrule.rrule(
                rrule.MONTHLY,
                dtstart=datetime.date(start_date.year, start_date.month, 1),
                until=end_date
        ):
            worksheet_month = month_date.month
            worksheet_year = month_date.year
            worksheet_name = get_worksheet_name_by_month(month_date)

            if not worksheets.get(worksheet_name):
                open_or_create_worksheet(worksheet_name, spreadsheet, worksheets)

            # default border values for a range of cells (sets right and left border)
            # these values are changed later if booking period starts and ends in different months.
            border_values = [1, 1, 1, 1]

            if start_date.month == worksheet_month:
                start_range_date = start_date
            else:
                start_range_date = datetime.date(worksheet_year, worksheet_month, 1)
                border_values[3] = 0

            _, start_cell = get_cell_address_by_date(start_range_date, record)

            if end_date.month == worksheet_month:
                end_range_date = end_date
            else:
                end_range_date = datetime.date(
                    worksheet_year,
                    worksheet_month,
                    calendar.monthrange(worksheet_year, worksheet_month)[1]
                )
                border_values[1] = 0

            _, end_cell = get_cell_address_by_date(end_range_date, record)

            price_values = [[record['daily_amount']] * ((end_range_date - start_range_date).days + 1)]
            update_range_with_values(start_cell, end_cell, worksheets[worksheet_name], price_values, border_values)

        final_amount_cell_address, _ = get_cell_address_by_date(start_date, record)
        update_cell_with_value(
            final_amount_cell_address, record['final_amount'],
            worksheets[get_worksheet_name_by_month(start_date)]
        )

        print(f'booking from {record["source"]} for {record["category"]} ({start_date} - {get_date(record["leaving_date"])}) is recorded.')
        print(f'final profit: {record["final_amount"]} -- {record["days"]} day(s) {record["daily_amount"]} each.')
        print()

    print('DOOOOOOOOOOONE')

