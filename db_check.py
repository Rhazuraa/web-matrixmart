import mysql.connector

# Connect to MySQL server in XAMPP
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    port="3306"
)

# Create the database
db_cursor = db_connection.cursor()
db_cursor.execute("CREATE DATABASE IF NOT EXISTS tekd")
db_cursor.execute("USE toko")

# Create the Barang table
db_cursor.execute("CREATE TABLE IF NOT EXISTS Barang ("
                  "id_barang INT AUTO_INCREMENT PRIMARY KEY,"
                  "nama_barang VARCHAR(255) NOT NULL,"
                  "stok INT NOT NULL,"
                  "harga INT NOT NULL)"
                  )

# Create the Transaksi_Jual table
db_cursor.execute("CREATE TABLE IF NOT EXISTS Transaksi_Jual ("
                  "id_transaksi INT AUTO_INCREMENT PRIMARY KEY,"
                  "id_barang INT NOT NULL,"
                  "jumlah INT NOT NULL,"
                  "tanggal DATE NOT NULL,"
                  "FOREIGN KEY (id_barang) REFERENCES Barang(id_barang))"
                  )

# Create the Riwayat_Transaksi table
db_cursor.execute("CREATE TABLE IF NOT EXISTS Riwayat_Transaksi ("
                  "id_riwayat INT AUTO_INCREMENT PRIMARY KEY,"
                  "id_transaksi INT NOT NULL,"
                  "tanggal DATE NOT NULL,"
                  "FOREIGN KEY (id_transaksi) REFERENCES Transaksi_Jual(id_transaksi))"
                  )

# Commit the changes and close the connection
db_connection.commit()
db_connection.close()
