from ..entropy import *

expected_parsers = [
    ("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa", parse_bitcoin_address), # Bitcoin P2PKH
    ("1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2", parse_bitcoin_address), # Bitcoin P2PKH
    ("mipcBbFg9gMiCh81Kj8tqqdgoZub1ZJRfn", parse_bitcoin_address), # Bitcoin P2PKH, testnet
    ("nipcBbFg9gMiCh81Kj8tqqdgoZub1ZJRfn", parse_bitcoin_address), # Bitcoin P2PKH, testnet
    ("3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy", parse_bitcoin_address), # Bitcoin P2SH
    ("bc1qrp33g2q55j75r5psq4zhdjfx5u27q2sqjycr2xnwatqpzrqj", parse_bitcoin_address), # Bitcoin Bech32
    ("0x32Be343B94f860124dC4fEe278FDCBD38C102D88", parse_ethereum_address),
    ("rUocf1ixKzTuEe34kmVhRvGqNCofY1NJzV", parse_ripple_address),
    ("LTC1q2V4Enf6z9nqLgqFZMA5GtRmZj9bsJ",  parse_litecoin_address),
    ("bitcoincash:qqs3kax2g6r4swha54jpwelusnh3dkh7pvu23rzrru", parse_bitcoin_cash_address),
    ("bchtest:qqs3kax2g6r4swha54jpwelusnh3dkh7pvu23rzrru", parse_bitcoin_cash_address),
    ("qqs3kax2g6r4swha54jpwelusnh3dkh7pvu23rzrru", parse_bitcoin_cash_address),
    ("DdzFFzCqrht1D2Tv5F9HLtZHEd4P9Tddf9DFv3d4KXa2RxudcL4uHKWtc2HfiDopch5UHyZkXQx7", parse_cardano_address),
    ("Ae2tdPwUPEZ7SZaSCeU8sGZXGZ7YrVc96FnzYdZcLkbry4CqUKax9dNeEoe", parse_cardano_address),
    ("addr1q7vggz4gzfn6c6xxp3q4t6gyg3e7azjrdms7hyhfpaam7hrcc2ha2lhxj2htfz7ndxhm6vfcvhx4zkszt2dfpqfy7w7sy72c2d",  parse_cardano_address),
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
    ("QmInvalidAddress12345",  None), # Invalid CIDv0
    ("bInvalidBase32Address12345", None), # Invalid CIDv1
    ("notAValidAddress12345", None),
]

def test_parsing():
    last_answer = None
    answer = None
    errors = []
    def fail(msg):
        nonlocal answer, last_answer, input
        if answer is None or (answer != last_answer):
            errors.append(f"For input {input} with result {answer}:")
            answer = last_answer
        errors.append(f"  " + msg)

    for input, parse_func in expected_parsers:
        for func in parse_funcs:
            answer = func(input)
            if bool(answer) != (func == parse_func): 
                fail(f"expected {func.__name__} to match")
            if answer:
                if not answer.type: fail("expected a descriptive type for the entropy")
                if answer.prefix: 
                    if not input.startswith(answer): fail("expected prefix to begin the input")
                    if answer.core.startswith(answer.prefix): fail("expected prefix to not be in the core")
                if answer.suffix: 
                    if not input.endswith(answer.suffix): fail("expected suffix to end the input")
                    if answer.core.endswith(answer.suffix): fail("expected suffix to not be in the core")
                # roughly, cut off some stuff that should never be in the body
                min_core = input[input.rfind(':') + 1:] if ':' in input else input[5:]
                # If we have a suffix, cut that off from the body, too
                if answer.suffix: min_core = min_core[:-len(answer.suffix)]
                # If we're doing a UUID, do normalization.
                if answer.type == 'UUID': min_core = min_core.lower().replace('-', '').replace('{', '').replace('}', '')
                # Now do a sanity check that our body has a chunk of what we expected.
                if min_core not in answer.core: fail(f"expected core to contain at least '{min_core}'")
    if errors:
        print('\n'.join(errors))
    assert not errors
