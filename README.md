
Installation
============

As the first step, be sure to activate the Python virtualenv environment
containing your Keystone setup, if applicable.

Install keystone-redis and dependencies:

    python setup.py install

Configuration
=============

To use keystone-redis in a Keystone configuration, edit the `driver` option
in the `token` section of `keystone.conf`.

    [token]
    driver = keystoneredis.token.Token

If you do not need to support the ability to invalidate tokens when a user is
disabled or changes their password, you could use the following instead:

    [token]
    driver = keystoneredis.token.TokenNoList

If the redis instance is only running on the local machine, you are all set.
To point it to a redis instance on another machine:

    [redis]
    connection = redis-instance.example.com
    # This option can be suffixed with a port number, e.g. :6379.

To configure the redis database number (see the
[SELECT](http://redis.io/commands/select) command), use the `database` option in
the `redis` section. To configure the idle timeout, use the `idle_timeout`
option.

    [redis]
    idle_timeout = 200
    database = 0

Multi-Datacenter Configuration
==============================

The keystone-redis module can optionally be configured to also write tokens to
secondary redis instances, such as in the case of multiple datacenters. If
writing to the primary connection fails, the operation fails, but if writing to
a secondary connection fails the error is logged but success will still be
returned.

This feature is configured by adding at least one `xdc_connection` option to the
`redis` section, using the same format as the `connection` option above.

    [redis]
    connection = redis.local.example.com
    xdc_connection = redis.remote1.example.com
    xdc_connection = redis.remote2.example.com
    xdc_connection = redis.remote3.example.com
    # ...

These writes are not asynchronous, success or failure will not be returned to
the client until all secondary connections have been written to.

Key Schema
==========

The keys written to redis are as follows

## Tokens

The token entries themselves will look like:

    token e3f75b94322746989868f07d61370086

### User Tokens List

To allow searching for all a particular user's tokens, a second key is generated
for every token in the following format:

    usertoken dXNlcmlk e3f75b94322746989868f07d61370086

The second piece of the key is a base64 encoded version of the user ID. In this
example, the user ID is `userid`.

