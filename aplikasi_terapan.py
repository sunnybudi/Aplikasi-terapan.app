import streamlit as st

# SET CONFIG HARUS PALING ATAS
st.set_page_config(page_title="Aplikasi Matematika Industri", layout="centered")

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

# =======================
# Konfigurasi Halaman
# =======================
st.set_page_config(page_title="Optimasi Produksi Meja & Kursi", layout="centered")

# =======================
# Tab Aplikasi
# =======================
tab1, _ = st.tabs(["Optimasi Produksi", "Tab Lain"])

with tab1:
    st.header("1️⃣ Optimasi Produksi (Linear Programming)")
    st.write("Studi kasus: Menentukan kombinasi produk meja dan kursi yang memaksimalkan keuntungan dengan keterbatasan sumber daya.")

    st.markdown("""
    ### Studi Kasus
    Sebuah perusahaan memproduksi **Meja (Produk X)** dan **Kursi (Produk Y)**.  
    Setiap produk memerlukan waktu produksi:

    | Produk     | Waktu Kayu (jam) | Waktu Finishing (jam) | Keuntungan per unit |
    |------------|------------------|------------------------|----------------------|
    | Meja (X)   | 4 jam            | 2 jam                 | Rp 400.000           |
    | Kursi (Y)  | 2 jam            | 1 jam                 | Rp 300.000           |
    """)

    st.latex(r"Z = c_1 \cdot X + c_2 \cdot Y")

    # ==================================
    # INPUT DATA
    # ==================================
    st.markdown("### Masukkan Harga dan Jumlah Produksi")

    col1, col2 = st.columns(2)
    with col1:
        c1 = st.number_input("Harga per unit Meja (X)", value=400_000)
        x = st.number_input("Jumlah produksi Meja (X)", value=25)

    with col2:
        c2 = st.number_input("Harga per unit Kursi (Y)", value=300_000)
        y = st.number_input("Jumlah produksi Kursi (Y)", value=80)

    # ==================================
    # PERHITUNGAN
    # ==================================
    st.markdown("### 🔎 Hasil Perhitungan Fungsi Objektif")

    z_meja = c1 * x
    z_kursi = c2 * y
    total_z = z_meja + z_kursi

    st.write(f"Keuntungan dari {int(x)} Meja = Rp {z_meja:,.0f}")
    st.write(f"Keuntungan dari {int(y)} Kursi = Rp {z_kursi:,.0f}")
    st.success(f"💰 Total Keuntungan = Rp {total_z:,.0f}")

    # Menentukan alternatif solusi optimal secara manual (jika hanya memilih satu produk)
    z_0 = 0
    z_x_only = c1 * x
    z_y_only = c2 * y

    if z_x_only >= z_y_only and z_x_only >= z_0:
        solusi_optimal = f"(X={x}, Y=0)"
        z_opt = z_x_only
    elif z_y_only >= z_x_only and z_y_only >= z_0:
        solusi_optimal = f"(X=0, Y={y})"
        z_opt = z_y_only
    else:
        solusi_optimal = "(0, 0)"
        z_opt = 0

    st.info(f"📌 Solusi Alternatif Maksimum (jika hanya satu produk): {solusi_optimal} dengan Z = Rp {z_opt:,.0f}")

    # ==================================
    # GRAFIK PERBANDINGAN KEUNTUNGAN
    # ==================================
    st.markdown("### 📈 Grafik Perbandingan Jumlah Produk dan Keuntungan")

    # Dataset
    produk_x = list(range(0, int(x)+20, 10))
    keuntungan_x = [c1 * i for i in produk_x]

    produk_y = list(range(0, int(y)+20, 10))
    keuntungan_y = [c2 * j for j in produk_y]

    fig, ax = plt.subplots()

    # Garis keuntungan meja
    ax.plot(produk_x, keuntungan_x, 'o-b', label='Meja (X) vs Keuntungan')
    # Garis keuntungan kursi
    ax.plot(produk_y, keuntungan_y, 'o-g', label='Kursi (Y) vs Keuntungan')

    # Tambahkan titik aktual produksi
    ax.plot(x, z_meja, 's', color='blue', label=f'Meja Aktual ({int(x)}, Rp {z_meja:,.0f})')
    ax.plot(y, z_kursi, 's', color='green', label=f'Kursi Aktual ({int(y)}, Rp {z_kursi:,.0f})')

    # Tambahkan total keuntungan
    ax.plot(x + y, total_z, 'd', color='purple', label=f'Total Produksi ({int(x+y)}, Rp {total_z:,.0f})')

    # Label grafik
    ax.set_xlabel("Jumlah Produk")
    ax.set_ylabel("Keuntungan (Z)")
    ax.set_title("Perbandingan Jumlah Produk dan Keuntungan")
    ax.legend()
    st.pyplot(fig)
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
