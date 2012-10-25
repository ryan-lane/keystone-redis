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

import redis
from keystoneredis.common.redissl import Connection as SslConnection

from keystone.common import logging
from keystone import config
from keystone.openstack.common import cfg


CONF = config.CONF

CONF.register_opt(cfg.StrOpt('read_connection', default=None), group='redis')
CONF.register_opt(cfg.StrOpt('connection', default='localhost'), group='redis')
CONF.register_opt(cfg.MultiStrOpt('xdc_connection'), group='redis')
CONF.register_opt(cfg.IntOpt('idle_timeout', default=200), group='redis')
CONF.register_opt(cfg.IntOpt('database', default=0), group='redis')
CONF.register_opt(cfg.BoolOpt('ssl', default=False), group='redis')
CONF.register_opt(cfg.StrOpt('keyfile', default=None), group='redis')
CONF.register_opt(cfg.StrOpt('certfile', default=None), group='redis')
CONF.register_opt(cfg.StrOpt('ca_certs', default=None), group='redis')


class RedisSession(object):


    def __init__(self, **kwargs):
        read = kwargs.get('read_connection', CONF.redis.read_connection)
        local = kwargs.get('connection', CONF.redis.connection)
        xdc = kwargs.get('xdc_connections', CONF.redis.xdc_connection) or []
        database = kwargs.get('database', CONF.redis.database)
        idle_timeout = kwargs.get('idle_timeout', CONF.redis.idle_timeout)

        self.ttl_seconds = CONF.token.expiration
        self.local_client = self._create_client(local, database, idle_timeout)
        self.xdc_clients = [self._create_client(conn, database, idle_timeout)
                            for conn in xdc]

        if read:
            self.read_client = self._create_client(read, database, idle_timeout)
        else:
            self.read_client = self.local_client


    def _create_client(self, connection, database, idle_timeout):
        try:
            host, port = connection.rsplit(':', 1)
        except ValueError:
            host = connection
            port = 6379

        if CONF.redis.ssl:
            pool = redis.ConnectionPool(connection_class=SslConnection,
                                        host=host, port=port, db=database,
                                        socket_timeout=idle_timeout,
                                        keyfile=CONF.redis.keyfile,
                                        certfile=CONF.redis.certfile,
                                        ca_certs=CONF.redis.ca_certs)
        else:
            pool = redis.ConnectionPool(host=host, port=port, db=database,
                                        socket_timeout=idle_timeout)

        return redis.StrictRedis(connection_pool=pool)


