# TODO:
#	fix broken fr description encoding

#%define	_prefix	/usr
%define	libversion	2.0x_cvs
%define	__ln		ln

%bcond_with xmondo

Summary:	mondo - a program which a Linux user can utilize to create a rescue/restore CD/tape
Summary(fr):	mondo - un programme pour les utilisateurs de Linux pour cr�r un CD/tape de sauvegarde/restauration
Summary(it):	mondo - un programma per utenti Linux per creare un CD/tape di rescue
Summary(sp):	mondo - un programa para los usuarios de Linux por crear una CD/cinta de restoracion/rescate
Summary(pl):	mondo - program do tworzenia kopii zapasowych na CD/ta�mie i odtwarzania z nich
Name:		mondo
Version:	2.10
Release:	1
License:	GPL
Group:		Applications/Archiving
Source0:	http://www.microwerks.net/~hugo/download/MondoCD/TGZS/%{name}-%{version}.tgz
URL:		http://www.microwerks.net/~hugo/index.html
BuildRequires:	gcc
BuildRequires:	newt-devel >= 0.50
BuildRequires:	slang-devel >= 1.4.1
%if %{with xmondo}
BuildRequires:	X11-devel
BuildRequires:	arts-devel
BuildRequires:	gcc-c++
BuildRequires:	kdelibs-devel
BuildRequires:	libart_lgpl-devel
BuildRequires:	libpng-devel
BuildRequires:	qt-devel
%endif
Requires:	afio
Requires:	binutils
Requires:	bzip2 >= 0.9
Requires:	cdrtools-mkisofs
Requires:	cdrtools-cdrecord
%ifarch ia64
Requires:	elilo
%endif
Requires:	mindi >= 1.10
Requires:	newt >= 0.50
Requires:	parted
Requires:	slang >= 1.4.1
Requires:	syslinux >= 1.52
#Requires:	buffer
Autoreq:	0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Objective """"""""" to produce a program which any Linux user can
utilize to create a rescue/restore CD (or CDs, if their installation
is >2Gb approx.). Also works for tapes and NFS.

%description -l pl
Program do robienia kopii zapasowych. Wsp�pracuje z CD-R(RW),
streamerami, NFS, LVM, RAID, ext2, ext3, JFS, XFS, ReiserFS, VFAT,
NTFS.

%description -l es
Objectivo """"""""" Mondo es un programa que permite cualquier usuario
de Linux a crear una CD de restoracion/rescate (o CDs, si su
instalacion es >2GO aprox.). Funciona con cintas y NFS, tambien.

%description -l fr
Objectif """""""" Mondo a pour but de fournir un programme utilisable
par n'importe quel utilsateur de Linux pour cr�r un CD de
sauvegarde/restauration (ou plusieurs CDs, si son installation
d�asse les 2Go environ). Cela functionne avec des systemes
d'entrainement de bande magnetique, et NFS, aussi.

%description -l it
Scopo """"" Mondo e' un programma che permette a qualsiasi utente
Linux di creare un cd di rescue/restore (o piu' cd qualora
l'installazione dovesse occupare piu' di 2Gb circa). Funziona con gli
azionamenti di nastro, ed il NFS, anche.

%package xmondo
Summary:	A QT based graphical front end for mondo
Summary(pl):    Graficzna nak�adka do mondoarchive oparta o QT
Group:		Applications/Archiving
Requires:	kdelibs
Requires:	%{name} = %{version}-%{release}
Requires:	qt

%description xmondo
Xmondo is a QT based graphical frontend to mondoarchive. It can help
you set up a backup by following onscreen prompts.

%description xmondo -l pl
Xmondo jest graficzn� nak�adk� do mondoarchive opart� o QT.

%package devel
Summary:	Header files for building against mondo
Summary(pl):    Pliki nag��wkowe bibliotek mondo
Group:		Development/Libraries

%description devel
mondo-devel contains a few header files that are necessary for
developing with mondo.

%description devel -l pl
Pliki nag��wkowe bibliotek mondo.

%prep
%setup -q
# clear out any CVS directories if they exist
#for dir in `find . -name CVS`
#do
#  rm -rf ${dir}
#tdone

%build
%configure \
	%{?with_xmondo:--with-x11}

%{__make} \
	VERSION=%{version} \
	CFLAGS="-D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_REENTRANT"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir}/mondo,%{_includedir}/mondo,%{_sbindir}} \
	$RPM_BUILD_ROOT{%{_libdir},%{_mandir}/man8}

for fname in mondo/mondoarchive/.libs/mondoarchive mondo/mondorestore/.libs/mondorestore; do
	install $fname $RPM_BUILD_ROOT%{_sbindir}
	install $fname $RPM_BUILD_ROOT%{_datadir}/mondo
done
%if %{with xmondo}
install mondo/xmondo/.libs/xmondo $RPM_BUILD_ROOT%{_sbindir}
%endif

for f in libmondo libmondo.so libmondo-newt libmondo-newt.so libmondo-newt.1 libmondo-newt.so.1 libmondo-newt.1.0.0 libmondo-newt.so.1.0.0 libmondo.2 libmondo.so.2 libmondo.2.0.3 libmondo.so.2.0.3 ; do
	fname=mondo/common/.libs/$f
	if [ -e "$fname" ]; then
# Hugo's way
		install $fname $RPM_BUILD_ROOT%{_libdir}
# ----------
# Joshua's way
#		cp -d $fname $RPM_BUILD_ROOT%{_libdir}
# ----------
	fi
done
%if %{with xmondo}
install mondo/common/.libs/libXmondo-%{libversion}.so $RPM_BUILD_ROOT%{_libdir}
ln -s libXmondo-%{libversion}.so $RPM_BUILD_ROOT%{_libdir}/libXmondo.so
install mondo/xmondo/mondo.png $RPM_BUILD_ROOT%{_datadir}/mondo
%endif
install mondo/do-not-compress-these $RPM_BUILD_ROOT%{_datadir}/mondo
install mondo/autorun $RPM_BUILD_ROOT%{_datadir}/mondo
install mondo/mondoarchive/mondoarchive.8 $RPM_BUILD_ROOT%{_mandir}/man8
cp -Rf mondo/restore-scripts $RPM_BUILD_ROOT%{_datadir}/mondo
cp -Rf mondo/post-nuke.sample $RPM_BUILD_ROOT%{_datadir}/mondo
for fname in mondo/common/my-stuff.h mondo/common/mondostructures.h mondo/common/libmondo-*-EXT.h mondo/common/X-specific-EXT.h mondo/common/newt-specific-EXT.h; do
	install $fname $RPM_BUILD_ROOT%{_includedir}/mondo
done

%post	-p ldconfig
%postun	-p ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog mondo/docs/en/*
%dir %{_datadir}/mondo
%attr(755,root,root) %{_sbindir}/mondorestore
%attr(755,root,root) %{_sbindir}/mondoarchive
%{_datadir}/mondo/mondorestore
%{_datadir}/mondo/post-nuke.sample/*
%{_datadir}/mondo/restore-scripts/*
%{_datadir}/mondo/do-not-compress-these
%{_datadir}/mondo/mondoarchive
%{_datadir}/mondo/autorun
%{_mandir}/man8/mondoarchive.8*
%{_libdir}

%if %{with xmondo}
%files xmondo
%defattr(644,root,root,755)
%{_sbindir}/xmondo
%{_libdir}/libXmondo-%{libversion}.so
%{_libdir}/libXmondo.so
%{_datadir}/mondo/mondo.png
%endif

%files devel
%defattr(644,root,root,755)
%dir %{_includedir}/mondo
%{_includedir}/mondo/*
