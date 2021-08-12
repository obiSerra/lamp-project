#!/usr/bin/env bash

curl -d '{"rgb":[0, 105, 105]}' -H "Content-Type: application/json" -X POST http://192.168.1.165:80/leds