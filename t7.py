import os
import numpy as np
import pandas as pd
from scipy.stats import pearsonr
from kripto_core import RSACryptosystem, ElGamalCryptosystem, ECCCryptosystem, HybridRSAAES

# =======================================================
# 1. FUNGSI KHUSUS TUGAS 7 — PEARSON CORRELATION
# =======================================================
def hitung_pearson_correlation(plain_bytes, cipher_bytes):
    """
    Menghitung koefisien korelasi Pearson antara array biner plaintext & ciphertext.
    Array diselaraskan berdasarkan panjang minimum untuk menghindari dimensi mismatch.
    """
    len_min = min(len(plain_bytes), len(cipher_bytes))
    if len_min < 2:
        return 0.0
    
    # Mengonversi byte stream mentah ke representasi array numerik 8-bit (0-255)
    arr_plain = np.frombuffer(plain_bytes[:len_min], dtype=np.uint8)
    arr_cipher = np.frombuffer(cipher_bytes[:len_min], dtype=np.uint8)
    
    # Menghitung koefisien korelasi pearson (r)
    corr, _ = pearsonr(arr_plain, arr_cipher)
    
    # Mengembalikan 0 jika hasil komputasi menghasilkan nilai NaN (Not a Number)
    return 0.0 if np.isnan(corr) else corr

# =======================================================
# 2. INISIALISASI ENVIRONMENT & GENERATE KEYPAIR
# =======================================================
rsa_priv, rsa_pub = RSACryptosystem.generate_keys()
ecc_pub = ECCCryptosystem.generate_keys()

dataset_dir = 'dataset_plaintexts'
files = sorted([f for f in os.listdir(dataset_dir) if f.endswith(('.txt', '.csv', '.json'))])[:100]

tugas_7_results = []
print(f"Memproses {len(files)} file fisik dari '{dataset_dir}' Khusus Tugas 7 (Korelasi Pearson)...")

# Loop memproses file yang sama persis dengan dataset utama
for idx, file_name in enumerate(files, 1):
    file_path = os.path.join(dataset_dir, file_name)
    with open(file_path, 'rb') as f:
        plaintext = f.read()
        
    p_size = len(plaintext) / 1024.0 # Ukuran Plaintext (KB)
    
    # --- PROSES ENKRIPSI DATA ASLI ---
    c_rsa = RSACryptosystem.encrypt(plaintext, rsa_pub)
    c_elgamal = ElGamalCryptosystem.encrypt(plaintext)
    c_ecc = ECCCryptosystem.encrypt(plaintext, ecc_pub)
    c_hybrid = HybridRSAAES.encrypt(plaintext, rsa_pub)
    
    # --- PENCATATAN NILAI KORELASI (TUGAS 7) ---
    tugas_7_results.append({
        'Id': idx,
        'Ukuran (KB)': round(p_size, 2),
        'RSA': round(hitung_pearson_correlation(plaintext, c_rsa), 6),
        'ELGamal': round(hitung_pearson_correlation(plaintext, c_elgamal), 6),
        'ECC': round(hitung_pearson_correlation(plaintext, c_ecc), 6),
        'RSA-AES': round(hitung_pearson_correlation(plaintext, c_hybrid), 6)
    })

# =======================================================
# 3. EXPORT HASIL DAN PENGHITUNGAN RATA-RATA AKHIR
# =======================================================
df_tugas_7 = pd.DataFrame(tugas_7_results)

# Membuat baris rata-rata sesuai format LKM kamu
avg_row = {
    'Id': 'Rata-Rata', 
    'Ukuran (KB)': round(df_tugas_7['Ukuran (KB)'].mean(), 2),
    'RSA': round(df_tugas_7['RSA'].mean(), 6), 
    'ELGamal': round(df_tugas_7['ELGamal'].mean(), 6), 
    'ECC': round(df_tugas_7['ECC'].mean(), 6), 
    'RSA-AES': round(df_tugas_7['RSA-AES'].mean(), 6)
}

df_tugas_7 = pd.concat([df_tugas_7, pd.DataFrame([avg_row])], ignore_index=True)

# Simpan hasil ke Excel khusus Tugas 7
output_excel = 'tugas_7_korelasi_lkm.xlsx'
df_tugas_7.to_excel(output_excel, index=False, sheet_name='Tugas 7 - Korelasi')

print("\n" + "="*60)
print(f"SUKSES! Data Tabel Tugas 7 selesai dievaluasi.")
print(f"Silakan buka file: '{output_excel}' untuk menyalin data.")
print("="*60)