import logging

import pandas as pd
import requests

BNOVA_AUTH_URL = 'https://online.bnovo.ru/'
BNOVA_DASHBOARD_URL = 'https://online.bnovo.ru/dashboard'

BNOVA_USERNAME = '63baa1730b510+19057@customapp.bnovo.ru'
BNOVA_PASSWORD = '54739b599f7a63b4'

BNOVA_CREDENTIALS = {
    'username': BNOVA_USERNAME,
    'password': BNOVA_PASSWORD,
}

STATUS_IDS = '1, 3, 4, 5, 6'  # any except cancelled


# logger = logging.getLogger('record.bookings')


class BnovaClient:
    session = None
    auth_response = None

    def authorize(self):
        self.session = requests.Session()
        self.auth_response = self.session.post(
            BNOVA_AUTH_URL,
            data=BNOVA_CREDENTIALS,
            headers={'accept': 'application/json'}
        )


    def build_dashboard_url_params(self, arrival_from, arrival_to, page=1):
        return {
            'status_ids': STATUS_IDS,
            'arrival_from': arrival_from,
            'arrival_to': arrival_to,
            'p': 2,
            'c': 100,
            'page': page,
            'advanced_search': 2,
            'order_by': 'create_date.desc',
        }

    def get_bookings(self, arrival_from='01.12.2022', arrival_to='02.12.2022'):

        self.authorize()

        params = self.build_dashboard_url_params(arrival_from, arrival_to)
        response = self.session.get(BNOVA_DASHBOARD_URL, params=params, headers={'accept': 'application/json'}).json()
        print('total pages:', response['pages']['total_pages'])
        bookings = response['bookings']

        if response['pages']['next_page']:
            pages_count = response['pages']['total_pages']
            for i in range(2, pages_count+1):
                params = self.build_dashboard_url_params(arrival_from, arrival_to, page=i)
                response = self.session.get(BNOVA_DASHBOARD_URL, params=params, headers={'accept': 'application/json'}).json()
                bookings += response['bookings']

        print('total items: ', len(bookings))

        bookings = pd.DataFrame.from_records(
            bookings,
            columns=['source_id', 'arrival', 'departure', 'prices_rooms_total', 'initial_room_type_name']
        )

        column_names = ['source', 'arrival_date', 'leaving_date', 'total_amount', 'category']
        bookings = bookings.set_axis(column_names, axis=1, copy=False)

        bookings.loc[bookings["source"] == '356', "source"] = 'Ostrovok'
        bookings.loc[bookings["source"] == '14', "source"] = 'Sutochno'
        bookings.loc[bookings["source"] == '0', "source"] = 'Прямой'

        print(bookings.head())

        return bookings
