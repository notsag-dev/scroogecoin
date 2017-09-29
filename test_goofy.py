import unittest
from goofy import Goofy
from goofycoin import Goofycoin
from transaction import CoinCreation, Payment

class GoofyTest(unittest.TestCase):
    def test_genesis_is_included(self):
        goofy = Goofy()
        self.assertEqual(len(goofy.blockchain.blocks), 1)

    def test_coin_creation(self):
        goofy = Goofy()
        coins = [
            Goofycoin(value=2, wallet_id=goofy.wallet.id),
            Goofycoin(value=5, wallet_id=goofy.wallet.id)
        ]
        goofy.create_coins(coins)
        self.assertTrue(isinstance(goofy.blockchain.blocks[1].transaction,
            CoinCreation))

    def test_process_payment_without_signature(self):
        """ Put coins in the Goofy's wallet, and transfer them
            to the same wallet without signing
        """
        goofy = Goofy()
        coin = Goofycoin(value=2, wallet_id=goofy.wallet.id)
        created_coins = goofy.create_coins([coin]).transaction.created_coins
        payment = Payment(created_coins=[coin], consumed_coins=created_coins)
        payment_result = goofy.process_payment(payment, [])
        self.assertEqual(payment_result, None)

    def test_process_payment_with_signature(self):
        """ Put coins in the Goofy's wallet, and transfer them
            to the same wallet
        """
        goofy = Goofy()
        coin = Goofycoin(value=2, wallet_id=goofy.wallet.id)
        created_coins = goofy.create_coins([coin]).transaction.created_coins
        print(goofy.blockchain)
        payment = Payment(created_coins=[coin], consumed_coins=created_coins)
        signature = goofy.wallet.sign(str(payment).encode('utf-8'))
        payment_result = goofy.process_payment(
            payment, [(goofy.wallet.verifying_key, signature)]
        )
        self.assertFalse(payment_result == None)

if __name__ == '__main__':
    unittest.main()
