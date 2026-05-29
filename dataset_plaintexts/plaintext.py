import os
import random

# Kumpulan kalimat bermakna agar isi file tetap logis dan bervariasi
base_sentences = [
    "Sistem kriptografi ini digunakan untuk mengamankan data sensitif dari akses yang tidak sah.",
    "Pengujian performa algoritma dilakukan dengan mengukur waktu eksekusi dan penggunaan memori.",
    "Proses enkripsi mengubah plaintext menjadi ciphertext menggunakan kunci rahasia tertentu.",
    "Analisis data skala besar memerlukan infrastruktur komputasi yang kuat dan efisien.",
    "Keamanan informasi menjadi pilar utama dalam pengembangan aplikasi berbasis web saat ini.",
    "Mahasiswa wajib memastikan variasi ukuran file dan isi data tidak boleh ada yang identik.",
    "Implementasi fungsi hash membantu menjaga integritas data dari manipulasi pihak ketiga.",
    "Kombinasi antara metode simetris dan asimetris menghasilkan sistem keamanan yang hibrida.",
    "Protokol jaringan bertugas mengatur komunikasi data antar perangkat agar berjalan lancar.",
    "Optimasi kode pemrograman dapat meningkatkan kecepatan pemrosesan data secara signifikan.",
    "The quick brown fox jumps over the lazy dog to test typography and rendering speeds.",
    "Data science combines statistical analysis, machine learning, and domain expertise to solve problems.",
    "Cloud computing provides scalable resources over the internet for modern applications.",
    "Artificial intelligence models require structured training datasets to improve accuracy.",
    "Software engineering principles emphasize clean code, documentation, and thorough testing."
]

def generate_meaningful_text(target_bytes):
    """Menghasilkan teks bermakna dengan ukuran mendekati target bytes"""
    lines = []
    current_bytes = 0
    sentences_pool = base_sentences.copy()
    random.shuffle(sentences_pool)
    
    while current_bytes < target_bytes:
        # Menambahkan angka acak di setiap baris agar hash / isi tiap file selalu unik
        line = f"[{random.randint(100000, 999999)}] " + " ".join(random.choices(sentences_pool, k=4)) + "\n"
        line_bytes = len(line.encode('utf-8'))
        lines.append(line)
        current_bytes += line_bytes
        
    return "".join(lines)

def main():
    # Folder output akan dibuat di dalam folder tempat skrip ini berada
    output_dir = "dataset_pengujian_total"
    os.makedirs(output_dir, exist_ok=True)
    
    # Semua rentang ukuran sudah dipastikan bertipe Integer (Aman untuk Python 3.14+)
    categories = [
        {"name": "Sangat_Kecil", "range": (int(1 * 1024), int(9 * 1024)), "count": 20},       # < 10 KB
        {"name": "Kecil", "range": (int(15 * 1024), int(95 * 1024)), "count": 20},          # 10 - 100 KB
        {"name": "Sedang", "range": (int(150 * 1024), int(950 * 1024)), "count": 20},        # 100 KB - 1 MB
        {"name": "Besar", "range": (int(1.5 * 1024 * 1024), int(4.5 * 1024 * 1024)), "count": 20},  # 1 - 5 MB
        {"name": "Sangat_Besar", "range": (int(5.5 * 1024 * 1024), int(7 * 1024 * 1024)), "count": 20} # > 5 MB
    ]
    
    file_counter = 1
    
    print("==================================================")
    print("Mulai membuat 100 file dataset dari awal (001 - 100)")
    print("==================================================")
    
    for cat in categories:
        print(f"\n[Kategori {cat['name']}] Sedang membuat {cat['count']} file...")
        for i in range(cat["count"]):
            target_size = random.randint(cat["range"][0], cat["range"][1])
            
            # Generate konten teks
            content = generate_meaningful_text(target_size)
            
            # Formatting nama file berdasarkan ukuran
            size_bytes = len(content.encode('utf-8'))
            if size_bytes >= 1024 * 1024:
                size_str = f"{size_bytes / (1024 * 1024):.2f}MB"
            else:
                size_str = f"{size_bytes / 1024:.2f}KB"
                
            file_name = f"file_{file_counter:03d}_{cat['name']}_{size_str}.txt"
            file_path = os.path.join(output_dir, file_name)
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
                
            file_counter += 1
            
        print(f"-> Kategori {cat['name']} Selesai!")

    print("\n==================================================")
    print(f"Sukses! 100 file utuh berhasil dibuat di: '{output_dir}'")
    print("==================================================")

if __name__ == "__main__":
    main()