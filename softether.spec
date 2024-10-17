%define debug_package %{nil}

Name: softether
Version: 4.42
Release: 1
Source0: http://www.softether-download.com/files/softether/v%{version}-9798-rtm-2023.06.30-tree/Source_Code/softether-src-v%{version}-9798-rtm.tar.gz
Patch0: softether-4.42-compile.patch
Summary: VPN software
URL: https://softether.org/
License: GPL
Group: Networking/Other
BuildRequires: readline-devel
BuildRequires: pkgconfig(libssl)
BuildRequires: pkgconfig(zlib)
BuildRequires: pkgconfig(ncurses)
BuildRequires: pkgconfig(libssl)
BuildRequires: pkgconfig(libcrypto)

%description
SoftEther VPN ("SoftEther" means "Software Ethernet") is one of the world's
most powerful and easy-to-use multi-protocol VPN software.

%prep
%autosetup -p1 -n v%{version}-9798

sed -i -e "s,DIR=/,DIR=\$(DESTDIR)/,g;s,/usr/vpn,%{_libexecdir}/vpn,g" src/makefiles/*
sed -i -e 's|-O2|%{optflags}|g' src/makefiles/*
sed -i -e "s,/opt,%{_libexecdir},g" systemd/*.service

if uname -p |grep -q 64 || [ "`uname -p`" = "s390x" ]; then
	BITS=64bit
else
	BITS=32bit
fi
ln -s src/makefiles/%{_target_os}_$BITS.mak Makefile

%build
%make_build

%install
mkdir -p %{buildroot}%{_bindir}
%make_install
sed -i -e 's,%{buildroot},,g' %{buildroot}%{_bindir}/*

mkdir -p %{buildroot}%{_unitdir}
cp -a systemd/*.service %{buildroot}%{_unitdir}/

%files
%{_bindir}/*
%{_libexecdir}/vpn*
%{_unitdir}/*.service
