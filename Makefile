MKDIR=/bin/mkdir
INSTALL=/usr/bin/install
PYTHON_SITE_DIR="/usr/lib/python2.7/site-packages/"
PYTHON=/usr/bin/python
WORK_DIR=$PWD
BIN=/usr/bin
PROJECT=ramldoc
CWD=cd
COPY=/usr/bin/cp
ITER=`(date +%Y%m%d%H%M%s)`
HOMEDIR=$(shell git rev-parse --show-toplevel)
VERSION=$(shell cat $(HOMEDIR)/RELEASE)
RM=/usr/bin/rm
RMDIR=/usr/bin/rmdir


yumrepo=/var/www/yumrepo/ramldoc/releases/$(VERSION)/

ROOT:=$(shell mktemp -d /tmp/$(PROJECT)_XXXXXXXXXX)

build:
	$(MKDIR) -p $(ROOT)$(PYTHON_SITE_DIR)
	cd python; $(PYTHON) setup.py install --root=$(ROOT); rm -rf build ; cd - ;

buildrpm:build
	set -x
	fpm -t rpm --version $(VERSION) --iteration $(ITER) -n ramldoc  --description 'Python module for raml documentation' -s dir -C $(ROOT) usr/
	rm -rf $(ROOT)

clean:
	set -x
	$(RM) -f ramldoc*.rpm
	$(RM) -f python/ramldoc.egg-info/*
	$(RMDIR) python/ramldoc.egg-info
    

