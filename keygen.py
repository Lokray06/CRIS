import rsa  # You'll need to install the 'rsa' library

def generate_rsa_keys(key_size=2048):
    """
    Generate RSA key pair.
    Returns (public_key, private_key)
    """
    # Generate public and private keys with a given key length 'key_size'
    public_key, private_key = rsa.newkeys(key_size)
    return public_key, private_key

def save_keys(name, public_key, private_key):
    """
    Save the RSA keys to separate files.
    """
    # Public key is saved into a .pem file with the given name
    with open(f"{name}_public.pem", "wb") as f:
        f.write(public_key.save_pkcs1())
    
    # Private key is saved into another .pem file
    with open(f"{name}_private.pem", "wb") as f:
        f.write(private_key.save_pkcs1())

if __name__ == "__main__":
    # Generate a key pair with the default key size (2048 bits)
    public_key, private_key = generate_rsa_keys()
    
    # Provide a name for the keypair (the key name)
    name = input("Enter key name: ")
    save_keys(name, public_key, private_key)
    print(f"RSA keys saved as '{name}_public.pem' and '{name}_private.pem'")
