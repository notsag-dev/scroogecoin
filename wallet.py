from ecdsa import SigningKey
from hashutils import hash_sha256
from base64 import b64encode
from transaction import Payment
from goofycoin import Goofycoin

class Wallet():
    """ A user of the goofycoin """
    def __init__(self, signing_key=None):
        if signing_key is None:
            self.signing_key = SigningKey.generate()
        else:
            self.signing_key = signing_key

        self.verifying_key = self.signing_key.get_verifying_key()
        self.id = hash_sha256(b64encode(self.verifying_key.to_string()))

    def sign(self, message):
        """ Sign a message using the signing key """
        return self.signing_key.sign(message)

    def pay(self, payments, blockchain):
        """ Transfer coins from this wallet to other(s).
            Parameters:
             - payments: List of duples (wallet id, amount)
             - blockchain: The complete blockchain
        """
        # TODO
        pass

    def devide_coin(self, coin, value):
        """ Devide a coin in two new coins. The paramenter
            'value' is the value of one of the new coins
            and the value of the other is the rest.
            The original coin is consumed and cannot be used
            again.
        """
        created_coins = []
        created_coins.append(GoofyCoin(value, self.id))
        created_coins.append(GoofyCoin(coin.value - value, self.id))
        payment = Payment(created_coins=created_coins, consumed_coins=[coin])
        self.sign(str(payment))

    def get_coins(self, blockchain):
        """ Get all active coins of the blockchain associated
            to this wallet
        """
        coins = []
        for block in blockchain:
            for coin in block.created_coins:
                if coin.wallet_id == self.id:
                    coins.append(coin)
            for coin in block.consumed_coins:
                if con.wallet_id == self.id:
                    coins.remove(coin)
        return coins
