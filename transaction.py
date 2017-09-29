from hashutils import hash_sha256
from ecdsa import SigningKey

class Transaction():
    """ Generic coin transaction """
    pass

class Payment(Transaction):
    """ Transfer coins between wallets """
    def __init__(self, created_coins, consumed_coins, transaction_id=-1):
        self.created_coins = created_coins
        self.consumed_coins = consumed_coins
        self.id = transaction_id

    def verify_balance(self):
        """ Verify that the total amount of created coins is
            equal to the total amount of consumed coins
        """
        total_created = 0
        total_consumed = 0

        for consumed_coin in self.consumed_coins:
            total_consumed += consumed_coin.value
        for created_coin in self.created_coins:
            total_created += created_coin.value
        return total_consumed == total_created

    def __str__(self):
        concat = 'TransID: ' + str(self.id) + '\t' + 'Type: Payment\n' + \
            '\nConsumed coins: \n'
        for coin in self.consumed_coins:
            concat += str(coin) + '\n'
        concat += '\nCreated coins: \n'
        for coin in self.created_coins:
            concat += str(coin) + '\n'
        return concat

class CoinCreation(Transaction):
    """ Creation of coins """
    def __init__(self, created_coins, transaction_id=-1):
        self.created_coins = created_coins
        self.id = transaction_id

    def __str__(self):
        concat = 'TransID: ' + str(self.id) + '\t' + 'Type: Coin creation\n' + \
            '\nCreated coins: \n'
        for coin in self.created_coins:
            concat += str(coin) + '\n'
        return concat
