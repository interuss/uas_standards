#!/usr/bin/env python3
import os
import subprocess
import sys


def main():
    private_key_path = "private_key.pem"
    # Write the public key to the same directory as this script.
    tools_dir = os.path.dirname(os.path.abspath(__file__))
    public_key_path = os.path.join(tools_dir, "public_key.pem")

    if os.path.exists(private_key_path) or os.path.exists(public_key_path):
        print(f"Error: {private_key_path} or {public_key_path} already exists. Please delete or move them before generating new ones.")
        sys.exit(1)

    try:
        # Generate private key
        print("Generating private key (2048-bit RSA)...")
        subprocess.run([
            "openssl", "genpkey",
            "-algorithm", "RSA",
            "-out", private_key_path,
            "-pkeyopt", "rsa_keygen_bits:2048"
        ], check=True)

        # Restrict permissions of the private key
        os.chmod(private_key_path, 0o600)

        # Generate public key from private key
        print("Generating public key...")
        subprocess.run([
            "openssl", "rsa",
            "-pubout",
            "-in", private_key_path,
            "-out", public_key_path
        ], check=True)

        print("\nSuccess! Key pair generated successfully.")
        print(f"Private key saved to: {private_key_path} (Keep this secret and secure!)")
        print(f"Public key saved to:  {public_key_path}")
        print("\nCommit the updated public_key.pem file to the repository so the workflow can use it.")

    except subprocess.CalledProcessError as e:
        print(f"Error executing OpenSSL: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
