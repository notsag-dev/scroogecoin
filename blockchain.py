from transaction import Transaction, CoinCreation, Payment
from hashutils import hash_sha256
from base64 import b64encode

class Blockchain():
    """ Blockchain is composed by the blockchain itself (represented
        by the class block in this project, and a series of
        functions to manage it
    """
    def __init__(self):
        self.blocks = []

    def add_block(self, block):
        """ Add a block to the blockchain. Return the hash
            of the added block
        """
        if len(self.blocks) > 0:
            block.hash_previous_block = hash_sha256(self.blocks[-1])
        else:
            block.hash_previous_block = None
        block.transaction.id = len(self.blocks)
        self.blocks.append(block)
        return hash_sha256(str(block).encode('utf-8'))

    def check_blockchain(self):
        """ Check the blockchain to find inconsistencies """
        blocks = self.blocks

        # The list must have at least one block (the genesis block)
        if len(blocks) == 0:
            return False

        for ind in range(len(blocks) - 1, 0, -1):
            if blocks[ind].hash_previous_block != hash_sha256(blocks[ind - 1]):
                return False
        return True

    def check_coin(self, coin):
        """ Check if the coin was created and was not consumed """
        create_coins = self.blocks[coin.id.transaction_id]

        for block in self.blocks:
            tx = block.transaction
            if not created and coin in tx.created_coins:
                created = True
            if isinstance(tx, Payment) and coin in tx.consumed_coins:
                consumed = True
                break
        return created and not consumed

    def check_coins(self, coins):
        """ Check a group of coins. If the check_coin function
            returns false for any of the coins then the result is
            false, otherwise the result is true
        """
        for coin in coins:
            if not self.check_coin(coin):
                return False
        return True

    def get_hash_last_block(self):
        """ Return the hash of the last block of the
            blockchain. If there are not blocks, return
            None.
        """
        if len(blocks) > 0:
            return hash_sha256(blocks[-1])
        else:
            return None

    def __str__(self):
        concat = ''
        for block in self.blocks:
            concat += str(block)
        return concat

class Block():
    """ Node of the blockchain """
    def __init__(self, transaction, hash_previous_block=None):
        self.transaction = transaction
        self.hash_previous_block = hash_previous_block

    def __str__(self):
        return 'Block: ' + str(self.transaction.id) + \
            '\tHash previous block: ' + str(self.hash_previous_block) + '\n' + \
            str(self.transaction)





