from random import randint

g = 666 # shared base
p = 6661 # shared prime
bob_pub_key = 2227 # bobs public key (g ^ x mod p), his private key is 66

# Exercise 1
# Generate private key for alice

def create_random_key(upper_limit):
    return randint(1, upper_limit)

def generate_public_key(base, prime, private_key):
    return (base ** private_key) % prime

def cipher(message, receiving_public_key, private_key, prime):
    return ((receiving_public_key ** private_key % prime) * (message % prime))

alice_priv_key = create_random_key(p)
alice_pub_key = generate_public_key(g, p, alice_priv_key)

m = input()
if len(m) == 0:
    m = 2000 # If no input, set message to 2000 (DKK)
else:
    m = int(m)

c = cipher(m, bob_pub_key, alice_priv_key, p) # cipher-text

print("Generated private key:", alice_priv_key)
print("Generated public key:", alice_pub_key)
print("Ciphertext:", c)

# Exercise 2
# Bobs public key is computed by 
def bruteforce_private_key(public_key, base, prime):
    for i in range(prime):
        if (base ** i) % prime == public_key:
            return i # Brute-force solution that runs in O(p log p) where p = prime 

def decipher(ciphertext, sender_public_key, private_key, prime):
    return ciphertext / (((sender_public_key ** private_key)) % prime)

bob_priv_key = bruteforce_private_key(bob_pub_key, g, p)

deciphered = decipher(c, alice_pub_key, bob_priv_key, p)

print("Bob's private key:", bob_priv_key)
print("Deciphered:", int(deciphered)) # converted to int to remove .0

# Exercise 3
# Modify encrypted message to show 4000 instead of 2000 (i.e. double the amount)
# as a*n = b*n mod p then we can just double the ciphertext when we intercept the message:

c *= 2

deciphered = decipher(c, alice_pub_key, bob_priv_key, p)

# Print a deciphered version of the altered message to illustrate effect of the encryption
print("Decipher altered message:", int(deciphered))
