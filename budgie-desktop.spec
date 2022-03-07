%global _hardened_build 1
%global _vpath_builddir build
%undefine _disable_source_fetch
%global _git_release 0

%global commit 8ec06a14135520105254d3fe23571d2c0c713e34
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:		budgie-desktop
Version:	10.6
%if 0%{?_git_release} == 1
Release:	4.%{shortcommit}%{?dist}
%else
Release:	1%{?dist}
%endif
License:	GPLv2 and LGPLv2.1
Summary:	An elegant desktop with GNOME integration
URL:		https://github.com/BuddiesOfBudgie/budgie-desktop

%if 0%{?_git_release:1}
# The source used to be generated from a git repository, but now Ultramarine's spec file can also download the submodules properly :D
Source0: https://github.com/BuddiesOfBudgie/budgie-desktop/archive/%{commit}.tar.gz
%else
Source0: https://github.com/BuddiesOfBudgie/budgie-desktop/releases/download/v%{version}/budgie-desktop-v%{version}.tar.xz
%endif

# the submodules are not included in the source tarball, so we need to download them
# and add them to the source list

Patch1:   0001-remove-screenshot-keybinds.patch
Patch2:   0002-default-wallpaper.patch

%if 0%{?_git_release:1}
Source4:   https://gitlab.gnome.org/GNOME/libgnome-volume-control/-/archive/c5ab6037f460406ac9799b1e5765de3ce0097a8b/libgnome-volume-control-c5ab6037f460406ac9799b1e5765de3ce0097a8b.tar.gz
%endif
Source11: 10_ultramarine-budgie.gschema.override
Source15: ultramarine-marina.layout


BuildRequires:	pkgconfig(accountsservice) >= 0.6.55
BuildRequires:	pkgconfig(ibus-1.0) >= 1.5.10
BuildRequires:	pkgconfig(gdk-x11-3.0) >= 3.24.0
BuildRequires:	pkgconfig(glib-2.0) >= 2.64.0
BuildRequires:	pkgconfig(gnome-bluetooth-1.0) >= 3.34.0
BuildRequires:	pkgconfig(gnome-desktop-3.0) >= 3.26.0
BuildRequires:	pkgconfig(graphene-gobject-1.0) >= 1.10
BuildRequires:	pkgconfig(gsettings-desktop-schemas) >= 3.26.0
BuildRequires:	pkgconfig(gnome-settings-daemon) >= 3.26.0
BuildRequires:	pkgconfig(gtk+-3.0) >= 3.24.0
BuildRequires:	pkgconfig(libgnome-menu-3.0) >= 3.10.3
BuildRequires:	pkgconfig(libpeas-1.0) >= 1.26.0
BuildRequires:	pkgconfig(libpulse) >= 2.0
BuildRequires:	pkgconfig(libnotify) >= 0.7
BuildRequires:	pkgconfig(libwnck-3.0) >= 3.36.0
BuildRequires:	pkgconfig(polkit-gobject-1) >= 0.110
BuildRequires:	pkgconfig(upower-glib) >= 0.99.0
BuildRequires:	vala >= 0.48.0
BuildRequires:  cmake

%if 0%{?fedora} >= 36
BuildRequires:	pkgconfig(libmutter-10) >= 3.36.0
%endif

%if 0%{?fedora} == 35
BuildRequires:	pkgconfig(libmutter-9) >= 3.36.0
%endif

%if 0%{?fedora} == 34
BuildRequires:	pkgconfig(libmutter-8) >= 3.36.0
%endif

%if 0%{?fedora} == 33
BuildRequires:	pkgconfig(libmutter-7) >= 3.36.0
%endif

%if 0%{?fedora} == 32
BuildRequires:	pkgconfig(libmutter-6) >= 3.36.0
%endif

BuildRequires:	pkgconfig(uuid)
BuildRequires:	pkgconfig(alsa)

BuildRequires:	meson
BuildRequires:	intltool
BuildRequires:	gtk-doc
BuildRequires:	sassc
BuildRequires:	mesa-libEGL-devel
BuildRequires:	glibc-langpack-en
BuildRequires:  git

Requires:	hicolor-icon-theme
Requires:	gnome-session
Requires:	gnome-settings-daemon
Requires:	budgie-control-center
Requires:	network-manager-applet

Requires:	%{name}-libs
Requires:	%{name}-schemas
Requires:	%{name}-rundialog

BuildRequires:	budgie-screensaver >= 4.0
Requires:	budgie-screensaver >= 4.0

%description
Budgie is the flagship desktop of the Solus, and is an Solus project.
The Budgie Desktop a modern desktop designed to keep out the way of
the user. It features heavy integration with the GNOME stack in order
for an enhanced experience.


%package	rundialog
Summary:	Budgie Run Dialog for the Budgie Desktop
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Requires:	%{name}-schemas%{?_isa} = %{version}-%{release}
%description	rundialog
%{summary}

