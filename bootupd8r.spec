# SPEC file overview:
# https://docs.fedoraproject.org/en-US/quick-docs/creating-rpm-packages/#con_rpm-spec-file-overview
# Fedora packaging guidelines:
# https://docs.fedoraproject.org/en-US/packaging-guidelines/

Name: bootupd8r
Version: 1
Release: 1%{?dist}
Summary: Updates boot loaders

License: GPLv3
URL:     https://github.com/marta-lewandowska/bootupd8r

BuildRequires: git
BuildRequires: make
BuildRequires: systemd

Source0: bootupd8r-%{version}.tar.xz
Source1: install_bootloader
Source2: create_boot_path
Source3: set_boot_entry

# For %%_userunitdir and %%systemd_* macros
BuildRequires:  systemd-rpm-macros

%{?systemd_requires}

%description
bootupd8r creates a fallback mechanism on UEFI for installing new boot loaders.

%prep
%autosetup -S git_am

%build
make all

%install
set -e
install -d -m 0755 %{buildroot}%{_prefix}/lib/bootloader
install -m 0755 %{SOURCE1} %{buildroot}%{_prefix}/lib/bootloader/
install -m 0755 %{SOURCE2} %{buildroot}%{_sbindir}/
install -m 0755 %{SOURCE3} %{buildroot}%{_sbindir}/
install -D -m 0755 -t %{buildroot}%{_userunitdir} \
        AB-boot.service
install -d -m 0755 %{buildroot}%{_unitdir}/multi-user.target.wants
ln -s ../AB-boot.service \
        %{buildroot}%{_unitdir}/multi-user.target.wants

%files
%defattr(-,root,root,-)
%dir %{_prefix}/lib/bootloader
%{_prefix}/lib/bootloader/install_bootloader
%{_sbindir}/set_boot_entry
%{_sbindir}/create_boot_path
%{_unitdir}/AB-boot.service

%posttrans
. %{_sbindir}/create_boot_path

%changelog
* Fri Nov 14 2025 Marta Lewandowska <mlewando@redhat.com>
- First trial of bootupdr
