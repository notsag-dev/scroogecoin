from ecdsa import SigningKey
from hashutils import hash_sha256
from base64 import b64encode
from transaction import Payment, CoinCreation
from goofycoin import Goofycoin

class Wallet():
    """ A user of the goofycoin """
    def __init__(self, signing_key=None):
        if signing_key is None:
            self.signing_key = SigningKey.generate()
        else:
            self.signing_key = signing_key
        self.verifying_key = self.signing_key.get_verifying_key()
        self.id = self.get_wallet_id_from_verifying_key(
            self.verifying_key.to_string()
        )

    def sign(self, message):
        """ Sign a message using the signing key """
        return self.signing_key.sign(message)

    def verify_signature(self, verifying_key, signature, message):
        """ Verify a signature of a message using the verifying key """
        return verifying_key.verify(signature, message)

    def get_wallet_id_from_verifying_key(self, verifying_key):
        """ Return the wallet key from the verifying key """
        return hash_sha256(b64encode(verifying_key))

    def create_payment(self, payments, blockchain):
        """ Transfer coins from this wallet to other(s).
            Parameters:
             - payments: List of duples (wallet id, amount)
             - blockchain: The complete blockchain
        """
        consumed_coins = []
        created_coins = []
        my_coins = self.get_coins(blockchain)
        # TODO: Order coins by their values

        for wallet_id, amount in payments:
            for coin in coins:
                if coin.value <= amount:
                    consumed_coins.append(coin)
                    my_coins.remove(coin)
                    amount -= coin.value
                else:
                    new_coins = self.devide_coin(coin, amount)
                    consumed_ind = self.index_coin_value(new_coins, amount)
                    consumed_coins += new_coins[consumed_ind]
                    my_coins += new_coins[condumed_ind + 1]
                    amount = 0
                coins.remove(coin)
                if amount == 0:
                    break
        return Payment(created_coins, consumed_coins)

    def index_coin_value(self, coins, value):
        """ Return the index of the first coin with the value
            passed as parameter
        """
        ind = 0
        while ind < len(coins):
            if coins[ind].value == value:
                return ind
            else:
                ind += 1
        return None

    def devide_coin(self, coin, value):
        """ Devide a coin in two new coins. The paramenter
            'value' is the value of one of the new coins
            and the value of the other is the rest.
            The original coin is consumed and cannot be used
            again.
        """
        if value > coin.value:
            return
        created_coins = []
        created_coins.append(Goofycoin(value, self.id))
        created_coins.append(Goofycoin(coin.value - value, self.id))
        payment = Payment(created_coins=created_coins, consumed_coins=[coin])
        self.sign(str(payment).encode('utf-8'))
        # TODO send payment to goofy. This method must return the created
        # coins returned by goofy (with their ids)
        return created_coins

    def get_coins(self, blockchain):
        """ Get all active coins of the blockchain associated
            to this wallet
        """
        coins = []
        for block in blockchain.blocks:
            tx = block.transaction
            for coin in tx.created_coins:
                if coin.wallet_id == self.id:
                    coins.append(coin)
            if isinstance(tx, CoinCreation):
                continue
            for coin in tx.consumed_coins:
                if con.wallet_id == self.id:
                    coins.remove(coin)
        return coins
