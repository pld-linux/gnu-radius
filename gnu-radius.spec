Summary:	GNU RADIUS Server
Summary(pl):	Serwer GNU RADIUS
Name:		gnu-radius
Version:	1.1
Release:	2
License:	GPL
Group:		Networking/Daemons
Source0:	ftp://ftp.gnu.org/pub/gnu/radius/radius-%{version}.tar.gz
# Source0-md5:	78ac1582afaee5ca438841eb28c1e7ce
Source1:	%{name}.pamd
Source2:	%{name}.init
Source3:	%{name}.logrotate
Patch0:		%{name}-info.patch
Patch1:		%{name}-gcc33.patch
Patch2:		%{name}-nolibs.patch
URL:		http://www.gnu.org/software/radius/
BuildRequires:	m4
BuildRequires:	mysql-devel
BuildRequires:	pam-devel
BuildRequires:	postgresql-devel
BuildRequires:	guile-devel
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	libtool
BuildRequires:	guile-devel >= 1.4
BuildRequires:	readline-devel
BuildRequires:	texinfo
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires(post):	fileutils
Requires:	logrotate
Requires:	pam >= 0.77.3
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

%description -l pl
Serwer RADIUS z wieloma funkcjami. Kr�tki przegl�d:
- obs�uga PAM,
- uwierzytelnianie z u�yciem SQL,
- obs�uga dost�pu opartego na huntgroups,
- wiele wpis�w DEFAULT w pliku u�ytkownik�w,
- wszystkie wpisy w pliku u�ytkownik�w mog� opcjonalnie
  "przepuszcza�",
- buforowanie wszystkich plik�w konfiguracyjnych w pami�ci,
- przechowywanie listy zalogowanych u�ytkownik�w (plik radutmp),
- program "radwho", kt�ry mo�na zainstalowa� jako "fingerd"
- logowanie w formacie uniksowego pliku "wtmp" oraz szczeg�owych
  log�w RADIUS
- obs�uga parametru Simultaneous-Use = X; tak, to oznacza, �e mo�na
  zablokowa� podw�jne logowania.

%prep
%setup -q -n radius-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__gettextize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-mysql \
	--with-postgresql \
	--enable-pam \
	--enable-shadow \
  --with-dbm
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{logrotate.d,rc.d/init.d,pam.d},/var/log/radacct} \
	$RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_mandir}/man{1,5,8},%{_sysconfdir}/raddb}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \

install %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/radius
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/radius
install %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/radius

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
%doc {ChangeLog,README*}
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/raddb/*
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/pam.d/radius
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/radius
%attr(640,root,root) /etc/logrotate.d/radius
%attr(750,root,root) %dir /var/log/radacct
%attr(750,root,root) %dir %{_sysconfdir}/raddb
%attr(640,root,root) %ghost /var/log/radutmp
%attr(640,root,root) %ghost /var/log/radwtmp
%attr(640,root,root) %ghost /var/log/radius.log
%{_datadir}/radius
%{_mandir}/*/*
%{_infodir}/*.info*
