# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 Ian Good
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""Redis backends for the various services."""

import dateutil.parser
import datetime
import copy

from keystone import exception
from keystone.openstack.common import timeutils
from keystone import token
from keystone.openstack.common import jsonutils

from common.session import RedisSession
from common import keys

class Token(RedisSession, token.Driver):

    def __init__(self, *args, **kwargs):
        RedisSession.__init__(self, *args, **kwargs)

    def flush_all(self):
        self.read_client.flushall()

    def get_token(self, token_id):
        token_key = keys.token(token_id)
        value = self.read_client.get(token_key)
        if value:
            token = jsonutils.loads(value)
            if token.get('expires', None) is not None:
                token['expires'] = dateutil.parser.parse(token['expires'])
                if token['expires'] > timeutils.utcnow():
                    return token
            else:
                return token
        raise exception.TokenNotFound(token_id=token_id)

    def _set_on_client(self, client, user_id, token_id, json_data, ttl_seconds):
        pipe = client.pipeline()
        token_key = keys.token(token_id)
        if user_id:
            user_key = keys.usertoken(user_id['id'], token_id)
        if ttl_seconds is None:
            pipe.set(token_key, json_data)
            if user_id:
                pipe.set(user_key, '')
        else:
            pipe.setex(token_key, ttl_seconds, json_data)
            if user_id:
                pipe.setex(user_key, ttl_seconds, '')
        pipe.execute()

    def create_token(self, token_id, data):
        data_copy = copy.deepcopy(data)
        user_id = data_copy.get('user', None)
        if 'expires' not in data_copy:
            data_copy['expires'] = self._get_default_expire_time()
        json_data = jsonutils.dumps(data_copy)
        self._set_on_client(self.local_client, user_id, token_id,
                            json_data, self.ttl_seconds)
        for xdc_client in self.xdc_clients:
            try:
                self._set_on_client(xdc_client, user_id, token_id,
                                    json_data, self.ttl_seconds)
            except RedisError:
                pass
        return data_copy

    def _delete_on_client(self, client, user_id, token_id):
        pipe = client.pipeline()
        token_key = keys.token(token_id)
        pipe.delete(token_key)
        if user_id is not None:
            user_key = keys.usertoken(user_id['id'], token_id)
            pipe.delete(user_key)
        pipe.sadd(keys.revoked(), token_id)
        pipe.execute()

    def delete_token(self, token_id):
        data = self.get_token(token_id)
        user_id = data.get('user', None)
        self._delete_on_client(self.local_client, user_id, token_id)
        for xdc_client in self.xdc_clients:
            try:
                self._delete_on_client(xdc_client, user_id, token_id)
            except RedisError:
                pass

    def list_tokens(self, user_id, tenant=None):
        pattern = keys.usertoken(user_id, '*')
        user_keys = self.read_client.keys(pattern)
        return [keys.parse_usertoken(key)[1] for key in user_keys]

    def list_revoked_tokens(self):
        return [{'id': s} for s in self.read_client.smembers(keys.revoked())]


class TokenNoList(Token):

    def _set_on_client(self, client, user_id, token_id, json_data, ttl_seconds):
        token_key = keys.token(token_id)
        if ttl_seconds is None:
            client.set(token_key, json_data)
        else:
            client.setex(token_key, ttl_seconds, json_data)

    def delete_token(self, token_id):
        self._delete_on_client(self.local_client, None, token_id)
        for xdc_client in self.xdc_clients:
            try:
                self._delete_on_client(xdc_client, None, token_id)
            except RedisError:
                pass

    def list_tokens(self, user_id):
        raise exception.NotImplemented()

    def list_revoked_tokens(self):
        raise exception.NotImplemented()

