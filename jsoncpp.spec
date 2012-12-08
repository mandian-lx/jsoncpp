%bcond_with	docs

Name:		jsoncpp
Version:	0.5.0
Release:	14
Summary:	C++ JSON Library
License:	Public Domain
Group:		System/Libraries
Url:		http://jsoncpp.sourceforge.net/
Source0:	%{name}-%{version}.tar.gz
Patch0:		jsoncpp-0.5.0-add-soname.patch
Patch1:		jsoncpp-0.5.0-cflags-ldflags.patch
BuildRequires:	scons 
#To generate docs
%if %{with docs}
BuildRequires:	doxygen graphviz
%endif

%description
JsonCpp is a simple API to manipulate JSON value, handle serialization 
and unserialization to string.

It can also preserve existing comment in unserialization/serialization steps,
making it a convenient format to store user input files.

Unserialization parsing is user friendly and provides precise error reports.

# XXX: There isn't really any major due to lack of SONAME :/
%define major	0
%define	libname	%mklibname %{name} %{major}
%define	devname	%mklibname -d %{name}

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
%setup -q -n jsoncpp-src-%{version}
%patch0 -p1 -b .soname~
%patch1 -p1 -b .flags~

%build
CXXFLAGS="%{optflags}" LINKFLAGS="%{ldflags}" scons platform=linux-gcc
#Docs generation is broken at the moment, return to it ASAP 

%install
#Scons file is missing an 'install' target
#XXX: Hardcoded GCC version
%define	gcc_ver	%(gcc -dumpversion)
%define	library	libjson_linux-gcc-%{gcc_ver}_libmt.so
install -m755 buildscons/linux-gcc-%{gcc_ver}/src/lib_json/%{library} -D %{buildroot}%{_libdir}/%{library}
ln -s %{library} %{buildroot}%{_libdir}/lib%{name}.so.0
ln -s %{library} %{buildroot}%{_libdir}/lib%{name}.so
mkdir -p %{buildroot}%{_includedir}
cp -r include/json %{buildroot}%{_includedir}/jsoncpp

%files -n %{libname}
%doc README.txt 
%{_libdir}/%{library}
%{_libdir}/lib%{name}.so.0

%files -n %{devname}
%{_libdir}/lib%{name}.so
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*


%changelog
* Tue Apr 26 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 0.5.0-12
+ Revision: 659457
- build with %%optflags & %%ldflags

* Tue Apr 26 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 0.5.0-11
+ Revision: 659396
- add soname (P0)
- cleanup

* Fri Jul 30 2010 Nicolas Vigier <nvigier@mandriva.com> 0.5.0-9mdv2011.0
+ Revision: 563704
- fix post

* Fri Jul 30 2010 Nicolas Vigier <nvigier@mandriva.com> 0.5.0-8mdv2011.0
+ Revision: 563691
- fix filename for .so file

* Fri Jul 30 2010 Nicolas Vigier <nvigier@mandriva.com> 0.5.0-7mdv2011.0
+ Revision: 563645
- add jsoncpp-devel and libjsoncpp-devel provides

* Fri Jul 30 2010 Stéphane Laurière <slauriere@mandriva.com> 0.5.0-6mdv2011.0
+ Revision: 563409
+ rebuild (emptylog)

* Thu Jul 29 2010 Stéphane Laurière <slauriere@mandriva.com> 0.5.0-5mdv2011.0
+ Revision: 563220
- updated group and file attributes
- first release, based on Caixa M?\195?\161gica's jsoncpp

