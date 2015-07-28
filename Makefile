PYTHON=$(shell which python)
VERSION=$(shell $(PYTHON) $(CURDIR)/avocadoserver/version.py)

RELEASE_COMMIT=$(shell git log --pretty=format:'%H' -n 1 $(VERSION))
RELEASE_SHORT_COMMIT=$(shell git log --pretty=format:'%h' -n 1 $(VERSION))

COMMIT=$(shell git log --pretty=format:'%H' -n 1)
SHORT_COMMIT=$(shell git log --pretty=format:'%h' -n 1)

all:
	@echo "make clean - Get rid of scratch and byte files"
	@echo "make source - Create source package"
	@echo "make srpm - Generate a source RPM package (.srpm)"
	@echo "make rpm  - Generate binary RPMs"
	@echo "Release related targets:"
	@echo "make source-release - Create source package for the latest tagged release"
	@echo "make srpm-release - Generate a source RPM package (.srpm) for the latest tagged release"
	@echo "make rpm-release  - Generate binary RPMs for the latest tagged release"

clean:
	rm -fr SOURCES BUILD

source: clean
	if test ! -d SOURCES; then mkdir SOURCES; fi
	git archive --prefix="avocado-server-$(COMMIT)/" -o "SOURCES/avocado-server-$(VERSION)-$(SHORT_COMMIT).tar.gz" HEAD

srpm: source
	if test ! -d BUILD/SRPM; then mkdir -p BUILD/SRPM; fi
	mock --resultdir BUILD/SRPM -D "commit $(COMMIT)" --buildsrpm --spec avocado-server.spec --sources SOURCES

rpm: srpm
	if test ! -d BUILD/RPM; then mkdir -p BUILD/RPM; fi
	mock --resultdir BUILD/RPM -D "commit $(COMMIT)" --rebuild BUILD/SRPM/avocado-server-$(VERSION)-*.src.rpm

source-release: clean
	if test ! -d SOURCES; then mkdir SOURCES; fi
	git archive --prefix="avocado-server-$(RELEASE_COMMIT)/" -o "SOURCES/avocado-server-$(VERSION)-$(RELEASE_SHORT_COMMIT).tar.gz" $(VERSION)

srpm-release: source-release
	if test ! -d BUILD/SRPM; then mkdir -p BUILD/SRPM; fi
	mock --resultdir BUILD/SRPM -D "commit $(RELEASE_COMMIT)" --buildsrpm --spec avocado-server.spec --sources SOURCES

rpm-release: srpm-release
	if test ! -d BUILD/RPM; then mkdir -p BUILD/RPM; fi
	mock --resultdir BUILD/RPM -D "commit $(RELEASE_COMMIT)" --rebuild BUILD/SRPM/avocado-server-$(VERSION)-*.src.rpm

check:
	./scripts/avocado-server-manage test
	./selftests/modules_boundaries
	inspekt lint
	inspekt style
