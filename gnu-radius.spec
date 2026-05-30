Summary:	GNU RADIUS Server
Summary(pl.UTF-8):	Serwer GNU RADIUS
Name:		gnu-radius
Version:	1.7
Release:	1
License:	GPL v3+
Group:		Networking/Daemons/Radius
Source0:	https://ftp.gnu.org/gnu/radius/radius-%{version}.tar.bz2
# Source0-md5:	fe461bdc1f143881f02caf86ec6d17d0
Source1:	%{name}.pamd
Source2:	%{name}.init
Source3:	%{name}.logrotate
Source4:	%{name}-mysql.sql
Source5:	%{name}-pgsql.sql
Source6:	%{name}.sysconfig
Patch0:		radius-info.patch
Patch1:		radius-types.patch
URL:		http://www.gnu.org/software/radius/
BuildRequires:	autoconf >= 2.71
BuildRequires:	automake >= 1:1.16
BuildRequires:	gettext-tools >= 0.21
BuildRequires:	groff
BuildRequires:	guile-devel >= 5:2.2
BuildRequires:	libltdl-devel >= 2:2
BuildRequires:	libtool >= 2:2
BuildRequires:	m4
BuildRequires:	mysql-devel
BuildRequires:	pam-devel
BuildRequires:	postgresql-devel
BuildRequires:	readline-devel
BuildRequires:	tar >= 1:1.22
BuildRequires:	texinfo
BuildRequires:	xz
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
%patch -P0 -p1
%patch -P1 -p1

%{__rm} po/stamp-po

%build
%{__libtoolize}
%{__aclocal} -I m4 -I am -I gint
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-dbm \
	--with-mysql \
	--with-postgresql \
	--with-sql=mysql,postgres \
	--enable-pam \
	--enable-shadow \
	--disable-silent-rules \

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

%{__rm} $RPM_BUILD_ROOT%{_libdir}/radius/%{version}/modules/*.{la,a}
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
%attr(755,root,root) %{_bindir}/builddbm
%attr(755,root,root) %{_bindir}/radgrep
%attr(755,root,root) %{_bindir}/radlast
%attr(755,root,root) %{_bindir}/radping
%attr(755,root,root) %{_bindir}/radsession
%attr(755,root,root) %{_bindir}/radtest
%attr(755,root,root) %{_bindir}/radwho
%attr(755,root,root) %{_bindir}/radzap
%attr(755,root,root) %{_sbindir}/radauth
%attr(755,root,root) %{_sbindir}/radctl
%attr(755,root,root) %{_sbindir}/radiusd
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
%{_mandir}/man1/radgrep.1*
%{_mandir}/man1/radlast.1*
%{_mandir}/man1/raduse.1*
%{_mandir}/man1/radwho.1*
%{_mandir}/man8/builddbm.8*
%{_mandir}/man8/radctl.8*
%{_mandir}/man8/radiusd.8*
%{_mandir}/man8/radping.8*
%{_mandir}/man8/radzap.8*
%{_infodir}/radius.info*

%files mysql
%defattr(644,root,root,755)
%doc mysql.sql
%{_libdir}/radius/%{version}/modules/mysql.so

%files postgres
%defattr(644,root,root,755)
%doc pgsql.sql
%{_libdir}/radius/%{version}/modules/postgres.so

%files libs
%defattr(644,root,root,755)
%{_libdir}/libgnuradius.so.*.*.*
%ghost %{_libdir}/libgnuradius.so.0
%{_libdir}/libradscm.so.*.*.*
%ghost %{_libdir}/libradscm.so.1
%{_libdir}/libguile-gnuradius-v-%{version}.so

%files devel
%defattr(644,root,root,755)
%{_libdir}/libgnuradius.so
%{_libdir}/libradscm.so
%{_libdir}/libgnuradius.la
%{_libdir}/libradscm.la
%{_includedir}/radius
%{_aclocaldir}/radius.m4

%files static
%defattr(644,root,root,755)
%{_libdir}/libgnuradius.a
%{_libdir}/libradscm.a
