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
import uuid

from keystone import config
from keystone import exception
from keystone import test
from keystoneredis import token as token_redis

import default_fixtures
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
        raise nose.exc.SkipTest('N/A')

#    def test_list_revoked_tokens_for_multiple_tokens(self):
#        raise nose.exc.SkipTest('N/A')
#
#    def test_list_revoked_tokens_for_single_token(self):
#        raise nose.exc.SkipTest('N/A')
#
#    def test_list_revoked_tokens_returns_empty_list(self):
#        raise nose.exc.SkipTest('N/A')
