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

1. **Optimasi Mesin & Operator**  
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
    "1. Optimasi Mesin & Operator",
    "2. Model Persediaan (EOQ)",
    "3. Model Antrian (M/M/1)",
    "4. Model Matematika Lain (Turunan Parsial)"
])

# =============================
# TAB 1: Optimasi Mesin & Operator
# =============================
with tab1:
    st.header("1️⃣ Optimasi Jumlah Mesin dan Operator")

    st.markdown("**Studi Kasus: Kombinasi Mesin dan Operator untuk Produksi Harian**")
    st.markdown("""
    Sebuah pabrik ingin memproduksi **minimal 100 unit per hari** dengan kombinasi mesin dan operator.  
    Tujuan: **Minimalkan biaya total**.

    - **Mesin (x)**: memproses 5 unit/jam, biaya Rp200.000/hari  
    - **Operator (y)**: memproses 4 unit/jam, biaya Rp150.000/hari  
    """)

    target_unit = st.number_input("Target unit yang harus diproduksi", value=100.0)

    st.subheader("📐 Model Matematika")
    st.latex(r"\text{Minimalkan: } Z = 200x + 150y")
    st.latex(r"\text{Kendala: } 5x + 4y \geq " + str(target_unit))
    st.latex(r"x \geq 0, \quad y \geq 0")

    if st.button("🔍 Hitung Kombinasi Optimal"):
        c = [200, 150]
        A = [[-5, -4]]  # dikali -1 karena linprog hanya mendukung <=
        b = [-target_unit]
        bounds = [(0, None), (0, None)]

        result = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

        if result.success:
            x_opt = result.x[0]
            y_opt = result.x[1]
            cost = result.fun

            st.success(f"✅ Biaya minimum: Rp{cost:,.0f}")
            st.markdown(f"""
            **Kombinasi Optimal:**
            - Mesin: {x_opt:.2f} unit  
            - Operator: {y_opt:.2f} orang  
            """)

            # Grafik kontur biaya
            x_vals = np.linspace(0, x_opt*2, 100)
            y_vals = np.linspace(0, y_opt*2, 100)
            X, Y = np.meshgrid(x_vals, y_vals)
            Z = 200*X + 150*Y
            feasible = (5*X + 4*Y) >= target_unit
            Z_masked = np.where(feasible, Z, np.nan)

            fig, ax = plt.subplots()
            cs = ax.contourf(X, Y, Z_masked, levels=20, cmap='viridis')
            ax.plot(x_opt, y_opt, 'ro', label='Solusi Optimal')
            ax.set_xlabel("Jumlah Mesin")
            ax.set_ylabel("Jumlah Operator")
            ax.set_title("Kontur Biaya Total")
            fig.colorbar(cs, ax=ax, label='Biaya')
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

    st.subheader("📐 Rumus EOQ")
    st.latex(r"\text{EOQ} = \sqrt{\frac{2DS}{H}}")

    if D > 0 and S > 0 and H > 0:
        EOQ = np.sqrt((2 * D * S) / H)
        st.success(f"🔢 EOQ = {EOQ:.2f} unit per pesanan")

        Q = np.linspace(1, 2 * EOQ, 100)
        TC = (D / Q) * S + (Q / 2) * H

        fig, ax = plt.subplots()
        ax.plot(Q, TC, label='Total Biaya')
        ax.axvline(EOQ, color='red', linestyle='--', label='EOQ')
        ax.set_xlabel("Jumlah Pesanan (Q)")
        ax.set_ylabel("Total Biaya")
        ax.set_title("Total Biaya vs Jumlah Pesanan")
        ax.legend()
        st.pyplot(fig)
    else:
        st.warning("❗ D, S, dan H harus lebih besar dari 0.")

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
