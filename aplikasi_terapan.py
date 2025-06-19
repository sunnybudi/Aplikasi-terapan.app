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
4. **Model Lain** 
5. **Turunan Parsial** 

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
    "4. Model Lain",
    "5. Turunan Parsial"
])

# ================================================
# TAB 1: Optimasi Produksi (Linear Programming)
# ================================================

with tab1:
    st.header("1️⃣ Optimasi Produksi (Linear Programming)")
    st.markdown("""
    ### 🔧 Studi Kasus
    PT Kreasi Untung Indonesia yang merupakan sebuah perusahaan furnitur memproduksi **Meja (X)** dan **Kursi (Y)**. 
    Untuk mengetahui berapa banyak penjualan dan keuntungan pada hasil produksi, pemiliknya menggunakan perhitungan 
    matematika dengan rumus:
    """)

    st.latex(r"Z = c₁X + c₂Y")
    st.markdown("""Keterangan""")
    st.markdown(r"""
    - $Z$ : Total biaya atau total keuntungan  
    - $c₁$ : Biaya atau keuntungan per unit $X$  
    - $c₂$ : Biaya atau keuntungan per unit $Y$  
    - $X$ : Jumlah unit produk (misal: Meja)  
    - $Y$ : Jumlah unit produk (misal: Kursi)
    """)

    # ===============================
    # Input Harga dan Keuntungan
    # ===============================
    st.markdown("### Harga Jual dan Keuntungan per Unit")
    col1, col2= st.columns(2)
    with col1:
        x = st.number_input("Jumlah Produksi Meja (X)", value=10)
        laba_meja = st.number_input("Keuntungan per Meja (c₁)", value=400_000)
        harga_meja = st.number_input("Harga Jual Meja", value=800_000)
    with col2:
        y = st.number_input("Jumlah Produksi Kursi (Y)", value=20)
        laba_kursi = st.number_input("Keuntungan per Kursi (c₂)", value=200_000)
        harga_kursi = st.number_input("Harga Jual Kursi", value=500_000)

    # Hitung biaya produksi dari selisih harga dan keuntungan
    biaya_meja = harga_meja - laba_meja
    biaya_kursi = harga_kursi - laba_kursi
    
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
    # Grafik Perbandingan (Diagram Batang Vertikal)
    # ===============================
    st.markdown("### 📊 Diagram Perbandingan Penjualan dan Keuntungan")
    
    # Data per kategori
    kategori = ['Meja (X)', 'Kursi (Y)', 'Total']
    penjualan = [total_penjualan_meja, total_penjualan_kursi, total_penjualan]
    keuntungan = [total_laba_meja, total_laba_kursi, total_keuntungan_bersih]
    
    # Grafik
    x_pos = np.arange(len(kategori))
    width = 0.35
    fig2, ax2 = plt.subplots()
    
    # Buat batang grafik
    bar1 = ax2.bar(x_pos - width/2, keuntungan, width=width, color='skyblue', label='Keuntungan')
    bar2 = ax2.bar(x_pos + width/2, penjualan, width=width, color='lightgreen', label='Penjualan')
    
    # Gabungan semua nilai untuk menentukan batas Y
    values = penjualan + keuntungan
    max_val = max(values)
    ax2.set_ylim(0, max_val * 1.3)  # Ruang ekstra di atas grafik
    
    # Label angka tetap (tidak menempel batang)
    for bars in [bar1, bar2]:
        for bar in bars:
            value = bar.get_height()
            text = f"{value:,.0f}".replace(",", ".")
            ax2.text(
                bar.get_x() + bar.get_width() / 2,
                value + (max_val * 0.03),  # Jarak 3% dari tinggi maksimal
                text,
                ha='center', va='bottom',
                fontsize=10,
                color='black',
                fontweight='bold'
            )
    
    # Pengaturan axis dan label
    ax2.set_ylabel("Rupiah", fontsize=10)
    ax2.set_xlabel("Kategori Produk", fontsize=10)
    ax2.set_title("Perbandingan Penjualan dan Keuntungan", fontsize=12)
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(kategori, fontsize=10)
    ax2.legend(fontsize=10)
    
    # Format angka di sumbu Y
    ax2.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x):,}'.replace(",", ".")))
    
    plt.tight_layout()
    st.pyplot(fig2)

