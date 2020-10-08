import unittest
from scrooge import Scrooge
from scroogecoin import Scroogecoin
from transaction import CoinCreation, Payment
from hashutils import encoded_hash_object

class ScroogeTest(unittest.TestCase):
    def test_genesis_is_included(self):
        scrooge = Scrooge()
        self.assertEqual(len(scrooge.blockchain.blocks), 1)

    def test_coin_creation(self):
        scrooge = Scrooge()
        coins = [
            Scroogecoin(value=2, wallet_id=scrooge.wallet.id),
            Scroogecoin(value=5, wallet_id=scrooge.wallet.id)
        ]
        scrooge.create_coins(coins)
        self.assertTrue(isinstance(scrooge.blockchain.blocks[1].transaction,
            CoinCreation))

    def test_process_payment_without_signature(self):
        """ Put coins in Scrooge's wallet, and transfer them
            to the same wallet without signing
        """
        scrooge = Scrooge()
        coin = Scroogecoin(value=2, wallet_id=scrooge.wallet.id)
        created_coins = scrooge.create_coins([coin]).transaction.created_coins
        payment = Payment(created_coins=[coin], consumed_coins=created_coins)
        payment_result = scrooge.process_payment(payment, [])
        self.assertEqual(payment_result, None)

    def test_process_payment_with_signature(self):
        """ Put coins in Scrooge's wallet, and transfer them
            to the same wallet
        """
        scrooge = Scrooge()
        coin = Scroogecoin(value=2, wallet_id=scrooge.wallet.id)
        created_coins = scrooge.create_coins([coin]).transaction.created_coins
        payment = Payment(created_coins=[coin], consumed_coins=created_coins)
        signature = scrooge.wallet.sign(encoded_hash_object(payment))
        payment_result = scrooge.process_payment(
            payment, [(scrooge.wallet.verifying_key, signature)]
        )
        self.assertFalse(payment_result == None)

if __name__ == '__main__':
    unittest.main()
