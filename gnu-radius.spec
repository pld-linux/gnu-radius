Summary:	GNU RADIUS Server
Name:		gnu-radius
Version:	1.1
Release:	1
License:	GPL
Group:		Networking/Daemons
Source0:	ftp://ftp.gnu.org/pub/gnu/radius/radius-%{version}.tar.gz
# Source0-md5:	78ac1582afaee5ca438841eb28c1e7ce
Source1:	%{name}.pamd
Source2:	%{name}.init
Source3:	%{name}.logrotate
#Patch0:		%{name}-DESTDIR.patch
#Patch1:		%{name}-prefix.patch
#Patch2:		%{name}-buff_over_fix.patch
#Patch3:		%{name}-makefile.patch
URL:		http://www.gnu.org/software/radius/
BuildRequires:	m4
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

%prep
%setup  -q -n radius-%{version}
#%patch0 -p1
#%patch1 -p1
#%patch2 -p1
#%patch3 -p1

%build
%{configure}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{etc/{raddb,logrotate.d,rc.d/init.d,pam.d},var/log/radacct} \
	$RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_mandir}/man{1,5,8}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \

install %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/radius
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/radius
install %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/radius

touch $RPM_BUILD_ROOT/etc/pam.d/radius
touch $RPM_BUILD_ROOT/var/log/rad{utmp,wtmp,ius.log}

%clean
rm -rf $RPM_BUILD_ROOT

%post
touch /var/log/radutmp /var/log/radwtmp
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
	/etc/rc.d/init.d/radius stop >&2
	/sbin/chkconfig --del radius
fi

%files
%defattr(644,root,root,755)
%doc {ChangeLog,README*}
%attr(640,root,root) %config %verify(not size mtime md5) %{_sysconfdir}/raddb/*
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

%{_infodir}/*
%lang(es) %{_prefix}/share/locale/es/LC_MESSAGES/radius.mo
%lang(no) %{_prefix}/share/locale/no/LC_MESSAGES/radius.mo
%lang(pl) %{_prefix}/share/locale/pl/LC_MESSAGES/radius.mo
%lang(ru) %{_prefix}/share/locale/ru/LC_MESSAGES/radius.mo
%{_prefix}/share/radius/*

%{_mandir}/*/*
