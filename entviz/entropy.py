import base32
import base58
import collections
import re

ParseSuccess = collections.namedtuple('ParseSuccess', ['type', 'prefix', 'body', 'suffix'])

BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
BASE32_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
BASE58_CHECK_LENGTH = 25  # Expected length of Base58Check encoded Bitcoin addresses

UUID_REGEX = re.compile(r'^\{?[0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12}\}?$', re.I)
DID_REGEX = re.compile(r'^(did:[a-z0-9]+:)((?:[a-zA-Z0-9_.-]|%[a-fA-F0-9]{2})+)((/[^?]*)?([?].*)?)$')
STELLAR_REGEX = re.compile(r'^(G)([' + BASE32_ALPHABET + ']{55})$')
IPFS_CIDV0_REGEX = re.compile(r'^(Qm)([' + BASE58_ALPHABET + ']{44})$')
IPFS_CIDV1_256_REGEX = re.compile(r'^(b)([' + BASE32_ALPHABET + ']{58})$')
IPFS_CIDV1_512_REGEX = re.compile(r'^(b)([' + BASE32_ALPHABET + ']{112})$')
EOS_REGEX = re.compile(r'^[a-z1-5.]{1,12}$')
CARDANO_BYRON_REGEX = re.compile(r'^(Ae2|DdzFF)([' + BASE58_ALPHABET + ']{72,})([' + BASE58_ALPHABET + ']{6})$')
CARDANO_SHELLEY_REGEX = re.compile(r'^(addr|stake)([' + BASE32_ALPHABET + ']{50,})([' + BASE32_ALPHABET + ']{6})$')
BITCOIN_CASH_REGEX = re.compile(r'^(bitcoincash:)([pq][' + BASE32_ALPHABET + ']{42,52})$')
LITECOIN_LEGACY_REGEX = re.compile(r'^(t?L)([' + BASE58_ALPHABET + ']{33})$')
LITECOIN_REGEX = re.compile(r'^(ltc)([' + BASE58_ALPHABET + ']{42,62})$')
ETHEREUM_REGEX = re.compile(r'^(0x)([a-fA-F0-9]{32})([a-fA-F0-9]{8})$')
RIPPLE_REGEX = re.compile(r'^(r)([' + BASE58_ALPHABET + ']{33})$')
BITCOIN_LEGACY_REGEX = re.compile(r'^([123mn])([' + BASE58_ALPHABET + ']{21,30})([' + BASE58_ALPHABET + ']{4})$')
BITCOIN_SEGWIT_REGEX = re.compile(r'^(bc1|tb1)([' + BASE32_ALPHABET + ']{26,34})$')

MULTIHASH_CODES = {
    0x11: "sha1",
    0x12: "sha2-256",
    0x13: "sha2-512",
    0x14: "sha3-224",
    0x15: "sha3-256",
    0x16: "sha3-384",
    0x17: "sha3-512",
    0x18: "shake-128",
    0x19: "shake-256",
    0x1a: "keccak-224",
    0x1b: "keccak-256",
    0x1c: "keccak-384",
    0x1d: "keccak-512",
    0x22: "blake2b-8",
    0x23: "blake2b-16",
    0x24: "blake2b-24",
    0x25: "blake2b-32",
    0x26: "blake2b-40",
    0x27: "blake2b-48",
    0x28: "blake2b-56",
    0x29: "blake2b-64",
    0x2a: "blake2b-72",
    0x2b: "blake2b-80",
    0x2c: "blake2b-88",
    0x2d: "blake2b-96",
    0x2e: "blake2b-104",
    0x2f: "blake2b-112",
    0x30: "blake2b-120",
    0x31: "blake2b-128",
    0x32: "blake2b-136",
    0x33: "blake2b-144",
    0x34: "blake2b-152",
    0x35: "blake2b-160",
    0x36: "blake2b-168",
    0x37: "blake2b-176",
    0x38: "blake2b-184",
    0x39: "blake2b-192",
    0x3a: "blake2b-200",
    0x3b: "blake2b-208",
    0x3c: "blake2b-216",
    0x3d: "blake2b-224",
    0x3e: "blake2b-232",
    0x3f: "blake2b-240",
    0x40: "blake2b-248",
    0x41: "blake2b-256",
    0xb201: "dbl-sha2-256",
    0xb202: "murmur3-128",
    0xb203: "murmur3-32"
}

def decode_multihash(multihash):
    """Decode a multihash and return its hash function and length."""
    if len(multihash) < 2:
        return None
    code = multihash[0]
    length = multihash[1]
    if code in MULTIHASH_CODES:
        return MULTIHASH_CODES[code], length
    return None

def parse_bitcoin_address(address):
    """
    See if we can parse text as a Bitcoin address.
    If yes, return ParseSuccess("bitcoin", prefix, body, None).
    """
    m = BITCOIN_LEGACY_REGEX.match(address)
    if m:
        return ParseSuccess("Bitcoin legacy", m.group(1), m.group(2), m.group(3))
    m = BITCOIN_SEGWIT_REGEX.match(address)
    if m:
        return ParseSuccess("Bitcoin SegWit", m.group(1), m.group(2), None)

