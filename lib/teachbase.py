import json
from typing import List
from urllib.parse import urljoin

import requests
from django.conf import settings
from requests import HTTPError


class APIException(Exception):
    pass


class APIClient:
    """Базовый класс для взаимодействия с API"""
    def __init__(self, client_id: str, client_secret: str, base_url: str):
        self._client_id = client_id
        self._client_secret = client_secret
        self._base_url = base_url

    def make_get_request(self, endpoint: str, params: dict = None) -> dict | list:
        url = urljoin(self._base_url, endpoint)
        try:
            response = requests.get(url=url, params=params, headers=self._get_headers())
            response.raise_for_status()
            return json.loads(response.content)
        except HTTPError as e:
            raise APIException(e.response.content, e.response.status_code)

    def make_post_request(self, endpoint: str, data: dict = None) -> dict | list:
        url = urljoin(self._base_url, endpoint)
        try:
            response = requests.post(url=url, data=json.dumps(data, ensure_ascii=False), headers=self._get_headers())
            response.raise_for_status()
            return json.loads(response.content)
        except HTTPError as e:
            raise APIException(e.response.content, e.response.status_code)

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

    def _get_headers(self) -> dict:
        return {'Content-type': 'application/json', 'Authorization': f'Bearer {self._get_access_token()}'}


class TeachbaseClient:
    """Класс-обвязка для работы с API Teachbase"""
    def __init__(self):
        self.client = APIClient(client_id=settings.TEACHBASE_PUBLIC_KEY,
                                client_secret=settings.TEACHBASE_SECRET_KEY,
                                base_url=settings.TEACHBASE_URL)

    def get_courses_list(self, page: int = None, per_page: int = None, types: List[int] = None) -> list:
        params = self._parse_params(page=page, per_page=per_page, types=types)

        return self.client.make_get_request(endpoint='endpoint/v1/courses/', params=params)

    def get_course(self, course_id: int) -> dict:
        return self.client.make_get_request(endpoint=f'endpoint/v1/courses/{course_id}')

    def create_user(self, name: str, last_name: str, password: str, phone: str,
                    description: str = None, email: str = None) -> dict:
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

    def get_course_sessions(self, course_id: int, status: str = None, participant_ids: List[int] = None) -> list:
        params = self._parse_params(status=status, participant_ids=participant_ids)

        return self.client.make_get_request(endpoint=f'/endpoint/v1/courses/{course_id}/course_sessions/',
                                            params=params)

    def register_course_session_user(self, session_id: int, user_id: int, phone: int, email: str = None) -> dict:
        data = {
            'email': email,
            'phone': phone,
            'user_id': user_id,
        }

        return self.client.make_post_request(endpoint=f'endpoint/v1/course_sessions/{session_id}/register/', data=data)

    def _parse_params(self, **kwargs):
        params = {}
        for key, value in kwargs.items():
            if value is not None:
                params[key] = value
        return params
