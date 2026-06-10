#!/usr/bin/env python3
import base64
import os
import subprocess
import sys


# Path to the public key file in the same directory as this script.
PUBLIC_KEY_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public_key.pem")

def encrypt_secret(secret_value: str, public_key_path: str) -> str:
    # Use openssl pkeyutl to encrypt the secret value.
    # Pass the secret value via stdin.
    process = subprocess.Popen(
        ["openssl", "pkeyutl", "-encrypt", "-pubin", "-inkey", public_key_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate(input=secret_value.encode('utf-8'))
    if process.returncode != 0:
        raise RuntimeError(f"OpenSSL error: {stderr.decode('utf-8')}")
    # Return base64 encoded encrypted value
    return base64.b64encode(stdout).decode('utf-8')

def main():
    # Check if the public key file exists
    if not os.path.exists(PUBLIC_KEY_PATH):
        print(f"Error: Public key file not found at '{PUBLIC_KEY_PATH}'.", file=sys.stderr)
        print("Please run tools/generate_keypair.py to generate the key pair.", file=sys.stderr)
        sys.exit(1)

    # Read secrets from environment variables
    pypi_token = os.environ.get("PYPI_API_TOKEN")
    test_pypi_token = os.environ.get("TEST_PYPI_API_TOKEN")

    if not pypi_token and not test_pypi_token:
        print("Error: Neither PYPI_API_TOKEN nor TEST_PYPI_API_TOKEN environment variables are set.", file=sys.stderr)
        sys.exit(1)

    if pypi_token:
        try:
            encrypted_pypi = encrypt_secret(pypi_token, PUBLIC_KEY_PATH)
            print("=== ENCRYPTED PYPI_API_TOKEN ===")
            print(encrypted_pypi)
            print("================================\n")
        except Exception as e:
            print(f"Failed to encrypt PYPI_API_TOKEN: {e}", file=sys.stderr)

    if test_pypi_token:
        try:
            encrypted_test_pypi = encrypt_secret(test_pypi_token, PUBLIC_KEY_PATH)
            print("=== ENCRYPTED TEST_PYPI_API_TOKEN ===")
            print(encrypted_test_pypi)
            print("=====================================\n")
        except Exception as e:
            print(f"Failed to encrypt TEST_PYPI_API_TOKEN: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()

