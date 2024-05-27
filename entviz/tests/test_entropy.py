from ..entropy import *

expected_parsers = [
    ("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa", parse_bitcoin_address), # Bitcoin P2PKH
    ("3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy", parse_bitcoin_address), # Bitcoin P2SH
    ("bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kygt080", parse_bitcoin_address), # Bitcoin Bech32
    ("0x32Be343B94f860124dC4fEe278FDCBD38C102D88", parse_ethereum_address),
    ("rUocf1ixKzTuEe34kmVhRvGqNCofY1NJzV", parse_ripple_address), # Ripple
    ("LTC1q2V4Enf6z9nqLgqFZMA5GtRmZj9bsJ",  parse_litecoin_address), # Litecoin P2PKH
    ("bitcoincash:qz3qvz82zhk69j0jv7e4f46f8kge33k76e3kkm6e57", parse_bitcoin_cash_address),
    ("addr1q9vggz4gzfn6c6xxp3q4t6gyg3e7azjrdms9hy0fpaam9hrcc80a2l0xj80tfz9ndx0m6vfcv0x4zkszt8dfpqfy7w9sy92c8d",  parse_cardano_address),
    ("eosio.token", parse_eos_address),
    ("GDFW2Z2IWGRJAJH5UNZ5B4PL5JY2X2BTHXVD5J7P64ICBRQJXP6VXABM", parse_stellar_address), # Stellar
    ("QmYwAPJzv5CZsnAzt8auVTLmk2d6y1ZH87oJZoYw1h7wQv", parse_ipfs_cid),  # CIDv0 (SHA-256)
    ("bafkreidgvpkjawlxz6sffxzwgooowe5yt7i6wsyg236mfoks77nywkptdq", parse_ipfs_cid),  # CIDv1 (Blake2b-256)
    ("bafybeigdyrzt3hn26tudveik3jtrgkef7sfx5abxg7xgxxzveitmk7pjki", parse_ipfs_cid),  # CIDv1 (SHA-256)
    ("bafybeidjex4v6szrhv5qrqzkjvnk4rr6vlcl63exs6xmfco4gic2pypku4", parse_ipfs_cid),  # CIDv1 (Blake2b-256)
    ("087f9afc-5e79-4c14-98eb-3217e477242c", parse_uuid),
    ("{087f9afc-5e79-4c14-98eb-3217e477242c}", parse_uuid),
    ("087f9afc5e794c1498eb3217e477242c", parse_uuid),    
    ("did:peer:abc123", parse_did),
    ("QmInvalidAddress12345",  None) # Invalid CIDv0
    ("bInvalidBase32Address12345", None), # Invalid CIDv1
    ("notAValidAddress12345", None),
]

def test_parsing():
    for input, parse_func in expected_parsers:
        for func in parse_funcs:
            answer = func(input)
            assert bool(answer) == (func == parse_func)
            if answer:
                assert answer.type                
                at_least_body = input[input.rfind(':') + 1:] if ':' in input else input[4:]
                if '/' in body: body = body[:body.find('/')]
                if '?' in body: body = body[:body.find('?')]
                assert at_least_body in answer.body
