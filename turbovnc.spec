Summary:	A highly-optimized version of VNC that can be used with real-time video applications
Name:		turbovnc
Version:	1.0.2
Release:	1
License:	GPL
Group:		X11/Applications
Source0:	http://downloads.sourceforge.net/virtualgl/%{name}-%{version}.tar.gz
# Source0-md5:	1d836e2cadaf2f67a19f4d298480cdc4
Source1:	%{name}.desktop
Patch0:		%{name}-applet.patch
URL:		http://www.virtualgl.org
BuildRequires:	perl
BuildRequires:	libjpeg-turbo >= 1.1.1-2
BuildRequires:	zlib-devel
#Requires:	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Virtual Network Computing (VNC) is a remote display system which
allows you to view a computing 'desktop' environment not only on the
machine where it is running, but from anywhere on the Internet and
from a wide variety of machine architectures. TurboVNC is a sleek and
fast VNC distribution, containing a high-performance implementation of
Tight encoding designed to work in conjunction with VirtualGL.

%package server
Summary:	VNC X server - TurboVNC version
Summary(pl.UTF-8):	X serwer VNC - wersja TurboVNC
Group:		X11/Applications/Networking
Requires:	xorg-app-rgb
# for vncpasswd tool
Requires:	%{name}-utils = %{version}-%{release}
# for mcookie
Requires:	util-linux
Requires:	libjpeg-turbo
Obsoletes:	vnc-server

%description server
This package contains VNC X server in TurboVNC version.

%description server -l pl.UTF-8
Ten pakiet zawiera X serwer VNC w wersji TurboVNC.

%package utils
Summary:	Additional utilities for TigerVNC
Summary(pl.UTF-8):	Dodatkowe narzędzia do TigerVNC
Group:		X11/Applications/Networking
Obsoletes:	vnc-utils

%description utils
This package contains additional TigerVNC utilities: vncpasswd.
vncpasswd generates password file (both on server and viewer side).

%description utils -l pl.UTF-8
Ten pakiet zawiera dodatkowe narzędzia do turbovnc: vncpasswd.
vncpasswd służy to tworzenia pliku z hasłem (zarówno po
stronie serwera, jak i przeglądarki).

%prep
%setup -q -n vnc/vnc_unixsrc
%patch0 -p2

%build
%{__aclocal}
%{__autoconf}
%{__automake}
export JPEG_CFLAGS="-I%{_includedir}"
export JPEG_LDFLAGS="-lturbojpeg"
%configure

%{__make}
%{__make} -j1 xserver

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1,%{_desktopdir}} \
	$RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

%{__make} install xserver-install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}/turbovnc.desktop

#install tvncservers $RPM_BUILD_ROOT/etc/sysconfig/tvncservers

%clean
rm -rf $RPM_BUILD_ROOT

%if 0
%post server
if [ "$1" = 1 ]; then
	/sbin/chkconfig --add tvncserver;
fi

%preun server
if [ "$1" = 0 ]; then
	/etc/init.d/tvncserver stop >/dev/null 2>&1
	/sbin/chkconfig --del tvncserver
fi

%postun server
if [ "$1" -ge "1" ]; then
	/etc/init.d/tvncserver condrestart >/dev/null 2>&1
fi
%endif

%files
%defattr(644,root,root,755)
%doc LICENCE.TXT  ../TurboVNC-ChangeLog.txt
%doc ../vnc_docs/{LICEN*.txt,*.html,*.png,*.css}
%attr(755,root,root) %{_bindir}/vncviewer
%dir %{_datadir}/turbovnc
%dir %{_datadir}/turbovnc/classes
%{_datadir}/turbovnc/classes/index.vnc
%{_datadir}/turbovnc/classes/VncViewer.jar
%{_datadir}/turbovnc/classes/README
%{_desktopdir}/turbovnc.desktop
%{_mandir}/man1/vncviewer.1*

%files server
%defattr(644,root,root,755)
#%attr(754,root,root) /etc/rc.d/init.d/tvncserver
#%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/tvncservers
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/turbovncserver.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/turbovncserver-auth.conf
%attr(755,root,root) %{_bindir}/Xvnc
%attr(755,root,root) %{_bindir}/autocutsel
%attr(755,root,root) %{_bindir}/vncconnect
%attr(755,root,root) %{_bindir}/vncserver
%{_mandir}/man1/Xvnc.1*
%{_mandir}/man1/vncconnect.1*
%{_mandir}/man1/vncserver.1*

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/vncpasswd
%{_mandir}/man1/vncpasswd.1*
