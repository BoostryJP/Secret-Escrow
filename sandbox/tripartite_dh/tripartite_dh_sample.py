import base64
import secrets
from hashlib import sha256

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from py_ecc.bls12_381 import G1, G2, curve_order, multiply, pairing
from py_ecc.fields import bls12_381_FQ12

###############################################
# Generate Alice's key
###############################################
print(
    """
== Generate Alice's key ==
"""
)

A_sk = int.from_bytes(secrets.token_bytes(32)) % curve_order
print("<A_sk>")
print(A_sk)

A_pk1 = multiply(G1, A_sk)
print("<A_pk1>")
print(A_pk1)

A_pk2 = multiply(G2, A_sk)
print("<A_pk2>")
print(A_pk2)

###############################################
# Generate Bob's key
###############################################
print(
    """
== Generate Bob's key ==
"""
)

B_sk = int.from_bytes(secrets.token_bytes(32)) % curve_order
print("<B_sk>")
print(B_sk)

B_pk1 = multiply(G1, B_sk)
print("<B_pk1>")
print(B_pk1)

B_pk2 = multiply(G2, B_sk)
print("<B_pk2>")
print(B_pk2)

###############################################
# Generate Charlie's key
###############################################
print(
    """
== Generate Charlie's key ==
"""
)

C_sk = int.from_bytes(secrets.token_bytes(32)) % curve_order
print("<C_sk>")
print(C_sk)

C_pk1 = multiply(G1, C_sk)
print("<C_pk1>")
print(C_pk1)

C_pk2 = multiply(G2, C_sk)
print("<C_pk2>")
print(C_pk2)


###############################################
# Key Exchange
###############################################
print(
    """
== DH key (Alice) ==
"""
)
A_dh: bls12_381_FQ12 = pairing(B_pk2, C_pk1) ** A_sk
_hash = sha256()
for _item in A_dh.coeffs:
    _item = int(_item)
    _hash.update(_item.to_bytes(48))
A_shared_key = _hash.digest()
print(A_shared_key)

print(
    """
== DH key (Bob) ==
"""
)
B_dh: bls12_381_FQ12 = pairing(C_pk2, A_pk1) ** B_sk
_hash = sha256()
for _item in B_dh.coeffs:
    _item = int(_item)
    _hash.update(_item.to_bytes(48))
B_shared_key = _hash.digest()
print(B_shared_key)

print(
    """
== DH key (Charlie) ==
"""
)
C_dh: bls12_381_FQ12 = pairing(A_pk2, B_pk1) ** C_sk
_hash = sha256()
for _item in C_dh.coeffs:
    _item = int(_item)
    _hash.update(_item.to_bytes(48))
C_shared_key = _hash.digest()
print(C_shared_key)


print(
    """
!!! Result !!!
"""
)
print(
    f"A_shared_key == B_shared_key == C_shared_key -> {A_shared_key == B_shared_key == C_shared_key}"
)

message_org = "A One Round Protocol for Tripartite Diffie–Hellman"
aes_iv = secrets.token_bytes(AES.block_size)
aes_cipher = AES.new(A_shared_key, AES.MODE_CBC, aes_iv)
pad_message = pad(message_org.encode("utf-8"), AES.block_size)
encrypted_message = base64.b64encode(aes_iv + aes_cipher.encrypt(pad_message)).decode()
print("Original message = 'A One Round Protocol for Tripartite Diffie–Hellman'")
print(f"Encrypted message = {encrypted_message}")
