%define library_version 1.0.4
Summary: A file compression utility
Name: bzip2
Version: 1.0.5
Release: 2
License: BSD
Group: Base/Compression
URL: http://www.bzip.org/
Source: http://www.bzip.org/%{version}/%{name}-%{version}.tar.gz
Source1001: packaging/bzip2.manifest 

# Change soname from libbz2.so.1.0 to libbz2.so.1
Patch1: change_soname.patch

%description
Bzip2 is a freely available, patent-free, high quality data compressor.
Bzip2 compresses files to within 10 to 15 percent of the capabilities 
of the best techniques available.  However, bzip2 has the added benefit 
of being approximately two times faster at compression and six times 
faster at decompression than those techniques.  Bzip2 is not the 
fastest compression utility, but it does strike a balance between speed 
and compression capability.

Install bzip2 if you need a compression utility.

%package devel
Summary: Header files developing apps which will use bzip2
Group: Development/Libraries
Requires: bzip2-libs = %{version}-%{release}

%description devel

Header files and a static library of bzip2 functions, for developing apps
which will use the library.

%package libs
Summary: Libraries for applications using bzip2
Group: System Environment/Libraries

%description libs

Libraries for applications using the bzip2 compression format.

%prep
%setup -q 
%patch1 -p1 -b .change_soname

%build
cp %{SOURCE1001} .

make -f Makefile-libbz2_so CC="%{__cc}" AR=%{__ar} RANLIB=%{__ranlib} \
	CFLAGS="$RPM_OPT_FLAGS -D_FILE_OFFSET_BITS=64 -fpic -fPIC" \
	%{?_smp_mflags} all

rm -f *.o
make CC="%{__cc}" AR=%{__ar} RANLIB=%{__ranlib} \
	CFLAGS="$RPM_OPT_FLAGS -D_FILE_OFFSET_BITS=64" \
	%{?_smp_mflags} all

%install
rm -rf %{buildroot}

chmod 644 bzlib.h 
mkdir -p %{buildroot}/{%{_bindir},%{_mandir}/man1,/%{_lib},%{_libdir},%{_includedir}}
cp -p bzlib.h %{buildroot}/%{_includedir}
# temporary for rpm
install -m 644 libbz2.a %{buildroot}/%{_libdir}
install -m 755 libbz2.so.%{library_version} %{buildroot}//%{_lib}
install -m 755 bzip2-shared  %{buildroot}/%{_bindir}/bzip2
install -m 755 bzip2recover bzgrep bzdiff bzmore  %{buildroot}/%{_bindir}/
cp -p bzip2.1 bzdiff.1 bzgrep.1 bzmore.1  %{buildroot}/%{_mandir}/man1/
ln -s bzip2 %{buildroot}/%{_bindir}/bunzip2
ln -s bzip2 %{buildroot}/%{_bindir}/bzcat
ln -s bzdiff %{buildroot}/%{_bindir}/bzcmp
ln -s bzmore %{buildroot}/%{_bindir}/bzless
ln -s libbz2.so.%{library_version} %{buildroot}//%{_lib}/libbz2.so.1
ln -s ../../%{_lib}/libbz2.so.1 %{buildroot}//%{_libdir}/libbz2.so
ln -s bzip2.1 %{buildroot}/%{_mandir}/man1/bzip2recover.1
ln -s bzip2.1 %{buildroot}/%{_mandir}/man1/bunzip2.1
ln -s bzip2.1 %{buildroot}/%{_mandir}/man1/bzcat.1
ln -s bzdiff.1 %{buildroot}/%{_mandir}/man1/bzcmp.1
ln -s bzmore.1 %{buildroot}/%{_mandir}/man1/bzless.1


%post libs -p /sbin/ldconfig

%postun libs  -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%manifest bzip2.manifest
%defattr(-,root,root,-)
%doc LICENSE CHANGES README 
%{_bindir}/*
%doc %{_mandir}/*/*

%files libs
%manifest bzip2.manifest
%defattr(-,root,root,-)
/%{_lib}/*so.*

%files devel
%manifest bzip2.manifest
%defattr(-,root,root,-)
%{_includedir}/*
/%{_libdir}/*so
# Temporary for rpm
%{_libdir}/*.a

