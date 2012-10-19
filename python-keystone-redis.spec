Name:           python-keystone-redis.spec
Version:        20121019
Release:        1%{?dist}
Summary:        Keystone Redis token storage backend

License:        ASL 2.0
URL:            https://github.rackspace.com/sao-paulo/keystone-redis
Source0:	python-keystone-redis-git.tar.bz2

BuildArch:	noarch
BuildRequires:  python, git
Requires:	python-keystone
Requires:	python-redis >= 2.6.2

%description
Keystone is a Python implementation of the OpenStack
(http://www.openstack.org) identity service API.

This package contains the Rackspace Apps Keystone Redis token storage backend.

%prep
# Keystone
rm -rf %{_sourcedir}/python-keystone-redis-git
git clone git://github.rackspace.com/sao-paulo/keystone-redis.git %{_sourcedir}/python-keystone-redis-git
cd %{_sourcedir}/python-keystone-redis-git
git archive  --format=tar --prefix=python-keystone-redis-git/ HEAD | bzip2 > python-keystone-redis-git.tar.bz2
mv python-keystone-redis-git.tar.bz2 %{_sourcedir}
%setup -q -n python-keystone-redis-git

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
