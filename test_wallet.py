import unittest
from wallet import Wallet
from scroogecoin import Scroogecoin
from scrooge import Scrooge
from transaction import CoinCreation
from hashutils import hash_object, encoded_hash_object

class TestWallet(unittest.TestCase):
    def test_devide_coin_in_two_coins(self):
        """ Check that the coin division is done correctly """
        scrooge = Scrooge()
        wallet = Wallet()
        coin = Scroogecoin(value=20, wallet_id=wallet.id)
        created_block = scrooge.create_coins([coin])
        created_coins = created_block.transaction.created_coins
        new_coins = wallet.devide_coin(
            coin=created_coins[0], value=15, scrooge=scrooge
        )
        self.assertTrue(len(new_coins) == 2)
        self.assertTrue(
            new_coins[0].wallet_id == wallet.id and
            new_coins[1].wallet_id == wallet.id
        )
        self.assertEqual(new_coins[0].value + new_coins[1].value, 20)

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
            Scroogecoin(value=20, wallet_id=wallet1.id),
            Scroogecoin(value=100, wallet_id=wallet2.id),
            Scroogecoin(value=30, wallet_id=wallet1.id),

        ]
        scrooge.create_coins(coins)
        wallet_coins = wallet1.get_coins(scrooge.blockchain)
        self.assertEqual(len(wallet_coins), 2)
        self.assertEqual(wallet_coins[0].value + wallet_coins[1].value, 50)

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