# =========================
# TAB 2: EOQ
# =========================
with tab2:
    st.header("📦 Model Persediaan EOQ")
    st.markdown("""
        ### 🔧 Studi Kasus
        PT Kreasi Untung Indonesia yang merupakan sebuah perusahaan furnitur memproduksi Meja dan Kursi. 
        Pihak manajemen ingin mengetahui berapa banyak lembar kayu yang sebaiknya dipesan pada setiap batch 
        order untuk menghemat biaya total persediaan.
        """)


    st.subheader("📐 Rumus-Rumus:")
    st.latex(r"""
    \begin{aligned}
    \textbf{EOQ} &= \sqrt{\frac{2DS}{H}} \\
    \textbf{N} &= \frac{D}{EOQ} \\
    \textbf{T} &= \frac{365}{\text{N}}
    \end{aligned}
    """)

    
    st.markdown("""Keterangan""")
    st.code("""
        EOQ   = Economic Order Quantity (jumlah pemesanan ekonomis)
        D     = Demand (jumlah kebutuhan (tuntutan barang per tahun)
        S     = Ordering Cost (biaya pemesanan per pesanan)
        H     = Holding Cost (biaya penyimpanan per unit per tahun)
        N     = Frekuensi pemesanan
        T     = Interval pemesanan
        """)
    
    D = st.number_input("📅 Permintaan Tahunan (D/unit)", value=10000)
    S = st.number_input("🛒 Biaya Pemesanan per Order (S/Rp)", value=50000)
    H = st.number_input("🏬 Biaya Penyimpanan per Unit per Tahun (H/Rp)", value=2000)

    if D > 0 and S > 0 and H > 0:
        EOQ = math.sqrt((2 * D * S) / H)
        freq = D / EOQ
        cycle_days = 365 / freq

        st.success(
            f"""
            EOQ: {EOQ:.2f} unit\\
            N: {freq:.2f} kali/tahun\\
            T: {cycle_days:.0f} hari
            """
        )

        st.markdown("### 📊 Diagram EOQ dan Permintaan Tahunan")
        fig, ax = plt.subplots()
        labels = ["Permintaan", "EOQ"]
        values = [D, EOQ]
        colors = ['red', 'green']
        
        bars = ax.bar(labels, values, color=colors)
        ax.set_ylabel("Jumlah Unit")
        ax.set_title("EOQ dan Permintaan Tahunan")
        
        # Tambahkan nilai di atas tiap batang
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,  # posisi tengah batang
                height + 0 * max(values),        # sedikit di atas batang
                f"{height:.2f}",                    # format angka
                ha='center', va='bottom', fontsize=10, fontweight='bold'
            )
        
        st.pyplot(fig)

