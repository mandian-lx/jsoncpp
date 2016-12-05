%bcond_with	docs
%define major	1
%define	libname	%mklibname %{name} %{major}
%define	devname	%mklibname -d %{name}

Summary:	C++ JSON Library
Name:		jsoncpp
Version:	1.7.5
Release:	1
License:	Public Domain
Group:		System/Libraries
Url:		http://jsoncpp.sourceforge.net/
Source0:	https://github.com/open-source-parsers/jsoncpp/archive/%{version}.tar.gz
Patch0:		jsoncpp-1.6.0-work-around-i586-float-inaccuracy.patch
BuildRequires:	cmake
BuildRequires:	ninja
#To generate docs
%if %{with docs}
BuildRequires:	doxygen 
BuildRequires:	graphviz
%endif

%description
JsonCpp is a simple API to manipulate JSON value, handle serialization 
and unserialization to string.

It can also preserve existing comment in unserialization/serialization steps,
making it a convenient format to store user input files.

Unserialization parsing is user friendly and provides precise error reports.

%package -n	%{libname}
Summary:	JsonCpp library
Group:		System/Libraries

%description -n	%{libname}
JsonCpp is a simple API to manipulate JSON value, handle serialization 
and unserialization to string.

It can also preserve existing comment in unserialization/serialization steps,
making it a convenient format to store user input files.

Unserialization parsing is user friendly and provides precise error reports.

%package -n	%{devname}
Summary:	Development files for %{name}
Group:		System/Libraries
Requires:	%{libname} = %{EVRD}
%rename		jsoncpp-devel

%description -n	%{devname}
Files for building applications with %{name} support.

%prep 
%setup -q
%apply_patches
%cmake -G Ninja \
	-DJSONCPP_LIB_BUILD_SHARED:BOOL=ON \
	-DJSONCPP_LIB_BUILD_STATIC:BOOL=OFF \
	-DJSONCPP_WITH_TESTS:BOOL=OFF \
	-DJSONCPP_WITH_POST_BUILD_UNITTES:BOOL=OFF \
	-DJSONCPP_WITH_CMAKE_PACKAGE:BOOL=ON

%build
export LD_LIBRARY_PATH=`pwd`/build/src/lib_json:$LD_LIBRARY_PATH
ninja -C build

%install
DESTDIR="%{buildroot}" ninja install -C build

%files -n %{libname}
%{_libdir}/lib%{name}.so.1*

%files -n %{devname}
%{_libdir}/lib%{name}.so
%{_includedir}/json
%{_libdir}/cmake/jsoncpp
%{_libdir}/pkgconfig/*.pc
