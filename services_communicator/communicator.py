import requests
import logging
from django.conf import settings
from django.shortcuts import get_object_or_404

from services_communicator import exceptions
from services_communicator.models import ServiceList

_session = requests.Session()

__all__ = [
    "Communicator",
]

logger = logging.getLogger("service_communicator")


class ServiceAction:

    @staticmethod
    def _post_action(path: str, data: dict, headers=None, timeout=25):
        """
        :param path:
        :param data:
        :param headers:
        :param timeout:
        :return:
        """
        try:
            with _session as session:
                response = session.post(path, json=data, headers=headers, timeout=timeout)
        except (requests.ConnectionError, requests.Timeout) as err:
            raise exceptions.ServiceUnavailable()

        return response

    @staticmethod
    def _patch_action(path: str, data: dict, headers=None, timeout=25):
        """
        :param path:
        :param data:
        :param headers:
        :param timeout:
        :return:
        """
        try:
            with _session as session:
                response = session.patch(path, json=data, headers=headers, timeout=timeout)
        except (requests.ConnectionError, requests.Timeout) as err:
            raise exceptions.ServiceUnavailable()

        return response

    @staticmethod
    def _get_action(path: str, params=None, headers=None, timeout=25):
        """
        :param path:
        :param params:
        :param headers:
        :param timeout:
        :return:
        """
        try:
            with _session as session:
                response = session.get(path, headers=headers, timeout=timeout)
        except (requests.ConnectionError, requests.Timeout) as err:
            raise exceptions.ServiceUnavailable(err)

        return response


class ServiceObject:
    def __init__(self, *args, **kwargs):
        allowed_attributes = ["service_id", "service_slug", "service_guid"]
        for name, value in kwargs.items():
            assert name in allowed_attributes
            setattr(self, name, value)

    def get_service(self):
        try:
            obj = ServiceList.objects.get(**self.__dict__)
            return obj
        except:
            logger.warning("No database or service found in your database")
            return None


class Communicator(ServiceObject, ServiceAction):

    def __init__(self, *args, **kwargs):
        super(Communicator, self).__init__(*args, **kwargs)
        self.service = self.get_service()
        if self.service:
            self.base_url = self.service.service_url
            self.version = self.service.api_version
            self.token_url = self.service.service_token_url
        else:
            pass

    def _token(self):
        data = self._get_cred_data()
        try:
            path = self.base_url + self.version + self.token_url
            response = self._post_action(path=path, data=data)
            if response.status_code != 200:
                raise exceptions.ServiceUnavailable()
            token = response.json()
        except requests.HTTPError as err:
            raise exceptions.ServiceUnavailable()

        return {"Authorization": f"JWT {token['token']}"}

    def _get_cred_data(self):
        cred = settings.CREDENTIALS
        data, = [cred.get(self.service.service_id) if cred.get(self.service.service_id) else cred.get(
            self.service.service_slug)]
        return data
