import hashlib
import csv
import os

# Database sederhana untuk menyimpan user dan perannya
users = {
    'supervisor': {'password': hashlib.sha256('supervisorpass'.encode()).hexdigest(), 'role': 'Supervisor'},
    'admin': {'password': hashlib.sha256('adminpass'.encode()).hexdigest(), 'role': 'Administrator'},
    'operator': {'password': hashlib.sha256('operatorpass'.encode()).hexdigest(), 'role': 'Operator'}
}

# Nama file CSV untuk menyimpan data
sales_data_file = 'sales_data.csv'
inventory_data_file = 'inventory_data.csv'

# Fungsi untuk memuat data dari file CSV
def load_csv_data(file):
    data = []
    if os.path.exists(file):
        with open(file, mode='r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
    return data

# Fungsi untuk menyimpan data ke file CSV
def save_csv_data(file, data, fieldnames):
    with open(file, mode='w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

# Memuat data penjualan dan inventori dari CSV
sales_data = load_csv_data(sales_data_file)
inventory_data = load_csv_data(inventory_data_file)

# Fungsi untuk login user
def login():
    print("=== Sistem Login ===")
    username = input("Masukkan username: ")
    password = input("Masukkan password: ")
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    if username in users and users[username]['password'] == password_hash:
        print(f"\nLogin berhasil! Selamat datang, {username}.\n")
        return users[username]['role']
    else:
        print("Login gagal! Username atau password salah.\n")
        return None

# Fungsi untuk menambah user (hanya Administrator yang memiliki akses)
def tambah_user():
    print("\n=== Tambah User Baru ===")
    new_username = input("Masukkan username baru: ")
    new_password = input("Masukkan password baru: ")
    new_role = input("Masukkan role (Supervisor/Administrator/Operator): ")

    if new_role not in ['Supervisor', 'Administrator', 'Operator']:
        print("Role tidak valid. Gagal menambah user.\n")
        return

    password_hash = hashlib.sha256(new_password.encode()).hexdigest()
    users[new_username] = {'password': password_hash, 'role': new_role}
    print(f"User {new_username} berhasil ditambahkan dengan role {new_role}.\n")

# Fungsi untuk menghapus user (hanya Administrator yang memiliki akses)
def hapus_user():
    print("\n=== Hapus User ===")
    del_username = input("Masukkan username yang ingin dihapus: ")

    if del_username in users:
        del users[del_username]
        print(f"User {del_username} berhasil dihapus.\n")
    else:
        print("User tidak ditemukan.\n")

# Fungsi halaman Supervisor
def halaman_supervisor():
    print("=== Halaman Supervisor ===")
    print("1. Lihat Laporan Penjualan")
    print("2. Analisis Total Transaksi")
    pilihan = input("Pilih opsi: ")
    if pilihan == "1":
        lihat_laporan_penjualan()
    elif pilihan == "2":
        analisis_total_transaksi()
    else:
        print("Opsi tidak valid.\n")

# Fungsi untuk melihat laporan penjualan
def lihat_laporan_penjualan():
    if not sales_data:
        print("Belum ada data penjualan.\n")
    else:
        print("Laporan Penjualan:")
        for sale in sales_data:
            print(f"Pembeli: {sale['pembeli']}, Barang: {sale['barang']}, Jumlah: {sale['jumlah']}, Total: Rp{sale['total']}")
        print()

# Fungsi untuk analisis total transaksi
def analisis_total_transaksi():
    total_transaksi = sum(float(sale['total']) for sale in sales_data)
    print(f"Total transaksi penjualan: Rp{total_transaksi}\n")

# Fungsi halaman Administrator
def halaman_administrator():
    print("=== Halaman Administrator ===")
    print("1. Tambah User")
    print("2. Hapus User")
    print("3. Analisis Aktivitas User")
    pilihan = input("Pilih opsi: ")
    if pilihan == "1":
        tambah_user()
    elif pilihan == "2":
        hapus_user()
    elif pilihan == "3":
        analisis_user_aktif()
    else:
        print("Opsi tidak valid.\n")

# Fungsi untuk analisis user yang aktif
def analisis_user_aktif():
    print(f"Total user yang terdaftar: {len(users)}")
    for username, info in users.items():
        print(f"Username: {username}, Role: {info['role']}")
    print()

# Fungsi halaman Operator
def halaman_operator():
    print("=== Halaman Operator ===")
    print("1. Masukkan Data Penjualan")
    print("2. Kelola Inventori")
    pilihan = input("Pilih opsi: ")
    if pilihan == "1":
        masukkan_data_penjualan()
    elif pilihan == "2":
        kelola_inventori()
    else:
        print("Opsi tidak valid.\n")

# Fungsi untuk memasukkan data penjualan
def masukkan_data_penjualan():
    pembeli = input("Masukkan nama pembeli: ")
    barang = input("Masukkan nama barang: ")
    jumlah = int(input("Masukkan jumlah barang: "))
    total = float(input("Masukkan total harga: "))

    sales_data.append({
        'pembeli': pembeli,
        'barang': barang,
        'jumlah': jumlah,
        'total': total
    })
    save_csv_data(sales_data_file, sales_data, ['pembeli', 'barang', 'jumlah', 'total'])
    print("Data penjualan berhasil disimpan!\n")

# Fungsi untuk mengelola inventori
def kelola_inventori():
    print("=== Kelola Inventori ===")
    print("1. Tambah Barang")
    print("2. Lihat Daftar Barang")
    pilihan = input("Pilih opsi: ")
    if pilihan == "1":
        tambah_barang_inventori()
    elif pilihan == "2":
        lihat_inventori()
    else:
        print("Opsi tidak valid.\n")

# Fungsi untuk menambah barang di inventori
def tambah_barang_inventori():
    barang = input("Masukkan nama barang: ")
    stok = int(input("Masukkan jumlah stok: "))
    harga = float(input("Masukkan harga barang: "))

    inventory_data.append({
        'barang': barang,
        'stok': stok,
        'harga': harga
    })
    save_csv_data(inventory_data_file, inventory_data, ['barang', 'stok', 'harga'])
    print("Barang berhasil ditambahkan ke inventori!\n")

# Fungsi untuk melihat inventori
def lihat_inventori():
    if not inventory_data:
        print("Inventori kosong.\n")
    else:
        print("Daftar Inventori:")
        for item in inventory_data:
            print(f"Barang: {item['barang']}, Stok: {item['stok']}, Harga: Rp{item['harga']}")
        print()

# Fungsi utama untuk menentukan akses berdasarkan role
def akses_halaman(role):
    if role == 'Supervisor':
        halaman_supervisor()
    elif role == 'Administrator':
        halaman_administrator()
    elif role == 'Operator':
        halaman_operator()
    else:
        print("Role tidak valid.\n")

# Program utama
def main():
    while True:
        role = login()
        if role:
            while True:
                print(f"Anda login sebagai {role}.")
                print("1. Akses halaman")
                print("2. Logout")
                pilihan = input("Pilih opsi: ")

                if pilihan == "1":
                    akses_halaman(role)
                elif pilihan == "2":
                    print("Logout berhasil.\n")
                    break
                else:
                    print("Opsi tidak valid.\n")
        else:
            print("Gagal login. Silakan coba lagi.")

if __name__ == "__main__":
    main()
