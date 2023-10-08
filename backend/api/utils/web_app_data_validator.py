from urllib.parse import parse_qs
import hashlib
import hmac
import time
import json


class WebAppDataHelper:
    '''
    https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app

    The data received via the mini-app is a URL-encoded string of the following
    format:

    query_id=<query_id>auth_date=<unix_time>&user={“id":123456789,“first_name":“John",“last_name":""}&hash=123abc

    The hash parameter is a hexademical representation of the hmac-sha-256
    signature of the data-check-string, which is generated as follows:

    1. Sort all key/value pairs of the data received via the mini-app in
    lexicographical order by key name, in ascending order. For example, the
    data-check-string for the above example would be:

    auth_date=1614811840&query_id=123456789&user={“first_name":“John",“id":123456789,“last_name":""}

    2. Calculate the hmac-sha-256 signature of the data-check-string using the
    bot token as a secret key.

    3. Compare the resulting signature with the hash parameter. If the
    signatures match, the data is valid and you can use it.

    4. Check the auth_date parameter. If the difference between the current
    time and auth_date exceeds 24 hours, discard the data. This check is
    necessary to prevent replay attacks.
    '''
    def __init__(self, data: str, bot_token: str, diff: int = 60000):
        self.data = data
        self.bot_token = bot_token
        self.diff = diff

    @property
    def parsed_data(self):
        return {
            key: val[0]
            if len(val) == 1
            else val for key, val in parse_qs(self.data).items()
        }

    @property
    def parsed_user_data(self):
        return json.loads(self.parsed_data['user'])

    def _validate_integrity(self, data):
        secret_key = hashlib.sha256(self.bot_token.encode()).digest()

        del data['hash']
        key_value_pairs = [f'{k}={v}' for k, v in sorted(data.items())]
        data_check_string = '\n'.join(key_value_pairs)

        secret_key = hmac.new(
            key=b"WebAppData",
            msg=self.bot_token.encode(),
            digestmod=hashlib.sha256)
        _result = hmac.new(
            secret_key.digest(),
            data_check_string.encode(),
            hashlib.sha256)

        return _result.hexdigest()

    @property
    def is_valid(self):
        data = self.parsed_data

        result = self._validate_integrity(data.copy())
        unix_time_now = int(time.time())
        unix_time_auth_date = int(data['auth_date'])
        diff = unix_time_now - unix_time_auth_date

        # hexademical representation of the hmac-sha-256 signature of the
        # data-check-string
        data_check_string_hash = data.pop('hash')

        # check if the data is valid and timeout exceeded
        return result == data_check_string_hash and diff <= self.diff
