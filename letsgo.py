

  # THIS CODE IS FOR AN ALGORITHM CALLED LETS GO THAT ENCRYPTS THE MESSAGE 
  # WITH GIVEN KEY BASED ON FIESTEL 


def rotate_left(val, n, bits=32):
    """Perform a left rotation on a value with a given number of bits."""
    return ((val << n) & (2**bits - 1)) | (val >> (bits - n))

def generate_subkeys(key, rounds=16):
    """Generate subkeys for each round from the original key."""
    subkeys = []
    key_left, key_right = key >> 32, key & 0xFFFFFFFF  # Split key into two 32-bit halves
    for i in range(1, rounds + 1):
        key_left = rotate_left(key_left, i % 32)
        key_right = rotate_left(key_right, i % 32)
        subkey = ((key_left << 16) | (key_right >> 16)) & 0xFFFFFFFFFFFF  # Combine parts to make a 48-bit subkey
        subkeys.append(subkey)
    return subkeys

def feistel_function(right_half, subkey):
    """Feistel function using XOR, rotation, and a simple substitution (S-Box)."""
    right_expanded = ((right_half << 16) | (right_half >> 16)) & 0xFFFFFFFFFFFF  # Expand to 48 bits
    mixed = right_expanded ^ subkey  # XOR with the subkey
    s_box_output = (mixed ^ rotate_left(mixed, 4, 48)) & 0xFFFFFFFF  # Substitute and reduce to 32 bits
    return s_box_output

def letsgo_encrypt(plain_text, key):
    """Encrypt a 64-bit block of plaintext using the LetsGo algorithm."""
    assert len(bin(plain_text)[2:]) <= 64, "Plain text must be 64 bits or less."
    assert len(bin(key)[2:]) <= 64, "Key must be 64 bits or less."
    
    # Split plaintext into two 32-bit halves
    left, right = plain_text >> 32, plain_text & 0xFFFFFFFF
    subkeys = generate_subkeys(key)

    # Perform 16 rounds of Feistel structure
    for subkey in subkeys:
        left, right = right, left ^ feistel_function(right, subkey)

    # Combine final halves to produce the ciphertext
    cipher_text = (right << 32) | left
    return cipher_text


# here we add the plain text we want 
plain_text = 0x0123456789ABCDEF  # Example plaintext
key = 0x133457799BBCDFF1         # Example key

# We can get plain text and input like this too 
#plain_text = input("enter the text you want to encrypt")
#key = input("enter the key you want to encrypt with")

cipher_text = letsgo_encrypt(plain_text, key)
print(f"Cipher Text: {hex(cipher_text)}")
