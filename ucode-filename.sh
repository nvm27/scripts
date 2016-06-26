#!/bin/bash

FAMILY=$(cat /proc/cpuinfo | grep "cpu family" | head -n 1 | cut -d ':' -f 2 | xargs)
MODEL=$(cat /proc/cpuinfo | grep "model[[:space:]]*:" | head -n 1 | cut -d ':' -f 2 | xargs)
STEPPING=$(cat /proc/cpuinfo | grep "stepping" | head -n 1 | cut -d ':' -f 2 | xargs)

FW_DIR="/lib/firmware"
FW_FILE=$(printf "intel-ucode/%02x-%02x-%02x\n" ${FAMILY} ${MODEL} ${STEPPING})

FW_PATH="${FW_DIR}/${FW_FILE}"

if [ ! -r ${FW_PATH} ]; then
  echo "Selected Intel microcode file ${FW_PATH} does not exist"
  exit 1
fi

echo ${FW_FILE}
