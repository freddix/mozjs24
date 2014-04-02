Summary:	JavaScript interpreter and libraries
Name:		mozjs24
Version:	24.2.0
Release:	1
License:	MPL 1.1 or GPL v2+ or LGPL v2.1+
Group:		Libraries
Source0:	http://ftp.mozilla.org/pub/mozilla.org/js/mozjs-%{version}.tar.bz2
# Source0-md5:	5db79c10e049a2dc117a6e6a3bc78a8e
Patch0:		%{name}-virtualenv.patch
URL:		https://developer.mozilla.org/En/SpiderMonkey/
BuildRequires:	libstdc++-devel
BuildRequires:	nspr-devel >= 4.7.0
BuildRequires:	perl-base
BuildRequires:	python
BuildRequires:	readline-devel
BuildRequires:	rpm-perlprov
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
JavaScript Reference Implementation (codename SpiderMonkey). The
package contains JavaScript runtime (compiler, interpreter,
decompiler, garbage collector, atom manager, standard classes) and
small "shell" program that can be used interactively and with .js
files to run scripts.

%package devel
Summary:	Header files for JavaScript reference library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel

%description devel
Header files for JavaScript reference library.

%prep
%setup -qn mozjs-%{version}
cd js/src
%patch0 -p0

%{__rm} -r editline

%build
cd js/src
%configure2_13 \
	--enable-readline	\
	--enable-threadsafe	\
	--with-system-ffi	\
	--with-system-nspr
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C js/src install \
	DESTDIR=$RPM_BUILD_ROOT

%check
%{__make} -j1 -C js/src check

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/ldconfig
%postun	-p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc js/src/README.html
%attr(755,root,root) %{_bindir}/js24
%attr(755,root,root) %{_libdir}/libmozjs-24.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/js24-config
%{_includedir}/mozjs-24
%{_pkgconfigdir}/mozjs-24.pc

