%define NAME	CCOLAMD
%define major	2
%define libname	%mklibname %{name} %{major}
%define devname	%mklibname %{name} -d

Name:		ccolamd
Version:	2.8.0
Release:	6
Epoch:		1
Summary:	Routines for computing column approximate minimum degree ordering
Group:		System/Libraries
License:	LGPLv2+
URL:		http://www.cise.ufl.edu/research/sparse/ccolamd/
Source0:	http://www.cise.ufl.edu/research/sparse/ccolamd/%{NAME}-%{version}.tar.gz
BuildRequires:	suitesparse-common-devel >= 4.0.0

%description
The CCOLAMD column approximate minimum degree ordering algorithm computes
a permutation vector P such that the LU factorization of A (:,P)
tends to be sparser than that of A.  The Cholesky factorization of
(A (:,P))'*(A (:,P)) will also tend to be sparser than that of A'*A.

%package -n %{libname}
Summary:	Library of routines for computing column approximate minimum degree ordering
Group:		System/Libraries
%define	oldname	%{mklibname %{name} 2.8.0}
%rename		%{oldname}

%description -n %{libname}
The CCOLAMD column approximate minimum degree ordering algorithm computes
a permutation vector P such that the LU factorization of A (:,P)
tends to be sparser than that of A.  The Cholesky factorization of
(A (:,P))'*(A (:,P)) will also tend to be sparser than that of A'*A.

This package contains the library needed to run programs dynamically
linked against %{NAME}.

%package -n %{devname}
Summary:	C routines for computing column approximate minimum degree ordering
Group:		Development/C
Requires:	suitesparse-common-devel >= 4.0.0
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
The CCOLAMD column approximate minimum degree ordering algorithm computes
a permutation vector P such that the LU factorization of A (:,P)
tends to be sparser than that of A.  The Cholesky factorization of
(A (:,P))'*(A (:,P)) will also tend to be sparser than that of A'*A.

This package contains the files needed to develop applications which
use %{name}.

%prep
%setup -q -c -n %{name}-%{version}
cd %{NAME}
find . -perm 0640 | xargs chmod 0644
mkdir ../SuiteSparse_config
ln -sf %{_includedir}/suitesparse/SuiteSparse_config.* ../SuiteSparse_config

%build
cd %{NAME}
pushd Lib
    %global optflags %{optflags} -fforce-addr -frename-registers -funroll-loops -Ofast
    %make -f Makefile CC=gcc CFLAGS="%{optflags} -fPIC -I%{_includedir}/suitesparse" INC=
    gcc %{ldflags} -shared -Wl,-soname,lib%{name}.so.%{major} -o lib%{name}.so.%{version} -lm *.o
popd

%install
cd %{NAME}

install -d -m 755 %{buildroot}%{_libdir} 
install -d -m 755 %{buildroot}%{_includedir}/suitesparse 

for f in Lib/*.so*; do
    install -m 755 $f %{buildroot}%{_libdir}/`basename $f`
done
for f in Lib/*.a; do
    install -m 644 $f %{buildroot}%{_libdir}/`basename $f`
done
for f in Include/*.h; do
    install -m 644 $f %{buildroot}%{_includedir}/suitesparse/`basename $f`
done

ln -s lib%{name}.so.%{version} %{buildroot}%{_libdir}/lib%{name}.so

install -d -m 755 %{buildroot}%{_docdir}/%{name}
install -m 644 README.txt Doc/*.txt Doc/ChangeLog %{buildroot}%{_docdir}/%{name}

%files -n %{libname}
%{_libdir}/*.so.*

%files -n %{devname}
%{_docdir}/%{name}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a

