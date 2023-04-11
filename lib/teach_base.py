import json
from typing import List
from urllib.parse import urljoin

import requests
from django.conf import settings


class APIClient:
    def __init__(self, client_id: str, client_secret: str, base_url: str):
        self._client_id = client_id
        self._client_secret = client_secret
        self._base_url = base_url

    def _get_access_token(self) -> str:
        url = urljoin(self._base_url, '/oauth/token')
        response = requests.post(
            url=url,
            data={'client_id': self._client_id,
                  'client_secret': self._client_secret,
                  'grant_type': 'client_credentials'}
        )
        response.raise_for_status()
        return json.loads(response.content).get('token')

    def make_get_request(self, endpoint: str, detail_key: str | int = None, params: dict = None) -> dict | list:
        url = urljoin(self._base_url, endpoint)

        if detail_key:
            url += f'{detail_key}/'

        response = requests.get(url=url, params=params,
                                headers={'Content-type': 'application/json',
                                         'Authorization': f'Bearer {self._get_access_token()}'})
        return json.loads(response.content)

    def make_post_request(self, endpoint: str, data: dict = None) -> dict | list:
        url = urljoin(self._base_url, endpoint)

        response = requests.post(url=url, data=data,
                                 headers={'Content-type': 'application/json',
                                          'Authorization': f'Bearer {self._get_access_token()}'})
        return json.loads(response.content)


class TeachbaseClient:
    def __init__(self):
        self.client = APIClient(client_id=settings.TEACHBASE_SECRET_KEY,
                                client_secret=settings.TEACHBASE_PUBLIC_KEY,
                                base_url=settings.TEACHBASE_URL)

    def get_courses_list(self, page: int, per_page: int, types: List[int]) -> list:
        params = {}

        if page:
            params.update({'page': page})
        if per_page:
            params.update({'per_page': per_page})
        if types:
            params.update({'types': types})

        return self.client.make_get_request(endpoint='endpoint/v1/courses', params=params)

    def get_course(self, course_id: int) -> dict:
        return self.client.make_get_request(endpoint='endpoint/v1/courses', detail_key=course_id)
