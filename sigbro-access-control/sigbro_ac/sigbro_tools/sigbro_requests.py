# -*- coding: UTF-8 -*-

import requests
from .sigbro_logs import sigbroLogs

log = sigbroLogs()


class sigbroRequests:
    """Sigbro Team Request class"""

    def __init__(self):
        """Initializaton."""

    def get(self, url: str, headers=None):
        """GET Request to remote url."""
        full_headers = { "Content-Type": "application/json", }
        if headers:
            full_headers.update(headers)
        
        result = requests.get(url=url, headers=full_headers)

        if result.status_code != 200:
            log.error(msg="GET request error", status_code=result.status_code, reason=result.reason)
            return False

        return result.json()

    def post(self, url: str, params, headers=None, encoded='json'):
        """POST Request to remote url with params."""
        if encoded == 'json':
            full_headers = { "Content-Type": "application/json", }
            if headers:
                full_headers.update(headers)
            
            result = requests.post(url=url, json=params, headers=full_headers)
        else:
            full_headers = {"Content-Type": "application/x-www-form-urlencoded", }
            if headers:
                full_headers.update(headers)
    
            result = requests.post(url=url, data=params, headers=full_headers)

        if result.status_code != 200:
            log.error(msg="POST request error", status_code=result.status_code, reason=result.reason)
            return False

        return result.json()
