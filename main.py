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
avg_row = {
    'Id': 'Rata-rata',
    'Plaintext': round(df_hasil['Plaintext'].mean(), 2),
    'RSA': round(df_hasil['RSA'].mean(), 2),
    'ElGamal': round(df_hasil['ElGamal'].mean(), 2),
    'ECC': round(df_hasil['ECC'].mean(), 2),
    'RSA-AES': round(df_hasil['RSA-AES'].mean(), 2)
}
df_hasil = pd.concat([df_hasil, pd.DataFrame([avg_row])], ignore_index=True)
df_hasil.to_csv('hasil_ukuran_lkm_l6.csv', index=False)
df_hasil.to_excel('hasil_ukuran_lkm_l6.xlsx', index=False)
print("Eksperimen selesai! Data ukuran file telah direkam ke 'hasil_ukuran_lkm_l6.csv'.\n")

# =======================================================
# GENERASI GRAFIK PERBANDINGAN UKURAN (TUGAS 4)
# =======================================================
# Menghitung nilai rata-rata ukuran untuk grafik
avg_data = df_hasil[['Plaintext', 'RSA', 'ElGamal', 'ECC', 'RSA-AES']].mean()

plt.figure(figsize=(11, 6))
sns.set_theme(style="whitegrid")

# Buat grafik batang (Bar Chart)
colors = ['#7f8c8d', '#e74c3c', '#3498db', '#2ecc71', '#9b59b6']
ax = sns.barplot(x=avg_data.index, y=avg_data.values, palette=colors)

# Atur label dan judul grafik sesuai LKM
plt.title('Analisis Perbandingan Rata-Rata Ukuran Plaintext vs Ciphertext (Tugas 4)', fontsize=14, fontweight='bold')
plt.ylabel('Ukuran File Rata-Rata (KB)', fontsize=12)
plt.xlabel('Jenis Algoritma / Data', fontsize=12)

# Tambahkan angka nilai di atas bar masing-masing
for p in ax.patches:
    ax.annotate(f"{p.get_height():.2f} KB", (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', xytext=(0, 9), textcoords='offset points', fontsize=11, fontweight='bold')

# Simpan grafik sebagai file gambar PNG
plt.savefig('grafik_perbandingan_ukuran_lkm.png', dpi=300, bbox_inches='tight')
plt.show()

# =======================================================
# GENERASI GRAFIK PERBANDINGAN BERPASANGAN (TUGAS 4)
# =======================================================
sns.set_theme(style="whitegrid")

# Ambil nilai rata-rata dari dict avg_row yang sudah kamu buat
p_avg = avg_row['Plaintext']
algorithms = {
    'RSA': {'val': avg_row['RSA'], 'color': '#e74c3c', 'filename': '1_perbandingan_plain_rsa.png'},
    'ElGamal': {'val': avg_row['ElGamal'], 'color': '#3498db', 'filename': '2_perbandingan_plain_elgamal.png'},
    'ECC': {'val': avg_row['ECC'], 'color': '#2ecc71', 'filename': '3_perbandingan_plain_ecc.png'},
    'RSA-AES': {'val': avg_row['RSA-AES'], 'color': '#9b59b6', 'filename': '4_perbandingan_plain_rsa_aes.png'}
}

# Lakukan perulangan untuk membuat 4 grafik terpisah
for algo_name, info in algorithms.items():
    plt.figure(figsize=(7, 5))
    
    # Data pasangannya (Plain vs Algoritma Spesifik)
    categories = ['Plaintext', f'Ciphertext {algo_name}']
    values = [p_avg, info['val']]
    
    # Plot diagram batang
    ax = sns.barplot(x=categories, y=values, palette=['#7f8c8d', info['color']], width=0.5)
    
    # Kustomisasi teks dan judul
    plt.title(f'Perbandingan Rata-Rata Ukuran:\nPlaintext vs {algo_name}', fontsize=12, fontweight='bold')
    plt.ylabel('Ukuran File (KB)', fontsize=11)
    plt.ylim(0, max(values) * 1.15) # Beri ruang di atas bar untuk label angka
    
    # Tambahkan angka presisi di atas masing-masing batang
    for p in ax.patches:
        ax.annotate(f"{p.get_height():.2f} KB", (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 8), textcoords='offset points', fontsize=10, fontweight='bold')
    
    # Simpan masing-masing gambar ke storage Colab
    plt.savefig(info['filename'], dpi=300, bbox_inches='tight')
    plt.show()
    print(f"Berhasil menyimpan: {info['filename']}")

print("\nSemua 4 grafik berpasangan siap diunduh untuk LKM!")