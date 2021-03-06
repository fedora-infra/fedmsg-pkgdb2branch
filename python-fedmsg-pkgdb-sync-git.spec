%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2:        %global __python2 /usr/bin/python2}
%{!?python2_sitelib:  %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

%global modname fedmsg_pkgdb_sync_git

Name:               python-fedmsg-pkgdb-sync-git
Version:            0.1
Release:            1%{?dist}
Summary:            A fedmsg consumer that runs pkgdb_sync_git in response to FAS messages

Group:              Development/Libraries
License:            LGPLv2+
URL:                https://github.com/fedora-infra/fedmsg-pkgdb_sync_git/
Source0:            http://pypi.python.org/packages/source/f/%{modname}/%{modname}-%{version}.tar.gz

BuildArch:          noarch

BuildRequires:      python2-devel
BuildRequires:      python-setuptools
BuildRequires:      fedmsg

Requires:           fedmsg
Requires:           fedmsg-hub
Requires:           python-fedmsg-meta-fedora-infrastructure

%description
A simple script monitoring fedmsg for FAS messages, delaying action
for a few seconds to accumulate messages and avoid pile-up and run
pkgdb2branch via ansible.

%prep
%setup -q -n %{modname}-%{version}

# Remove bundled egg-info in case it exists
rm -rf %{modname}.egg-info

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --skip-build --root=%{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}/fedmsg.d/
cp -p fedmsg.d/pkgdb_sync_git-example-config.py \
    %{buildroot}%{_sysconfdir}/fedmsg.d/pkgdb_sync_git.py

%files
%doc README.rst LICENSE
%{python2_sitelib}/%{modname}.py*
%{python2_sitelib}/%{modname}-%{version}*

%config(noreplace) %{_sysconfdir}/fedmsg.d/pkgdb_sync_git.py*

%changelog
* Fri Aug 22 2014 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.1-1
- Original work on packaging for Fedora and EPEL
