#!/usr/bin/env bash
function clearBuildDir() {
    if [ -d "./build" ]; then
        rm -rf ./build
    fi
    mkdir ./build
}
function packFetcher() {
    echo "Starting pack fetch"
    clearBuildDir
    cp -r main.py fetcher core config utils entities.py build
    pip install -t $(pwd)/build -r ./requirements/fetch.txt
#    tar -zcf build fetcher.tar.gz
    # pip install --install-option="--install-lib=$(pwd)/build" -r ./requirements/fetch.txt
}

function packToutiaoPublisher() {
    echo "Starting pack publisher for toutiao"
    clearBuildDir
    cp -r main.py publisher core config utils entities.py build
    pip install -t $(pwd)/build -r ./requirements/publisher.txt
}

if [ "$1" == "pack" ]; then
    if [ "$2" == "fetcher" ]; then
        packFetcher
    elif [ "$2" == "publisher" ]; then
        packToutiaoPublisher
    fi
fi