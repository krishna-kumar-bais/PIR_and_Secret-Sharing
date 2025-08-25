def mod_divide(numerator, denominator, prime):
    denominator_inv = pow(denominator % prime, -1, prime)   # modular inverse
    return (numerator % prime) * denominator_inv % prime

def ReconstructSecret(shares, prime):
    secret = 0
    t = len(shares)

    LagrangeCoefficient = []
    for i in range(0,t):
        x = shares[i][0]
        coeff = 1
        for j in range(0,t):
            if i==j :
                continue
            # using helper function instead of raw division
            coeff *= mod_divide(shares[j][0], shares[j][0] - x, prime)
            coeff = coeff % prime
        LagrangeCoefficient.append(coeff)

    for i in range(0,t):
        y = shares[i][1]
        secret += y * LagrangeCoefficient[i]
        secret = secret % prime
    return secret