%package	libs
Summary:	Common libs for the Budgie Desktop
Requires:	gtk3 >= 3.18.0
%description	libs
%{summary}

%package	schemas
Summary:	GLib schemas for the Budgie Desktop
%description	schemas
%{summary}

%package	docs
Summary:	GTK3 Desktop Environment -- Documentation files
Group:		Documentation/HTML
%description	docs
GTK3 Desktop Environment -- Documentation files.
This package provides API Documentation for the Budgie Plugin API, in the
GTK-Doc HTML format.

%package	devel
Summary:	Development files for the Budgie Desktop
Requires:	%{name}%{?_isa} = %{version}-%{release}
%description	devel
%{summary}

%prep
%if 0%{?_git_release:1}
%autosetup -p1 -n %{name}-%{commit}
# Extract the submodules to subprojects
tar -xvzf %{SOURCE4} --strip-components=1 --no-same-owner -C subprojects/gvc
%else
%autosetup
%endif


%build
export LC_ALL=en_US.utf8
%meson
%meson_build

%install
export LC_ALL=en_US.utf8
%meson_install
find %{buildroot} -name '*.la' -delete
#rm %{buildroot}%{_datadir}/glib-2.0/schemas/20_solus-project.budgie.wm.gschema.override
%find_lang %{name}

mkdir -p %{buildroot}%{_datadir}/glib-2.0/schemas/
install %{SOURCE11} %{buildroot}%{_datadir}/glib-2.0/schemas/
mkdir -p %{buildroot}%{_datadir}/budgie-desktop/layouts/
install %{SOURCE15} %{buildroot}%{_datadir}/budgie-desktop/layouts/


%post
/sbin/ldconfig
/bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :

%postun
/sbin/ldconfig
if [ $1 -eq 0 ]; then
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2/schemas &> /dev/null || :
    /bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null
    /usr/bin/update-desktop-database &> /dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
fi

%posttrans
/usr/bin/glib-compile-schemas %{_datadir}/glib-2/schemas &> /dev/null || :
/usr/bin/update-desktop-database &> /dev/null
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :

%files -f %{name}.lang
%doc README.md
%license LICENSE LICENSE.LGPL2.1
%{_bindir}/budgie-*
%config(noreplace) %{_sysconfdir}/xdg/autostart/budgie-desktop-*.desktop
%{_libdir}/budgie-desktop/
%{_libdir}/girepository-1.0/Budgie*.typelib
%{_datadir}/applications/budgie-*.desktop
%{_datadir}/backgrounds/budgie/default.jpg
%{_datadir}/gnome-session/sessions/budgie-desktop.session
%{_datadir}/icons/hicolor/scalable/apps/budgie-desktop-symbolic.svg
%{_datadir}/icons/hicolor/scalable/actions/notification-alert-symbolic.svg
%{_datadir}/icons/hicolor/scalable/actions/notification-disabled-symbolic.svg
%{_datadir}/icons/hicolor/scalable/actions/pane-hide-symbolic.svg
%{_datadir}/icons/hicolor/scalable/actions/pane-show-symbolic.svg
%{_datadir}/icons/hicolor/scalable/actions/system-hibernate-symbolic.svg
%{_datadir}/icons/hicolor/scalable/actions/system-log-out-symbolic.svg
%{_datadir}/icons/hicolor/scalable/actions/system-restart-symbolic.svg
%{_datadir}/icons/hicolor/scalable/actions/system-suspend-symbolic.svg
%{_datadir}/icons/hicolor/scalable/apps/clock-applet-symbolic.svg
%{_datadir}/icons/hicolor/scalable/apps/icon-task-list-symbolic.svg
%{_datadir}/icons/hicolor/scalable/apps/my-caffeine-on-symbolic.svg
%{_datadir}/icons/hicolor/scalable/apps/notifications-applet-symbolic.svg
%{_datadir}/icons/hicolor/scalable/apps/separator-symbolic.svg
%{_datadir}/icons/hicolor/scalable/apps/spacer-symbolic.svg
%{_datadir}/icons/hicolor/scalable/apps/system-tray-symbolic.svg
%{_datadir}/icons/hicolor/scalable/apps/task-list-symbolic.svg
%{_datadir}/icons/hicolor/scalable/apps/workspace-switcher-symbolic.svg
%{_datadir}/icons/hicolor/scalable/status/budgie-caffeine-cup-empty.svg
%{_datadir}/icons/hicolor/scalable/status/budgie-caffeine-cup-full.svg
%{_datadir}/icons/hicolor/scalable/status/caps-lock-symbolic.svg
%{_datadir}/icons/hicolor/scalable/status/num-lock-symbolic.svg
%{_datadir}/xsessions/budgie-desktop.desktop
%{_datadir}/budgie/budgie-version.xml

