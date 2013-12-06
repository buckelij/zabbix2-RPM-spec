Name: zabbix	
Version: 2.0.3	
Release: 1%{?dist}
Summary: zabbix agent	

Group:		Applications/Internet
License:	GPLv2+
URL:		http://www.zabbix.com
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Requires(pre): /usr/sbin/useradd

%description
Zabbix (built at TJC)

%package agent
Summary:         Zabbix Agent
Group:           Applications/Internet
Requires:        zabbix = %{version}-%{release}
Requires(post):  /sbin/chkconfig
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service

%description agent
Zabbix Agent (built at TJC)

%prep
%setup -q


%build
%configure --enable-agent --prefix=/usr --sysconfdir=%{_sysconfdir}/%{name}
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/init.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/zabbix
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/%{name}
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log/%{name}
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/run/%{name}
#remove a couple files we don't want actually installed
rm $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/zabbix_agent.conf
rm $RPM_BUILD_ROOT/usr/bin/zabbix_get
rm $RPM_BUILD_ROOT/usr/share/man/man1/zabbix_get.1
install -m 0644 -p conf/zabbix_agentd.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
install -m 0755 -p misc/init.d/fedora/core/zabbix_agentd $RPM_BUILD_ROOT%{_sysconfdir}/init.d/zabbix-agent
sed -i'' -e's|BASEDIR=/usr/local|BASEDIR=/usr|' $RPM_BUILD_ROOT%{_sysconfdir}/init.d/zabbix-agent

%clean
rm -rf $RPM_BUILD_ROOT

%pre
getent group zabbix > /dev/null || groupadd -r zabbix
getent passwd zabbix > /dev/null || useradd -r -g zabbix -d %{_localstatedir}/lib/%{name} -s /sbin/nologin zabbix
:

%post agent
/sbin/chkconfig --add zabbix-agent || :

%preun agent
if [ "$1" = 0 ]
then
  /sbin/service zabbix-agent stop >/dev/null 2>&1
  /sbin/chkconfig --del zabbix-agent
fi
:

%postun agent
if [ $1 -ge 1 ]
then
  /sbin/service zabbix-agent try-restart >/dev/null 2>&1 || :
fi

%files
%defattr(-,root,root,-)
%attr(0755,zabbix,zabbix) %dir %{_localstatedir}/log/zabbix
%attr(0755,zabbix,zabbix) %dir %{_localstatedir}/run/zabbix
%attr(0755,zabbix,zabbix) %dir %{_localstatedir}/lib/zabbix

%files agent
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/zabbix/zabbix_agentd.conf
%{_sysconfdir}/init.d/zabbix-agent
%{_sbindir}/zabbix_agent
%{_sbindir}/zabbix_agentd
%{_bindir}/zabbix_sender
%{_mandir}/man1/zabbix_sender.1*
%{_mandir}/man8/zabbix_agentd.8*

%changelog
* Mon Nov 12 2012 Elijah Buck <ebuck@tjctechnology.com> - 2.0.3-1
- Update to 2.0.3
* Wed Aug 1 2012 Elijah Buck <ebuck@tjctechnology.com> - 2.0.2-1
- Agent spec for zabbix 2, based on EPEL zabbix 1 spec http://dl.fedoraproject.org/pub/epel/6/SRPMS/repoview/zabbix.html

