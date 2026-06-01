import os
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from kripto_core import RSACryptosystem, ElGamalCryptosystem, ECCCryptosystem, HybridRSAAES

# 1. Inisialisasi Keypair awal untuk pengujian
rsa_priv, rsa_pub = RSACryptosystem.generate_keys()
ecc_pub = ECCCryptosystem.generate_keys()

dataset_dir = 'dataset_plaintexts'
os.makedirs(dataset_dir, exist_ok=True)

# Memastikan dataset 100 file siap
if len(os.listdir(dataset_dir)) == 0:
    for i in range(1, 101):
        with open(f"{dataset_dir}/file_{i}.txt", "wb") as f:
            f.write(os.urandom(i * 2 * 1024)) # Dummy file bervariasi ukuran

files = sorted([f for f in os.listdir(dataset_dir) if f.endswith(('.txt', '.csv', '.json'))])[:100]
results_log = []

print(f"Memproses {len(files)} file untuk komparasi Waktu & Ukuran...")

# 2. Proses Eksperimen dan Pencatatan Waktu (Perf Counter)
for idx, file_name in enumerate(files, 1):
    file_path = os.path.join(dataset_dir, file_name)
    with open(file_path, 'rb') as f:
        plaintext = f.read()
        
    p_size = len(plaintext) / 1024.0 # Ukuran Plaintext (KB)
    
    # --- PENGUJIAN RSA MURNI ---
    t0 = time.perf_counter()
    c_rsa = RSACryptosystem.encrypt(plaintext, rsa_pub)
    t1 = time.perf_counter()
    rsa_enc_time = (t1 - t0) * 1000 # Mengubah ke millisecond
    
    t0 = time.perf_counter()
    _ = RSACryptosystem.decrypt(c_rsa, rsa_priv)
    t1 = time.perf_counter()
    rsa_dec_time = (t1 - t0) * 1000
    
    # --- PENGUJIAN ELGAMAL MURNI ---
    t0 = time.perf_counter()
    c_elgamal = ElGamalCryptosystem.encrypt(plaintext)
    t1 = time.perf_counter()
    elg_enc_time = (t1 - t0) * 1000
    
    t0 = time.perf_counter()
    _ = ElGamalCryptosystem.decrypt(c_elgamal, rsa_priv)
    t1 = time.perf_counter()
    elg_dec_time = (t1 - t0) * 1000
    
    # --- PENGUJIAN ECC MURNI ---
    t0 = time.perf_counter()
    c_ecc = ECCCryptosystem.encrypt(plaintext, ecc_pub)
    t1 = time.perf_counter()
    ecc_enc_time = (t1 - t0) * 1000
    
    t0 = time.perf_counter()
    _ = ECCCryptosystem.decrypt(c_ecc, rsa_priv)
    t1 = time.perf_counter()
    ecc_dec_time = (t1 - t0) * 1000
    
    # --- PENGUJIAN HYBRID RSA-AES ---
    t0 = time.perf_counter()
    c_hybrid = HybridRSAAES.encrypt(plaintext, rsa_pub)
    t1 = time.perf_counter()
    hybrid_enc_time = (t1 - t0) * 1000
    
    t0 = time.perf_counter()
    _ = HybridRSAAES.decrypt(c_hybrid, rsa_priv)
    t1 = time.perf_counter()
    hybrid_dec_time = (t1 - t0) * 1000
    
    # Rekam data ke dalam dictionary log
    results_log.append({
        'Id': idx,
        'Plaintext_Size': round(p_size, 2),
        'RSA_Enc': round(rsa_enc_time, 4), 'RSA_Dec': round(rsa_dec_time, 4),
        'ElGamal_Enc': round(elg_enc_time, 4), 'ElGamal_Dec': round(elg_dec_time, 4),
        'ECC_Enc': round(ecc_enc_time, 4), 'ECC_Dec': round(ecc_dec_time, 4),
        'Hybrid_Enc': round(hybrid_enc_time, 4), 'Hybrid_Dec': round(hybrid_dec_time, 4)
    })

# 3. Penyusunan Dataframe dan Penghitungan Baris Rata-Rata
df_waktu = pd.DataFrame(results_log)

