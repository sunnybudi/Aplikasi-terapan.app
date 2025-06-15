import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import math

# =========================
# SIDEBAR - PETUNJUK
# =========================
st.sidebar.title("\U0001F4D8 Petunjuk Penggunaan")
st.sidebar.markdown("""
Aplikasi ini memiliki 5 model matematika industri:

1. **Optimasi Produksi**
2. **Model Persediaan EOQ**  
3. **Model Antrian (M/M/1)**  
4. **Turunan Parsial**  
5. **Perencanaan Bahan Baku (Inventory Requirement)**

Masukkan data sesuai tab. Hasil & grafik akan muncul secara otomatis.
""")

# =========================
# TAB UTAMA
# =========================
st.title("\U0001F4CA Aplikasi Model Matematika Industri")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "1. Optimasi Produksi",
    "2. Model Persediaan (EOQ)",
    "3. Model Antrian (M/M/1)",
    "4. Turunan Parsial",
    "5. Kebutuhan Bahan Baku"
])

# =========================
# TAB 1: Simulasi Manual Mesin & Operator
# =========================
with tab1:
    st.header("1️⃣ Optimasi Produksi")
    st.write("Tujuan optimasi produksi adalah untuk memaksimalkan efisiensi dan menghasilkan output terbaik dari sumber daya yang terbatas (seperti tenaga kerja, mesin, bahan baku, dan waktu) guna mencapai tujuan bisnis tertentu.")

    target = st.number_input("🎯 Target Produksi Harian (unit)", min_value=1, value=600, step=10)
    jam_kerja = st.number_input("🕒 Jam Kerja per Hari (jam)", min_value=1, value=8)
    kapasitas = st.number_input("⚙️ Kapasitas Mesin & Operator (unit/jam)", value=6)
    biaya_mesin = st.number_input("💰 Biaya Mesin (biaya/hari)", value=300)
    biaya_operator = st.number_input("💰 Biaya Operator (upah/hari)", value=200)
    kapasitas_harian = kapasitas * jam_kerja

    mesin = st.number_input("🔧 Jumlah Mesin (input manual)", min_value=0, step=1)
    operator = st.number_input("👷 Jumlah Operator (input manual)", min_value=0, step=1)

    produksi_aktual = min(mesin, operator) * kapasitas_harian
    total_biaya = (mesin * biaya_mesin) + (operator * biaya_operator)

    st.write(f"🏭 Total Produksi Aktual: **{produksi_aktual} unit/hari**")
    st.write(f"💵 Total Biaya Harian: **Rp {total_biaya:,.0f}**")

    fig, ax = plt.subplots()
    ax.bar(["Mesin", "Operator"], [mesin, operator], color=["skyblue", "orange"])
    ax.set_ylabel("Jumlah")
    st.pyplot(fig)

# =========================
# TAB 2: EOQ
# =========================
with tab2:
    st.header("📦 Model Persediaan EOQ")
    st.write("Model persediaan EOQ (Economic Order Quantity) atau Model Jumlah Pemesanan Ekonomis adalah model matematika yang digunakan dalam manajemen persediaan untuk menentukan jumlah pembelian atau produksi yang paling efisien guna meminimalkan total biaya persediaan, yaitu biaya pemesanan dan biaya penyimpanan.")
    D = st.number_input("📅 Permintaan Tahunan (unit)", value=10000)
    S = st.number_input("🛒 Biaya Pemesanan per Order (Rp)", value=50000)
    H = st.number_input("🏬 Biaya Penyimpanan per Unit per Tahun (Rp)", value=2000)

    if D > 0 and S > 0 and H > 0:
        EOQ = math.sqrt((2 * D * S) / H)
        freq = D / EOQ
        cycle_days = 365 / freq

        st.success(f"EOQ: {EOQ:.2f} unit")
        st.write(f"Frekuensi Pemesanan: {freq:.2f} kali/tahun")
        st.write(f"Interval Pemesanan: {cycle_days:.0f} hari")

        # Grafik EOQ mirip gaya model antrian (bar chart untuk ilustrasi frekuensi)
        x_vals = ["Permintaan", "EOQ"]
        y_vals = [D, EOQ]

        fig, ax = plt.subplots()
        ax.bar(x_vals, y_vals, color=['red', 'green'])
        ax.set_ylabel("Jumlah Unit")
        ax.set_title("EOQ dan Permintaan Tahunan")
        st.pyplot(fig)
    else:
        st.warning("Input harus lebih besar dari 0")

