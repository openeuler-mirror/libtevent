%{!?python3_sitearch: %define python3_sitearch %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

Name:      libtevent
Version:   0.9.37
Release:   4
Summary:   Tevent is an event system based on the talloc memory management library.
License:   LGPLv3+
URL:       http://tevent.samba.org
Source0:   http://samba.org/ftp/tevent/tevent-%{version}.tar.gz

Patch6000: 6000-tevent-fix-CID-1437976-dereference-before-null-check.patch
Patch6001: 6001-tevent-fix-CID-1437974-dereference-after-null-check.patch
Patch6002: 6002-lib-tevent-Use-correct-C99-initializer-for-tevent_re.patch

BuildRequires: gcc libtirpc-devel docbook-style-xsl doxygen libxslt git
BuildRequires: python2-devel python2-talloc-devel >= 2.1.0 libtalloc-devel >= 2.1.0
BuildRequires: python3-devel python3-talloc-devel >= 2.0.7

Provides: bundled(libreplace)


%description
Tevent is an event system based on the talloc memory management library. It is the core event system used in Samba.
The low level tevent has support for many event types, including timers, signals, and the classic file descriptor events.
Tevent also provide helpers to deal with asynchronous code providing the tevent_req (tevent request) functions.

%package devel
Summary: Libraries and header files for tevent
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: libtalloc-devel%{?_isa} >= 2.0.7 pkgconfig

%description devel
Libraries and header files for tevent

%package -n python2-tevent
Summary: Python 2 libraries files for tevent
Requires: libtevent%{?_isa} = %{version}-%{release}

%{?python_provide:%python_provide python2-tevent}

%description -n python2-tevent
Python2 libraries files for tevent

%package -n python3-tevent
Summary: Python 3 libraries files for tevent
Requires: libtevent%{?_isa} = %{version}-%{release}

%{?python_provide:%python_provide python3-tevent}

%description -n python3-tevent
Python3 libraries files for tevent

%package help
Summary: Man for tevent
Requires: man

%description help
Man for tevent

%prep
%autosetup -n tevent-%{version} -p1 -Sgit

%build

pathfix.py -npi %{__python2} buildtools/bin/waf

%configure --disable-rpath --bundled-libraries=NONE --builtin-libraries=replace --extra-python=%{__python3}

%make_build V=1
doxygen doxy.config

%install
%make_install
find $RPM_BUILD_ROOT -name "*.so*" -exec chmod -c +x {} \;

mkdir -p $RPM_BUILD_ROOT/%{_mandir}
cp -a ./doc/man/* $RPM_BUILD_ROOT/%{_mandir}/

%check
%make_build check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_libdir}/libtevent.so.*

%files devel
%{_includedir}/tevent.h
%{_libdir}/libtevent.so
%{_libdir}/pkgconfig/tevent.pc

%files -n python2-tevent
%{python2_sitearch}/*

%files -n python3-tevent
%{python3_sitearch}/*

%files help
%exclude %{_mandir}/man3/todo*
%{_mandir}/man3/tevent*


%changelog
* Tue Sep 3 2019  wubo<wubo40@huawei.com> - 0.9.37-4
- Package init
