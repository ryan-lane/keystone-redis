
About
=====

This package provides a redis-based token driver for
[Openstack Keystone](http://keystone.openstack.org/). This
works for the "Folsom" release and above.

### Known issues

* The optional tenant ID argument to `list_tokens()` is unused. No plans exist
  to change this, as it is not currently implementable without a full table scan
  of each and every token.

Installation
============

As the first step, be sure to activate the Python virtualenv environment
containing your Openstack Keystone setup, if applicable.

Install keystone-redis and dependencies:

    python setup.py install

To run the tests, make sure the `tests/` directory of the Openstack Keystone
repository is in your Python path:

    nosetests

Configuration
=============

To use keystone-redis in a Keystone configuration, edit the `driver` option
in the `token` section of `keystone.conf`.

    [token]
    driver = keystoneredis.token.Token

If the redis instance is only running on the local machine, you are all set.
To point it to a redis instance on another machine:

    [redis]
    connection = redis-instance.example.com
    # This option can be suffixed with a port number, e.g. :6379.

If you have read-only slaves that should handle any read operations, you can
configure a custom read-only connection:

    [redis]
    read_connection = redis-slave.example.com

To configure the redis database number (see the
[SELECT](http://redis.io/commands/select) command), use the `database` option in
the `redis` section. To configure the idle timeout, use the `idle_timeout`
option.

    [redis]
    idle_timeout = 200
    database = 0

Key Schema
==========

The keys written to redis are as follows

### Tokens

The token entries themselves will look like:

    token e3f75b94322746989868f07d61370086

### User Tokens List

To allow searching for all a particular user's tokens, a second key is generated
for every token in the following format:

    usertoken dXNlcmlk e3f75b94322746989868f07d61370086

The second piece of the key is a base64 encoded version of the user ID. In this
example, the user ID is `userid`.