%files schemas
%{_datadir}/glib-2.0/schemas/com.solus-project.*.gschema.xml
%{_datadir}/glib-2.0/schemas/20_solus-project.budgie.wm.gschema.override
%{_datadir}/glib-2.0/schemas/10_ultramarine-budgie.gschema.override
%{_datadir}/budgie-desktop/layouts/ultramarine-marina.layout

%files libs
%{_libdir}/libbudgie*.so.*
%{_libdir}/libraven*.so.*

%files rundialog
%{_bindir}/budgie-run-dialog

%files docs
%{_datadir}/gtk-doc/html/budgie-desktop/
%{_datadir}/man/man1/budgie-daemon.1.gz
%{_datadir}/man/man1/budgie-desktop-settings.1.gz
%{_datadir}/man/man1/budgie-desktop.1.gz
%{_datadir}/man/man1/budgie-panel.1.gz
%{_datadir}/man/man1/budgie-polkit-dialog.1.gz
%{_datadir}/man/man1/budgie-run-dialog.1.gz
%{_datadir}/man/man1/budgie-wm.1.gz

%files devel
%{_includedir}/budgie-desktop/
%{_libdir}/pkgconfig/budgie*.pc
%{_libdir}/lib*.so
%{_datadir}/gir-1.0/Budgie-1.0.gir
%{_datadir}/vala/vapi/budgie-1.0.*

%changelog
* Tue Feb 22 2022 Cappy Ishihara <cappy@cappuchino.xyz> - 10.5.3-4.%{shortcommit}.um35
- Support for GNOME 42

* Tue Jan 11 2022 Cappy Ishihara <cappy@cappuchino.xyz> - 10.5.3-4- 9f26e39d118
- Update spec file to properly handle submodules
- Documentation is now properly installed

* Mon Dec 06 2021 Cappy Ishihara <cappy@cappuchino.xyz> - 10.5.3-3
- Patch to remove GNOME Screenshot keybindings due to conflicts
- Patch for setting default wallpaper

* Fri Apr 16 2021 Thomas Batten <stenstorpmc@gmail.com> - 10.5.2-2
- Support building git releases when '_git_release' is defined as '1'
- Add support for Fedora 34; '_git_release' defined as 1
- Fedora 34 requires libmutter-8

* Thu Dec 03 2020 Thomas Batten <stenstorpmc@gmail.com> - 10.5.2-1
- Update to version 10.5.2
- Drop Fedora versions < 32
- Clean up BuildRequires

* Tue Oct 27 2020 Thomas Batten <stenstorpmc@gmail.com> - 10.5.1-20201027.git.2106089
- Fedora 33 requires libmutter-7
- update to latest git revision to support libmutter-7

* Mon Jun 15 2020 Thomas Batten <stenstorpmc@gmail.com> - 10.5.1-3
- Fedora 32 requires libmutter-6
- Support mutter 3.36
- fix running on Fedora

* Thu Jan 16 2020 Thomas Batten <stenstorpmc@gmail.com> - 10.5.1-2
- EL8 requires libmutter-4

* Sun Oct 27 2019 Thomas Batten <stenstorpmc@gmail.com> - 10.5.1-1
- Update to version 10.5.1
- Remove EL8 definitions
- Update Source0 URL
- Use mutter version appropriate to Fedora version
- Add file to schemas subpackage

* Sun Oct 27 2019 Thomas Batten <stenstorpmc@gmail.com> - 10.5-1
- Update to version 10.5
- Add definitions for EL8
- Update Source0 URL
- Add patch to launch pkexec based menu apps via spawn_async

* Sat Sep 15 2018 La Ode Muh. Fadlun Akbar <fadlun.net@gmail.com> - 10.4-10
- recommends: adapta-gtk-theme and pop-icon-theme
- update URL of the project

* Mon May 14 2018 La Ode Muh. Fadlun Akbar <fadlun.net@gmail.com> - 10.4-8
- disable desktop icons on Fedora 28

* Sun Apr 22 2018 La Ode Muh. Fadlun Akbar <fadlun.net@gmail.com> - 10.4-7
- cherry-pick https://github.com/budgie-desktop/budgie-desktop/commit/fb0ef1e21a50c983dbc3a13ff446c5c838133da8
- cherry-pick https://github.com/budgie-desktop/budgie-desktop/commit/bf07458143599f9891606e97a727234cb07b8a99
- rebuild

* Tue Apr 03 2018 La Ode Muh. Fadlun Akbar <fadlun.net@gmail.com> - 10.4-6
- cherry-pick https://github.com/budgie-desktop/budgie-desktop/commit/e6fbc45256c9f5119a0d696255b95773659c9fb9
- rebuild

* Mon Nov 20 2017 La Ode Muh. Fadlun Akbar <fadlun.net@gmail.com> - 10.4-5
- rebuild for F27

