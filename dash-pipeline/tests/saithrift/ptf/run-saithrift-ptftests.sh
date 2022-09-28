#!/bin/bash
# To be run inside saithrift-client container, assumes SAI repo portions exist under /SAI directory

# Usage: $0 [<PTF_TESTDIR> [<PTF_TESTCLASS>]]

if [ $# -ge 1 ]; then
	PTF_TESTDIR=$1
else
	PTF_TESTDIR=.
fi
if [ $# -ge 2 ]; then
	PTF_TESTCLASS=$2
else
	PTF_TESTCLASS=
fi

echo sudo ptf --test-dir $PTF_TESTDIR --pypath /SAI/ptf \
	 --interface 0@veth1 --interface 1@veth3 $PTF_TESTCLASS

sudo ptf --test-dir $PTF_TESTDIR --pypath /SAI/ptf \
	 --interface 0@veth1 --interface 1@veth3 $PTF_TESTCLASS

