import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from scipy.optimize import linprog

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

Masukkan data sesuai tab. Hasil & grafik akan muncul otomatis.
""")

# =============================
# TAB UTAMA
# =============================
st.title("📊 Aplikasi Model Matematika Industri")

tab1, tab2, tab3, tab4 = st.tabs([
    "1. Optimasi Produksi (LP)",
    "2. Model Persediaan (EOQ)",
    "3. Model Antrian (M/M/1)",
    "4. Analisis Turunan Parsial"
])

# =============================
# TAB 1: Linear Programming
# =============================
with tab1:
    st.header("1️⃣ Optimasi Produksi (Linear Programming)")

    st.markdown("**📚 Studi Kasus: Produksi Kursi (x) dan Meja (y)**")
    st.markdown("""
    PT Maju Jaya memproduksi **kursi (x)** dan **meja (y)**.  
    - Kursi memberi keuntungan Rp30.000 dan memerlukan 3 jam kerja serta 4 meter kayu.  
    - Meja memberi keuntungan Rp50.000 dan memerlukan 5 jam kerja serta 2 meter kayu.
    """)

    st.subheader("🔧 Input Parameter Produksi")
    jam_kerja = st.number_input("Total jam kerja tersedia", value=240.0)
    kayu = st.number_input("Total kayu tersedia (meter)", value=160.0)

    st.subheader("📐 Model Matematika")
    st.latex(r"\text{Maksimalkan:} \quad Z = 30x + 50y")
    st.latex(r"\text{Dengan kendala:}")
    st.latex(r"3x + 5y \leq " + str(jam_kerja))
    st.latex(r"4x + 2y \leq " + str(kayu))
    st.latex(r"x \geq 0, \quad y \geq 0")

    if st.button("🔍 Hitung Solusi Optimal"):
        c = [-30, -50]
        A = [[3, 5], [4, 2]]
        b = [jam_kerja, kayu]
        bounds = [(0, None), (0, None)]

        result = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

        if result.success:
            x_opt, y_opt = result.x
            z_max = -result.fun
            st.success(f"✅ Keuntungan Maksimal: Rp{z_max * 1000:,.0f}")
            st.markdown(f"- Kursi (x): {x_opt:.2f} unit  \n- Meja (y): {y_opt:.2f} unit")

            # Visualisasi solusi
            x_vals = np.linspace(0, jam_kerja / 3 + 10, 200)
            y1 = (jam_kerja - 3 * x_vals) / 5
            y2 = (kayu - 4 * x_vals) / 2

            fig, ax = plt.subplots()
            ax.plot(x_vals, y1, label="3x + 5y ≤ jam kerja")
            ax.plot(x_vals, y2, label="4x + 2y ≤ kayu")
            ax.fill_between(x_vals, 0, np.minimum(y1, y2), where=(np.minimum(y1, y2) >= 0), color='lightblue', alpha=0.5)
            ax.plot(x_opt, y_opt, 'ro', label="Solusi Optimal")
            ax.set_xlabel("Kursi (x)")
            ax.set_ylabel("Meja (y)")
            ax.set_xlim(left=0)
            ax.set_ylim(bottom=0)
            ax.set_title("Wilayah Solusi Linear Programming")
            ax.legend()
            st.pyplot(fig)
        else:
            st.error("❌ Gagal menemukan solusi.")

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
# =============================
with tab4:
    st.header("4️⃣ Analisis Turunan Parsial f(x, y)")

    x, y = sp.symbols('x y')
    fungsi_str = st.text_input("Masukkan fungsi f(x, y):", "x**3 + y + y**2")

    try:
        f = sp.sympify(fungsi_str)
        fx = sp.diff(f, x)
        fy = sp.diff(f, y)

        st.latex(f"f(x, y) = {sp.latex(f)}")
        st.latex(f"\\frac{{\\partial f}}{{\\partial x}} = {sp.latex(fx)}")
        st.latex(f"\\frac{{\\partial f}}{{\\partial y}} = {sp.latex(fy)}")

        x0 = st.number_input("Nilai x₀:", value=1.0)
        y0 = st.number_input("Nilai y₀:", value=2.0)

        f_val = f.subs({x: x0, y: y0})
        fx_val = fx.subs({x: x0, y: y0})
        fy_val = fy.subs({x: x0, y: y0})

        st.write(f"Nilai fungsi di titik (x₀, y₀): {f_val}")
        st.write(f"Gradien di titik (x₀, y₀): ({fx_val}, {fy_val})")

        x_vals = np.linspace(x0 - 2, x0 + 2, 50)
        y_vals = np.linspace(y0 - 2, y0 + 2, 50)
        X, Y = np.meshgrid(x_vals, y_vals)

        f_lambdified = sp.lambdify((x, y), f, 'numpy')
        Z = f_lambdified(X, Y)
        Z_tangent = float(f_val) + float(fx_val)*(X - x0) + float(fy_val)*(Y - y0)

        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, alpha=0.7, cmap='viridis')
        ax.plot_surface(X, Y, Z_tangent, alpha=0.5, color='red')
        ax.set_title("Permukaan f(x, y) dan bidang singgungnya")
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
