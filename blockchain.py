from transaction import Transaction, CoinCreation, Payment
from hashutils import hash_sha256
from base64 import b64encode
from scroogecoin import CoinId

class Blockchain():
    """ Blockchain is composed by the blockchain itself
        (represented as an array of blocks), and a series
        of functions to manage it.
    """
    def __init__(self):
        self.blocks = []

    def add_block(self, block):
        """ Add a block to the blockchain. Return the hash
            of the block.
        """
        if len(self.blocks) > 0:
            block.hash_previous_block = hash_sha256(str(self.blocks[-1]).encode('utf-8'))
        else:
            block.hash_previous_block = None
        block.transaction.id = len(self.blocks)

        coin_num = 0
        for coin in block.transaction.created_coins:
            coin.id = CoinId(coin_num, block.transaction.id)
            coin_num += 1

        self.blocks.append(block)
        return block

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
        creation_id = coin.id.transaction_id

        # Check created
        if coin not in self.blocks[creation_id].transaction.created_coins:
            print('WARNING: Coin creation not found')
            return False

        # Check not consumed
        for ind in range(creation_id + 1, len(self.blocks)):
            transaction = self.blocks[ind].transaction
            if isinstance(transaction, Payment) and coin in transaction.consumed_coins:
                print('WARNING: Double spent attempt detected')
                return False

        return True

    def check_coins(self, coins):
        """ Check a group of coins. If the check_coin function
            returns false for any of the coins then the result is
            false, otherwise the result is true.
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
        separator = '-' * 30 + '\n'
        concat = 'Blockchain \n' + separator
        for block in self.blocks:
            concat += str(block) + separator
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
