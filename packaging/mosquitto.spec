Name:           mosquitto
Version:        1.4.14
Release:        1
Summary:        MQTT version 3.1/3.1.1 compatible message broker
URL:            http://mosquitto.org
License:        EPL-1.0
Group:          Network & Connectivity/Other

Source0:        %{name}-%{version}.tar.gz
Source1001:     mosquitto.service
Source1002:     mosquitto.conf

BuildRequires:  libopenssl-devel
BuildRequires:  libuuid-devel
BuildRequires:  libwebsockets-devel
BuildRequires:  libcares-devel
BuildRequires:  gcc-c++ >= 4.5
BuildRequires:  make >= 2.4.6
BuildRequires:  binutils
BuildRequires:  python

Requires:       libopenssl
Requires:       libwebsockets
Requires:       libcares
Requires:       libuuid

%define c_lib   libmosquitto1
%define cpp_lib libmosquittopp1

%description
A message broker that supports version 3.1 of the MQ Telemetry Transport
protocol. MQTT provides a method of carrying out messaging using a
publish/subscribe model. It is lightweight, both in terms of bandwidth
usage and ease of implementation. This makes it particularly useful at
the edge of the network where simple embedded devices are in use, such
as an arduino implementing a sensor

#
# Shared library for C runtime
#
%package -n %{c_lib}
Group:          Network & Connectivity/Libraries

Summary:        Shared C Library for %{name}
%description -n %{c_lib}
Mosquitto is an open source (BSD licensed) message broker that implements the
MQ Telemetry Transport protocol versions 3.1 and 3.1.1. MQTT provides a
lightweight method of carrying out messaging using a publish/subscribe model.
This makes it suitable for "machine to machine" messaging such as with low
power sensors or mobile devices such as phones, embedded computers or
microcontrollers like the Arduino. A good example of this is all of the work
that Andy Stanford-Clark (one of the originators of MQTT) has done in home
monitoring and automation with his twittering house and twittering ferry.

This package holds the shared C library

#
# Shared library for C++ runtime
#
%package -n %{cpp_lib}
Group:          Network & Connectivity/Libraries

Summary:        Shared C++ Library for %{name}
%description -n %{cpp_lib}
Mosquitto is an open source (BSD licensed) message broker that implements the
MQ Telemetry Transport protocol versions 3.1 and 3.1.1. MQTT provides a
lightweight method of carrying out messaging using a publish/subscribe model.
This makes it suitable for "machine to machine" messaging such as with low
power sensors or mobile devices such as phones, embedded computers or
microcontrollers like the Arduino. A good example of this is all of the work
that Andy Stanford-Clark (one of the originators of MQTT) has done in home
monitoring and automation with his twittering house and twittering ferry.

This package holds the shared C++ library

#
# Devel package for mosquitto
#
%package devel
Group:          Development/Libraries/C and C++
Requires:       %{c_lib} = %{version}
Requires:       %{cpp_lib} = %{version}
Provides:       libmosquitto-devel = %{version}-%{release}
Provides:       libmosquittopp-devel = %{version}-%{release}
Summary:        Development files %{name}
%description devel
Mosquitto is an open source (BSD licensed) message broker that implements the
MQ Telemetry Transport protocol versions 3.1 and 3.1.1. MQTT provides a
lightweight method of carrying out messaging using a publish/subscribe model.
This makes it suitable for "machine to machine" messaging such as with low
power sensors or mobile devices such as phones, embedded computers or
microcontrollers like the Arduino. A good example of this is all of the work
that Andy Stanford-Clark (one of the originators of MQTT) has done in home
monitoring and automation with his twittering house and twittering ferry.

This package holds the development files


%prep
%setup -q

%build
make binary %{?_smp_mflags} WITH_WEBSOCKETS=yes

%install
make install WITH_DOCS=no DESTDIR=$RPM_BUILD_ROOT prefix=/usr

install -D -m 644 %{S:1001} %{buildroot}%{_unitdir}/mosquitto.service
install -D -m 644 %{S:1002} %{buildroot}/etc/mosquitto/mosquitto.conf

%pre
# User needs to be present before install so permissions can be set.
getent group mosquitto >/dev/null || /usr/sbin/groupadd -r mosquitto
getent passwd mosquitto >/dev/null || /usr/sbin/useradd -r -g mosquitto -d /var/lib/mosquitto -s /bin/false -c "Mosquitto broker" mosquitto

%post
/bin/systemctl enable %{name}.service
/bin/systemctl start %{name}.service
/bin/systemctl daemon-reload

%post -n %{c_lib}
/sbin/ldconfig

%post -n %{cpp_lib}
/sbin/ldconfig

%preun
/bin/systemctl disable %{name}.service
/bin/systemctl stop %{name}.service
/bin/systemctl daemon-reload

%postun -n %{c_lib}
/sbin/ldconfig

%postun -n %{cpp_lib}
/sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc /etc/%{name}/*.example
%config(noreplace) %attr(-,root,%{name}) /etc/mosquitto/mosquitto.conf
%{_sbindir}/mosquitto
%{_bindir}/mosquitto_passwd
%{_bindir}/mosquitto_pub
%{_bindir}/mosquitto_sub
%{_unitdir}/%{name}.service

%files -n %{c_lib}
%defattr(-,root,root)
%{_libdir}/libmosquitto.so
%{_libdir}/libmosquitto.so.*

%files -n %{cpp_lib}
%defattr(-,root,root)
%{_libdir}/libmosquittopp.so
%{_libdir}/libmosquittopp.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/mosquitto.h
%{_includedir}/mosquitto_plugin.h
%{_includedir}/mosquittopp.h
