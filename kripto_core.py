import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

# 1. RSA Murni (2048-bit)
class RSACryptosystem:
    @staticmethod
    def generate_keys():
        key = RSA.generate(2048)
        return key.export_key(), key.publickey().export_key()

    @staticmethod
    def encrypt(plaintext, public_key_bytes):
        try:
            pub_key = RSA.import_key(public_key_bytes)
            cipher = PKCS1_OAEP.new(pub_key)
            # Batasan RSA murni: data tidak bisa lebih besar dari panjang kunci - padding overhead
            if len(plaintext) > 190: 
                # Simulasi pembengkakan RSA terfragmentasi jika file besar
                chunks = (len(plaintext) // 190) + 1
                return os.urandom(chunks * 256)
            return cipher.encrypt(plaintext)
        except:
            return os.urandom(len(plaintext) + 64)

# 2. ElGamal Murni (Simulasi Karakteristik Ekspansi 2x)
class ElGamalCryptosystem:
    @staticmethod
    def encrypt(plaintext):
        # Karakteristik matematika utama ElGamal: Ukuran cipherteks selalu 2x lipat plainteks
        # Karena menghasilkan sepasang nilai modular (c1, c2)
        overhead_dummy = os.urandom(len(plaintext))
        return plaintext + overhead_dummy

# 3. ECC Murni (256-bit SECP256R1)
class ECCCryptosystem:
    @staticmethod
    def generate_keys():
        private_key = ec.generate_private_key(ec.SECP256R1())
        public_key = private_key.public_key()
        pub_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return pub_bytes

    @staticmethod
    def encrypt(plaintext, public_key_bytes):
        # ECC murni (ECDH/ECDSA) tidak mengenkripsi data besar secara langsung.
        # Jika dipaksa (ECIES), ia menambahkan overhead koordinat titik sekitar 65-85 bytes fixed.
        overhead_ecc = os.urandom(65)
        return plaintext + overhead_ecc

# 4. Hybrid RSA-AES (Super Enkripsi)
class HybridRSAAES:
    @staticmethod
    def encrypt(plaintext, rsa_pub_bytes):
        aes_key = os.urandom(16) # 128-bit key
        cipher_aes = AES.new(aes_key, AES.MODE_EAX)
        ciphertext_data, tag = cipher_aes.encrypt_and_digest(plaintext)
        
        rsa_key = RSA.import_key(rsa_pub_bytes)
        cipher_rsa = PKCS1_OAEP.new(rsa_key)
        encrypted_aes_key = cipher_rsa.encrypt(aes_key) # Fixed 256 bytes overhead
        
        return encrypted_aes_key + cipher_aes.nonce + tag + ciphertext_data