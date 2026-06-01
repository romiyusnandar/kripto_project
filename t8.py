import os
import numpy as np
import pandas as pd
from kripto_core import RSACryptosystem, ElGamalCryptosystem, ECCCryptosystem, HybridRSAAES

# =======================================================
# 1. FUNGSI KHUSUS TUGAS 8 — AVALANCHE EFFECT
# =======================================================
def hitung_avalanche_effect(cipher_bytes_1, cipher_bytes_2):
    """
    Menghitung persentase perubahan bit biner antara dua cipherteks.
    Sesuai Rumus LKM: (Jumlah bit berubah / Total bit) * 100%
    """
    len_min = min(len(cipher_bytes_1), len(cipher_bytes_2))
    if len_min == 0:
        return 0.0
    
    total_bits = len_min * 8  # 1 Byte = 8 Bit
    bit_berubah = 0
    
    # Operasi XOR (^) untuk mendeteksi perbedaan posisi bit biner
    for b1, b2 in zip(cipher_bytes_1[:len_min], cipher_bytes_2[:len_min]):
        xor_result = b1 ^ b2
        bit_berubah += bin(xor_result).count('1')  # Menghitung bit bernilai '1' (yang berubah)
        
    return (bit_berubah / total_bits) * 100

# =======================================================
# 2. INISIALISASI ENVIRONMENT & PARAMETER REFF
# =======================================================
rsa_priv, rsa_pub = RSACryptosystem.generate_keys()
ecc_pub = ECCCryptosystem.generate_keys()

dataset_dir = 'dataset_plaintexts'
files = sorted([f for f in os.listdir(dataset_dir) if f.endswith(('.txt', '.csv', '.json'))])[:100]

tugas_8_results = []
print(f"Memproses {len(files)} file fisik Khusus Tugas 8 (Avalanche Effect)...")

for idx, file_name in enumerate(files, 1):
    file_path = os.path.join(dataset_dir, file_name)
    with open(file_path, 'rb') as f:
        plaintext = f.read()
        
    p_size = len(plaintext) / 1024.0 # Ukuran Plaintext (KB)
    
    # MANIPULASI BINER: Membalik tepat 1 bit di byte pertama (XOR dengan 1)
    plaintext_altered = bytearray(plaintext)
    if len(plaintext_altered) > 0:
        plaintext_altered[0] ^= 1  # Mengubah tepat 1 bit awal
    plaintext_altered = bytes(plaintext_altered)
    
    # --- ENKRIPSI CIPHERTEKS 1 (DATA ASLI) ---
    c_rsa = RSACryptosystem.encrypt(plaintext, rsa_pub)
    c_elgamal = ElGamalCryptosystem.encrypt(plaintext)
    c_ecc = ECCCryptosystem.encrypt(plaintext, ecc_pub)
    c_hybrid = HybridRSAAES.encrypt(plaintext, rsa_pub)
    
    # --- ENKRIPSI CIPHERTEKS 2 (DATA TERUBAH 1 BIT) ---
    c_rsa_alt = RSACryptosystem.encrypt(plaintext_altered, rsa_pub)
    c_elg_alt = ElGamalCryptosystem.encrypt(plaintext_altered)
    c_ecc_alt = ECCCryptosystem.encrypt(plaintext_altered, ecc_pub)
    c_hybrid_alt = HybridRSAAES.encrypt(plaintext_altered, rsa_pub)
    
    # --- HITUNG PERSENTASE AVALANCHE EFFECT ---
    tugas_8_results.append({
        'Id': idx,
        'Ukuran (KB)': round(p_size, 2),
        'RSA': round(hitung_avalanche_effect(c_rsa, c_rsa_alt), 2),
        'ELGamal': round(hitung_avalanche_effect(c_elgamal, c_elg_alt), 2),
        'ECC': round(hitung_avalanche_effect(c_ecc, c_ecc_alt), 2),
        'RSA-AES': round(hitung_avalanche_effect(c_hybrid, c_hybrid_alt), 2)
    })

# =======================================================
# 3. EXPORT HASIL DAN PENGHITUNGAN RATA-RATA AKHIR
# =======================================================
df_tugas_8 = pd.DataFrame(tugas_8_results)

# Membuat baris rata-rata sesuai format laporan LKM
avg_row = {
    'Id': 'Rata-Rata', 
    'Ukuran (KB)': round(df_tugas_8['Ukuran (KB)'].mean(), 2),
    'RSA': round(df_tugas_8['RSA'].mean(), 2), 
    'ELGamal': round(df_tugas_8['ELGamal'].mean(), 2), 
    'ECC': round(df_tugas_8['ECC'].mean(), 2), 
    'RSA-AES': round(df_tugas_8['RSA-AES'].mean(), 2)
}

df_tugas_8 = pd.concat([df_tugas_8, pd.DataFrame([avg_row])], ignore_index=True)

# Simpan hasil ke Excel khusus Tugas 8
output_excel = 'tugas_8_avalanche_lkm.xlsx'
df_tugas_8.to_excel(output_excel, index=False, sheet_name='Tugas 8 - Avalanche')

print("\n" + "="*60)
print(f"SUKSES! Data Tabel Tugas 8 selesai dievaluasi.")
print(f"Silakan buka file: '{output_excel}' untuk menyalin data.")
print("="*60)