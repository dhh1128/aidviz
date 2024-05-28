from ..entropy import *
import hashlib
import random

hello_world = "Hello, world!"
hashed_hello_world = bytes.fromhex(hashlib.sha256(hello_world.encode()).hexdigest())
multihash = b'\x12\x20' + hashed_hello_world
hexified_multihash = bytes.hex(multihash)

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
    (hexified_multihash.lower(), parse_hex_multihash),
    (hexified_multihash.upper(), parse_hex_multihash),
    ("0x32Be343B94f860124dC4fEe278FDCBD38C102D", parse_hex),
    ("0x60124dC4fEe278FDCBD38C102D", parse_hex),
    ("0x601", parse_hex),
    ("32Be343B94f860124dC4fEe278FDCBD38C102D", parse_hex),
    ("60124dC4fEe278FDCBD38C102D", parse_hex),
    ("BlJbbpxQMJUPE_BaZVxi8jsHuxNM5HEDt-JSyvOTm6U6", parse_cesr),
    ("did:peer:abc123", parse_did),
    ("did:tdw:abc123swoeireulf?arg=val", parse_did),
    ("did:web:abc123swoeireulf/path/path", parse_did),
    ("did:webs:abc123swoeireulf/path/path?arg=val", parse_did),
    ("did:webs:abc123swoeireulf/path/path?arg=val", parse_did),
    ("AAAAC3NzaC1lZDI1NTE5AAAAIB0UIIW091sZULC1ojG1x7N+/SybeFJMu9dGGKCBRiR+", parse_ssh_key), # ed25519
    ("AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBNSBA0Md9M/Cwp0J32Rvk/aiElw77t6l9YQbMmJSP4PfybRxeGP4fqsrIvr6ckdRms5N8Bp/kvug/iAgX6OK59E=", parse_ssh_key), # ecdsa
    ("AAAAB3NzaC1kc3MAAACBAKGcEm/5P2PSlg6+Vj8NTlR4elcBzhVgegS3zgpJ7WdzhC857ggkAs9M/KHQVcEDbg3BiRk2r4cRMqPUZ2i61u9lL63WuhkY/eaMdkqR7Df5ZdoRsduKP0ENpciAFhHnaUlvDbujDPSxSNRJq5+zQuzoJxIJRbLCbAnp/jPBAqWTAAAAFQDjDPh4NhNLDneMFFPSDrLC7NJR1QAAAIBDfQ+Yuufm2W19Oafm6ei/XyTskVYwx/rPp+H/m3Jczt47DzTsjzzVLgQS2GPLcu3Ms6XLP9/ko4aEK2dgTox1SV4T//NOrSIgJM3u/UbXaacY9g3C9wAHwOKV9iondUL+Qn+pJ/fphLStqmyIpXqmjXKqT+gv1uJFQZuPq1oh1QAAAIAxbOZot7HRRA9QX7kayXv7o00w9St7LrxhOjIAudU6IBsigqpNeIPXcK74mOotZ2OhMLMfggsUZUkNQ1oMH+isJF7gEVMcatdPpTCa2AFQFKJRWpVNmKGueQ44Sl5l4mrNfSdW1IOf7Z5pHKzjrSgJGO9KRcm1N9sYow7GCEdP9Q==", parse_ssh_key), # DSA
    ("AAAAB3NzaC1yc2EAAAADAQABAAABgQDSD+oM4kLidAptE5pjRA8OBIWNysc9reQJjKegek2jATA3bSvKdq/wdQtpbihEx5OlKMo//V/8QpAIjCSsBaMb6G/e/D5kC9wCjnYJJ68+34L+H5Fx1Ofuiz3BidgssINw/qbV0u1vrCop+ggs6lkl+pIwa+9kPriD9xdowCOQABMVl4todcojY8gZK/Zs5XTwKi9Z8MRS/37FEPxlvpRExMmQU8v2tnP/TDqhR13NSyCZWqiH2ojMNDm2jWR+W65gIjFz4kNsu4EaSNOfKY4U7VRBLXg7om3pvIoarhBFMZvTPQ9FqJU/08BJ/A1tCjCIAY0+zGAAvfRHQt5R2wZXl83n9Xh+9IukW5r/pynpdLx1+WyAOKLxIUKflTWaIcYKBqmfaxz64Gm2lDbF0+9r/0Xf//P8TFDWFo9bo4loIukgjtwQmp8Kn6ngEKj8gS3vLApZ3wN18q3emtglyQEmO+9VXckK4NPOqAzwOu7rQbr7oEPS6HrnY3PKe9JD570=", parse_ssh_key), # RSA
    ("QmInvalidAddress12345",  None), # Invalid CIDv0
    ("bInvalidBase32Address12345", None), # Invalid CIDv1
    ("notAValidAddress12345", None),
    ("601", None),
    ("", None)
]

def random_cesr(length):
    # Why '2' at the beginning, and length -1 at the end? Because we want
    # to guarantee that the first character is not something that could also
    # be a prefix. There's nothing wrong with that in CESR, generally -- but here
    # in our test, we check whether the prefix is also the beginning of the core,
    # and by always starting with '2', we can guarantee that this is never the case.
    return '2' + ''.join(random.choice(BASE64URL_ALPHABET) for _ in range(length - 1))

