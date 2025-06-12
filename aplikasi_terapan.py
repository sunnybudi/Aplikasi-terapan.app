import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from scipy.optimize import linprog

st.set_page_config(layout="wide")

# =============================
# SIDEBAR - PETUNJUK
# =============================
st.sidebar.title("📘 Petunjuk Penggunaan")
st.sidebar.markdown("""
Aplikasi ini memiliki 4 model matematika industri:

1. **Optimasi Produksi (LP)**  
2. **Model Persediaan EOQ**  
3. **Model Antrian (M/M/1)**  
4. **Analisis Turunan Parsial**

Masukkan data sesuai tab. Hasil & grafik akan muncul secara otomatis.
""")

# =============================
# TAB UTAMA
# =============================
st.title("📊 Aplikasi Model Matematika Industri")

tab1, tab2, tab3, tab4 = st.tabs([
    "1. Optimasi Produksi (Linear Programming)",
    "2. Model Persediaan (EOQ)",
    "3. Model Antrian (M/M/1)",
    "4. Model Matematika Lain (Turunan Parsial)"
])

# =============================
# TAB 1: Linear Programming
# =============================
with tab1:
    st.header("1️⃣ Optimasi Produksi (Linear Programming)")

    st.markdown("Masukkan data berikut untuk menyelesaikan masalah LP:")

    c_str = st.text_input("**Fungsi Objektif (c):** Contoh: 40,60", value="40,60")
    A_str = st.text_area("**Matriks Kendala (A):** Pisahkan baris dengan enter\nContoh:\n2,1\n1,1", value="2,1\n1,1")
    b_str = st.text_input("**Batasan kanan (b):** Contoh: 100,80", value="100,80")

    try:
        # Parsing input
        c = list(map(float, c_str.split(',')))
        A = [list(map(float, row.split(','))) for row in A_str.strip().split('\n')]
        b = list(map(float, b_str.split(',')))

        # Visualisasi rumus matematika
        x = sp.symbols(f'x:{len(c)}')
        f_obj = sum(ci * xi for ci, xi in zip(c, x))
        st.latex(r"\text{Fungsi Objektif: } \max Z = " + sp.latex(f_obj))

        st.latex(r"\text{Kendala:}")
        for i, row in enumerate(A):
            lhs = sum(row[j] * x[j] for j in range(len(c)))
            st.latex(sp.latex(lhs) + r" \leq " + sp.latex(b[i]))

        if st.button("🔍 Hitung Solusi LP"):
            res = linprog([-ci for ci in c], A_ub=A, b_ub=b, method='highs')
            if res.success:
                st.success(f"✅ Solusi Optimal: Z = {round(-res.fun, 2)}")
                for i, val in enumerate(res.x):
                    st.write(f"x{i+1} = {round(val, 2)}")
            else:
                st.error("❌ Gagal menemukan solusi LP.")

        # Visualisasi wilayah solusi (hanya untuk 2 variabel)
        if len(c) == 2:
            x1_vals = np.linspace(0, max(b) * 1.2, 400)
            fig, ax = plt.subplots()
            for row, bi in zip(A, b):
                if row[1] != 0:
                    x2 = (bi - row[0]*x1_vals) / row[1]
                    ax.plot(x1_vals, x2, label=f"{row[0]}x₁ + {row[1]}x₂ ≤ {bi}")
            ax.set_xlim(0, max(b))
            ax.set_ylim(0, max(b))
            ax.set_xlabel("x₁")
            ax.set_ylabel("x₂")
            ax.set_title("Wilayah Solusi")
            ax.legend()
            st.pyplot(fig)

    except Exception as e:
        st.error(f"Terjadi kesalahan dalam input: {e}")

# =============================
# TAB 2: EOQ Model
# =============================
with tab2:
    st.header("2️⃣ Model Persediaan (EOQ)")

    D = st.number_input("Permintaan per tahun (D)", value=1000.0)
    S = st.number_input("Biaya pesan per pesanan (S)", value=50.0)
    H = st.number_input("Biaya simpan per unit per tahun (H)", value=2.0)

    if D > 0 and S > 0 and H > 0:
        EOQ = np.sqrt((2 * D * S) / H)
        st.success(f"🔢 EOQ = {EOQ:.2f} unit per pesanan")

        Q = np.linspace(1, 2 * EOQ, 100)
        TC = (D / Q) * S + (Q / 2) * H

        fig, ax = plt.subplots()
        ax.plot(Q, TC, label='Total Cost')
        ax.axvline(EOQ, color='red', linestyle='--', label='EOQ')
        ax.set_xlabel("Jumlah Pesanan (Q)")
        ax.set_ylabel("Total Biaya")
        ax.set_title("Total Biaya vs Jumlah Pesanan")
        ax.legend()
        st.pyplot(fig)

# =============================
# TAB 3: Antrian M/M/1
# =============================
with tab3:
    st.header("3️⃣ Model Antrian (M/M/1)")

    λ = st.number_input("Tingkat kedatangan (λ)", value=2.0)
    μ = st.number_input("Tingkat pelayanan (μ)", value=3.0)

    if μ > λ and λ > 0:
        ρ = λ / μ
        L = ρ / (1 - ρ)
        Lq = ρ**2 / (1 - ρ)
        W = 1 / (μ - λ)
        Wq = ρ / (μ - λ)

        st.markdown(f"""
        **📈 Hasil Perhitungan M/M/1:**

        - Utilisasi sistem (ρ): {ρ:.2f}  
        - Rata-rata jumlah dalam sistem (L): {L:.2f}  
        - Rata-rata jumlah dalam antrean (Lq): {Lq:.2f}  
        - Rata-rata waktu dalam sistem (W): {W:.2f}  
        - Rata-rata waktu tunggu (Wq): {Wq:.2f}
        """)

        ρ_vals = np.linspace(0.01, 0.99, 100)
        L_vals = ρ_vals / (1 - ρ_vals)

        fig, ax = plt.subplots()
        ax.plot(ρ_vals, L_vals)
        ax.set_xlabel("Utilisasi (ρ)")
        ax.set_ylabel("Jumlah rata-rata dalam sistem (L)")
        ax.set_title("Hubungan Utilisasi dan L")
        st.pyplot(fig)

    elif λ >= μ:
        st.error("λ harus lebih kecil dari μ agar sistem stabil.")

# =============================
# TAB 4: Turunan Parsial
# =====================
