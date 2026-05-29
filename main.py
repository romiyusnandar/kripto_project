import os
import time
import pandas as pd
from kripto_core import RSACryptosystem, ElGamalCryptosystem, ECCCryptosystem, HybridRSAAES

# Buat direktori output jika belum ada
os.makedirs('output_ciphertexts', exist_ok=True)

# Inisialisasi Keypair masing-masing skema 
rsa_priv, rsa_pub = RSACryptosystem.generate_keys()
elg_priv, elg_pub = ElGamalCryptosystem.generate_keys()
ecc_priv, ecc_pub = ECCCryptosystem.generate_keys()

# List penampung data evaluasi kuantitatif [cite: 31]
log_data = []

# Ambil 100 file dari direktori dataset 
dataset_dir = 'dataset_plaintexts'
files = sorted([f for f in os.listdir(dataset_dir) if f.endswith(('.txt', '.json', '.csv'))])[:100] [cite: 43, 66]

print(f"Memulai pemrosesan {len(files)} file plainteks...\n")

for idx, file_name in enumerate(files, 1):
    file_path = os.path.join(dataset_dir, file_name)
    
    with open(file_path, 'rb') as f:
        plaintext = f.read()
        
    p_size_kb = len(plaintext) / 1024.0 # Ukuran Plainteks (KB)
    
    # --- PENGUJIAN HYBRID RSA-AES ---
    t0 = time.perf_counter()
    c_hybrid = HybridRSAAES.encrypt(plaintext, rsa_pub)
    t1 = time.perf_counter()
    enc_time_hybrid = (t1 - t0) * 1000 # convert ke millisecond
    
    t2 = time.perf_counter()
    p_dec_hybrid = HybridRSAAES.decrypt(c_hybrid, rsa_priv)
    t3 = time.perf_counter()
    dec_time_hybrid = (t3 - t2) * 1000
    
    # Simpan hasil cipherteks ke disk 
    out_path = f"output_ciphertexts/{file_name}_hybrid.enc"
    with open(out_path, 'wb') as out_f:
        out_f.read(c_hybrid) if hasattr(c_hybrid, 'read') else out_f.write(c_hybrid) 
        
    c_size_hybrid_kb = len(c_hybrid) / 1024.0

    # Eksekusi untuk algoritma lainnya (RSA murni, ElGamal murni, ECC murni) 
    # Catatan: Masukkan logic try-except jika file berukuran besar (>100KB) membuat RSA murni crash 
    
    # Append records untuk dataframe analisis
    log_data.append({
        'Id': idx,
        'Ukuran Plaintext (KB)': round(p_size_kb, 2),
        'Enc Time Hybrid (ms)': round(enc_time_hybrid, 4),
        'Dec Time Hybrid (ms)': round(dec_time_hybrid, 4),
        'Cipher Size Hybrid (KB)': round(c_size_hybrid_kb, 2)
    })

# Konversi log ke Dataframe & Simpan ke CSV untuk bahan grafik spreadsheet
df_hasil = pd.DataFrame(log_data)
df_hasil.to_csv('hasil_pengujian_kripto.csv', index=False)
print("\nPengujian Selesai! File 'hasil_pengujian_kripto.csv' berhasil dibuat.")