avg_row = {
    'Id': 'Rata-rata', 'Plaintext_Size': round(df_waktu['Plaintext_Size'].mean(), 2),
    'RSA_Enc': round(df_waktu['RSA_Enc'].mean(), 4), 'RSA_Dec': round(df_waktu['RSA_Dec'].mean(), 4),
    'ElGamal_Enc': round(df_waktu['ElGamal_Enc'].mean(), 4), 'ElGamal_Dec': round(df_waktu['ElGamal_Dec'].mean(), 4),
    'ECC_Enc': round(df_waktu['ECC_Enc'].mean(), 4), 'ECC_Dec': round(df_waktu['ECC_Dec'].mean(), 4),
    'Hybrid_Enc': round(df_waktu['Hybrid_Enc'].mean(), 4), 'Hybrid_Dec': round(df_waktu['Hybrid_Dec'].mean(), 4)
}

# Gabungkan baris rata-rata ke dataframe utama untuk diexport
df_waktu = pd.concat([df_waktu, pd.DataFrame([avg_row])], ignore_index=True)
df_waktu.to_csv('hasil_waktu_lkm_l6.csv', index=False)
df_waktu.to_excel('hasil_waktu_lkm_l6.xlsx', index=False)

print("\n" + "="*60)
print("NILAI RATA-RATA RUNTIME UNTUK BARIS BAWAH TABEL TUGAS 5")
print("="*60)
print(f"RSA      -> Enkripsi: {avg_row['RSA_Enc']} ms | Dekripsi: {avg_row['RSA_Dec']} ms")
print(f"ElGamal  -> Enkripsi: {avg_row['ElGamal_Enc']} ms | Dekripsi: {avg_row['ElGamal_Dec']} ms")
print(f"ECC      -> Enkripsi: {avg_row['ECC_Enc']} ms | Dekripsi: {avg_row['ECC_Dec']} ms")
print(f"Hybrid   -> Enkripsi: {avg_row['Hybrid_Enc']} ms | Dekripsi: {avg_row['Hybrid_Dec']} ms")
print("="*60 + "\n")

# =======================================================
# 4. GENERASI 4 GAMBAR GRAFIK SEPARASI BERPASANGAN
# =======================================================
sns.set_theme(style="whitegrid")

algorithms = {
    'RSA': {'enc': avg_row['RSA_Enc'], 'dec': avg_row['RSA_Dec'], 'color': '#e74c3c', 'filename': '5_waktu_rsa.png'},
    'ElGamal': {'enc': avg_row['ElGamal_Enc'], 'dec': avg_row['ElGamal_Dec'], 'color': '#3498db', 'filename': '5_waktu_elgamal.png'},
    'ECC': {'enc': avg_row['ECC_Enc'], 'dec': avg_row['ECC_Dec'], 'color': '#2ecc71', 'filename': '5_waktu_ecc.png'},
    'Hybrid RSA-AES': {'enc': avg_row['Hybrid_Enc'], 'dec': avg_row['Hybrid_Dec'], 'color': '#9b59b6', 'filename': '5_waktu_hybrid.png'}
}

for algo_name, info in algorithms.items():
    plt.figure(figsize=(7, 5))
    metrics = ['Waktu Enkripsi', 'Waktu Dekripsi']
    values = [info['enc'], info['dec']]
    
    ax = sns.barplot(x=metrics, y=values, palette=['#34495e', info['color']], width=0.4)
    
    plt.title(f'Rata-Rata Waktu Proses Komputasi:\n{algo_name}', fontsize=12, fontweight='bold')
    plt.ylabel('Waktu Proses (millisecond)', fontsize=11)
    plt.ylim(0, max(values) * 1.2) # Beri space di atas bar
    
    for p in ax.patches:
        ax.annotate(f"{p.get_height():.4f} ms", (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 8), textcoords='offset points', fontsize=10, fontweight='bold')
        
    plt.savefig(info['filename'], dpi=300, bbox_inches='tight')
    plt.show()
    print(f"Grafik waktu berhasil disimpan: {info['filename']}")