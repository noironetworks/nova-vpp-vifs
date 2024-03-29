#!/bin/bash
# Should be run from the root of the source tree

BUILD_DIR=${BUILD_DIR:-`pwd`/rpmbuild}
mkdir -p $BUILD_DIR/BUILD $BUILD_DIR/SOURCES $BUILD_DIR/SPECS $BUILD_DIR/RPMS $BUILD_DIR/SRPMS
RELEASE=${RELEASE:-1}
VERSION=`python setup.py --version`
SPEC_FILE=nova-vpp-vifs.spec
sed -e "s/@VERSION@/$VERSION/" -e "s/@RELEASE@/$RELEASE/" rpm/$SPEC_FILE.in > $BUILD_DIR/SPECS/$SPEC_FILE
python setup.py sdist --dist-dir $BUILD_DIR/SOURCES
rpmbuild --clean -ba --define "_topdir $BUILD_DIR" $BUILD_DIR/SPECS/$SPEC_FILE
