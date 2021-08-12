#!/usr/bin/env bash

rm -rf src/frontend/* && cd lamp-fronted && yarn build && cp -r build/* ../src/frontend/