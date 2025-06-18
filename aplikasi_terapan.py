import streamlit as st

# SET CONFIG HARUS PALING ATAS
st.set_page_config(page_title="Aplikasi Matematika Industri", layout="centered")

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
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
5. **Model Lain (Kebutuhan Bahan Baku)**

Masukkan data sesuai tab. Hasil & grafik akan muncul secara otomatis.
""")

# =========================
# TAB UTAMA
# =========================
st.title("\U0001F4CA Aplikasi Matematika Terapan")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "1. Optimasi Produksi",
    "2. Model Persediaan (EOQ)",
    "3. Model Antrian (M/M/1)",
    "4. Turunan Parsial",
    "5. Model Lain"
])

# ================================================
# TAB 1: Optimasi Produksi (Linear Programming)
# ================================================

with tab1:
    st.header("1️⃣ Optimasi Produksi (Linear Programming)")
    st.markdown("""
    ### Studi Kasus
    Sebuah perusahaan furnitur memproduksi **Meja (X)** dan **Kursi (Y)**. Untuk mengetahui berapa banyak 
    penjualan dan keuntungan pada hasil produksi, pemiliknya menggunakan perhitungan matematika dengan rumus:
    """)

    st.latex(r"Z = c₁X + c₂Y")

    # ===============================
    # Input Harga dan Keuntungan
    # ===============================
    st.markdown("### Harga Jual dan Keuntungan per Unit")
    harga_meja = st.number_input("💰 Harga Jual Meja (X)", value=800_000)
    laba_meja = st.number_input("📈 Keuntungan per Meja (X)", value=400_000)
    harga_kursi = st.number_input("💰 Harga Jual Kursi (Y)", value=500_000)
    laba_kursi = st.number_input("📈 Keuntungan per Kursi (Y)", value=200_000)

    # Hitung biaya produksi dari selisih harga dan keuntungan
    biaya_meja = harga_meja - laba_meja
    biaya_kursi = harga_kursi - laba_kursi

    # ===============================
    # Input Jumlah Produksi
    # ===============================
    st.markdown("### Jumlah Produksi")
    x = st.number_input("Jumlah Produksi Meja (X)", value=10)
    y = st.number_input("Jumlah Produksi Kursi (Y)", value=20)

    # ===============================
    # Fungsi Format Rupiah
    # ===============================
    def format_rupiah(nilai):
        return f"Rp {nilai:,.0f}".replace(",", ".")

    # ===============================
    # Perhitungan Fungsi Tujuan Z
    # ===============================
    z1 = 0
    z2 = laba_meja * x
    z3 = laba_kursi * y

    st.markdown("### 🔎 Hasil Fungsi Tujuan Z:")
    st.write(f"Z(0, 0) = {z1}")
    st.write(f"Z({x}, 0) = {format_rupiah(z2)}")
    st.write(f"Z(0, {y}) = {format_rupiah(z3)}")

    z_opt = max(z1, z2, z3)
    if z_opt == z2:
        solusi = f"(0, {x})"
    elif z_opt == z3:
        solusi = f"({y}, 0)"
    else:
        solusi = "(0, 0)"

    st.success(f"💡 Solusi optimal: {solusi} dengan keuntungan maksimum sebesar {format_rupiah(z_opt)}")

    # ===============================
    # Total Penjualan dan Keuntungan
    # ===============================
    st.markdown("### 💰 Ringkasan Total Penjualan")

    total_penjualan_meja = harga_meja * x
    total_penjualan_kursi = harga_kursi * y
    total_penjualan = total_penjualan_meja + total_penjualan_kursi

    st.write(f"🪑 Penjualan Meja (X): {format_rupiah(total_penjualan_meja)}")
    st.write(f"🪑 Penjualan Kursi (Y): {format_rupiah(total_penjualan_kursi)}")
    st.write(f"📊 Total Penjualan: {format_rupiah(total_penjualan)}")

    # ===============================
    # Total Biaya Produksi & Laba Bersih
    # ===============================
    st.markdown("### 🧾 Total Keuntungan Bersih")

    total_biaya_meja = biaya_meja * x
    total_biaya_kursi = biaya_kursi * y
    total_biaya_produksi = total_biaya_meja + total_biaya_kursi

    total_laba_meja = laba_meja * x
    total_laba_kursi = laba_kursi * y
    total_keuntungan_bersih = total_laba_meja + total_laba_kursi

    st.write(f"🔹 Keuntungan Meja (X): {format_rupiah(z2)}")
    st.write(f"🔹 Keuntungan Kursi (Y): {format_rupiah(z3)}")
    st.write(f"✅ Total Keuntungan Bersih: {format_rupiah(z2 + z3)}")

    # ===============================
    # Grafik Perbandingan (Diagram Batang)
    # ===============================
    st.markdown("### 📊 Diagram Batang: Perbandingan Penjualan dan Keuntungan")
    
    # Data per kategori
    kategori = ['Meja (X)', 'Kursi (Y)', 'Total']
    penjualan = [total_penjualan_meja, total_penjualan_kursi, total_penjualan]
    keuntungan = [total_laba_meja, total_laba_kursi, total_keuntungan_bersih]
    
    x_pos = np.arange(len(kategori))
    width = 0.35  # lebar batang
    
    fig3, ax3 = plt.subplots(figsize=(20, 14))
    # Set font global (opsional, tapi efisien)
    plt.rcParams.update({'font.size': 10})
    
    # Atur label sumbu Y
    ax3.set_yticks(x_pos)
    ax3.set_yticklabels(kategori, fontsize=30)
    
    # Label sumbu X dan judul
    ax3.set_xlabel("Rupiah", fontsize=24)
    ax3.set_title("Perbandingan Penjualan dan Keuntungan", fontsize=30)
    
    # Legend dengan ukuran font lebih besar
    ax3.legend(loc='lower right', fontsize=24)
    
    # Batang horizontal
    bar1 = ax3.barh(x_pos - width/2, keuntungan, height=width, color='skyblue', label='Keuntungan')
    bar2 = ax3.barh(x_pos + width/2, penjualan, height=width, color='lightgreen', label='Penjualan')
    
    # Tampilkan label di dalam batang
    for bars in [bar1, bar2]:
        for bar in bars:
            value = int(bar.get_width())
            text = f"Rp {value:,.0f}".replace(",", ".")
            ax3.text(
                bar.get_x() + bar.get_width() * 0.95,
                bar.get_y() + bar.get_height()/2,
                text,
                ha='right', va='center',
                fontsize=24,
                color='black',
                fontweight='bold'
            )
    
    # Label dan layout
    ax3.set_yticks(x_pos)
    ax3.set_yticklabels(kategori)
    ax3.set_xlabel("Rupiah")
    ax3.set_title("Perbandingan Penjualan dan Keuntungan", fontsize=30)
    ax3.legend(loc='lower right')
    
    plt.tight_layout()
    st.pyplot(fig3)

# =========================
# TAB 2: EOQ
# =========================
with tab2:
    st.header("📦 Model Persediaan EOQ")
    st.write("Studi kasus: Untuk menentukan jumlah pemesanan ekonomis dalam permintaan pertahun.")

    st.subheader("📐 Rumus-Rumus:")
    st.latex(r"EOQ = \sqrt{\frac{2DS}{H}}")
    st.latex(r"\text{Frekuensi Pemesanan} = \frac{D}{EOQ}")
    st.latex(r"\text{Interval Pemesanan} = \frac{365}{\text{Frekuensi}}")

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

        fig, ax = plt.subplots()
        ax.bar(["Permintaan", "EOQ"], [D, EOQ], color=['red', 'green'])
        ax.set_ylabel("Jumlah Unit")
        ax.set_title("EOQ dan Permintaan Tahunan")
        st.pyplot(fig)
    else:
        st.warning("Input harus lebih besar dari 0")

# =========================
# TAB 3: Model Antrian (M/M/1)
# =========================
with tab3:
    st.header("3️⃣ Model Antrian (M/M/1)")
    st.write("""
    Model antrian M/M/1 digunakan untuk menganalisis sistem dengan satu server,
    di mana waktu antar kedatangan dan waktu pelayanan mengikuti distribusi eksponensial.
    """)
    st.write("Studi kasus: Efisiensi sebuah server dalam sebuah antrian pembelian.")

    # Input parameter
    lambd = st.number_input("📥 Tingkat Kedatangan (λ) - pelanggan/jam", min_value=0, value=2)
    mu = st.number_input("⚙️ Tingkat Pelayanan (μ) - pelanggan/jam", min_value=0, value=3)

    if lambd >= mu:
        st.error("⚠️ Sistem tidak stabil (λ ≥ μ). Harap pastikan λ < μ.")
    else:
        # Perhitungan
        rho = lambd / mu
        L = lambd / (mu - lambd)
        Lq = (lambd**2) / (mu * (mu - lambd))
        W = 1 / (mu - lambd)
        Wq = lambd / (mu * (mu - lambd))
        P0 = 1 - rho

        # Tampilkan Rumus
        st.subheader("🧮 Rumus-Rumus Model M/M/1")
        st.latex(rf"\rho = \frac{{\lambda}}{{\mu}} = \frac{{{lambd}}}{{{mu}}} = {rho:.3f}")
        st.latex(rf"L = \frac{{\lambda}}{{\mu - \lambda}} = \frac{{{lambd}}}{{{mu - lambd}}} = {L:.3f}")
        st.latex(rf"L_q = \frac{{\lambda^2}}{{\mu(\mu - \lambda)}} = \frac{{{lambd}^2}}{{{mu}({mu - lambd})}} = {Lq:.3f}")
        st.latex(rf"W = \frac{{1}}{{\mu - \lambda}} = \frac{{1}}{{{mu - lambd}}} = {W:.3f}")
        st.latex(rf"W_q = \frac{{\lambda}}{{\mu(\mu - \lambda)}} = \frac{{{lambd}}}{{{mu}({mu - lambd})}} = {Wq:.3f}")
        st.latex(rf"P_0 = 1 - \rho = 1 - {rho:.3f} = {P0:.3f}")

        # Grafik Ringkasan
        st.subheader("📊 Grafik Ringkasan")
        labels = ["ρ", "L", "Lq", "W", "Wq"]
        values = [rho, L, Lq, W, Wq]

        fig, ax = plt.subplots()
        bars = ax.bar(labels, values, color=['skyblue', 'orange', 'green', 'salmon', 'violet'])
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f"{height:.2f}", xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3), textcoords="offset points",
                        ha='center', va='bottom')
        ax.set_title("Ringkasan Parameter Antrian M/M/1")
        ax.set_ylabel("Nilai")
        st.pyplot(fig)

        st.subheader("📈 Hasil Perhitungan")
        st.markdown(f"""
        - **Tingkat Utilisasi (ρ):** {rho:.3f}
        - **Rata-rata pelanggan dalam sistem (L):** {L:.3f}
        - **Rata-rata dalam antrean (Lq):** {Lq:.3f}
        - **Waktu dalam sistem (W):** {W:.3f} jam ≈ {W*60:.0f} menit
        - **Waktu tunggu dalam antrean (Wq):** {Wq:.3f} jam ≈ {Wq*60:.0f} menit
        - **Probabilitas sistem kosong (P₀):** {P0:.3f}
        """)

        # Grafik Distribusi Pn
        st.subheader("📉 Distribusi Probabilitas Pn (Pelanggan ke-n)")
        n_vals = np.arange(0, 20)
        Pn_vals = (1 - rho) * rho ** n_vals

        fig2, ax2 = plt.subplots()
        ax2.bar(n_vals, Pn_vals, color='cornflowerblue')
        ax2.set_xlabel("n (jumlah pelanggan)")
        ax2.set_ylabel("P(n)")
        ax2.set_title("Distribusi Probabilitas Pelanggan dalam Sistem")
        st.pyplot(fig2)

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
# TAB 5: Kebutuhan Bahan Baku
# =========================
with tab5:
    st.header("5️⃣ Kebutuhan Bahan Baku")
    st.write("Studi kasus: Kebutuhan bahan baku untuk pemenuhan produksi.")
    produk = st.text_input("Nama Produk:", "Meja")
    jumlah_produk = st.number_input("Jumlah Produk yang Akan Diproduksi:", min_value=0, value=100)

    st.markdown("Masukkan kebutuhan bahan baku per unit produk:")
    bahan1 = st.text_input("Nama Bahan Baku 1:", "Kayu")
    jumlah1 = st.number_input(f"Jumlah {bahan1} per unit {produk}:", min_value=0, value=5)

    bahan2 = st.text_input("Nama Bahan Baku 2:", "Paku")
    jumlah2 = st.number_input(f"Jumlah {bahan2} per unit {produk}:", min_value=0, value=10)

    total1 = jumlah_produk * jumlah1
    total2 = jumlah_produk * jumlah2

    st.subheader("📐 Rumus Perhitungan")
    st.latex(r"\text{Total Bahan Baku} = \text{Jumlah Produk} \times \text{Jumlah Bahan Baku per Unit}")

    st.success("✅ Total Kebutuhan Bahan Baku:")
    st.write(f"🔹 {bahan1}: {total1} unit")
    st.write(f"🔹 {bahan2}: {total2} unit")

    fig, ax = plt.subplots()
    ax.bar([bahan1, bahan2], [total1, total2], color=['green', 'brown'])
    ax.set_ylabel("Jumlah Kebutuhan")
    ax.set_title("Total Kebutuhan Bahan Baku")
    st.pyplot(fig)
