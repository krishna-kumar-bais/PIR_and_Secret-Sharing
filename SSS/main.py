from GenerateShare import GenerateShare
from ReconstructSecret import ReconstructSecret


def main():
    # Example parameters
    secret = 1233456
    print(f"\nSecrete : {secret}")
    t = 3          # threshold
    n = 5          # total shares
    prime = 2147483647  # prime

    shares = GenerateShare(secret, t, n, prime)
    print("\nAll shares:")
    for x, y in shares:
        print(f"(x={x}, y={y})")

    # Reconstruct the secret from any t shares (here: first t shares)
    subset = [] # share :0,1,..,t-1
    for i in range(0,t):
        subset.append((shares[i][0],shares[i][1]))

    reconstructed = ReconstructSecret(subset, prime)
    print(f"\nReconstructed secret from {t} shares: {reconstructed}\n")


if __name__ == "__main__":
    main()


