# ScroogeCoin
ScroogeCoin implementation in Python. This currency is defined in the book "Bitcoin and Cryptocurrency Technologies" (Princeton University)

## High level specification of the currency
**Coin creation**
- Scrooge is a trusted entity that can create coins.

**Payment**
- Whoever owns a coin can transfer it on to someone else.
- Payments must be signed by all the owners whose coins are consumed in the transaction.
- Goofy check signatures, and verifies double-spending before approving the transaction.
- When a coin is consumed it is deleted and other coin with the new owner is created.
- The amount of created coins must be equal to the amout of consumed coins.

**Blockchain**
- Transactions are inserted by Scrooge into a blockchain.
- Scrooge publishes the blockchain along with the signature of the last block.

**Wallet**
- A wallet is identified by the sha256 hash of its public key.

**Signing and hashing**
- *ecdsa* is used for signing.
- *sha256* is used for hashing.

## Usage example
**Imports**
```
from scrooge import Scrooge
from scroogecoin import Scroogecoin
from wallet import Wallet
from transaction import CoinCreation, Payment
from hashutils import encoded_hash_object
```
**Creating Scrooge**
```
scrooge = Scrooge()
print(scrooge.wallet)
print(scrooge.blockchain)
```

**Output:**
```
Wallet
------------------------------
Id: 62a2fed508e58260232d2d11946078127e7ce52ad678baab429191c54184f7be
------------------------------

Blockchain 
------------------------------
Block: 0	Hash previous block: None
TransID: 0	Type: Coin creation

Created coins: 
Num: 0, Value: 1, Wallet id: 62a2fed508e58260232d2d11946078127e7ce52ad678baab429191c54184f7be
------------------------------
```
**Coin creation**
```
 wallet_1 = Wallet()
 coins = [
     Scroogecoin(value=200, wallet_id=wallet_1.id),
     Scroogecoin(value=500, wallet_id=wallet_1.id)
 ]
 scrooge.create_coins(coins)
 print(scrooge.blockchain)                
```

**Output:**
```
Blockchain 
------------------------------
Block: 0	Hash previous block: None
TransID: 0	Type: Coin creation

Created coins: 
Num: 0, Value: 1, Wallet id: 62a2fed508e58260232d2d11946078127e7ce52ad678baab429191c54184f7be
------------------------------
Block: 1	Hash previous block: fc0941cce9664b73359fb1d09535b74a1bb2367c0d477434d63b9b2a58c8d953
TransID: 1	Type: Coin creation

Created coins: 
Num: 0, Value: 200, Wallet id: 9cda018e47a2f4ea5977db970256364a141ffd691f9df08b2df734345ec640c2
Num: 1, Value: 500, Wallet id: 9cda018e47a2f4ea5977db970256364a141ffd691f9df08b2df734345ec640c2
------------------------------
``` 

**Payment**
```
wallet_2 = Wallet()
pay_coin = Scroogecoin(value=700, wallet_id=wallet_2.id)
payment = Payment(created_coins=[pay_coin], consumed_coins=created_coins)
signature = wallet_1.sign(encoded_hash_object(payment))
payment_result = scrooge.process_payment(
    payment, [(wallet_1.verifying_key, signature)]
)
print(scrooge.blockchain)
```
**Output:**
```
Blockchain 
------------------------------
Block: 0	Hash previous block: None
TransID: 0	Type: Coin creation

Created coins: 
Num: 0, Value: 1, Wallet id: 62a2fed508e58260232d2d11946078127e7ce52ad678baab429191c54184f7be
------------------------------
Block: 1	Hash previous block: fc0941cce9664b73359fb1d09535b74a1bb2367c0d477434d63b9b2a58c8d953
TransID: 1	Type: Coin creation

Created coins: 
Num: 0, Value: 200, Wallet id: 9cda018e47a2f4ea5977db970256364a141ffd691f9df08b2df734345ec640c2
Num: 1, Value: 500, Wallet id: 9cda018e47a2f4ea5977db970256364a141ffd691f9df08b2df734345ec640c2
------------------------------
Block: 2	Hash previous block: 91df213f6a915e22c7f852a4898bb62d1d7094ee66ec92ee28a90e1a020babd2
TransID: 2	Type: Payment

Consumed coins: 
Num: 0, Value: 200, Wallet id: 9cda018e47a2f4ea5977db970256364a141ffd691f9df08b2df734345ec640c2
Num: 1, Value: 500, Wallet id: 9cda018e47a2f4ea5977db970256364a141ffd691f9df08b2df734345ec640c2

Created coins: 
Num: 0, Value: 700, Wallet id: ba644435462ff1cbdcddcfc8069cd3fa07b58552a20289957d2264db65a07353
------------------------------
```
