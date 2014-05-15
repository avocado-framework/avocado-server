%global pymodulename avocadoserver
%global commit d077c15fb1543d8c16ed90f5c7d0c7d837c6fead
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Summary: REST based interface for applications to communicate with the avocado test server
Name: avocado-server
Version: 0.1.0
Release: 1%{?dist}
License: GPLv2
Group: Development/Tools
URL: http://avocado-framework.readthedocs.org/
BuildArch: noarch
Source0: https://github.com/avocado-framework/%{name}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
BuildRequires: python2-devel
Requires: python, python-django-restframework

%description
avocado-server provides a REST based interface for applications to communicate
with the avocado test server. It receives test activity updates by test jobs
running on other machines, consolidates various job and test results, etc.

%prep
%setup -q -n %{name}-%{commit}

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install --root %{buildroot} --skip-build

%files
%doc README.rst LICENSE
%{python_sitelib}/%{pymodulename}
%{python_sitelib}/%{pymodulename}-*.egg-info
%{_bindir}/avocado-server-manage

%changelog
* Mon May 12 2014 Cleber Rosa <cleber@redhat.com> - 0.1-1
- Initial build
