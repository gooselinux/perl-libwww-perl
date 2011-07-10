Name:           perl-libwww-perl
Version:        5.833
Release:        2%{?dist}
Summary:        A Perl interface to the World-Wide Web

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/libwww-perl/
Source0:        http://www.cpan.org/authors/id/G/GA/GAAS/libwww-perl-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(HTML::Entities), perl(URI), perl(Test::More), perl(ExtUtils::MakeMaker)
BuildRequires:  mailcap
BuildRequires:  perl(Compress::Zlib)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(Compress::Zlib)
Requires:       perl-HTML-Parser >= 3.33
Requires:       mailcap

%description
The libwww-perl collection is a set of Perl modules which provides a
simple and consistent application programming interface to the
World-Wide Web.  The main focus of the library is to provide classes
and functions that allow you to write WWW clients. The library also
contain modules that are of more general use and even classes that
help you implement simple HTTP servers.


%prep
%setup -q -n libwww-perl-%{version} 


# Filter unwanted Provides:
cat << \EOF > %{name}-prov
#!/bin/sh
%{__perl_provides} $* |\
  sed -e '/perl(HTTP::Headers)$/d'
EOF

%define __perl_provides %{_builddir}/libwww-perl-%{version}/%{name}-prov
chmod +x %{__perl_provides}


# Filter unwanted Requires:
cat << \EOF > %{name}-req
#!/bin/sh
%{__perl_requires} $* |\
  sed -e '/perl(HTTP::GHTTP)/d' |\
  sed -e '/perl(Win32)/d' |\
  sed -e '/perl(Authen::NTLM)/d'
EOF

%define __perl_requires %{_builddir}/libwww-perl-%{version}/%{name}-req
chmod +x %{__perl_requires}


%build
# Install the aliases by default
%{__perl} Makefile.PL INSTALLDIRS=vendor --aliases < /dev/null
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

for file in $RPM_BUILD_ROOT%{_mandir}/man3/LWP.3pm AUTHORS README Changes; do
  iconv -f iso-8859-1 -t utf-8 < "$file" > "${file}_"
  mv -f "${file}_" "$file"
done

# Use system wide MIME types (link also to blib/... for "make test").  Doing
# this stuff before "make install" would not cause the symlink to be packaged
# but a copy of /etc/mime.types.
for file in {blib/lib,$RPM_BUILD_ROOT%{perl_vendorlib}}/LWP/media.types ; do
  [ ! -f $file ] && echo ERROR && exit 1
  ln -sf /etc/mime.types $file
done

%check
make test


%clean 
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc AUTHORS Changes README*
%{_bindir}/*
%{perl_vendorlib}/lwp*.pod
%{perl_vendorlib}/LWP.pm
%{perl_vendorlib}/Bundle/
%{perl_vendorlib}/File/
%{perl_vendorlib}/HTML/
%{perl_vendorlib}/HTTP/
%{perl_vendorlib}/LWP/
%{perl_vendorlib}/Net/
%{perl_vendorlib}/WWW/
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*


%changelog
* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 5.833-2
- rebuild against perl 5.10.1

* Fri Nov  6 2009 Marcela Mašláňová <mmaslano@redhat.com> 5.833-1
- update

* Thu Sep 17 2009 Warren Togami <cweyl@alumni.drew.edu> 5.831-1
- update to 5.831

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.825-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.825-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 16 2009 Tom "spot" Callaway <tcallawa@redhat.com> 5.825-1
- update to 5.825

* Thu Jan 22 2009 Marcela Mašláňová <mmaslano@redhat.com> 5.823-1
- update to 5.823

* Mon Oct 10 2008 Marcela Mašláňová <mmaslano@redhat.com> 5.817-1
- update to 5.817

* Tue Oct  7 2008 Marcela Mašláňová <mmaslano@redhat.com> 5.816-1
- update to 5.816
- fix #465855 - install --aliases by default
- use upstream patch for previous problem (see rt 38736)

* Thu Sep 18 2008 Marcela Maslanova <mmaslano@redhat.com> 5.814-2
- use untaint patch from Villa Skyte

* Thu Sep 18 2008 Marcela Maslanova <mmaslano@redhat.com> 5.814-1
- update to 5.814
- remove patch, now we have all upstream tests on

* Fri Mar  7 2008 Ville Skyttä <ville.skytta at iki.fi> - 5.808-7
- Use system /etc/mime.types instead of an outdated private copy.

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 5.808-6
- Rebuild for perl 5.10 (again)

* Thu Jan 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 5.808-5
- rebuild for new perl

* Fri Oct 26 2007 Robin Norwood <rnorwood@redhat.com> - 5.808-4
- Fix various issues from package review:
- Fix tabs and spacing
- Remove unneeded BR: perl
- convert non-utf-8 files to utf-8
- Resolves: bz#226268

* Tue Aug 14 2007 Robin Norwood <rnorwood@redhat.com> - 5.808-3
- Make provides script filter out only the unversioned HTTP::Headers.

* Tue Aug 14 2007 Robin Norwood <rnorwood@redhat.com> - 5.808-2
- Disable some of the tests, with a long explanation.

* Mon Aug 13 2007 Robin Norwood <rnorwood@redhat.com> - 5.808-1
- Update to latest CPAN version
- Re-enable tests.  We'll see if they work now
- Move Requires filter into spec file
- Add Provides filter for unnecessary unversioned provides

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 5.805-1.1.1
- rebuild

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 5.805-1.1
- rebuild for new perl-5.8.8

* Mon Dec 18 2005 Jason Vas Dias<jvdias@redhat.com> - 5.805-1
- Upgrade to 5.805-1

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Sat Apr 02 2005 Warren Togami <wtogami@redhat.com> - 5.803-2
- skip make test (#150363)

* Sat Apr 02 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 5.803-1
- Update to 5.803.
- spec cleanup (#150363)

* Thu Nov 25 2004 Miloslav Trmac <mitr@redhat.com> - 5.79-6
- Convert man page to UTF-8

* Fri Aug 13 2004 Bill Nottingham <notting@redhat.com> 5.76-5
- fix %%defattr

* Mon Aug 09 2004 Alan Cox <alan@redhat.com> 5.76-4
- added missing BuildRequires on perl(HTML::Parser) [Steve Grubb]

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Apr 16 2004 Warren Togami <wtogami@redhat.com> 5.76-2
- #12051 misc fixes from Ville Skyttä

* Fri Feb 13 2004 Chip Turner <cturner@redhat.com> 5.76-1
- update to 5.76

* Tue Aug  6 2002 Chip Turner <cturner@redhat.com>
- automated release bump and build

* Tue Jul 16 2002 Chip Turner <cturner@redhat.com>
- added missing Requires on perl(HTML::Entities)

* Fri Mar 29 2002 Chip Turner <cturner@redhat.com>
- added Requires: for perl-URI and perl-Digest-MD5

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Dec 7 2001 root <root@redhat.com>
- Spec file was autogenerated. 
