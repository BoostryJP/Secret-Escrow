from py_ecc.bls12_381 import pairing, G2, G1, multiply

p3 = pairing(multiply(G2, 27), multiply(G1, 37))
po3 = pairing(G2, multiply(G1, 999))

# print(p3)
# print(po3)

print("p3 == po3")
print(p3 == po3)
