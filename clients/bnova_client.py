import logging

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


logger = logging.getLogger('record.bookings')


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
        logger.info('Bnova client successfully authorized.')


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

    def get_bookings_data(self, arrival_from, arrival_to):

        self.authorize()

        logger.info(f'Start getting data from Bnova for bookings from {arrival_from} to {arrival_to}')

        params = self.build_dashboard_url_params(arrival_from, arrival_to)
        response = self.session.get(BNOVA_DASHBOARD_URL, params=params, headers={'accept': 'application/json'}).json()
        bookings = response['bookings']

        if response['pages']['next_page']:
            pages_count = response['pages']['total_pages']
            for i in range(2, pages_count+1):
                params = self.build_dashboard_url_params(arrival_from, arrival_to, page=i)
                response = self.session.get(BNOVA_DASHBOARD_URL, params=params, headers={'accept': 'application/json'}).json()
                bookings += response['bookings']

        logger.info(f'Total amount of bookings for specified period: {len(bookings)}\n')

        return bookings
