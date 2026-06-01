import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from kripto_core import RSACryptosystem, ElGamalCryptosystem, ECCCryptosystem, HybridRSAAES

# 1. Inisialisasi Keypair awal
rsa_priv, rsa_pub = RSACryptosystem.generate_keys()
ecc_pub = ECCCryptosystem.generate_keys()

# Pastikan folder dataset tersedia (Simulasi 100 file jika belum di-clone dari Github)
dataset_dir = 'dataset_plaintexts'
os.makedirs(dataset_dir, exist_ok=True)
if len(os.listdir(dataset_dir)) == 0:
    for i in range(1, 101):
        with open(f"{dataset_dir}/file_{i}.txt", "wb") as f:
            # Membuat variasi ukuran file dari 1 KB hingga 200 KB agar grafiknya terlihat kontras
            f.write(os.urandom(i * 2 * 1024))

# 2. Proses Eksperimen 100 File
files = sorted([f for f in os.listdir(dataset_dir) if f.endswith(('.txt', '.csv', '.json'))])[:100]
results_log = []

print(f"Memproses {len(files)} file untuk komparasi 4 algoritma...")

for idx, file_name in enumerate(files, 1):
    file_path = os.path.join(dataset_dir, file_name)
    with open(file_path, 'rb') as f:
        plaintext = f.read()
        
    p_size = len(plaintext) / 1024.0 # Satuan Kilobytes (KB)
    
    # Enkripsi ke masing-masing algoritma untuk mengukur ukuran hasil (Ciphertext)
    c_rsa = RSACryptosystem.encrypt(plaintext, rsa_pub)
    c_elgamal = ElGamalCryptosystem.encrypt(plaintext)
    c_ecc = ECCCryptosystem.encrypt(plaintext, ecc_pub)
    c_hybrid = HybridRSAAES.encrypt(plaintext, rsa_pub)
    
    # Catat data ukuran file (KB)
    results_log.append({
        'Id': idx,
        'Plaintext': round(p_size, 2),
        'RSA': round(len(c_rsa) / 1024.0, 2),
        'ElGamal': round(len(c_elgamal) / 1024.0, 2),
        'ECC': round(len(c_ecc) / 1024.0, 2),
        'RSA-AES': round(len(c_hybrid) / 1024.0, 2)
    })

# Simpan hasil log ke dalam Dataframe & CSV
df_hasil = pd.DataFrame(results_log)
df_hasil.to_csv('hasil_ukuran_lkm_l6.csv', index=False)
print("Eksperimen selesai! Data ukuran file telah direkam ke 'hasil_ukuran_lkm_l6.csv'.\n")
