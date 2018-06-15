#!/usr/bin/env bash
function packFetcher() {
    echo "Starting pack fetch"
    if [ -d "./build" ]; then
        rm -rf ./build
    fi
    mkdir ./build
    cp -r main.py fetcher core config utils entities.py build
    pip install -t $(pwd)/build -r ./requirements/fetch.txt
#    tar -zcf build fetcher.tar.gz
    # pip install --install-option="--install-lib=$(pwd)/build" -r ./requirements/fetch.txt
}

if [ "$1" == "pack" ]; then
    if [ "$2" == "fetcher" ]; then
        packFetcher
    fi
fi