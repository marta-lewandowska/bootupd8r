# Makefile
# Copyright Marta Lewandowska <mlewando@redhat.com
#

TOPDIR ?= .
DESTDIR ?= temp
VERSION := 1
RELEASE := 1
OS_DIST := $(shell rpm --eval '%{dist}')
VR := $(VERSION)-$(RELEASE)$(OS_DIST)
RPMBUILD_ARGS := -D "_topdir $(TOPDIR)" \
                 -D '_builddir %{_topdir}' \
                 -D '_rpmdir %{_topdir}' \
                 -D '_sourcedir %{_topdir}' \
                 -D '_specdir %{_topdir}' \
                 -D '_srcrpmdir %{_topdir}' \
                 -D 'dist %nil'

all:

bootupd8r : bootupd8r-$(VR).src.rpm

archive: bootupd8r-$(VERSION).tar.xz

bootupd8r-$(VERSION).tar.xz :
	@git archive --format=tar --prefix=bootupd8r-$(VERSION)/ HEAD -- \
		AB-boot.service \
		create_boot_path \
		install_bootloader \
		set_boot_entry \
	| xz > $@

bootupd8r-$(VR).src.rpm : bootupd8r.spec bootupd8r-$(VERSION).tar.xz
	rpmbuild $(RPMBUILD_ARGS) -bs $<

bootupd8r-$(VR).noarch.rpm : bootupd8r-$(VR).src.rpm
	mock  -r "$(MOCK_ROOT_NAME)" --installdeps bootupd8r-$(VR).src.rpm --cache-alterations --no-clean --no-cleanup-after
	mock -r "$(MOCK_ROOT_NAME)" --rebuild bootupd8r-$(VR).src.rpm --no-clean

clean :
	@rm -vf bootupd8r-$(VERSION).tar.xz

.PHONY: all install clean archive
