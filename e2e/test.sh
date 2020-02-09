#!/usr/bin/env bash

tier=$1
account=$2

echo "for tier = ${tier} account = ${account}"

if [[ "${tier}" == 'DEV' ]]; then
    ./acceptance_test.sh ${account}
elif [[ "${tier}" == 'STAGING' ]]; then
    ./security_and_performance_tests.sh ${account}
else
    ./smoke_tests.sh ${account}
fi
