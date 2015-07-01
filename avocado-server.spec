%global modulename avocadoserver
%if ! 0%{?commit:1}
 %define commit 0f1a6cefc485a64e495e1b4986b4fa0540333234
%endif
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Summary: REST based interface for applications to communicate with the avocado test server
Name: avocado-server
Version: 0.25.0
Release: 2%{?dist}
License: GPLv2
Group: Development/Tools
URL: http://avocado-framework.readthedocs.org/
BuildArch: noarch
Source0: https://github.com/avocado-framework/%{name}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
BuildRequires: python2-devel
BuildRequires: systemd
Requires: python
Requires: python-django-rest-framework
Requires: python-django-rest-framework-nestedrouters
Requires: python-gunicorn
Requires: systemd
Requires(pre): shadow-utils

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
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
install -p -m 644 data/systemd/%{modulename}.service $RPM_BUILD_ROOT%{_unitdir}/%{modulename}.service

%pre
getent group avocadoserver >/dev/null || groupadd -r avocadoserver
getent passwd avocadoserver >/dev/null || \
    useradd -r -g avocadoserver -d /dev/null -s /sbin/nologin \
    -c "Avocado Test Result Server" avocadoserver
exit 0

%post
%systemd_post %{modulename}.service

%preun
%systemd_preun %{modulename}.service

%postun
%systemd_postun

%files
%doc README.rst LICENSE
%{python_sitelib}/%{modulename}
%{python_sitelib}/%{modulename}-*.egg-info
%{_bindir}/avocado-server-manage
%{_unitdir}/%{modulename}.service

%changelog
* Mon Jun 29 2015 Cleber Rosa <cleber@redhat.com> - 0.25.0-2
- Update python-django-rest-framework package names

* Tue Jun 16 2015 Lucas Meneghel Rodrigues <lmr@redhat.com> - 0.25.0-1
- Update to upstream version 0.25.0

* Thu May 29 2014 Cleber Rosa <cleber@redhat.com> - 0.2.0-1
- Release 0.2.0

* Mon May 12 2014 Cleber Rosa <cleber@redhat.com> - 0.1-1
- Initial build
