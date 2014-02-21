# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 OpenStack LLC
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

import nose

from keystone import config
from keystone import test
from keystoneredis import token as token_redis
from keystoneredis.common import keys as redis_keys

import test_backend


CONF = config.CONF


class RedisToken(test.TestCase, test_backend.TokenTests):
    def setUp(self):
        super(RedisToken, self).setUp()
        self.config([test.etcdir('keystone.conf.sample'),
                     test.testsdir('test_overrides.conf'),
                     test.testsdir('backend_redis.conf')])
        self.token_api = token_redis.Token()
        self.token_api.flush_all()

    def tearDown(self):
        self.token_api.flush_all()
        super(RedisToken, self).tearDown()

    def test_token_list(self):
        tokens = self.token_api.list_tokens('testuserid')
        self.assertEquals(len(tokens), 0)
        token_id1 = self.create_token_sample_data()
        tokens = self.token_api.list_tokens('testuserid')
        self.assertEquals(len(tokens), 1)
        self.assertIn(token_id1, tokens)
        token_id2 = self.create_token_sample_data()
        tokens = self.token_api.list_tokens('testuserid')
        self.assertEquals(len(tokens), 2)
        self.assertIn(token_id2, tokens)
        self.assertIn(token_id1, tokens)
        self.token_api.delete_token(token_id1)
        tokens = self.token_api.list_tokens('testuserid')
        self.assertIn(token_id2, tokens)
        self.assertNotIn(token_id1, tokens)
        self.token_api.delete_token(token_id2)
        tokens = self.token_api.list_tokens('testuserid')
        self.assertNotIn(token_id2, tokens)
        self.assertNotIn(token_id1, tokens)

        # XXX: Please note: keystoneredis does NOT support tenant-specific
        #      tokens, so that piece of this test (originally copied from
        #      Keystone proper) has been removed.
