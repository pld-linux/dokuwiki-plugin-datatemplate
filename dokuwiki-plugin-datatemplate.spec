%define		plugin		datatemplate
%define		php_min_version 5.1.0
%include	/usr/lib/rpm/macros.php
Summary:	DokuWiki plugin to add template capabilities to the data plugin
Name:		dokuwiki-plugin-%{plugin}
Version:	20110827
Release:	6
License:	GPL v2
Group:		Applications/WWW
Source0:	https://github.com/ccl/dokuwiki-plugin-datatemplate/tarball/master#/%{plugin}-%{version}.tgz
# Source0-md5:	011bca52756c29137d1715a37395cc45
URL:		http://www.dokuwiki.org/plugin:datatemplate
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpmbuild(macros) >= 1.520
Requires:	dokuwiki >= 20090214
Requires:	dokuwiki-plugin-data
Requires:	php(pcre)
Requires:	php-common >= 4:%{php_min_version}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dokuconf	/etc/webapps/dokuwiki
%define		dokudir		/usr/share/dokuwiki
%define		plugindir	%{dokudir}/lib/plugins/%{plugin}

# this is data plugin dependency
%define		_noautophp	php-sqlite

# put it together for rpmbuild
%define		_noautoreq	%{?_noautophp} %{?_noautopear}

%description
This plugin adds the possibility to display the structered data of the
data plugin using templates. Templates can be applied to individual
data entries or lists of multiple entries. Additionally, this plugin
offers a custom search form, pagination and result caching.

%prep
%setup -qc
mv *-%{plugin}-*/* .
rm *-%{plugin}-*/.gitignore

version=$(awk '/^date/{print $2}' plugin.info.txt)
if [ "$(echo "$version" | tr -d -)" != %{version} ]; then
	: %%{version} mismatch
	exit 1
fi

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{plugindir}
cp -a . $RPM_BUILD_ROOT%{plugindir}

%clean
rm -rf $RPM_BUILD_ROOT

# use this post section if you package .css or .js files
%post
# force js/css cache refresh
if [ -f %{dokuconf}/local.php ]; then
	touch %{dokuconf}/local.php
fi

%files
%defattr(644,root,root,755)
%dir %{plugindir}
%{plugindir}/*.css
%{plugindir}/*.txt
%{plugindir}/*.php
%{plugindir}/syntax
