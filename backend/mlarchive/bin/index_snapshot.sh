#!/bin/bash

# Create a snapshot of the mail archive elasticsearch index

# PUT /_snapshot/my_backup/<snapshot-{now/d}>
OUT=`curl -s -X PUT "localhost:9200/_snapshot/es_snapshot_repo/%3Csnapshot-%7Bnow%2Fd%7D%3E"`

if [ "$OUT" != '{"accepted":true}' ]; then
    echo "$OUT"
fi

