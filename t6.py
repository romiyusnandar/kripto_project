import os
import math
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from kripto_core import RSACryptosystem, ECCCryptosystem

# 1. Fungsi Matematis untuk Menghitung Entropi Shannon
def hitung_entropi_shannon(data_bytes):
    if not data_bytes:
        return 0.0
    
    # Hitung frekuensi kemunculan setiap nilai byte (0-255)
    frekuensi = {}
    for b in data_bytes:
        frekuensi[b] = frekuensi.get(b, 0) + 1
        
    total_bytes = len(data_bytes)
    entropi = 0.0
    
    # Terapkan Rumus Shannon Entropy: H(X) = -sum(P(x) * log2(P(x)))
    for count in frekuensi.values():
        p_x = count / total_bytes
        entropi -= p_x * math.log2(p_x)
        
    return entropi

# 2. Inisialisasi Environment & Keypair
rsa_priv, rsa_pub = RSACryptosystem.generate_keys()
ecc_pub = ECCCryptosystem.generate_keys()

dataset_dir = 'dataset_plaintexts'
files = sorted([f for f in os.listdir(dataset_dir) if f.endswith(('.txt', '.csv', '.json'))])[:100]

entropy_log = []
print(f"Menghitung nilai entropi Shannon pada {len(files)} file...")

# 3. Proses Perulangan 100 File
for idx, file_name in enumerate(files, 1):
    file_path = os.path.join(dataset_dir, file_name)
    with open(file_path, 'rb') as f:
        plaintext_bytes = f.read()
        
    # Eksekusi Enkripsi untuk RSA dan ECC
    ciphertext_rsa = RSACryptosystem.encrypt(plaintext_bytes, rsa_pub)
    ciphertext_ecc = ECCCryptosystem.encrypt(plaintext_bytes, ecc_pub)
    
    # Hitung Entropi Shannon masing-masing
    h_plain = hitung_entropi_shannon(plaintext_bytes)
    h_rsa = hitung_entropi_shannon(ciphertext_rsa)
    h_ecc = hitung_entropi_shannon(ciphertext_ecc)
    
    # Rekam hasil ke log
    entropy_log.append({
        'Id': idx,
        'Entropi_Plaintext': round(h_plain, 4),
        'Entropi_RSA': round(h_rsa, 4),
        'Entropi_ECC': round(h_ecc, 4)
    })

# 4. Pembuatan Dataframe & Baris Rata-Rata
df_entropy = pd.DataFrame(entropy_log)

avg_row = {
    'Id': 'Rata-rata',
    'Entropi_Plaintext': round(df_entropy['Entropi_Plaintext'].mean(), 4),
    'Entropi_RSA': round(df_entropy['Entropi_RSA'].mean(), 4),
    'Entropi_ECC': round(df_entropy['Entropi_ECC'].mean(), 4)
}

# Gabungkan baris rata-rata dan export berkas data
df_entropy = pd.concat([df_entropy, pd.DataFrame([avg_row])], ignore_index=True)
df_entropy.to_csv('hasil_entropi_lkm_l6.csv', index=False)

print("\n" + "="*55)
print("NILAI RATA-RATA ENTROPI UNTUK BARIS BAWAH TABEL TUGAS 6")
print("="*55)
print(f"Rata-Rata Entropi Plaintext       : {avg_row['Entropi_Plaintext']} bit")
print(f"Rata-Rata Entropi Ciphertext RSA  : {avg_row['Entropi_RSA']} bit")
print(f"Rata-Rata Entropi Ciphertext ECC  : {avg_row['Entropi_ECC']} bit")
print("="*55 + "\n")

# =======================================================
# 5. GENERASI GRAFIK SEPARASI BERPASANGAN (TUGAS 6)
# =======================================================
sns.set_theme(style="whitegrid")

# Grafik Pasangan 1: Plaintext vs RSA
plt.figure(figsize=(7, 5))
ax1 = sns.barplot(x=['Plaintext', 'Ciphertext RSA'], 
                  y=[avg_row['Entropi_Plaintext'], avg_row['Entropi_RSA']], 
                  palette=['#7f8c8d', '#e74c3c'], width=0.4)
plt.title('Perbandingan Rata-Rata Ukuran Entropi:\nPlaintext vs RSA', fontsize=12, fontweight='bold')
plt.ylabel('Nilai Entropi (bit)', fontsize=11)
plt.ylim(0, 9.5)
for p in ax1.patches:
    ax1.annotate(f"{p.get_height():.4f} bit", (p.get_x() + p.get_width() / 2., p.get_height()),
                 ha='center', va='center', xytext=(0, 8), textcoords='offset points', fontsize=10, fontweight='bold')
plt.savefig('6_entropi_plain_vs_rsa.png', dpi=300, bbox_inches='tight')
plt.show()

# Grafik Pasangan 2: Plaintext vs ECC
plt.figure(figsize=(7, 5))
ax2 = sns.barplot(x=['Plaintext', 'Ciphertext ECC'], 
                  y=[avg_row['Entropi_Plaintext'], avg_row['Entropi_ECC']], 
                  palette=['#7f8c8d', '#2ecc71'], width=0.4)
plt.title('Perbandingan Rata-Rata Ukuran Entropi:\nPlaintext vs ECC', fontsize=12, fontweight='bold')
plt.ylabel('Nilai Entropi (bit)', fontsize=11)
plt.ylim(0, 9.5)
for p in ax2.patches:
    ax2.annotate(f"{p.get_height():.4f} bit", (p.get_x() + p.get_width() / 2., p.get_height()),
                 ha='center', va='center', xytext=(0, 8), textcoords='offset points', fontsize=10, fontweight='bold')
plt.savefig('6_entropi_plain_vs_ecc.png', dpi=300, bbox_inches='tight')
plt.show()