def parse_ripple_address(text):
    """
    See if we can parse text as a Ripple address.
    If yes, return ParseSuccess("Ripple", prefix, body, None).
    """
    m = RIPPLE_REGEX.match(text)
    if m:
        return ParseSuccess("Ripple", m.group(1), m.group(2), m.group(3))

def parse_ethereum_address(text):
    """
    See if we can parse text as an Ethereum address.
    If yes, return ParseSuccess("Ethereum", prefix, body, None).
    """
    m = ETHEREUM_REGEX.match(text)
    if m:
        return ParseSuccess("Ethereum", m.group(1), m.group(2), m.group(3))

def parse_litecoin_address(text):
    """
    See if we can parse text as a Litecoin address.
    If yes, return ParseSuccess("Litecoin...", prefix, body, None).
    """
    m = LITECOIN_LEGACY_REGEX.match(text)
    if m:
        return ParseSuccess("Litecoin legacy", m.group(1), m.group(2), None)
    m = LITECOIN_REGEX.match(text)
    if m:
        return ParseSuccess("Litecoin", m.group(1), m.group(2), None)

def parse_bitcoin_cash_address(text):
    """
    See if we can parse text as a Bitcoin cash address.
    If yes, return ParseSuccess("Bitcoin cash", prefix, body, None).
    """
    m = BITCOIN_CASH_REGEX.match(text)
    if m:
        return ParseSuccess("Bitcoin Cash", m.group(1), m.group(2), None)

def parse_cardano_address(text):
    """
    See if we can parse text as a Cardano address.
    If yes, return ParseSuccess("Cardano...", prefix ("addr", "stake", etc.), body, checksum).
    """
    m = CARDANO_BYRON_REGEX.match(text)
    if m:
        return ParseSuccess("Cardano Byron", m.group(1), m.group(2), m.group(3))
    m = CARDANO_SHELLEY_REGEX.match(text)
    if m:
        return ParseSuccess("Cardano Shelley", m.group(1), m.group(2), m.group(3))

def parse_eos_address(text):
    """
    See if we can parse text as an EOS address.
    If yes, return ParseSuccess("EOS", None, body (address), None).
    """
    m = EOS_REGEX.match(address)
    if m:
        return ParseSuccess("EOS", None, m.group(0), None)

def parse_stellar_address(text):
    """
    See if we can parse text as a Stellar address.
    If yes, return prefix (G), body (rest of address), and suffix (empty).
    """
    m = STELLAR_REGEX.match(text)
    if m:
        return ParseSuccess("Stellar", m.group(1), m.group(2), None)
    
def parse_uuid(text):
    """
    See if we can parse text as a UUID.
    If yes, return ParseSuccess("UUID", prefix (None), body (lower-case UUID sans punct), suffix (None)).
    """
    m = UUID_REGEX.match(text)
    if m:
        body = m.group(0).lower().replace('-', '').replace('{', '').replace('}', '')
        return ParseSuccess("UUID", None, body, None)

def parse_did(text) -> ParseSuccess
    """
    See if we can parse text as a DID or DID URL.
    If yes, return ParseSuccess("DID", "did:" + method + ":", body (rest of DID1), URL if any).
    """
    m = DID_REGEX.match(text)
    if m:
        return ParseSuccess("DID", m.group(1), m.group(2), m.group(3))

def parse_ipfs_cid(text):
    """
    See if we can parse text as an IPFS CID.
    If yes, return ParseSuccess("IPFS CID...", prefix (Qm or b), body, None)
    """
    m = IPFS_CIDV0_REGEX.match(text)
    if m:
        decoded = base58.b58decode(text)
        hash_function, length = decode_multihash(decoded)
        if hash_function == "sha2-256" and length == 32:
            return ParseSuccess("IPFS CID v0 (sha2-256)", m.group(1), m.group(2), None)
    m = IPFS_CIDV1_256_REGEX.match(text)
    if m:
        # Remove the 'b' prefix and decode the rest
        base32_decoded = base32.b32decode(m.group(1))
        hash_function, length = decode_multihash(base32_decoded)
        return ParseSuccess(f"IPFS CID v1 ({hash_function})", m.group(1), m.group(2), None)
    m = IPFS_CIDV1_512_REGEX.match(text)
    if m:
        # Remove the 'b' prefix and decode the rest
        base32_decoded = base32.b32decode(m.group(1))
        hash_function, length = decode_multihash(base32_decoded)
        return ParseSuccess(f"IPFS CID v1 ({hash_function})", m.group(1), m.group(2), None)

parse_funcs = []
for name, value in globals().items():
    if name.startswith("parse_") and callable(value):
        parse_funcs.append(value)

def normalize(entropy: str):
    entropy = entropy.strip()
    if UUID_REGEX.match(entropy):
        return entropy.lower().replace('-', '').replace('{', '').replace('}', '')
    