# =========================
# TAB 3: Model Antrian (M/M/1)
# =========================
with tab3:
    st.header("3️⃣ Model Antrian (M/M/1)")
    st.markdown("""
        ### 🔧 Studi Kasus
        PT Kreasi Untung Indonesia yang merupakan sebuah perusahaan furnitur memproduksi Meja dan Kursi. 
        Perusahaan menginginkan semua aktivitas pembelian dialihkan ke website, maka dari itu diperlukan aplikasi
        untuk memantau proses pembelian di server web perusahaan.
    """)

    # Tampilkan Rumus Umum Sebelum Input
    st.subheader("📘 Rumus-Rumus Umum Model M/M/1")
    st.latex(r"""
    \begin{align*}
    \rho &= \frac{\lambda}{\mu} \\
    L &= \frac{\lambda}{\mu - \lambda} \\
    L_q &= \frac{\lambda^2}{\mu(\mu - \lambda)} \\
    W &= \frac{1}{\mu - \lambda} \\
    W_q &= \frac{\lambda}{\mu(\mu - \lambda)} \\
    P_0 &= 1 - \rho
    \end{align*}
    """)

    st.markdown("**📘 Keterangan Simbol Model M/M/1**")
    st.markdown(r"""
    - $\lambda$: Tingkat kedatangan pelanggan per satuan waktu (misalnya pelanggan per jam)  
    - $\mu$: Tingkat pelayanan pelanggan per satuan waktu  
    - $\rho$: Utilisasi server, yaitu $\rho = \lambda / \mu$  
    - $L$: Rata-rata jumlah pelanggan dalam sistem (antrian + dilayani)  
    - $L_q$: Rata-rata jumlah pelanggan dalam antrian  
    - $W$: Waktu rata-rata pelanggan berada dalam sistem  
    - $W_q$: Waktu rata-rata pelanggan dalam antrian  
    - $P_0$: Probabilitas sistem kosong (tidak ada pelanggan)  
    - $P_n$: Probabilitas terdapat $n$ pelanggan dalam sistem  
    <br>
    """, unsafe_allow_html=True)


    # Input parameter
    col1, col2 = st.columns(2)
    with col1:
        lambd = st.number_input("📥 Tingkat Kedatangan (λ) - pelanggan/jam", min_value=0, value=2)
    with col2:
        mu = st.number_input("⚙️ Tingkat Pelayanan (μ) - pelanggan/jam", min_value=0, value=3)

    if lambd >= mu:
        st.error("⚠️ Sistem tidak stabil (λ ≥ μ). Harap pastikan λ < μ.")
    else:
        # Perhitungan
        rho = lambd / mu
        L = lambd / (mu - lambd)
        Lq = (lambd ** 2) / (mu * (mu - lambd))
        W = 1 / (mu - lambd)
        Wq = lambd / (mu * (mu - lambd))
        P0 = 1 - rho

        # Tampilkan Rumus Dengan Nilai
        st.subheader("🧮 Perhitungan Berdasarkan Input")
        st.latex(rf"""
        \begin{{align*}}
        \rho &= \frac{{\lambda}}{{\mu}} = \frac{{{lambd}}}{{{mu}}} = {rho:.3f} \\
        L &= \frac{{\lambda}}{{\mu - \lambda}} = \frac{{{lambd}}}{{{mu - lambd}}} = {L:.3f} \\
        L_q &= \frac{{\lambda^2}}{{\mu(\mu - \lambda)}} = \frac{{{lambd}^2}}{{{mu}({mu - lambd})}} = {Lq:.3f} \\
        W &= \frac{{1}}{{\mu - \lambda}} = \frac{{1}}{{{mu - lambd}}} = {W:.3f} \\
        W_q &= \frac{{\lambda}}{{\mu(\mu - \lambda)}} = \frac{{{lambd}}}{{{mu}({mu - lambd})}} = {Wq:.3f} \\
        P_0 &= 1 - \rho = 1 - {rho:.3f} = {P0:.3f}
        \end{{align*}}
        """)

        # Grafik Ringkasan
        st.subheader("📊 Grafik Ringkasan")
        labels = ["ρ", "L", "Lq", "W", "Wq"]
        values = [rho, L, Lq, W, Wq]

        fig, ax = plt.subplots()
        bars = ax.bar(labels, values, color=['skyblue', 'orange', 'green', 'salmon', 'violet'])
        ax.set_ylim(0, max(values) * 1.2)
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f"{height:.2f}", xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3), textcoords="offset points",
                        ha='center', va='bottom')
        ax.set_title("Ringkasan Parameter Antrian M/M/1")
        ax.set_ylabel("Nilai")
        st.pyplot(fig)

        # Hasil Perhitungan Teks
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
# TAB 4: Kebutuhan Bahan Baku
# =========================
with tab4:
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

# =========================
# TAB 5: Turunan Parsial
# =========================
with tab5:
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
