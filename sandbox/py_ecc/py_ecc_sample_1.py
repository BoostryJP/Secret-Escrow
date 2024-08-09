from py_ecc.bls12_381 import FQ12, G1, G2, multiply, neg, pairing

p1 = pairing(G2, G1)
p2 = pairing(G2, multiply(G1, 2))
po2 = pairing(multiply(G2, 2), G1)
np1 = pairing(neg(G2), G1)

# print(p1)
# print(p2)
# print(po2)
# print(np1)

print("p1 * p1 == p2")
print(p1 * p1 == p2)

print("p1 * p2 == p1 ** 3")
print(p1 * p2 == p1**3)

print("p1 * po2 == p1 ** 3")
print(p1 * po2 == p1**3)

print("p1 * np1 == FQ12.one")
print(p1 * np1 == FQ12.one())
