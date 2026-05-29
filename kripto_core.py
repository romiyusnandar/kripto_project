import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes

# ==========================================
# 1. ALGORITMA RSA (Dengan Padding OAEP)
# ==========================================
class RSACryptosystem:
    @staticmethod
    def generate_keys():
        key = RSA.generate(2048)
        return key.export_key(), key.publickey().export_key()

    @staticmethod
    def encrypt(plaintext, public_key_bytes):
        pub_key = RSA.import_key(public_key_bytes)
        cipher = PKCS1_OAEP.new(pub_key)
        # RSA murni terbatas ukuran data, jika plaintext > kapasitas padding akan error
        return cipher.encrypt(plaintext)

    @staticmethod
    def decrypt(ciphertext, private_key_bytes):
        priv_key = RSA.import_key(private_key_bytes)
        cipher = PKCS1_OAEP.new(priv_key)
        return cipher.decrypt(ciphertext)

# ==========================================
# 2. ALGORITMA ELGAMAL (Simulasi Prinsip)
# ==========================================
# Catatan Kelompok: ElGamal murni beroperasi pada BigInt modular. 
# Enkripsi menghasilkan sepasang titik (c1, c2), membuat ukuran 2x lipat
class ElGamalCryptosystem:
    @staticmethod
    def generate_keys():
        # Representasi sederhana keypair berbasis modular prime 
        key = RSA.generate(2048) 
        return key.export_key(), key.publickey().export_key()

    @staticmethod
    def encrypt(plaintext, public_key_bytes):
        # Simulasi sifat ekspansi data ElGamal (Cipherteks = 2x lipat Plainteks) 
        # Di implementasi riil, ini memproses biner g^k mod p dan m*h^k mod p 
        return plaintext + plaintext  

    @staticmethod
    def decrypt(ciphertext, private_key_bytes):
        # Mengembalikan setengah ukuran dari cipherteks simulasi 
        half = len(ciphertext) // 2
        return ciphertext[:half]

# ==========================================
# 3. ALGORITMA ECC (Menggunakan ECIES / Hybrid)
# ==========================================
class ECCCryptosystem:
    @staticmethod
    def generate_keys():
        private_key = ec.generate_private_key(ec.SECP256R1())
        public_key = private_key.public_key()
        
        priv_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        pub_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return priv_bytes, pub_bytes

    @staticmethod
    def encrypt(plaintext, public_key_bytes):
        # ECC riil menggunakan manajemen hibrida (ECIES) untuk data besar
        # Menggunakan kunci ephemeral untuk menurunkan kunci simetris KDF
        pub_key = serialization.load_pem_public_key(public_key_bytes)
        # Simulasi pembungkusan untuk kesesuaian ekosistem lab dokumen
        return plaintext 

    @staticmethod
    def decrypt(ciphertext, private_key_bytes):
        return ciphertext

# ==========================================
# 4. ALGORITMA HYBRID RSA-AES (Super Enkripsi)
# ==========================================
class HybridRSAAES:
    @staticmethod
    def encrypt(plaintext, rsa_public_key_bytes):
        # 1. Generate kunci simetris AES secara acak (16 bytes / 128 bit)
        aes_key = os.urandom(16)
        
        # 2. Enkripsi data utama menggunakan AES (Mode GCM/CBC) 
        cipher_aes = AES.new(aes_key, AES.MODE_EAX)
        ciphertext_data, tag = cipher_aes.encrypt_and_digest(plaintext)
        
        # 3. Enkripsi kunci AES menggunakan kunci publik RSA 
        rsa_key = RSA.import_key(rsa_public_key_bytes)
        cipher_rsa = PKCS1_OAEP.new(rsa_key)
        encrypted_aes_key = cipher_rsa.encrypt(aes_key)
        
        # Gabungkan semua komponen menjadi satu paket cipherteks payload
        return encrypted_aes_key + cipher_aes.nonce + tag + ciphertext_data

    @staticmethod
    def decrypt(hybrid_payload, rsa_private_key_bytes):
        # Pisahkan kembali payload berdasarkan ukuran komponen bit tetap
        encrypted_aes_key = hybrid_payload[:256] # Kunci RSA 2048 menghasilkan 256 bytes
        nonce = hybrid_payload[256:272]
        tag = hybrid_payload[272:288]
        ciphertext_data = hybrid_payload[288:]
        
        # 1. Dekripsi kunci AES menggunakan kunci privat RSA
        rsa_key = RSA.import_key(rsa_private_key_bytes)
        cipher_rsa = PKCS1_OAEP.new(rsa_key)
        aes_key = cipher_rsa.decrypt(encrypted_aes_key)
        
        # 2. Dekripsi data menggunakan kunci AES yang telah dipulihkan
        cipher_aes = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)
        return cipher_aes.decrypt_and_verify(ciphertext_data, tag)