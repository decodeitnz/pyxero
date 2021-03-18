from __future__ import unicode_literals

import requests

from .basemanager import BaseManager
from .constants import XERO_PAYROLL_URL
from .utils import singular


class PayrollManager(BaseManager):
    def __init__(self, name, credentials, unit_price_4dps=False, user_agent=None):
        from xero import __version__ as VERSION

        self.credentials = credentials
        self.name = name
        self.base_url = credentials.base_url + XERO_PAYROLL_URL
        self.extra_params = {"unitdp": 4} if unit_price_4dps else {}
        self.singular = singular(name)

        if user_agent is None:
            self.user_agent = (
                "pyxero/%s " % VERSION + requests.utils.default_user_agent()
            )
        else:
            self.user_agent = user_agent

        for method_name in self.DECORATED_METHODS:
            method = getattr(self, "_%s" % method_name)
            setattr(self, method_name, self._get_data(method))

    def _check_api_response_status(self, data, resource_name):
        assert data['problem'] is None, (
            'Expected no problem from API but received {}'.format(data['problem'])
        )

        try:
            return data[resource_name.lower()]
        except KeyError:
            return data

    def _fix_uri(self, uri, method, *args, **kwargs):
        if method == 'put':
            data = args[0]

            return '/'.join((uri, data['{}ID'.format(self.singular.lower())]))
        else:
            return uri
