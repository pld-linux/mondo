#%define _prefix /usr
%define libversion 2.0x_cvs
%define __ln ln
%define _without_xmondo yes

Summary:	A program which a Linux user can utilize to create a rescue/restore CD/tape.
Summary(fr):	Un programme pour les utilisateurs de Linux pour crï¿½r un CD/tape de sauvegarde/restauration
Summary(it):	Un programma per utenti Linux per creare un CD/tape di rescue
Summary(sp):	Un programa para los usuarios de Linux por crear una CD/cinta de restoracion/rescate.
Summary(pl):	Program do tworzenia kopi zapasowych na CD/tasmie i odtwarzania z nich
Name:		mondo
Version:	2.10
Release:	1
License:	GPL
Group:		Applications/Archiving
Url:		http://www.microwerks.net/~hugo/index.html
Source0:	http://www.microwerks.net/~hugo/download/MondoCD/TGZS/%{name}-%{version}.tgz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

BuildRequires:	newt-devel >= 0.50
BuildRequires:	slang-devel >= 1.4.1
BuildRequires:	gcc

Requires:	cdrtools-mkisofs
Requires:	cdrtools-cdrecord
Requires:	parted
Requires:	afio
Requires:	slang >= 1.4.1
Requires:	newt >= 0.50
Requires:	binutils
Requires:	bzip2 >= 0.9
Requires:	mindi >= 1.10
Requires:	syslinux >= 1.52
#Requires:   buffer
%{!?_without_xmondo:BuildRequires:    gcc-c++, X11-devel, qt-devel, kdelibs-devel, arts-devel, libart_lgpl-devel, libpng-devel}
%ifarch ia64
Requires:	elilo

%endif
Autoreq:	0

%package xmondo
Summary:	A QT based graphical front end for %{name}
Summary(pl):    Graficzna nak³adka oparta o QT do mondoarchive.

Group:		Applications/Archiving
Requires:	%{name} = %{version}-${release}, qt, kdelibs

%package devel
Summary:	Header files for building against Mondo
Summary(pl):    Pliki nag³ówkowe bibliotek Mondo

Group:		Development/Libraries

%description
Objective """"""""" To produce a program which any Linux user can
utilize to create a rescue/restore CD (or CDs, if their installation
is >2Gb approx.). Also works for tapes and NFS.

%description -l pl
Program do robienia kopii zapasowych. Wspó³pracuje z CD-R(RW),streamerami
,NFS, LVM, RAID, ext2, ext3, JFS, XFS, ReiserFS, VFAT, NTFS.

%description -l fr
Objectif """""""" Mondo a pour but de fournir un programme utilisable
par n'importe quel utilsateur de Linux pour crï¿½r un CD de
sauvegarde/restauration (ou plusieurs CDs, si son installation
dï¿½asse les 2Go environ). Cela functionne avec des systemes
d'entrainement de bande magnetique, et NFS, aussi.

%description -l it
Scopo """"" Mondo e' un programma che permette a qualsiasi utente
Linux di creare un cd di rescue/restore (o piu' cd qualora
l'installazione dovesse occupare piu' di 2Gb circa). Funziona con gli
azionamenti di nastro, ed il NFS, anche.