* Sun Oct 08 2017 La Ode Muh. Fadlun Akbar <fadlun.net@gmail.com> - 10.4-4
- recommends arc-theme, arc-icon-theme, and moka-icon-theme
- fix license short name based on https://fedoraproject.org/wiki/Licensing:Main?rd=Licensing#Software_License_List

* Tue Aug 15 2017 La Ode Muh. Fadlun Akbar <fadlun.net@gmail.com> - 10.4-2
- revert some CSS stuff that affect global menu padding

* Tue Aug 15 2017 La Ode Muh. Fadlun Akbar <fadlun.net@gmail.com> - 10.4-1
- update to Budgie 10.4 "Irish Summer"

* Sat Jul 22 2017 La Ode Muh. Fadlun Akbar <fadlun.net@gmail.com> - 10.3.1-3
- try to rebuild with meson 0.41.2 

* Sat Jul 08 2017 La Ode Muh. Fadlun Akbar <fadlun.net@gmail.com> - 10.3.1-2
- rebuild
- backport some patches from upstream

* Tue Apr 18 2017 La Ode Muh. Fadlun Akbar <fadlun.net@gmail.com> - 10.3.1-1
- update spec file to build from stable branch

* Tue Apr 18 2017 La Ode Muh. Fadlun Akbar <fadlun.net@gmail.com> - 20170418.932cd0c-1
- build from commit 932cd0c656bb8134a290316274f5d698e47d1a27

* Tue Apr 18 2017 La Ode Muh. Fadlun Akbar <fadlun.net@gmail.com> - 20170418.83d57d4-1
- build from commit 83d57d4b9be3b75b3ac62bdf6ec18e851aa8080a

* Mon Apr 17 2017 La Ode Muh. Fadlun Akbar <fadlun.net@gmail.com> - 20170417.27637cb-1
- build from commit 27637cb5833a1765dbc2191cfe3c87a0911a3199

* Sun Apr 16 2017 La Ode Muh. Fadlun Akbar <fadlun.net@gmail.com> - 20170416.0087b0b-1
- build from commit 0087b0b31fac03d65526a35b47a0493d936c9a2b

* Sun Apr 16 2017 La Ode Muh. Fadlun Akbar <fadlun.net@gmail.com> - 20170416.aad18b3-1
- build from commit aad18b3e81a599662624b3967d023e7647ad8580

* Mon Apr 10 2017 La Ode Muh. Fadlun Akbar <fadlun.net@gmail.com> - 20170410.cfd4f19-1
- build from commit cfd4f1939c2862f945b98f4f550d41257e2dbac7

* Mon Apr 03 2017 La Ode Muh. Fadlun Akbar <fadlun.net@gmail.com> - 20170403.97d78d1-1
- build from commit 97d78d14941c4538389d18492fd44fdd92cdb5b9

* Tue Mar 14 2017 La Ode Muh. Fadlun Akbar <fadlun.net@gmail.com> - 20170314.17c7b07-1
- build from commit 17c7b0750866116b6accf0fd9ea9f55f923967b7

* Mon Feb 27 2017 La Ode Muh. Fadlun Akbar <fadlun.net@gmail.com> - 20170227.5991c79-1
- build from commit 5991c79
- edit spec file to adapt meson build system
- add budgie-devel as dependency
- enable debuginfo package again

* Sun Feb 12 2017 La Ode Muh. Fadlun Akbar <fadlun.net@gmail.com> - 20170212.647ad8d-1
- Split into some packages: libs, schemas, devel, and rundialog
- build from commit 647ad8d

* Thu Feb 02 2017 La Ode Muh. Fadlun Akbar <fadlun.net@gmail.com> - 20170202.8ad63dd-2
- add git to build dependency list

* Thu Feb 02 2017 La Ode Muh. Fadlun Akbar <fadlun.net@gmail.com> - 20170202.8ad63dd-1
- revert to manual build
- commit 8ad63dd

* Wed Nov 02 2016 La Ode Muh. Fadlun Akbar <fadlun.net@gmail.com> - 20161102
- automatic build

* Fri Jul 29 2016 Leigh Scott <leigh123linux@googlemail.com> - 10.2.6-2
- add requires gnome-screensaver

* Fri Jul 29 2016 Leigh Scott <leigh123linux@googlemail.com> - 10.2.6-1
- update to 10.2.6
- add requires for required startup components
- add suggests nautilus

* Sun Dec  7 2014 Michel Alexandre Salim <salimma@fedoraproject.org> - 8-2
- Propagate configuration parameters to budgie-1.0.pc.in
- Validate the Budgie desktop session file
- Verbose build output
- Fix directory ownerships

* Fri Dec  5 2014 Michel Alexandre Salim <salimma@fedoraproject.org> - 8-1
- Initial package

