#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
%bcond_with		tests		# skip tests

%define		bzr	895
Summary:	MySQL database connector for C++
Name:		mysql-connector-c++
Version:	1.1.0
%if 0%{?bzr}
Release:	0.8.bzr%{?bzr}
%else
Release:	1
%endif
License:	GPLv2 with exceptions
Group:		Libraries
URL:		http://forge.mysql.com/wiki/Connector_C++
%if 0%{?bzr}
# bzr branch -r 895 lp:~mysql/mysql-connector-cpp/trunk mysql-connector-c++-1.1.0
# less mysql-connector-c++-1.1.0/driver/mysql_metadata.cpp
# check getDriverMajorVersion / getDriverMinorVersion / getDriverPatchVersion
# tar czf mysql-connector-c++-bzr895.tgz --exclude .bzr mysql-connector-c++-1.1.0
# rm -rf mysql-connector-c++-1.1.0
Source0:	%{name}-bzr%{bzr}.tgz
%else
# Upstream has a mirror redirector for downloads, so the URL is hard to
# represent statically.  You can get the tarball by following a link from
# http://dev.mysql.com/downloads/connector/cpp
Source0:	http://vesta.informatik.rwth-aachen.de/mysql/Downloads/Connector-C++/%{name}-%{version}.tar.gz
%endif
BuildRequires:	boost-devel
BuildRequires:	cmake
BuildRequires:	mysql-devel
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
Requires:	mysql-devel

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
%{__sed} -i -e 's/lib$/%{_lib}/' driver/CMakeLists.txt
%{__chmod} -x examples/*.cpp examples/*.txt

# Save examples to keep directory clean (for doc)
%{__mkdir} _doc_examples
%{__cp} -pr examples _doc_examples

%build
%cmake \
	-DMYSQLCPPCONN_BUILD_EXAMPLES:BOOL=0 \
	%{!?with_static_libs:-DMYSQLCLIENT_STATIC_BINDING:BOOL=0}
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

rm $RPM_BUILD_ROOT%{_prefix}/{COPYING,README}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ANNOUNCEMEN* COPYING README CHANGES
%attr(755,root,root) %{_libdir}/libmysqlcppconn.so.*.*.*
%ghost %{_libdir}/libmysqlcppconn.so.5

%files devel
%defattr(644,root,root,755)
%{_libdir}/libmysqlcppconn.so
%{_includedir}/mysql_connection.h
%{_includedir}/mysql_driver.h
%{_includedir}/cppconn
%{_examplesdir}/%{name}-%{version}

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libmysqlcppconn-static.a
%endif
