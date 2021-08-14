# script to read EIP-1559 blocks, save it to SQLite and serve it as json using Flask


## requirements
1. web3py
2. flask
3. python-dotenv

## How to use
1. run 'python ethmetrics.py'  to update the database with block data
2. run 'flask run' to server the data as json