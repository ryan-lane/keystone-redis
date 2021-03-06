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

from setuptools import setup
from keystoneredis import VERSION

setup(name='keystone-redis',
      version=VERSION,
      description='Redis backends for Openstack Keystone.',
      author='Ian Good',
      author_email='ian.good@rackspace.com',
      url='https://github.com/icgood/keystone-redis',
      packages=['keystoneredis',
                'keystoneredis.common'],
      license='Apache License (2.0)',
      install_requires=[
          'setuptools',
          'python-dateutil',
          'redis',
      ],
      classifiers=['Development Status :: 3 - Alpha',
                   'Intended Audience :: Developers',
                   'Intended Audience :: Information Technology',
                   'License :: OSI Approved :: Apache Software License',
                   'Environment :: OpenStack',
                   'Programming Language :: Python'])

