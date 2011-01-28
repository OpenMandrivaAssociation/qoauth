Name:          qoauth
Summary:       Qt-based C++ library for OAuth authorization scheme
Group:         Graphical desktop/KDE
Version:       1.0.1
Release:       %mkrel 3
License:       LGPLv3+
URL:           http://github.com/ayoy/qoauth
Source0:       http://files.ayoy.net/qoauth/release/%version/src/%{name}-%{version}-src.tar.bz2
BuildRequires: qt4-devel
BuildRequires: qca2-devel 
BuildRequires: doxygen
BuildRoot: %_tmppath/%name-%version-%release-root

%description 
QOAuth is an attempt to support interaction with OAuth-powered network 
services in a Qt way, i.e. simply, clearly and efficiently. It gives 
the application developer no more than 4 methods, namely:

* requestToken() to obtain an unauthorized Request Token,
* accessToken() to exchange Request Token for the Access Token,
* createParametersString() to construct a request according to OAuth
  authorization scheme,
* inlineParemeters() - to construct a query string basing on given 
  parameters (provided only for convenience).

#-----------------------------------------------------------------------------   
%define qoauth_major 1
%define libqoauth %mklibname qoauth %qoauth_major

%package -n %libqoauth
Summary: %name core library
Group: System/Libraries
Requires: qca2-plugin-openssl

%description -n %libqoauth
%name core library.

%files -n %libqoauth
%defattr(-,root,root)
%_libdir/libqoauth.so.%{qoauth_major}*

#-----------------------------------------------------------------------------

%package devel
Summary: Devel stuff for %name
Group: Development/KDE and Qt
Requires: %libqoauth = %version-%release

%description  devel
This package contains header files needed if you wish to build applications
based on %{name} .

%files devel
%defattr(-,root,root)
%doc doc/html doc/examples
%_includedir/QtOAuth
%_libdir/libqoauth.prl
%_libdir/libqoauth.so
%_libdir/pkgconfig/qoauth.pc
%qt4dir/mkspecs/features/oauth.prf

#-----------------------------------------------------------------------------

%prep
%setup -q -n %{name}-%{version}-src
sed -i -e 's\/lib\/%{_lib}\g' src/pcfile.sh

%build
%qmake_qt4
%make

%install
rm -rf %buildroot

make install INSTALL="install -p" INSTALL_ROOT=%{buildroot}
doxygen Doxyfile

# fix the time stamp
for file in doc/html/*; do
     touch -r Doxyfile $file
done

%check
make check || :

%clean
rm -fr %buildroot
