import requests

BNOVA_AUTH_URL = 'https://online.bnovo.ru/'
BNOVA_DASHBOARD_URL = 'https://online.bnovo.ru/dashboard'

BNOVA_USERNAME = '63baa1730b510+19057@customapp.bnovo.ru'
BNOVA_PASSWORD = '54739b599f7a63b4'

BNOVA_CREDENTIALS = {
    'username': BNOVA_USERNAME,
    'password':BNOVA_PASSWORD,
}

STATUS_IDS = [1, 3, 4, 5, 6]  # any except cancelled

ROOM_IDS = [305032,375523,375524,375754,375755,375756,375757,375764,375766,375775,375776,375777,375784,375785,375787,375788,375789,375791,376017,376018,376019,376020,376021,376022,376023,376024,376025,376026,376027,376029,376030,376031,376032,376033,376034,376035,376036,376037,376039,376040,376042,376043,376046,376048,376061,376062,376064,376065,376067,376068,376070,376072,383674]


class BnovaClient:
    session = None
    auth_response = None

    def authorize(self):
        self.session = requests.Session()
        self.auth_response = self.session.post(
            BNOVA_AUTH_URL, BNOVA_CREDENTIALS,
            headers={'content-type': 'application/json'}
        )

    def build_dashboard_url_params(self, arrival_from, arrival_to, page=1):
        return {
            'roomtypes': ROOM_IDS,
            'status_ids': STATUS_IDS,
            'arrival_from': arrival_from | '01.12.2022',
            'arrival_to': arrival_to | '06.01.2023',
            'p': 2,
            'c': 100,
            'page': page,
            'advanced_search': 2,
            'order_by': 'create_date.desc',
        }

    def get_bookings(self, arrival_from, arrival_to):
        bookings = []
        params = self.build_dashboard_url_params(arrival_from, arrival_to)
        response = self.session.get(BNOVA_DASHBOARD_URL, params=params, headers={'accept': 'application/json'})
        bookings.append(response.content.json()['bookings'])
        pages_count = response.content.json()['pages']

        for i in range(2, pages_count+1):
            params = self.build_dashboard_url_params(arrival_from, arrival_to, page=i)
            response = self.session.get(BNOVA_DASHBOARD_URL, params=params, headers={'accept': 'application/json'})
            bookings.append(response.content.json()['bookings'])

        return bookings