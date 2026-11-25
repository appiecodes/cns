import json
from math import isqrt

from Crypto.Util.number import long_to_bytes
from sympy import continued_fraction, PolynomialRing, RationalField

with open("challenge.json", "r") as f:
    challenge = json.load(f)
n = challenge["n"]
c = challenge["c"]
e = challenge["e"]

print(n, '\n', c, '\n', e)


def wiener_attack(e, n):
    # Convergents van e/n
    num0, num1 = 0, 1
    den0, den1 = 1, 0

    a, b = e, n

    while b:
        quotient, a, b = a // b, b, a % b

        k = quotient * num1 + num0
        d = quotient * den1 + den0

        num0, num1 = num1, k
        den0, den1 = den1, d

        if k == 0 or (e * d - 1) % k != 0:
            continue

        phi = (e * d - 1) // k

        # p + q = n - phi + 1
        s = n - phi + 1
        delta = s * s - 4 * n

        if delta < 0:
            continue

        root = isqrt(delta)

        if root * root != delta:
            continue

        if (s + root) % 2 != 0:
            continue

        p = (s + root) // 2
        q = (s - root) // 2

        if p > 1 and q > 1 and p * q == n:
            return d

    return None

d = wiener_attack(e, n)
if d is None:
    print("Wiener attack failed")
else:
    print("Wiener attack succeeded, d =", d)
    m = pow(c, d, n)
    print("Decrypted message:", long_to_bytes(m))