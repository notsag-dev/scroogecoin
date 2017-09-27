from blockchain import Blockchain, Block
from ecdsa import SigningKey
from transaction import CoinCreation
from hashutils import hash_sha256
from goofycoin import Goofycoin, CoinId
from wallet import Wallet

class Goofy():
    """ Trusted entity that creates and manages the blockchain """
    def __init__(self):
        self.wallet = Wallet()
        self.blockchain = Blockchain()
        self.genesis_block_hash = self.add_genesis_block()
        self.last_block_signature = self.wallet.sign(
            self.genesis_block_hash.encode('utf-8'))

    def add_genesis_block(self):
        """ Add the genesis block to the blockchain and return
            the hash of the genesis block
        """
        coin = Goofycoin(1, self.wallet.id, CoinId(0,0))
        return self.create_coins([coin])

    def create_coins(self, coins):
        """ Add a CoinCreation transaction to the blockchain
            creating the coins passed as parameters. Return
            the hash of the added block.
        """
        transaction = CoinCreation(created_coins=coins)
        block = Block(transaction)
        return self.blockchain.add_block(block)

    def process_payment(self, payment, signatures):
        """ Process a payment sent by a user.
            The paramenter signatures is a dictionary with
            the users' validation keys as keys and the payment
            signatures as values.
        """
        # Verify users' signatures
        if (not payment.verify_signatures(signatures) or
                not payment.verify_balance()):
            return false

        # Check if all the coins that are being transferred
        # exist and were not consumed previously
        self.blockchain.check_coins(payment.consumed_coins)
