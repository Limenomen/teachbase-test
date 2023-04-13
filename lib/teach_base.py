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
        # TODO проработать автоматическое обновление токена по истечении времени
        url = urljoin(self._base_url, '/oauth/token')
        response = requests.post(
            url=url,
            data={'client_id': self._client_id,
                  'client_secret': self._client_secret,
                  'grant_type': 'client_credentials'}
        )
        response.raise_for_status()
        return json.loads(response.content).get('access_token')

    def make_get_request(self, endpoint: str, params: dict = None) -> dict | list:
        url = urljoin(self._base_url, endpoint)
        response = requests.get(url=url, params=params,
                                headers={'Content-type': 'application/json',
                                         'Authorization': f'Bearer {self._get_access_token()}'})
        return json.loads(response.content)

    def make_post_request(self, endpoint: str, data: dict = None) -> dict | list:
        url = urljoin(self._base_url, endpoint)
        response = requests.post(url=url, data=json.dumps(data, ensure_ascii=False),
                                 headers={'Content-type': 'application/json',
                                          'Authorization': f'Bearer {self._get_access_token()}'})
        return json.loads(response.content)


class TeachbaseClient:
    def __init__(self):
        self.client = APIClient(client_id=settings.TEACHBASE_PUBLIC_KEY,
                                client_secret=settings.TEACHBASE_SECRET_KEY,
                                base_url=settings.TEACHBASE_URL)

    def get_courses_list(self, page: int = None, per_page: int = None, types: List[int] = None) -> list:
        params = {}

        if page:
            params.update({'page': page})
        if per_page:
            params.update({'per_page': per_page})
        if types:
            params.update({'types': types})

        return self.client.make_get_request(endpoint='endpoint/v1/courses/', params=params)

    def get_course(self, course_id: int) -> dict:
        return self.client.make_get_request(endpoint=f'endpoint/v1/courses/{course_id}')

    def create_user(self, name: str, last_name: str, password: str, phone: str,
                    description: str = None, email: str = None) -> dict:
        """
        {
          "users": [
            {
              "email": "test@teachbase.ru",
              "name": "John",
              "description": "Corrupti natus quia recusandae.",
              "last_name": "Doe",
              "phone": "string",
              "role_id": 1,
              "password": "qwerty"
            }
          ]
        }
        """

        data = {
            'users': [
                {
                    'name': name,
                    'last_name': last_name,
                    'password': password,
                    'email': email,
                    'phone': phone,
                    'description': description,
                    'role_id': 1,
                },
            ]
        }
        return self.client.make_post_request(endpoint='endpoint/v1/users/create/', data=data)
