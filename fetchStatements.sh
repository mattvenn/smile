#!/bin/bash
cd /home/matthew/work/python/smile
./fetchStatements.py --spi-file spi.json --recent --account-num 0
./fetchStatements.py --spi-file spi.json --recent --account-num 1
./fetchStatements.py --spi-file spi.json --recent --account-num 2
