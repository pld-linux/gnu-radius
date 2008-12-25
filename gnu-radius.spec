Summary:	GNU RADIUS Server
Summary(pl.UTF-8):	Serwer GNU RADIUS
Name:		gnu-radius
Version:	1.6.1
Release:	1
License:	GPL v3+
Group:		Networking/Daemons/Radius
Source0:	ftp://ftp.gnu.org/pub/gnu/radius/radius-%{version}.tar.bz2
# Source0-md5:	58d6b3595735d00fa211979a99e87f3d
Source1:	%{name}.pamd
Source2:	%{name}.init
Source3:	%{name}.logrotate
Source4:	%{name}-mysql.sql
Source5:	%{name}-pgsql.sql
Source6:	%{name}.sysconfig
URL:		http://www.gnu.org/software/radius/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.8
BuildRequires:	gettext-devel
BuildRequires:	groff
BuildRequires:	guile-devel >= 1.4
BuildRequires:	libltdl-devel
BuildRequires:	libtool
BuildRequires:	m4
BuildRequires:	mysql-devel
BuildRequires:	pam-devel
BuildRequires:	postgresql-devel
BuildRequires:	readline-devel
BuildRequires:	texinfo
Requires(post):	fileutils
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-libs = %{version}-%{release}
Requires:	logrotate
Requires:	pam >= 0.77.3
Requires:	rc-scripts
Provides:	radius
Obsoletes:	radius
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%package mysql
Summary:	MySQL support module for GNU Radius
Summary(pl.UTF-8):	Moduł obsługi baz danych MySQL dla serwera GNU Radius
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description mysql
MySQL support module for GNU Radius.

%description mysql -l pl.UTF-8
Moduł obsługi baz danych MySQL dla serwera GNU Radius.

%package postgres
Summary:	PostgreSQL support module for GNU Radius
Summary(pl.UTF-8):	Moduł obsługi baz danych PostgreSQL dla serwera GNU Radius
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description postgres
PostgreSQL support module for GNU Radius.

%description postgres -l pl.UTF-8
Moduł obsługi baz danych PostgreSQL dla serwera GNU Radius.

%package libs
Summary:	GNU Radius libraries
Summary(pl.UTF-8):	Biblioteki GNU Radius
Group:		Libraries
Conflicts:	gnu-radius < 1.5-2

%description libs
GNU Radius libraries.

%description libs -l pl.UTF-8
Biblioteki GNU Radius.

%package devel
Summary:	Headers for GNU Radius
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek GNU Radius
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Headers for GNU Radius.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek GNU Radius

%package static
Summary:	Static GNU Radius libraries
Summary(pl.UTF-8):	Statyczne biblioteki GNU Radius
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
GNU Radius static libraries.

%description static -l pl.UTF-8
Statyczne biblioteki GNU Radius.

%prep
%setup -q -n radius-%{version}

rm -f po/stamp-po

%build
%{__libtoolize}
%{__aclocal} -I m4 -I db -I am
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-dbm \
	--with-mysql \
	--with-postgresql \
	--with-sql=mysql,postgres \
	--enable-pam \
	--enable-shadow

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{logrotate.d,rc.d/init.d,pam.d,sysconfig},/var/log/radacct} \
	$RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_mandir}/man{1,5,8},%{_sysconfdir}/raddb,%{_libdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/radius
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/radius
install %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/radius
install %{SOURCE4} mysql.sql
install %{SOURCE5} pgsql.sql
install %{SOURCE6} $RPM_BUILD_ROOT/etc/sysconfig/gnu-radius

touch $RPM_BUILD_ROOT/etc/pam.d/radius
touch $RPM_BUILD_ROOT/var/log/rad{utmp,wtmp,ius.log}

rm -f $RPM_BUILD_ROOT%{_libdir}/radius/%{version}/modules/*.{la,a}
# fix to point to library itself, not .so link
ln -sf $(basename $RPM_BUILD_ROOT%{_libdir}/libradscm.so.*.*.*) $RPM_BUILD_ROOT%{_libdir}/libguile-gnuradius-v-%{version}.so

%find_lang radius

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1
/sbin/chkconfig --add radius
touch /var/log/rad{utmp,wtmp,ius.log}
chmod 640 /var/log/rad{utmp,wtmp,ius.log}

%posttrans
%service radius restart "GNU RADIUS server"
exit 0

%preun
if [ "$1" = "0" ]; then
	%service radius stop
	/sbin/chkconfig --del radius
fi

%postun	-p	/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f radius.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%dir %{_libdir}/radius
%dir %{_libdir}/radius/%{version}
%dir %{_libdir}/radius/%{version}/modules
%{_datadir}/radius
%dir %{_sysconfdir}/raddb
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
%attr(754,root,root) /etc/rc.d/init.d/radius
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/gnu-radius
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/radius
%attr(750,root,root) %dir /var/log/radacct
%attr(640,root,root) %ghost /var/log/radutmp
%attr(640,root,root) %ghost /var/log/radwtmp
%attr(640,root,root) %ghost /var/log/radius.log
%{_mandir}/man[18]/*
%{_infodir}/*.info*

%files mysql
%defattr(644,root,root,755)
%doc mysql.sql
%attr(755,root,root) %{_libdir}/radius/%{version}/modules/mysql.so

%files postgres
%defattr(644,root,root,755)
%doc pgsql.sql
%attr(755,root,root) %{_libdir}/radius/%{version}/modules/postgres.so

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgnuradius.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgnuradius.so.0
%attr(755,root,root) %{_libdir}/libradscm.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libradscm.so.1
%attr(755,root,root) %{_libdir}/libguile-gnuradius-v-%{version}.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgnuradius.so
%attr(755,root,root) %{_libdir}/libradscm.so
%{_libdir}/libgnuradius.la
%{_libdir}/libradscm.la
%{_libdir}/libservscm.a
%{_includedir}/radius
%{_datadir}/aclocal/radius.m4

%files static
%defattr(644,root,root,755)
%{_libdir}/libgnuradius.a
%{_libdir}/libradscm.a
