from flask import Flask, render_template, request, redirect, flash, url_for
import mysql.connector

app = Flask(__name__)

# Koneksi ke MySQL
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="toko_db"
)
app.secret_key = "kunci_rahasia_anda"

@app.route("/")
def index():
    db_cursor = db_connection.cursor()
    db_cursor.execute("SELECT * FROM Barang")
    barang = db_cursor.fetchall()
    return render_template("index.html", barang=barang)

@app.route("/tambah_barang", methods=["GET", "POST"])
def tambah_barang():
    if request.method == "POST":
        nama_barang = request.form["nama_barang"]
        stok = int(request.form["stok"])
        harga = int(request.form["harga"])

        db_cursor = db_connection.cursor()
        db_cursor.execute("SELECT * FROM Barang WHERE nama_barang = %s", (nama_barang,))
        result = db_cursor.fetchall()

        if result:
            db_cursor.execute("UPDATE Barang SET stok = stok + %s WHERE nama_barang = %s",
                              (stok, nama_barang))
            db_connection.commit()
        else:
            db_cursor.execute("INSERT INTO Barang (nama_barang, stok, harga) VALUES (%s, %s, %s)",
                              (nama_barang, stok, harga))
            db_connection.commit()

        return redirect("/tambah_barang")
    else:
        return render_template("tambah_barang.html")

@app.route("/transaksi", methods=["GET", "POST"])
def transaksi():
    if request.method == "POST":
        id_barang = request.form["id_barang"]
        jumlah = int(request.form["jumlah"])
        tanggal = request.form["tanggal"]
        db_cursor = db_connection.cursor()
        db_cursor.execute("SELECT stok FROM Barang WHERE id_barang = %s", (id_barang,))
        result = db_cursor.fetchone()

        if result is None:
            flash("ID barang tidak valid.")
            return redirect("/transaksi")

        stok_barang = result[0]

        if jumlah > stok_barang:
            flash("Jumlah melebihi stok yang tersedia.")
            return redirect("/transaksi")

        db_cursor.execute("UPDATE Barang SET stok = stok - %s WHERE id_barang = %s",
                          (jumlah, id_barang))
        db_connection.commit()

        db_cursor.execute("INSERT INTO Transaksi_Jual (id_barang, jumlah, tanggal) VALUES (%s, %s, %s)",
                          (id_barang, jumlah, tanggal))
        db_connection.commit()

        transaksi_id = db_cursor.lastrowid
        db_cursor.execute("INSERT INTO Riwayat_Transaksi (id_transaksi, tanggal) VALUES (%s, %s)",
                          (transaksi_id, tanggal))
        db_connection.commit()

        return redirect("/")
    else:
        db_cursor = db_connection.cursor()
        db_cursor.execute("SELECT id_barang, nama_barang FROM Barang")
        barang = db_cursor.fetchall()

        db_cursor.execute("SELECT Riwayat_Transaksi.id_riwayat, Riwayat_Transaksi.tanggal, "
                          "Transaksi_Jual.jumlah, Barang.nama_barang, (Transaksi_Jual.jumlah * Barang.harga) "
                          "AS total FROM Riwayat_Transaksi JOIN Transaksi_Jual "
                          "ON Riwayat_Transaksi.id_transaksi = Transaksi_Jual.id_transaksi "
                          "JOIN Barang ON Transaksi_Jual.id_barang = Barang.id_barang "
                          "ORDER BY Riwayat_Transaksi.id_riwayat DESC")
        riwayat_transaksi = db_cursor.fetchall()

        total_pendapatan = sum(riwayat[4] for riwayat in riwayat_transaksi)

        return render_template("transaksi.html", barang=barang, riwayat_transaksi=riwayat_transaksi,
                               total_pendapatan=total_pendapatan)

@app.route("/edit_barang/<int:id_barang>", methods=["GET", "POST"])
def edit_barang(id_barang):
    if request.method == "POST":
        nama_barang = request.form["nama_barang"]
        stok = int(request.form["stok"])
        harga = int(request.form["harga"])

        db_cursor = db_connection.cursor()
        db_cursor.execute("UPDATE Barang SET nama_barang = %s, stok = %s, harga = %s WHERE id_barang = %s",
                          (nama_barang, stok, harga, id_barang))
        db_connection.commit()

        return redirect("/")
    else:
        db_cursor = db_connection.cursor()
        db_cursor.execute("SELECT * FROM Barang WHERE id_barang = %s", (id_barang,))
        barang = db_cursor.fetchone()

        return render_template("edit_barang.html", barang=barang)

if __name__ == "__main__":
    app.run(debug=True)
