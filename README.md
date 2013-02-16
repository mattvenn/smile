smile
=====

fetch smile statements

use makeSpi.py to create a file with your spi details in it. This should be kept safe!

python makeSpi.py > spi.json
chmod 400 spi.json

then use fetchStatements.py to pull your statements. Currently only supports "current accounts" which are 0 indexed.
