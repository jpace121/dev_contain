Name: python-dev-contain
Version: 8.0.1
Release: 1%{?dist}
Summary: Development container wrapper around podman

License: ASL 2.0
URL: https://github.com/jpace121/dev_contain
Source0: dev_contain-%version.tar.gz

BuildArch: noarch

%global _description %{expand:
CLI script to build and use containers for development leveraging podman.}

%description %_description

%package -n python3-dev-contain
Summary: Facilitate development container use
BuildRequires: python3-devel
Requires: (podman or docker-ce-cli or moby-engine)

%description -n python3-dev-contain %_description

%prep
%setup -n dev_contain-%version

%build
%py3_build

%install
%py3_install


%files -n python3-dev-contain
%license LICENSE
%doc README.md
%{python3_sitelib}/dev_contain-*.egg-info/
%{python3_sitelib}/dev_contain/
%{_bindir}/dev_contain



%changelog
* Wed Dec 21 2022 James Pace <jpace121@gmail.com>
- Update.
* Sat Jun 20 2020 James Pace <jpace121@gmail.com>
- Initial package.
