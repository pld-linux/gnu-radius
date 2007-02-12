Summary:	GNU RADIUS Server
Summary(pl.UTF-8):   Serwer GNU RADIUS
Name:		gnu-radius
Version:	1.3
Release:	1
License:	GPL
Group:		Networking/Daemons
Source0:	ftp://ftp.gnu.org/pub/gnu/radius/radius-%{version}.tar.bz2
# Source0-md5:	8bf4ebdc94415d8a25949b12aa04a337
Source1:	%{name}.pamd
Source2:	%{name}.init
Source3:	%{name}.logrotate
Source4:	%{name}-mysql.sql
Source5:	%{name}-pgsql.sql
URL:		http://www.gnu.org/software/radius/
BuildRequires:	gettext-devel
BuildRequires:	groff
BuildRequires:	guile-devel >= 1.4
BuildRequires:	libtool
BuildRequires:	m4
BuildRequires:	mysql-devel
BuildRequires:	pam-devel
BuildRequires:	postgresql-devel
BuildRequires:	readline-devel
BuildRequires:	texinfo
Requires(post):	fileutils
Requires(post,preun):	/sbin/chkconfig
Requires:	logrotate
Requires:	pam >= 0.77.3
Requires:	rc-scripts
Provides:	radius
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	radius

%description
RADIUS server with a lot of functions. Short overview:

- PAM support,
- SQL authentication
- Supports access based on huntgroups,
- Multiple DEFAULT entries in users file,
- All users file entries can optionally "fall through",
- Caches all config files in-memory,
- Keeps a list of logged in users (radutmp file),
- "radwho" program can be installed as "fingerd",
- Logs both UNIX "wtmp" file format and RADIUS detail logfiles,
- Supports Simultaneous-Use = X parameter. Yes, this means that you
  can now prevent double logins!.

%description -l pl.UTF-8
Serwer RADIUS z wieloma funkcjami. Krótki przegląd:
- obsługa PAM,
- uwierzytelnianie z użyciem SQL,
- obsługa dostępu opartego na huntgroups,
- wiele wpisów DEFAULT w pliku użytkowników,
- wszystkie wpisy w pliku użytkowników mogą opcjonalnie
  "przepuszczać",
- buforowanie wszystkich plików konfiguracyjnych w pamięci,
- przechowywanie listy zalogowanych użytkowników (plik radutmp),
- program "radwho", który można zainstalować jako "fingerd"
- logowanie w formacie uniksowego pliku "wtmp" oraz szczegółowych
  logów RADIUS
- obsługa parametru Simultaneous-Use = X; tak, to oznacza, że można
  zablokować podwójne logowania.

%package devel
Summary:	Headers for GNU Radius
Summary(pl.UTF-8):   Pliki nagłówkowe bibliotek GNU Radius
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Headers for GNU Radius.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek GNU Radius

%package static
Summary:	Static GNU Radius libraries
Summary(pl.UTF-8):   Statyczne biblioteki GNU Radius
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
GNU Radius static libraries.

%description static -l pl.UTF-8
Statyczne biblioteki GNU Radius.

%prep
%setup -q -n radius-%{version}

%build
%configure \
	--with-dbm \
	--with-mysql \
	--with-postgresql \
	--enable-pam \
	--enable-shadow

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{logrotate.d,rc.d/init.d,pam.d},/var/log/radacct} \
	$RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_mandir}/man{1,5,8},%{_sysconfdir}/raddb,%{_libdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/radius
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/radius
install %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/radius
install %{SOURCE4} mysql.sql
install %{SOURCE5} pgsql.sql

touch $RPM_BUILD_ROOT/etc/pam.d/radius
touch $RPM_BUILD_ROOT/var/log/rad{utmp,wtmp,ius.log}

%find_lang radius

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1
/sbin/chkconfig --add radius
if [ -f /var/lock/subsys/radius ]; then
	/etc/rc.d/init.d/radius restart >&2
else
	echo "Run \"/etc/rc.d/init.d/radius start\" to start radius daemon."
fi
touch /var/log/rad{utmp,wtmp,ius.log}
chmod 640 /var/log/rad{utmp,wtmp,ius.log}

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/radius ]; then
		/etc/rc.d/init.d/radius stop >&2
	fi
	/sbin/chkconfig --del radius
fi

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1

%files -f radius.lang
%defattr(644,root,root,755)
%doc {ChangeLog,README*,*.sql}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/naslist
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/nas.rc
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/nastypes
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/users
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/realms
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/client.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/clients
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/sqlserver
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/huntgroups
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/hints
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/config
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/access.deny
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/dict
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/dictionary
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/radius
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/radius
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/radius
%attr(750,root,root) %dir /var/log/radacct
%dir %{_sysconfdir}/raddb
%attr(640,root,root) %ghost /var/log/radutmp
%attr(640,root,root) %ghost /var/log/radwtmp
%attr(640,root,root) %ghost /var/log/radius.log
%{_datadir}/radius
%{_mandir}/*/*
%{_infodir}/*.info*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/radius

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
