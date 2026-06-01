import os
import math
import numpy as np
import pandas as pd
from scipy.stats import pearsonr
from kripto_core import RSACryptosystem, ElGamalCryptosystem, ECCCryptosystem, HybridRSAAES

# =======================================================
# 1. FUNGSI TEKNIS EVALUASI DATA
# =======================================================

def hitung_shannon_entropy(data_bytes):
    if not data_bytes:
        return 0.0
    freq = {}
    for b in data_bytes:
        freq[b] = freq.get(b, 0) + 1
    entropy = 0.0
    total = len(data_bytes)
    for count in freq.values():
        p = count / total
        entropy -= p * math.log2(p)
    return entropy

def hitung_pearson_correlation(plain_bytes, cipher_bytes):
    len_min = min(len(plain_bytes), len(cipher_bytes))
    if len_min < 2:
        return 0.0
    arr_plain = np.frombuffer(plain_bytes[:len_min], dtype=np.uint8)
    arr_cipher = np.frombuffer(cipher_bytes[:len_min], dtype=np.uint8)
    corr, _ = pearsonr(arr_plain, arr_cipher)
    return 0.0 if np.isnan(corr) else corr

def hitung_avalanche_effect(cipher_bytes_1, cipher_bytes_2):
    len_min = min(len(cipher_bytes_1), len(cipher_bytes_2))
    if len_min == 0:
        return 0.0
    total_bits = len_min * 8
    bit_berubah = 0
    for b1, b2 in zip(cipher_bytes_1[:len_min], cipher_bytes_2[:len_min]):
        xor_result = b1 ^ b2
        bit_berubah += bin(xor_result).count('1')
    return (bit_berubah / total_bits) * 100

# =======================================================
# 2. INISIALISASI ENVIRONMENT & PARAMETER REFF KODE KAMU
# =======================================================
rsa_priv, rsa_pub = RSACryptosystem.generate_keys()
ecc_pub = ECCCryptosystem.generate_keys()

dataset_dir = 'dataset_plaintexts'
files = sorted([f for f in os.listdir(dataset_dir) if f.endswith(('.txt', '.csv', '.json'))])[:100]

eval_results = []
print(f"Membaca {len(files)} file fisik dari '{dataset_dir}'...")

# Loop memproses file yang sama persis dengan Tugas Waktu & Ukuran
for idx, file_name in enumerate(files, 1):
    file_path = os.path.join(dataset_dir, file_name)
    with open(file_path, 'rb') as f:
        plaintext = f.read()
        
    p_size = len(plaintext) / 1024.0
    
    # Payload simulasi modifikasi bit (Balikan bit terakhir pada byte pertama) untuk Avalanche
    plaintext_altered = bytearray(plaintext)
    if len(plaintext_altered) > 0:
        plaintext_altered[0] ^= 1
    plaintext_altered = bytes(plaintext_altered)
    
    # --- PROSES ENKRIPSI DATA ASLI ---
    c_rsa = RSACryptosystem.encrypt(plaintext, rsa_pub)
    c_elgamal = ElGamalCryptosystem.encrypt(plaintext)
    c_ecc = ECCCryptosystem.encrypt(plaintext, ecc_pub)
    c_hybrid = HybridRSAAES.encrypt(plaintext, rsa_pub)
    
    # --- PROSES ENKRIPSI DATA TERUBAH 1 BIT ---
    c_rsa_alt = RSACryptosystem.encrypt(plaintext_altered, rsa_pub)
    c_elg_alt = ElGamalCryptosystem.encrypt(plaintext_altered)
    c_ecc_alt = ECCCryptosystem.encrypt(plaintext_altered, ecc_pub)
    c_hybrid_alt = HybridRSAAES.encrypt(plaintext_altered, rsa_pub)
    
    # --- PENILAIAN EVALUASI METRIKS ---
    eval_results.append({
        'Id': idx,
        'Ukuran (KB)': round(p_size, 2),
        'Entropi Plaintext': round(hitung_shannon_entropy(plaintext), 4),
        'Entropi RSA': round(hitung_shannon_entropy(c_rsa), 4),
        'Entropi ElGamal': round(hitung_shannon_entropy(c_elgamal), 4),
        'Entropi ECC': round(hitung_shannon_entropy(c_ecc), 4),
        'Entropi Hybrid': round(hitung_shannon_entropy(c_hybrid), 4),
        
        'Korelasi RSA': round(hitung_pearson_correlation(plaintext, c_rsa), 6),
        'Korelasi ElGamal': round(hitung_pearson_correlation(plaintext, c_elgamal), 6),
        'Korelasi ECC': round(hitung_pearson_correlation(plaintext, c_ecc), 6),
        'Korelasi Hybrid': round(hitung_pearson_correlation(plaintext, c_hybrid), 6),
        
        'Avalanche RSA (%)': round(hitung_avalanche_effect(c_rsa, c_rsa_alt), 2),
        'Avalanche ElGamal (%)': round(hitung_avalanche_effect(c_elgamal, c_elg_alt), 2),
        'Avalanche ECC (%)': round(hitung_avalanche_effect(c_ecc, c_ecc_alt), 2),
        'Avalanche Hybrid (%)': round(hitung_avalanche_effect(c_hybrid, c_hybrid_alt), 2),
    })

# =======================================================
# 3. EXPORT HASIL DAN PENGHITUNGAN RATA-RATA AKHIR
# =======================================================
df_eval = pd.DataFrame(eval_results)

# Membuat baris rata-rata numerik eksplisit
avg_metrics = df_eval.mean().to_dict()
avg_metrics['Id'] = 'Rata-rata'

df_eval = pd.concat([df_eval, pd.DataFrame([avg_metrics])], ignore_index=True)

# Tulis ke file spreadsheet Excel tunggal
output_excel = 'hasil_evaluasi_lkm_l6.xlsx'
df_eval.to_excel(output_excel, index=False, sheet_name='Metriks Keamanan')

print("\n" + "="*60)
print(f"SUKSES! 100 berkas fisik dievaluasi secara linier.")
print(f"Output disimpan pada: {output_excel}")
print("="*60)