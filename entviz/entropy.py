import collections
import re

Parsed = collections.namedtuple('Parsed', ['type', 'prefix', 'core', 'suffix'])

BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
BASE32_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
BASE32_ALPHABET_EITHER_CASE = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
BASE58_CHECK_LENGTH = 25  # Expected length of Base58Check encoded Bitcoin addresses

UUID_REGEX = re.compile(r'^\{?[0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12}\}?$', re.I)
DID_REGEX = re.compile(r'^(did:[a-z0-9]+:)((?:[a-zA-Z0-9_.-]|%[a-fA-F0-9]{2})+)((/[^?]*)?([?].*)?)$')
STELLAR_REGEX = re.compile(r'^(G)([' + BASE32_ALPHABET_EITHER_CASE + ']{55})$')
IPFS_CIDV0_REGEX = re.compile(r'^(Qm)([' + BASE58_ALPHABET + ']{44})$')
IPFS_CIDV1_REGEX = re.compile(r'^(b)([' + BASE32_ALPHABET_EITHER_CASE + ']{58,112})$')
EOS_REGEX = re.compile(r'^[a-z1-5.]{1,12}$')
CARDANO_SHORT_BYRON_REGEX = re.compile(r'^(Ae2)([' + BASE58_ALPHABET + ']{50})([' + BASE58_ALPHABET + ']{6})$')
CARDANO_LONG_BYRON_REGEX = re.compile(r'^(DdzFF)([' + BASE58_ALPHABET + ']{65})([' + BASE58_ALPHABET + ']{6})$')
CARDANO_SHELLEY_REGEX = re.compile(r'^((?:addr|stake)(?:_test)?)(1[' + BASE32_ALPHABET_EITHER_CASE + ']{50,100})([' + BASE32_ALPHABET_EITHER_CASE + ']{6})$')
BITCOIN_CASH_REGEX = re.compile(r'^((?:bitcoincash|bchtest):)?([pq][' + BASE32_ALPHABET + ']{41})', re.I)
LITECOIN_LEGACY_REGEX = re.compile(r'^(t?L)([' + BASE58_ALPHABET + ']{33})$')
LITECOIN_REGEX = re.compile(r'^(ltc)([' + BASE58_ALPHABET + ']{42,62})$')
ETHEREUM_REGEX = re.compile(r'^(0x)([a-fA-F0-9]{32})([a-fA-F0-9]{8})$')
RIPPLE_REGEX = re.compile(r'^(r)([' + BASE58_ALPHABET + ']{33})$')
BITCOIN_LEGACY_REGEX = re.compile(r'^([123mn])([' + BASE58_ALPHABET + ']{21,30})([' + BASE58_ALPHABET + ']{4})$')
BITCOIN_SEGWIT_REGEX = re.compile(r'^(bc1|tb1)([' + BASE32_ALPHABET_EITHER_CASE + ']{39,69})$', re.I)

def parse_bitcoin_address(address):
    """
    See if we can parse text as a Bitcoin address.
    If yes, return Parsed("bitcoin", prefix, body, None).
    """
    m = BITCOIN_LEGACY_REGEX.match(address)
    if m:
        return Parsed("Bitcoin legacy", m.group(1), m.group(2), m.group(3))
    m = BITCOIN_SEGWIT_REGEX.match(address)
    if m:
        return Parsed("Bitcoin SegWit", m.group(1), m.group(2), None)

def parse_ripple_address(text):
    """
    See if we can parse text as a Ripple address.
    If yes, return Parsed("Ripple", prefix, body, None).
    """
    m = RIPPLE_REGEX.match(text)
    if m:
        return Parsed("Ripple", m.group(1), m.group(2), None)

def parse_ethereum_address(text):
    """
    See if we can parse text as an Ethereum address.
    If yes, return Parsed("Ethereum", prefix, body, None).
    """
    m = ETHEREUM_REGEX.match(text)
    if m:
        return Parsed("Ethereum", m.group(1), m.group(2), m.group(3))

def parse_litecoin_address(text):
    """
    See if we can parse text as a Litecoin address.
    If yes, return Parsed("Litecoin...", prefix, body, None).
    """
    m = LITECOIN_LEGACY_REGEX.match(text)
    if m:
        return Parsed("Litecoin legacy", m.group(1), m.group(2), None)
    m = LITECOIN_REGEX.match(text)
    if m:
        return Parsed("Litecoin", m.group(1), m.group(2), None)

def parse_bitcoin_cash_address(text):
    """
    See if we can parse text as a Bitcoin cash address.
    If yes, return Parsed("Bitcoin cash", prefix, body, None).
    """
    m = BITCOIN_CASH_REGEX.match(text)
    if m:
        return Parsed("Bitcoin Cash", m.group(1), m.group(2), None)

def parse_cardano_address(text):
    """
    See if we can parse text as a Cardano address.
    If yes, return Parsed("Cardano...", prefix ("addr", "stake", etc.), body, checksum).
    """
    m = CARDANO_SHORT_BYRON_REGEX.match(text)
    if m:
        return Parsed("Cardano Byron", m.group(1), m.group(2), m.group(3))
    m = CARDANO_LONG_BYRON_REGEX.match(text)
    if m:
        return Parsed("Cardano Byron", m.group(1), m.group(2), m.group(3))
    m = CARDANO_SHELLEY_REGEX.match(text)
    if m:
        return Parsed("Cardano Shelley", m.group(1), m.group(2), m.group(3))

def parse_eos_address(text):
    """
    See if we can parse text as an EOS address.
    If yes, return Parsed("EOS", None, body (address), None).
    """
    m = EOS_REGEX.match(text)
    if m:
        return Parsed("EOS", None, m.group(0), None)

def parse_stellar_address(text):
    """
    See if we can parse text as a Stellar address.
    If yes, return prefix (G), body (rest of address), and suffix (empty).
    """
    m = STELLAR_REGEX.match(text)
    if m:
        return Parsed("Stellar", m.group(1), m.group(2), None)
    
def parse_uuid(text):
    """
    See if we can parse text as a UUID.
    If yes, return Parsed("UUID", prefix (None), body (lower-case UUID sans punct), suffix (None)).
    """
    m = UUID_REGEX.match(text)
    if m:
        body = m.group(0).lower().replace('-', '').replace('{', '').replace('}', '')
        return Parsed("UUID", None, body, None)

def parse_did(text) -> Parsed:
    """
    See if we can parse text as a DID or DID URL.
    If yes, return Parsed("DID", "did:" + method + ":", body (rest of DID1), URL if any).
    """
    m = DID_REGEX.match(text)
    if m:
        return Parsed("DID", m.group(1), m.group(2), m.group(3))
    
def parse_ipfs_cid(text):
    """
    See if we can parse text as an IPFS CID.
    If yes, return Parsed("IPFS CID...", prefix (Qm or b), body, None)
    """
    m = IPFS_CIDV0_REGEX.match(text)
    if m:
        return Parsed("IPFS CID v0", m.group(1), m.group(2), None)
    m = IPFS_CIDV1_REGEX.match(text)
    if m:
        return Parsed(f"IPFS CID v1 256", m.group(1), m.group(2), None)

def register_parse_funcs():
    g = globals()
    parse_funcs = []
    for name, value in g.items():
        if name.startswith("parse_") and callable(value):
            parse_funcs.append(value)
    return parse_funcs
parse_funcs = register_parse_funcs()
del register_parse_funcs

def normalize(entropy: str):
    entropy = entropy.strip()
    if UUID_REGEX.match(entropy):
        return entropy.lower().replace('-', '').replace('{', '').replace('}', '')
    
