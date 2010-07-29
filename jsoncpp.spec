
%define name jsoncpp
%define version 0.5.0
%define release %mkrel 5 
%define jsoncpp_major 0
%define libname %mklibname %name %{jsoncpp_major}

Name:       %name
Version:    %version
Release:    %release
Summary:    C++ JSON Library
License:    Public Domain
Group:      System/Libraries
Url:        http://jsoncpp.sourceforge.net/
BuildRoot:  %{_tmppath}/%{name}-%{version}-root
Source0:    %{name}-%{version}.tar.gz

BuildRequires: scons 
#To generate docs
#BuildRequires: doxygen, graphviz

%description
JsonCpp is a simple API to manipulate JSON value, handle serialization 
and unserialization to string.

It can also preserve existing comment in unserialization/serialization steps,
making it a convenient format to store user input files.

Unserialization parsing is user friendly and provides precise error reports.

%package        devel
Summary:        Development files for %{name}
Group:          System/Libraries
Provides:       devel(libjsoncpp)

%description    devel
Files for building applications with %{name} support.

%prep 
%setup -q -n jsoncpp-src-%version

%build
scons platform=linux-gcc
#Docs generation is broken at the moment, return to it ASAP 

%install
#Scons file is missing an 'install' target
#XXX: Hardcoded GCC version
mkdir -p %buildroot%{_libdir}
mkdir -p %buildroot%{_includedir}/jsoncpp
GCC_VERSION=`gcc --version | head -n 1 | cut -f3 -d " "` 
LIBNAME=libjson_linux-gcc-${GCC_VERSION}_libmt.so
cp %{_builddir}/%{name}-src-%{version}/buildscons/linux-gcc-$GCC_VERSION/src/lib_json/$LIBNAME %{buildroot}%{_libdir}
ln -s $LIBNAME %buildroot%{_libdir}/%{libname}
cp %{_builddir}/%{name}-src-%{version}/include/json/* %{buildroot}%{_includedir}/jsoncpp

%clean
%{__rm} -rf %buildroot

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%defattr(-,root,root)
%doc README.txt 
%{_libdir}/*

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}/*

