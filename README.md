zabbix2-RPM-spec
================

RPM spec for zabbix 2

EPEL does not have zabbix 2 RPMs, so we're maintaining our own zabbix 2 agent RPM. (I think zabbix.com actually has RPMs now)


## Install rpmbuild

    sudo yum install rpm-build redhat-rpm-config #also any other pacakages required for your build, gcc, etc
    mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
    echo '%_topdir %(echo $HOME)/rpmbuild' > ~/.rpmmacros

## Build the RPM

    cp zabbix-2.0.2.tar.gz ~/rpmbuild/SOURCES/
    vi ~/rpmbuild/SPECS/zabbix.spec
    rpmbbuild -bb ~/rpmbuild/SPECS/zabbix.spec

