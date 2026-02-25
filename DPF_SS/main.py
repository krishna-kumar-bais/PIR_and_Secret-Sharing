# DPF/main.py
from GenerateDPF import GenerateDPF
from EvalDPF import EvaluateDPF

def main():
    alpha = 3
    beta = 1233499956
    nbits = 5
    prime = 2147483647

    k0, k1 = GenerateDPF(alpha, beta, nbits, prime)
    print("x\tEval0\tEval1\tSum")
    for x in range(0, 8):
        v0 = EvaluateDPF(k0, x, nbits, prime)
        v1 = EvaluateDPF(k1, x, nbits, prime)
        s = (v0 + v1) % prime
        print(f"{x} -> {v0} + {v1} = {s}")

if __name__ == "__main__":
    main()
