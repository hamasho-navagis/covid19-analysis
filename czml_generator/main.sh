#!/bin/bash -ex

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PROJ_DIR=$(dirname "$DIR")

error() {
    echo "$@"
    exit 1
}

case $1 in
    up)
        gsutil \
            -h 'Content-Type:application/json' \
            -h 'Cache-Control:no-cache' \
            cp \
            $PROJ_DIR/datasets/COVID-19-geographic-disbtribution-worldwide-2020-03-19-latlon.czml \
            gs://hamasho-test-bucket/
        ;;
    *)
        error 'Invalid option'
        ;;
esac
