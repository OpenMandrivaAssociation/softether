%define debug_package %{nil}

Name: softether
Version: 4.21
Release: 1
Source0: http://www.softether-download.com/files/softether/v%{version}-9613-beta-2016.04.24-tree/Source_Code/softether-src-v%{version}-9613-beta.tar.gz
Patch0: https://patch-diff.githubusercontent.com/raw/SoftEtherVPN/SoftEtherVPN/pull/180.patch
Summary: VPN software
URL: http://softether.org/
License: GPL
Group: Networking/Other
BuildRequires: readline-devel
BuildRequires: pkgconfig(libssl)

%description
SoftEther VPN ("SoftEther" means "Software Ethernet") is one of the world's
most powerful and easy-to-use multi-protocol VPN software.

%prep
%setup -qn v%{version}-9613
%apply_patches

sed -i -e "s,DIR=/,DIR=\$(DESTDIR)/,g;s,/usr/vpn,%{_libexecdir}/vpn,g" src/makefiles/*
sed -i -e "s,/opt,%{_libexecdir},g" systemd/*.service

if uname -p |grep -q 64 || [ "`uname -p`" = "s390x" ]; then
	BITS=64bit
else
	BITS=32bit
fi
ln -s src/makefiles/%{_target_os}_$BITS.mak Makefile

%build
%make

%install
mkdir -p %{buildroot}%{_bindir}
%makeinstall_std
sed -i -e 's,%{buildroot},,g' %{buildroot}%{_bindir}/*

mkdir -p %{buildroot}/lib/systemd/system
cp -a systemd/*.service %{buildroot}/lib/systemd/system/

%files
%{_bindir}/*
%{_libexecdir}/vpn*
/lib/systemd/system/*.service
