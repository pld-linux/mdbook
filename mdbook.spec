Summary:	Utility to create modern online books from Markdown files
Summary(pl.UTF-8):	Narzędzie do tworzenia nowoczesnych książek online z plików Markdown
Name:		mdbook
Version:	0.5.2
Release:	1
License:	MPL v2.0
Group:		Applications/Text
#Source0Download: https://github.com/rust-lang/mdBook/releases
Source0:	https://github.com/rust-lang/mdBook/archive/v%{version}/mdBook-%{version}.tar.gz
# Source0-md5:	53ea68cf401c5328d558cbe552f0e088
# cd mdBook-%{version}
# cargo vendor
# cd ..
# tar cJf mdBook-vendor-%{version}.tar.xz mdBook-%{version}/vendor
Source1:	mdBook-vendor-%{version}.tar.xz
# Source1-md5:	af89d6c51af9a9ff6363b151a99991a2
URL:		https://github.com/rust-lang/mdBook
BuildRequires:	cargo
BuildRequires:	rpmbuild(macros) >= 2.050
BuildRequires:	rust >= 1.88.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%{?rust_req}
ExclusiveArch:	%{rust_arches}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
mdBook is a utility to create modern online books from Markdown files.

%description -l pl.UTF-8
mdBook to narzędzie do tworzenia nowoczesnych książek online z plików
Markdown.

%prep
%setup -q -n mdBook-%{version} -b1

# use our offline registry
export CARGO_HOME="$(pwd)/.cargo"

mkdir -p "$CARGO_HOME"
cat >.cargo/config <<EOF
[source.crates-io]
registry = 'https://github.com/rust-lang/crates.io-index'
replace-with = 'vendored-sources'

[source.vendored-sources]
directory = '$PWD/vendor'
EOF

%build
export CARGO_HOME="$(pwd)/.cargo"

%cargo_build --frozen

%install
rm -rf $RPM_BUILD_ROOT

export CARGO_HOME="$(pwd)/.cargo"

%cargo_install \
	--path . \
	--root $RPM_BUILD_ROOT%{_prefix}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md README.md
%attr(755,root,root) %{_bindir}/mdbook
