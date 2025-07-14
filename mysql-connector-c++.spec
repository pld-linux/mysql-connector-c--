#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
%bcond_with		tests		# skip tests

Summary:	MySQL database connector for C++
Name:		mysql-connector-c++
Version:	1.1.9
Release:	4
License:	GPL v2 with exceptions
Group:		Libraries
URL:		http://forge.mysql.com/wiki/Connector_C++
Source0:	http://vesta.informatik.rwth-aachen.de/mysql/Downloads/Connector-C++/%{name}-%{version}.tar.gz
# Source0-md5:	f262bef7e70178f95ceb72a71f0915f7
Source1:	get-source.sh
# Source0Download: http://dev.mysql.com/downloads/connector/cpp
Patch0:		cxx17.patch
BuildRequires:	/usr/bin/mysql_config
BuildRequires:	boost-devel >= 1.34.0
BuildRequires:	cmake >= 2.6.2
BuildRequires:	libatomic-devel
BuildRequires:	libstdc++-devel
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MySQL Connector/C++ is a MySQL database connector for C++.

The MySQL Driver for C++ mimics the JDBC 4.0 API. However,
Connector/C++ does not implement all of the JDBC 4.0 API.

The Connector/C++ preview features the following classes:
- Connection
- DatabaseMetaData
- Driver
- PreparedStatement
- ResultSet
- ResultSetMetaData
- Savepoint
- Statement

%package devel
Summary:	MySQL Connector/C++ developer files (headers, examples, etc.)
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	/usr/bin/mysql_config

%description devel
These are the files needed to compile programs using MySQL
Connector/C++.

%package static
Summary:	Static mysqlcppconn library
Summary(pl.UTF-8):	Statyczna biblioteka mysqlcppconn
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static mysqlcppconn library.

%description static -l pl.UTF-8
Statyczna biblioteka mysqlcppconn.

%prep
%setup -q
%patch -P0 -p1

%{__sed} -i -e 's/lib$/%{_lib}/' driver/CMakeLists.txt
%{__chmod} -x examples/*.cpp examples/*.txt

%if %{without tests}
%{__sed} -i -e '/ADD_SUBDIRECTORY.*test/d' CMakeLists.txt
%endif

# Save examples to keep directory clean (for doc)
%{__mkdir} _doc_examples
%{__cp} -pr examples _doc_examples

%build

# MYSQLCLIENT_STATIC_BINDING controls whether libmysqlclient is linked or dlopened
%cmake \
	-DMYSQLCPPCONN_BUILD_EXAMPLES:BOOL=0 \
	-DMYSQLCLIENT_STATIC_BINDING:BOOL=1
%{__make}

%if %{with tests}
# for documentation purpose only (A MySQL server is required)
# cd test
# ./static_test tcp://127.0.0.1 user password test_database
# Should output : Loops= 2 Tests=  592 Failures=   0
# ./driver_test tcp://127.0.0.1 user password test_database
# Should output :  Loops= 2 Tests=  592 Failures=   0
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a _doc_examples/examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

rm -f $RPM_BUILD_ROOT%{_prefix}/{COPYING,README,Licenses_for_Third-Party_Components.txt}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING README Licenses_for_Third-Party_Components.txt
%attr(755,root,root) %{_libdir}/libmysqlcppconn.so.*.*.*
%ghost %{_libdir}/libmysqlcppconn.so.7

%files devel
%defattr(644,root,root,755)
%{_libdir}/libmysqlcppconn.so
%{_includedir}/mysql_connection.h
%{_includedir}/mysql_driver.h
%{_includedir}/mysql_error.h
%{_includedir}/cppconn
%{_examplesdir}/%{name}-%{version}

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libmysqlcppconn-static.a
%endif
