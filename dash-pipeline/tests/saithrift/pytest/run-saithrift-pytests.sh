#!/bin/bash
# To be run inside saithrift-client container, assumes SAI repo portions exist under /SAI directory

# Usage: $0 [<PYTEST_TESTDIR> [<PTF_OPTIONS>]]


if [ $# -ge 1 ]; then
	PYTEST_TESTDIR=$1
    shift
else
	PYTEST_TESTDIR=.
fi
if [ $# -ge 1 ]; then
	PTF_OPTIONS=$*
else
	PTF_OPTIONS=
fi

echo python3 -m pytest -s ${PTF_OPTIONS} ${PYTEST_TESTDIR}
eval python3 -m pytest -s ${PTF_OPTIONS} ${PYTEST_TESTDIR}
