smile
=====

fetch most recent or all available statements from smile.co.uk. Parse results into csv files and store in a local directory. Currently only supports "current accounts" which are 0 indexed and accessible with the --account-num argument.

then use makeSpi.py to create a file with your spi details in it. This should be kept safe!

./makeSpi.py 

chmod 400 spi.json

then create directory structure for your statements

mkdir -p accounts/account0 ; mkdir -p accounts/account1

then use fetchStatements.py to pull your statements. 

./fetchStatements.py --recent --account-num 1 --spi-file ./spi.json --account-path ./accounts
