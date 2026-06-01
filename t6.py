import os
import math
import pandas as pd
from kripto_core import RSACryptosystem, ElGamalCryptosystem, ECCCryptosystem, HybridRSAAES

# =======================================================
# 1. FUNGSI KHUSUS TUGAS 6 — SHANNON ENTROPY
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

# =======================================================
# 2. INISIALISASI ENVIRONMENT & GENERATE KEYPAIR
# =======================================================
rsa_priv, rsa_pub = RSACryptosystem.generate_keys()
ecc_pub = ECCCryptosystem.generate_keys()

dataset_dir = 'dataset_plaintexts'
files = sorted([f for f in os.listdir(dataset_dir) if f.endswith(('.txt', '.csv', '.json'))])[:100]

tugas_6_results = []
print(f"Memproses {len(files)} file fisik dari '{dataset_dir}' Khusus Tugas 6 (Entropi)...")

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
    
    # --- PENCATATAN NILAI ENTROPI (TUGAS 6) ---
    tugas_6_results.append({
        'Id': idx,
        'Ukuran (KB)': round(p_size, 2),
        'Ukuran Entropi (bit)': round(hitung_shannon_entropy(plaintext), 4),
        'RSA': round(hitung_shannon_entropy(c_rsa), 4),
        'ELGamal': round(hitung_shannon_entropy(c_elgamal), 4),
        'ECC': round(hitung_shannon_entropy(c_ecc), 4),
        'RSA-AES': round(hitung_shannon_entropy(c_hybrid), 4)
    })

# =======================================================
# 3. EXPORT HASIL DAN PENGHITUNGAN RATA-RATA AKHIR
# =======================================================
df_tugas_6 = pd.DataFrame(tugas_6_results)

# Membuat baris rata-rata sesuai format LKM
avg_row = {
    'Id': 'Rata-Rata', 
    'Ukuran (KB)': round(df_tugas_6['Ukuran (KB)'].mean(), 2),
    'Ukuran Entropi (bit)': round(df_tugas_6['Ukuran Entropi (bit)'].mean(), 4),
    'RSA': round(df_tugas_6['RSA'].mean(), 4), 
    'ELGamal': round(df_tugas_6['ELGamal'].mean(), 4), 
    'ECC': round(df_tugas_6['ECC'].mean(), 4), 
    'RSA-AES': round(df_tugas_6['RSA-AES'].mean(), 4)
}

df_tugas_6 = pd.concat([df_tugas_6, pd.DataFrame([avg_row])], ignore_index=True)

# Simpan hasil ke Excel khusus Tugas 6
output_excel = 'tugas_6_entropi_lkm.xlsx'
df_tugas_6.to_excel(output_excel, index=False, sheet_name='Tugas 6 - Entropi')

print("\n" + "="*60)
print(f"SUKSES! Data Tabel Tugas 6 selesai dievaluasi.")
print(f"Silakan buka file: '{output_excel}' untuk menyalin data.")
print("="*60)