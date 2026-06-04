"""
encrypt_results.py
──────────────────
Encrypts alpha_scan_results.json using AES (OpenSSL-compatible format)
so CryptoJS can decrypt it in the browser with the dashboard password.

Usage:
    python encrypt_results.py --password "yourpassword"
    python encrypt_results.py  # reads password from .env or DASHBOARD_PASSWORD env var

Output:
    alpha-scanner/results.enc  (base64-encoded encrypted blob)
"""

import os, sys, base64, hashlib, json, argparse
from pathlib import Path

def get_password():
    # 1. Command-line argument
    parser = argparse.ArgumentParser()
    parser.add_argument('--password', default=None)
    args, _ = parser.parse_known_args()
    if args.password:
        return args.password

    # 2. Environment variable (set by GitHub Actions secrets)
    pw = os.environ.get('DASHBOARD_PASSWORD', '')
    if pw:
        return pw

    # 3. .env file
    for env_path in [Path('.env'), Path(__file__).parent / '.env']:
        if env_path.exists():
            for line in open(env_path):
                line = line.strip()
                if line.startswith('DASHBOARD_PASSWORD='):
                    return line.split('=', 1)[1].strip().strip('"').strip("'")

    print('ERROR: No DASHBOARD_PASSWORD found. Set it in .env or pass --password')
    sys.exit(1)


def evp_bytes_to_key(password: bytes, salt: bytes, key_len=32, iv_len=16):
    """OpenSSL EVP_BytesToKey — matches CryptoJS default key derivation."""
    d, d_i = b'', b''
    while len(d) < key_len + iv_len:
        d_i = hashlib.md5(d_i + password + salt).digest()
        d += d_i
    return d[:key_len], d[key_len:key_len + iv_len]


def encrypt_for_cryptojs(plaintext: str, password: str) -> str:
    """
    Encrypt plaintext using AES-256-CBC with OpenSSL-compatible salted format.
    The output base64 string can be decrypted by CryptoJS.AES.decrypt(enc, password).
    """
    try:
        from Crypto.Cipher import AES
        from Crypto.Util.Padding import pad
    except ImportError:
        print('Installing pycryptodome...')
        os.system(f'{sys.executable} -m pip install pycryptodome --quiet')
        from Crypto.Cipher import AES
        from Crypto.Util.Padding import pad

    salt      = os.urandom(8)
    key, iv   = evp_bytes_to_key(password.encode('utf-8'), salt)
    cipher    = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(plaintext.encode('utf-8'), AES.block_size))
    # OpenSSL format: b"Salted__" + salt (8 bytes) + ciphertext
    blob = base64.b64encode(b'Salted__' + salt + encrypted).decode('utf-8')
    return blob


def main():
    password    = get_password()
    input_file  = Path('alpha_scan_results.json')
    output_dir  = Path('alpha-scanner')
    output_file = output_dir / 'results.enc'

    if not input_file.exists():
        print(f'ERROR: {input_file} not found. Run alpha_scanner.py first.')
        sys.exit(1)

    output_dir.mkdir(exist_ok=True)

    plaintext = input_file.read_text(encoding='utf-8')
    encrypted = encrypt_for_cryptojs(plaintext, password)

    output_file.write_text(encrypted, encoding='utf-8')
    print(f'Encrypted: {input_file} → {output_file}')

    # Verify it's valid JSON before encryption (catch issues early)
    try:
        data = json.loads(plaintext)
        print(f'Verified: {len(data["stocks"])} stocks, scan date: {data["scan_date"]}')
    except Exception as e:
        print(f'Warning: JSON validation failed: {e}')


if __name__ == '__main__':
    main()