for item in CESR_1_BYTE_CODES:
    expected_parsers.append((item[0] + random_cesr(item[2] - 1), parse_cesr))
for item in CESR_2_BYTE_CODES:
    expected_parsers.append((item[0] + random_cesr(item[2] - 2), parse_cesr))
for item in CESR_4_BYTE_CODES:
    expected_parsers.append((item[0] + random_cesr(item[2] - 4), parse_cesr))

def test_parsing():
    last_answer = None
    answer = None
    errors = []
    def fail(msg):
        nonlocal answer, last_answer, input
        if answer is None or (answer != last_answer):
            errors.append(f"For input {input} with result {answer}:")
            last_answer = answer
        errors.append(f"  " + msg)

    for input, parse_func in expected_parsers:
        for func in parse_funcs:
            answer = func(input)
            if bool(answer) != (func == parse_func):
                # The parse_hex function is a bit of a special case, as it's a fallback for all hex-like inputs.
                # Therefore, don't fail if it matches something that should be matched by another function.
                if func == parse_hex and parse_func is not None: continue
                fail(f"expected {func.__name__} to match, got {answer}")
            if answer:
                if not answer.type: 
                    fail("expected a descriptive type for the entropy")
                if answer.prefix: 
                    if not input.lower().startswith(answer.prefix.lower()): 
                        fail("expected prefix to begin the input")
                    if answer.core.lower().startswith(answer.prefix.lower()): 
                        fail("expected prefix to not be in the core")
                if answer.suffix:
                    if not input.lower().endswith(answer.suffix.lower()): 
                        fail("expected suffix to end the input")
                    if answer.core.lower().endswith(answer.suffix.lower()): 
                        fail("expected suffix to not be in the core")
                # roughly, cut off some stuff that should never be in the body
                min_core = input[input.rfind(':') + 1:] if ':' in input else input[5:]
                # If we have a suffix, cut that off from the body, too
                if answer.suffix: min_core = min_core[:-len(answer.suffix)]
                # If we're doing a UUID, do normalization.
                if answer.type == 'UUID': min_core = min_core.lower().replace('-', '').replace('{', '').replace('}', '')
                # Now do a sanity check that our body has a chunk of what we expected.
                if min_core.lower() not in answer.core.lower(): 
                    fail(f"expected core to contain at least '{min_core}'")
    if errors:
        print('\n'.join(errors))
        raise AssertionError("Parsing didn't work as expected. See stdout for details.")

def test_generic_parse():
    for input, parse_func in expected_parsers:
        if parse_func:
            answer = parse(input)
            if not answer: raise AssertionError(f"Didn't parse input {input}.")

def test_hex_normalization():
    for input in [
        "0x32Be343B94f860124dC4fEe278FDCBD38C102D",
        "0x60124dC4fEe278FDCBD38C102D",
        "0x601", 
        "32Be343B94f860124dC4fEe278FDCBD38C102D",
        "60124dC4fEe278FDCBD38C102D",
        ]:
        answer = parse(input)
        assert answer
        if input.startswith('0'):
            prefix = '0x'
            core = input[2:]
        else:
            prefix = None
            core = input
        assert answer.prefix == prefix
        assert answer.core == core.upper()

def test_stellar_normalization():
    for input in [
        "GDFW2Z2IWGRJAJH5UNZ5B4PL5JY2X2BTHXVD5J7P64ICBRQJXP6VXABM",
        "gdfw2z2iwgrjajh5unz5b4pl5jy2x2bthxvd5j7p64icbrqjxp6vxabm",
        ]:
        answer = parse(input)
        assert answer.prefix == 'G'
        assert answer.core == "DFW2Z2IWGRJAJH5UNZ5B4PL5JY2X2BTHXVD5J7P64ICBRQJXP6VXABM"
        assert answer.type == "Stellar"

def test_hex_multihash_normalization():
    for input in [
        hexified_multihash.lower(),
        hexified_multihash.upper()
        ]:
        answer = parse(input)
        assert answer.core == hexified_multihash.lower()[4:]
        assert answer.type == "hex multihash sha2-256"

def test_etherereum_normalization():
    for input in [
        #"0xc932bE343B94f860124dC4fEe278FDCBD38C102D", # mixed case, but wrong
        #"0xc932be343b94f860124dc4fee278fdcbd38c102d", # all lower case
        "0xC932BE343B94F860124DC4FEE278FDCBD38C102D", # all upper case
        ]:
        answer = parse(input)
        assert answer.core == 'C932Be343b94f860124dc4FEe278fDcB'
        assert answer.suffix == 'd38c102d'
        assert answer.type == "Ethereum"

def test_UUID_normalization():
    for input in [
        "087f9afc-5e79-4c14-98eb-3217e477242c", 
        "{087f9afc-5e79-4c14-98eb-3217e477242c}", 
        "087f9afc5e794c1498eb3217e477242c"
        ]:
        answer = parse(input)
        assert answer.core == "087f9afc5e794c1498eb3217e477242c"
        assert answer.type == "UUID"

