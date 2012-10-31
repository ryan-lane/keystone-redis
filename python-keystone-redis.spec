Name:           python-keystone-redis
Version:        20121025
Release:        2%{?dist}
Summary:        Keystone Redis token storage backend

License:        ASL 2.0
URL:            https://github.rackspace.com/sao-paulo/keystone-redis
Source0:	keystone-redis.tar.bz2

BuildArch:	noarch
BuildRequires:  python, python-setuptools
Requires:	python-keystone
Requires:	python-redis >= 2.6.2
Requires:	python-dateutil

%description
Keystone is a Python implementation of the OpenStack
(http://www.openstack.org) identity service API.

This package contains the Rackspace Apps Keystone Redis token storage backend.

%prep

%setup -q -n keystone-redis

%build
%{__python} setup.py build

%install
%{__python} setup.py install --skip-build --root %{buildroot}

%pre

%files
%defattr(-,root,root,-)
%{python_sitelib}/keystoneredis
%{python_sitelib}/keystone_redis*.egg-info

%changelog
* Fri Oct 19 2012 Blake Atkins <blake.atkins@rackspace.com> 20121019-1
- Split out from openstack-keystone spec