# =========================
# TAB 3: Model Antrian M/M/1
# =========================
with tab3:
    st.header("3️⃣ Model Antrian M/M/1")
    st.write("""
    Model antrian M/M/1 digunakan untuk menganalisis sistem antrian dengan satu server, 
    di mana waktu antar kedatangan pelanggan dan waktu pelayanan bersifat acak (eksponensial/Poisson).
    """)

    # Input pengguna
    lambd = st.number_input("Tingkat Kedatangan (λ) - pelanggan/jam", min_value=0, value=2)
    mu = st.number_input("Tingkat Pelayanan (μ) - pelanggan/jam", min_value=0, value=3)

    # Validasi kestabilan sistem
    if lambd >= mu:
        st.warning("⚠️ Sistem tidak stabil (λ ≥ μ). Harap pastikan λ < μ agar sistem dapat dianalisis.")
    else:
        # Perhitungan nilai antrian
        rho = lambd / mu
        L = rho / (1 - rho)
        Lq = rho**2 / (1 - rho)
        W = 1 / (mu - lambd)
        Wq = rho / (mu - lambd)

        # Hasil perhitungan
        st.subheader("📊 Hasil Perhitungan Antrian M/M/1")
        st.write(f"Utilisasi Sistem (ρ): **{rho:.2f}**")
        st.write(f"Rata-rata pelanggan dalam sistem (L): **{L:.2f}**")
        st.write(f"Rata-rata pelanggan dalam antrian (Lq): **{Lq:.2f}**")
        st.write(f"Waktu rata-rata dalam sistem (W): **{W:.2f} jam**")
        st.write(f"Waktu tunggu rata-rata dalam antrian (Wq): **{Wq:.2f} jam**")

        # =========================
        # GRAFIK RINGKASAN SISTEM
        # =========================
        st.subheader("📉 Ringkasan Sistem dalam Bentuk Grafik")
        labels = ["ρ", "L", "Lq", "W", "Wq"]
        values = [rho, L, Lq, W, Wq]

        fig, ax = plt.subplots()
        bars = ax.bar(labels, values, color=['skyblue', 'orange', 'lightgreen', 'salmon', 'violet'])
        ax.set_ylabel("Nilai")
        ax.set_title("Ringkasan Parameter Antrian M/M/1")
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f"{height:.2f}", xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3), textcoords="offset points",
                        ha='center', va='bottom')
        st.pyplot(fig)

        # =========================
        # GRAFIK 1: Distribusi Pn
        # =========================
        st.subheader("📈 Distribusi Probabilitas Jumlah Pelanggan dalam Sistem (Pn)")

        n = np.arange(0, 20)
        Pn = (1 - rho) * rho ** n

        fig1, ax1 = plt.subplots()
        ax1.bar(n, Pn, color='cornflowerblue', alpha=0.8)
        ax1.set_xlabel("Jumlah Pelanggan dalam Sistem (n)")
        ax1.set_ylabel("Probabilitas Pn")
        ax1.set_title("Distribusi Probabilitas Pelanggan dalam Sistem")
        st.pyplot(fig1)

# =========================
# TAB 4: Turunan Parsial
# =========================
with tab4:
    st.header("4️⃣ Turunan Parsial")
    x, y = sp.symbols('x y')
    fungsi = st.text_input("Masukkan f(x, y):", "x**3 + y + y**2")

    try:
        f = sp.sympify(fungsi)
        fx = sp.diff(f, x)
        fy = sp.diff(f, y)
        x0 = st.number_input("x₀:", value=1.0)
        y0 = st.number_input("y₀:", value=2.0)

        f_val = f.subs({x: x0, y: y0})
        fx_val = fx.subs({x: x0, y: y0})
        fy_val = fy.subs({x: x0, y: y0})

        st.latex(rf"f(x, y) = {sp.latex(f)}")
        st.latex(rf"\frac{{\partial f}}{{\partial x}} = {sp.latex(fx)}")
        st.latex(rf"\frac{{\partial f}}{{\partial y}} = {sp.latex(fy)}")

        st.write(f"Nilai f: {f_val}, Gradien: ({fx_val}, {fy_val})")

        X, Y = np.meshgrid(np.linspace(x0-2, x0+2, 50), np.linspace(y0-2, y0+2, 50))
        f_np = sp.lambdify((x, y), f, 'numpy')
        Z = f_np(X, Y)
        Z_tangent = float(f_val) + float(fx_val)*(X - x0) + float(fy_val)*(Y - y0)

        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7)
        ax.plot_surface(X, Y, Z_tangent, color='red', alpha=0.5)
        ax.set_title("f(x, y) dan Bidang Singgung di (x₀, y₀)")
        st.pyplot(fig)
    except:
        st.error("Fungsi tidak valid. Gunakan format Python: x**2 + y**2")

# =========================
# TAB 5: Perencanaan Bahan Baku
# =========================
with tab5:
    st.header("5️⃣ Perencanaan Kebutuhan Bahan Baku")
    st.write("Tujuan perencanaan kebutuhan bahan baku (dalam bahasa Inggris sering disebut Material Requirements Planning / MRP) adalah untuk memastikan kesiapan bahan baku yang dibutuhkan dalam proses produksi selalu tersedia.")


    produk = st.text_input("Nama Produk:", "Meja")
    jumlah_produk = st.number_input("Jumlah Produk yang Akan Diproduksi:", min_value=0, value=100)

    st.markdown("Masukkan kebutuhan bahan baku per unit produk:")
    bahan1 = st.text_input("Nama Bahan Baku 1:", "Kayu")
    jumlah1 = st.number_input(f"Jumlah {bahan1} per unit {produk}:", min_value=0, value=5)

    bahan2 = st.text_input("Nama Bahan Baku 2:", "Paku")
    jumlah2 = st.number_input(f"Jumlah {bahan2} per unit {produk}:", min_value=0, value=10)

    total1 = jumlah_produk * jumlah1
    total2 = jumlah_produk * jumlah2

    st.success("Total Kebutuhan Bahan Baku:")
    st.write(f"🔹 {bahan1}: {total1} unit")
    st.write(f"🔹 {bahan2}: {total2} unit")

    fig, ax = plt.subplots()
    ax.bar([bahan1, bahan2], [total1, total2], color=['green', 'brown'])
    ax.set_ylabel("Jumlah Kebutuhan")
    ax.set_title("Total Kebutuhan Bahan Baku")
    st.pyplot(fig)
