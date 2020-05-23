#!/usr/bin/env bash
img=flowci/plugin-email-notify:latest

docker build -t ${img} .
echo "Image ${img} has been built"