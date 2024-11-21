# 📚 **Implementasi Pengiriman Kunci DES Menggunakan RSA dalam Lingkungan Client-Server**

![Status](https://img.shields.io/badge/Status-Tugas_Selesai-brightgreen?style=flat-square)
![Tipe](https://img.shields.io/badge/Tipe-Tugas_Keamanan_Informasi-blue?style=flat-square)

Proyek ini menunjukkan sistem komunikasi aman menggunakan model kriptografi hibrid. RSA digunakan untuk pertukaran kunci DES yang aman, dan DES digunakan untuk mengenkripsi pesan antara client dan server. Implementasi ini dilakukan tanpa menggunakan library kriptografi eksternal untuk tujuan pembelajaran.

## 👥 **Anggota Kelompok**

| Nama                        | NRP        |
| --------------------------- | ---------- |
| **RIYANDA CAVIN SINAMBELA** | 5025221100 |

## Fitur

- **RSA untuk Pertukaran Kunci yang Aman**: Kriptografi kunci publik memastikan kunci DES ditransmisikan secara aman.
- **DES untuk Enkripsi Pesan**: Enkripsi simetris digunakan untuk mengamankan komunikasi.
- **Model Client-Server Ringan**: Termasuk autentikasi dasar dan pengiriman pesan yang aman.
- **Implementasi Kriptografi Kustom**: RSA dan DES diimplementasikan secara manual untuk tujuan pembelajaran.

## Cara Kerja

1. **Pembuatan Kunci RSA**: Server menghasilkan pasangan kunci RSA (public dan private key).
2. **Distribusi Public Key**: Server membagikan public key-nya kepada client.
3. **Enkripsi Kunci DES**: Client mengenkripsi kunci DES menggunakan public key server.
4. **Dekripsi Kunci DES**: Server mendekripsi kunci DES menggunakan private key-nya.
5. **Enkripsi/Dekripsi Pesan**: Kedua pihak menggunakan kunci DES untuk mengamankan pesan yang dikirim.

## Teknologi yang Digunakan

- **Bahasa Pemrograman**: Python
- **Pustaka yang Digunakan**: Tidak ada (implementasi kustom untuk RSA dan DES)

## Struktur File

- `client.py`: Mengelola operasi sisi client, termasuk enkripsi RSA dan komunikasi berbasis DES.
- `server.py`: Mengelola operasi sisi server, termasuk pembuatan kunci RSA, dekripsi DES, dan pengiriman pesan yang aman.
- `library.py`: Menyediakan fungsi bantu untuk enkripsi dan dekripsi.
- `des.py`: Berisi implementasi algoritma enkripsi DES.
- `logic.py`: Termasuk logika pendukung untuk operasi kriptografi.

## Cara Menjalankan Proyek

1. Clone repository ini:

   ```bash
   git clone https://github.com/rcsinambela/Implementing-DES-Key-Exchange-via-RSA-in-a-Client-Server-Environment
   ```

2. Masuk ke direktori proyek:

   ```bash
   cd Implementing-DES-Key-Exchange-via-RSA-in-a-Client-Server-Environment
   ```

3. Jalankan server:

   ```bash
   python server.py
   ```

4. Jalankan client di terminal lain:

   ```bash
   python client.py
   ```
