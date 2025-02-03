import rsa

def generate_rsa_keys(key_size=2048):
    public_key, private_key = rsa.newkeys(key_size)
    return public_key, private_key

def save_keys(name, public_key, private_key):
    with open(f"{name}_public.pem", "wb") as f:
        f.write(public_key.save_pkcs1())
    with open(f"{name}_private.pem", "wb") as f:
        f.write(private_key.save_pkcs1())

if __name__ == "__main__":
    public_key, private_key = generate_rsa_keys()
    name = input("Enter key name: ")
    save_keys(name, public_key, private_key)
    print(f"RSA keys saved as '{name}_public.pem' and '{name}_private.pem'")
