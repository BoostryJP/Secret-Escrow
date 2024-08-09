import secrets

from py_ecc.bls12_381 import G1, G2, multiply, pairing

###############################################
# Generate Alice's key
###############################################
print(
    """
== Generate Alice's key ==
"""
)

A_sk = int.from_bytes(secrets.token_bytes(32))
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

B_sk = int.from_bytes(secrets.token_bytes(32))
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

C_sk = int.from_bytes(secrets.token_bytes(32))
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
A_dhk = pairing(B_pk2, C_pk1) ** A_sk
print(A_dhk)

print(
    """
== DH key (Bob) ==
"""
)
B_dhk = pairing(C_pk2, A_pk1) ** B_sk
print(B_dhk)

print(
    """
== DH key (Bob) ==
"""
)
C_dhk = pairing(A_pk2, B_pk1) ** C_sk
print(C_dhk)

print(
    """
== Assertion ==
"""
)
print(A_dhk == B_dhk == C_dhk)
