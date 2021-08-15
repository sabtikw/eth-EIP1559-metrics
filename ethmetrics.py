from web3 import Web3
import sqlite3
from dotenv import dotenv_values
import time

def main():
   
    # load API_KEY -  create .env file and add your infura API key
    config = dotenv_values('.env')

    # connect to HTTP Provider and connect to the mainnnet
    web3_provider =  "https://mainnet.infura.io/v3/%s" %(config['WEB3_INFURA_PROJECT_ID'])
    w3 = Web3(Web3.HTTPProvider(web3_provider))

    start_block = get_latest_block_db()

    if not start_block:
        start_block = 12965000 # specify your start block here start of EIP-1559 is at block # 12965000  
    else:
        start_block +=1


    end_block = w3.eth.block_number 

    print("start block : %d - end block : %d" %(start_block,end_block))
    
    update_blocks(start_block,end_block,w3)
        
        
    # for loop to read new blocks every 30 seconds
    while True:
        
        # if latest block > end_block , loop as above
        
        latest_block = w3.eth.block_number
        
        if latest_block > end_block:
            start_block = end_block + 1
            end_block = latest_block
            print("start_block %s - end block %d" % (start_block,end_block))
            update_blocks(start_block,end_block,w3)
        print("Waiting for new blocks...")
        # wait 30 seconds for new blocks
        time.sleep(30)




def get_latest_block_db():
     # create a Blockchain database if not exists
    conection = sqlite3.connect("blockchain.db")
    cursor = conection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS Blockchain (block_num INTEGER PRIMARY KEY, coinbase VARCHAR,basefeepergas INTEGER,gaslimit INTEGER,gasused INTEGER,numOfTrans Integer)")


    start_block = cursor.execute("SELECT MAX(block_num) from Blockchain").fetchone()[0]
    conection.close()

    return start_block


def update_database(query):

    conection = sqlite3.connect("blockchain.db")
    cursor = conection.cursor()
    cursor.execute(query)
    conection.commit()
    conection.close()

def update_blocks(start_block,end_block,w3):

    for blockNumber in range(start_block,end_block + 1):
        
        block = w3.eth.get_block(blockNumber)
        
        numOfTransactions = len(block['transactions'])
        coinbase = block.miner
        basefee = block.baseFeePerGas
        gasLimit = block.gasLimit 
        gasUsed = block.gasUsed
        
        update_database("INSERT INTO Blockchain VALUES (%d,\'%s\',%d,%d,%d,%d)" % (blockNumber,coinbase,basefee,gasLimit,gasUsed,numOfTransactions))
        
        # TODO: add another for loop for the transactions in a block to calculate the miner tips (maxFee)
        # check transaction type 1 or 2(EIP-1559)
        # get maxPriorityFeePerGas and maxFeePerGas


if __name__ == '__main__':
    main()