%description -l sp
Objectivo """"""""" Mondo es un programa que permite cualquier usuario
de Linux a crear una CD de restoracion/rescate (o CDs, si su
instalacion es >2GO aprox.). Funciona con cintas y NFS, tambien.

%description xmondo
Xmondo is a QT based graphical frontend to mondoarchive. It can help
you set up a backup by following onscreen prompts.

%description xmondo -l pl
Xmondo jest graficzn± nak³adk± opart± o QT do mondoarchive.

%description devel
mondo-devel contains a few header files that are necessary for
developing with mondo.

%description devel -l pl
pliki nag³ówkowe bibliotek mondo.

%prep

%setup -q
# clear out any CVS directories if they exist
#for dir in `find . -name CVS`
#do
#  rm -rf ${dir}
#tdone

%configure %{!?_without_xmondo:--with-x11}

%build
%{__make} VERSION=%{version} CFLAGS="-D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_REENTRANT"

%install
rm -rf $RPM_BUILD_ROOT
%{__mkdir} -p $RPM_BUILD_ROOT%{_datadir}/mondo
%{__mkdir} -p $RPM_BUILD_ROOT%{_includedir}/mondo
%{__mkdir} -p $RPM_BUILD_ROOT%{_sbindir}
%{__mkdir} -p $RPM_BUILD_ROOT%{_libdir}
%{__mkdir} -p $RPM_BUILD_ROOT%{_mandir}/man8
for fname in mondo/mondoarchive/.libs/mondoarchive mondo/mondorestore/.libs/mondorestore ; do
    %{__install} -m 644 $fname $RPM_BUILD_ROOT%{_sbindir}
    %{__install} -m 644 $fname $RPM_BUILD_ROOT%{_datadir}/mondo
done
%{!?_without_xmondo:%{__install} -m 644 mondo/xmondo/.libs/xmondo $RPM_BUILD_ROOT%{_sbindir}}

for f in libmondo libmondo.so libmondo-newt libmondo-newt.so libmondo-newt.1 libmondo-newt.so.1 libmondo-newt.1.0.0 libmondo-newt.so.1.0.0 libmondo.2 libmondo.so.2 libmondo.2.0.3 libmondo.so.2.0.3 ; do
    fname=mondo/common/.libs/$f
    if [ -e "$fname" ] ; then

# Hugo's way
        %{__install} -m 655 $fname $RPM_BUILD_ROOT%{_libdir}
# ----------
# Joshua's way
#         %{__cp} -d $fname $RPM_BUILD_ROOT%{_libdir}
# ----------

    fi
done
%{!?_without_xmondo:%{__install} -m 755 mondo/common/.libs/libXmondo-%{libversion}.so $RPM_BUILD_ROOT%{_libdir}}
%{!?_without_xmondo:%{__ln} -s libXmondo-%{libversion}.so $RPM_BUILD_ROOT%{_libdir}/libXmondo.so}
%{!?_without_xmondo:%{__install} -m 644 mondo/xmondo/mondo.png $RPM_BUILD_ROOT%{_datadir}/mondo}
%{__install} -m 755 mondo/do-not-compress-these       $RPM_BUILD_ROOT%{_datadir}/mondo
%{__install} -m 755 mondo/autorun                     $RPM_BUILD_ROOT%{_datadir}/mondo
%{__install} -m 644 mondo/mondoarchive/mondoarchive.8 $RPM_BUILD_ROOT%{_mandir}/man8
gzip -9 -f $RPM_BUILD_ROOT%{_mandir}/man8/mondoarchive.8
%{__cp} -Rf mondo/restore-scripts  $RPM_BUILD_ROOT%{_datadir}/mondo
%{__cp} -Rf mondo/post-nuke.sample $RPM_BUILD_ROOT%{_datadir}/mondo
for fname in mondo/common/my-stuff.h mondo/common/mondostructures.h mondo/common/libmondo-*-EXT.h mondo/common/X-specific-EXT.h mondo/common/newt-specific-EXT.h; do
    %{__install} -m 644 $fname $RPM_BUILD_ROOT%{_includedir}/mondo
done

%post
ldconfig

%clean
%{__rm} -rf $RPM_BUILD_ROOT

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

%{!?_without_xmondo:%files xmondo}
%{!?_without_xmondo:%{_sbindir}/xmondo}
%{!?_without_xmondo:%{_libdir}/libXmondo-%{libversion}.so}
%{!?_without_xmondo:%{_libdir}/libXmondo.so}
%{!?_without_xmondo:%{_datadir}/mondo/mondo.png}

%files devel
%defattr(644,root,root,755)
%dir %{_includedir}/mondo
%{_includedir}/mondo/*
