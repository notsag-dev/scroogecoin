class Goofycoin():
    """ Each coin has an id, a value that is how many goofycoins
        it represents, and a wallet id that is its owner.

        The coin id is assigned by Goofy when the transaction
        that creates the coin is included in the blockchain.
    """
    def __init__(self, value, wallet_id, coin_id=None):
        self.value = value
        self.wallet_id = wallet_id
        self.id = coin_id

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        if self.id != None:
            num = self.id.coin_num
        else:
            num = 'N/A'
        return 'Num: ' + str(num) + ', Value: ' + str(self.value) + \
            ', Wallet id: ' + self.wallet_id

class CoinId():
    """ The id of a coin. It has two properties:
        - transaction_id: the index of the block where the
            transaction is included.
        - coin_num: the index of the coin into the transaction.
    """
    def __init__(self, coin_num, transaction_id=None):
        self.coin_num = coin_num
        self.transaction_id = transaction_id
