#!/usr/bin/env bash


USAGE="$ ./deploy.sh -u <user@ssh-address> -p <path-for-deploy> [-r <y or yes for Running after deploy>] [-c <y or yes for Clean directory befor deploy>] [-f <y for Quick deploy (only *.py files)>]"

while getopts u:p:c:q:r flag
do
    case "${flag}" in
        c) clean=${OPTARG};;
        q) quick=${OPTARG};;
        r) run=${OPTARG};;
        u) URL=${OPTARG};;
        p) TARGET_DIR=${OPTARG};;
    esac
done

if [ "$URL" = "" ]; then
    echo "-u is required"
    echo "Usage:"
    echo "$USAGE"
    exit  
fi

if [ "$TARGET_DIR" = "" ]; then
    echo "-p is required"
    echo "Usage:"
    echo "$USAGE"
    exit  
fi

TO_UPLOAD=./src/*

if [ "$quick" = "y" ] || [ "$quick" = "yes" ]; then
    TO_UPLOAD=./src/*.py
fi

if [ "$clean" = "y" ] || [ "$clean" = "yes" ]; then
    echo "[+] Cleaning dir"
    ssh $url "rm -rf $TARGET_DIR*"    
fi
# 

echo "[+] Uploading files"
scp -r $TO_UPLOAD $URL:$TARGET_DIR


PID=$(ssh pi@green-grass-leaf-A ps aux | grep main.py | awk {'print $2'})
if [ "$PID" != "" ]; then
    echo "[!] Shutting down current version"
    ssh $URL kill -SIGINT $PID
    sleep 3
fi

if [ "$clean" = "y" ] || [ "$clean" = "yes" ]; then
    echo "[+] Running deployed version"
    ssh $URL "cd $TARGET_DIR && chmod +x run.sh && ./run.sh" &>/dev/null &
fi



