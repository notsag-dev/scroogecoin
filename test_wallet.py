import unittest
from wallet import Wallet
from goofycoin import Goofycoin
from goofy import Goofy

class TestWallet(unittest.TestCase):
    def test_devide_coin_in_two_coins(self):
        wallet = Wallet()
        coin = Goofycoin(value=2, wallet_id=wallet.id)
        new_coins = wallet.devide_coin(coin=coin, value=0.5)
        self.assertTrue(len(new_coins) == 2)

    def test_devide_coin_same_wallet(self):
        wallet = Wallet()
        coin = Goofycoin(value=2, wallet_id=wallet.id)
        new_coins = wallet.devide_coin(coin=coin, value=0.5)
        self.assertTrue(
            new_coins[0].wallet_id == wallet.id and
            new_coins[1].wallet_id == wallet.id)

    def test_index_coin_with_value(self):
        wallet = Wallet()
        coins = [
            Goofycoin(value=1, wallet_id=wallet.id),
            Goofycoin(value=2, wallet_id=wallet.id)]
        self.assertTrue(wallet.index_coin_value(coins, 2) == 1)

    def test_get_coins(self):
        goofy = Goofy()
        wallet1 = Wallet()
        wallet2 = Wallet()
        coins = [
            Goofycoin(value=2, wallet_id=wallet1.id),
            Goofycoin(value=3, wallet_id=wallet2.id)
        ]
        goofy.create_coins(coins)
        wallet_coins = wallet1.get_coins(goofy.blockchain)
        self.assertEqual(len(wallet_coins), 1)
        self.assertEqual(wallet_coins[0].value, 2)

if __name__ == '__main__':
    unittest.main()
