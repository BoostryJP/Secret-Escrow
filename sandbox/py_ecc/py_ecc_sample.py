from py_ecc.bls12_381 import pairing, G2, G1, multiply, neg, FQ12

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
print(p1 * p2 == p1 ** 3)

print("p1 * po2 == p1 ** 3")
print(p1 * po2 == p1 ** 3)

print("p1 * np1 == FQ12.one")
print(p1 * np1 == FQ12.one())

p3 = pairing(multiply(G2, 27), multiply(G1, 37))
po3 = pairing(G2, multiply(G1, 999))

# print(p3)
# print(po3)

print("p3 == po3")
print(p3 == po3)
