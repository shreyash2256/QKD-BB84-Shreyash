import random
import hashlib

# Step 1: Generate random bits
def generate_bits(n):
    return [random.randint(0, 1) for _ in range(n)]

# Step 2: Generate random bases
def generate_bases(n):
    return [random.choice(['Z', 'X']) for _ in range(n)]

# Step 3: Encode bits
def encode(bits, bases):
    return list(zip(bits, bases))

# Step 4: Measure with possible eavesdropping
def measure(encoded, bases, eavesdrop=False):
    measured = []
    for i in range(len(encoded)):
        bit, basis = encoded[i]

        if eavesdrop:
            eve_basis = random.choice(['Z', 'X'])
            if eve_basis != basis:
                bit = random.randint(0, 1)

        if bases[i] == basis:
            measured.append(bit)
        else:
            measured.append(random.randint(0, 1))
    return measured

# Step 5: Basis sifting
def sift(alice_bases, bob_bases, alice_bits, bob_bits):
    key_a, key_b = [], []
    for i in range(len(alice_bases)):
        if alice_bases[i] == bob_bases[i]:
            key_a.append(alice_bits[i])
            key_b.append(bob_bits[i])
    return key_a, key_b

# Step 6: Error correction (simple)
def error_rate(a, b):
    errors = sum([1 for i in range(len(a)) if a[i] != b[i]])
    return errors / len(a)

# Step 7: Privacy amplification (hashing)
def privacy_amplification(key):
    key_str = ''.join(map(str, key))
    return hashlib.sha256(key_str.encode()).hexdigest()

# MAIN EXECUTION
n = 50

alice_bits = generate_bits(n)
alice_bases = generate_bases(n)

encoded = encode(alice_bits, alice_bases)

bob_bases = generate_bases(n)

# Toggle eavesdropping
eavesdrop = True

bob_bits = measure(encoded, bob_bases, eavesdrop)

key_a, key_b = sift(alice_bases, bob_bases, alice_bits, bob_bits)

print("Alice Key:", key_a)
print("Bob Key:", key_b)

if len(key_a) > 0:
    err = error_rate(key_a, key_b)
    print("Error Rate:", err)

    final_key = privacy_amplification(key_a)
    print("Final Secure Key:", final_key)
else:
    print("No key generated.")