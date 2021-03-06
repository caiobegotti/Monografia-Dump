#!/bin/bash

for file in $(ls -1 *.xml); do xmllint --encode utf-8 --format ${file} > /tmp/${0} && mv -v /tmp/${0} ${file}; done

exit 0
