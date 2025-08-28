import random

def GenerateShare(secret, t, n, prime):
    if secret >= prime:
        raise ValueError("Secret must be less than prime.")

    # generate random coefficients (degree t-1 polynomial)
    coficent = [secret]
    for i in range(1, t):
        rand_cof = random.randint(0, prime - 1)
        coficent.append(rand_cof)

    # generate n shares (x, y)
    shares = []
    for i in range(1, n + 1):
        x = i # x-coordinate
        y = 0 # y-coordinate
        x_pow = 1
        for j in range(0,t):
            y = (y + coficent[j] * x_pow) % prime
            x_pow = (x_pow * x) % prime
        shares.append((x, y))
    return shares