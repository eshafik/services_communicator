import requests
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from django.conf import settings
from django.core.cache import cache

from services_communicator import exceptions
from services_communicator.models import ServiceList


__all__ = [
    "Communicator",
]


def retry_session(retries=3, back_off_factor=0.3, status_force_list=(500, 502, 503, 504), session=None):
    """
    Read More: https://www.peterbe.com/plog/best-practice-with-retries-with-requests
    :param retries:
    :param back_off_factor:
    :param status_force_list:
    :param session:
    :return:
    """
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=back_off_factor,
        status_forcelist=status_force_list,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


# _session = requests.Session()
_session = retry_session()

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
    def _get_action(path: str, headers=None, timeout=25):
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


class Communicator(ServiceAction):

    def __init__(self, *args, **kwargs):
        allowed_attributes = ["service_id", "service_slug", "service_guid"]
        for name, value in kwargs.items():
            assert name in allowed_attributes
            setattr(self, name, value)

    def _get_cred_data(self):
        """
            Get credential from settings file
        """
        cred = settings.CREDENTIALS
        data = cred.get(int(next(iter(self.__dict__.values()))))
        return data

    def _token(self):
        """
            Get token from the service
        """
        try:
            if cache.get("jwt_token"):
                token = cache.get("jwt_token")
            else:
                data = self._get_cred_data()
                service = self.get_service()
                path = service.service_url + service.api_version + service.service_token_url
                response = self._post_action(path=path, data=data)
                if response.status_code != 200:
                    raise exceptions.ServiceUnavailable()
                token = response.json()
                cache.set("jwt_token", token, 3000)
        except requests.HTTPError as err:
            raise exceptions.ServiceUnavailable()

        return {"Authorization": f"JWT {token['token']}"}

    def get_full_url(self):
        """
            Get full BASE URL of the Service
        """
        return self.get_service().get_full_url

    def get_service(self):
        """
            Get the service object
        """
        try:
            service = ServiceList.objects.get(**self.__dict__)
            return service
        except Exception as error:
            logger.warning("No service object found on service list. Check admin Dashboard. Error{}".format(error))
            raise exceptions.ValidationError("No service object found on service list. Check admin dashboard")
