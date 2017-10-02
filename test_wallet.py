import unittest
from wallet import Wallet
from scroogecoin import Scroogecoin
from scrooge import Scrooge
from transaction import CoinCreation
from hashutils import hash_object, encoded_hash_object

class TestWallet(unittest.TestCase):
    def test_devide_coin_in_two_coins(self):
        wallet = Wallet()
        coin = Scroogecoin(value=2, wallet_id=wallet.id)
        new_coins = wallet.devide_coin(coin=coin, value=0.5)
        self.assertTrue(len(new_coins) == 2)

    def test_devide_coin_same_wallet(self):
        wallet = Wallet()
        coin = Scroogecoin(value=2, wallet_id=wallet.id)
        new_coins = wallet.devide_coin(coin=coin, value=0.5)
        self.assertTrue(
            new_coins[0].wallet_id == wallet.id and
            new_coins[1].wallet_id == wallet.id)

    def test_index_coin_with_value(self):
        wallet = Wallet()
        coins = [
            Scroogecoin(value=1, wallet_id=wallet.id),
            Scroogecoin(value=2, wallet_id=wallet.id)]
        self.assertTrue(wallet.index_coin_value(coins, 2) == 1)

    def test_get_coins(self):
        scrooge = Scrooge()
        wallet1 = Wallet()
        wallet2 = Wallet()
        coins = [
            Scroogecoin(value=2, wallet_id=wallet1.id),
            Scroogecoin(value=3, wallet_id=wallet2.id)
        ]
        scrooge.create_coins(coins)
        wallet_coins = wallet1.get_coins(scrooge.blockchain)
        self.assertEqual(len(wallet_coins), 1)
        self.assertEqual(wallet_coins[0].value, 2)

    def test_sign_and_verify(self):
        """ Sign a transaction and verify the signature """
        wallet = Wallet()
        coins = [Scroogecoin(value=2, wallet_id=wallet.id)]
        transaction = CoinCreation(created_coins=coins)
        encoded_hash = encoded_hash_object(transaction)
        self.assertTrue(
            wallet.verify_signature(
                wallet.verifying_key,
                wallet.sign(encoded_hash),
                encoded_hash
            )
        )

if __name__ == '__main__':
    unittest.main()
