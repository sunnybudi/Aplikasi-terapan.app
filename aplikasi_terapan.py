import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sympy as sp
from scipy.optimize import linprog

# =============================
# SIDEBAR - PETUNJUK
# =============================
st.sidebar.title("\ud83d\udcd8\ufe0f Petunjuk Penggunaan")
st.sidebar.markdown("""
Aplikasi ini memiliki 4 model matematika industri:

1. **Optimasi Mesin & Operator (5 tipe)**  
2. **Model Persediaan EOQ**  
3. **Model Antrian (M/M/1)**  
4. **Analisis Turunan Parsial**

Masukkan data sesuai tab. Hasil & grafik akan muncul secara otomatis.
""")

# =============================
# TAB UTAMA
# =============================
st.title("\ud83d\udcca Aplikasi Model Matematika Industri")

tab1, tab2, tab3, tab4 = st.tabs([
    "1. Optimasi Mesin & Operator",
    "2. Model Persediaan (EOQ)",
    "3. Model Antrian (M/M/1)",
    "4. Model Matematika Lain (Turunan Parsial)"
])

# =============================
# TAB 1: Optimasi 5 Mesin & 5 Operator
# =============================
with tab1:
    st.header("1\ufe0f\ufe0f\ufe0f Optimasi 5 Mesin dan 5 Operator")

    target = st.number_input("\ud83c\udf1f Target Produksi Harian (unit)", min_value=1, value=500, step=1)

    kapasitas_mesin = [8, 7, 6, 5, 4]  # unit/jam
    biaya_mesin = [300, 280, 260, 240, 220]  # ribu/hari
    kapasitas_operator = [6, 5.5, 5, 4.5, 4]  # unit/jam
    biaya_operator = [200, 190, 180, 170, 160]  # ribu/hari
    jam_kerja = 8

    total_kap_mesin = [k * jam_kerja for k in kapasitas_mesin]
    total_kap_op = [k * jam_kerja for k in kapasitas_operator]

    c = biaya_mesin + biaya_operator
    A_ub = [-np.array(total_kap_mesin + total_kap_op)]
    b_ub = [-target]
    bounds = [(0, None)] * 10

    res = linprog(c=c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')

    if res.success:
        x_opt = res.x
        total_biaya = res.fun
        prod_mesin = np.dot(x_opt[:5], total_kap_mesin)
        prod_op = np.dot(x_opt[5:], total_kap_op)

        st.success(f"\u2705 Biaya Minimum: Rp {total_biaya*1000:,.0f}")

        st.subheader("\ud83e\uddf9 Mesin")
        mesin_df = pd.DataFrame({
            "Mesin": [f"M{i+1}" for i in range(5)],
            "Kapasitas": total_kap_mesin,
            "Biaya": biaya_mesin,
            "Jumlah": np.round(x_opt[:5], 2)
        })
        st.dataframe(mesin_df)

        st.subheader("\ud83d\udc69\u200d\ud83d\udcbc Operator")
        operator_df = pd.DataFrame({
            "Operator": [f"O{i+1}" for i in range(5)],
            "Kapasitas": total_kap_op,
            "Biaya": biaya_operator,
            "Jumlah": np.round(x_opt[5:], 2)
        })
        st.dataframe(operator_df)

        st.subheader("\ud83d\udcca Grafik Produksi")
        fig, ax = plt.subplots()
        ax.bar(["Mesin", "Operator"], [prod_mesin, prod_op], color=["skyblue", "orange"])
        ax.axhline(target, color='red', linestyle='--', label="Target")
        ax.set_ylabel("Produksi (unit/hari)")
        ax.legend()
        st.pyplot(fig)
    else:
        st.error("\u274c Gagal menemukan solusi optimal.")

# =============================
# TAB 2: EOQ
# =============================
with tab2:
    st.header("2\ufe0f\ufe0f\ufe0f Model Persediaan EOQ")
    D = st.number_input("Permintaan Tahunan (D)", value=1000.0)
    S = st.number_input("Biaya Pemesanan (S)", value=50.0)
    H = st.number_input("Biaya Simpan (H)", value=2.0)

    if D > 0 and S > 0 and H > 0:
        EOQ = np.sqrt((2 * D * S) / H)
        st.success(f"EOQ: {EOQ:.2f} unit")

        Q = np.linspace(1, 2 * EOQ, 100)
        TC = (D / Q) * S + (Q / 2) * H
        fig, ax = plt.subplots()
        ax.plot(Q, TC)
        ax.axvline(EOQ, color='red', linestyle='--', label='EOQ')
        ax.set_xlabel("Jumlah Pesanan")
        ax.set_ylabel("Total Biaya")
        ax.set_title("Total Biaya vs EOQ")
        ax.legend()
        st.pyplot(fig)
    else:
        st.warning("D, S, H harus > 0")

# =============================
# TAB 3: Antrian M/M/1
# =============================
with tab3:
    st.header("3\ufe0f\ufe0f\ufe0f Model Antrian M/M/1")
    lambd = st.number_input("Tingkat Kedatangan (λ)", value=2.0)
    mu = st.number_input("Tingkat Pelayanan (μ)", value=3.0)

    if mu > lambd and lambd > 0:
        rho = lambd / mu
        L = rho / (1 - rho)
        Lq = rho**2 / (1 - rho)
        W = 1 / (mu - lambd)
        Wq = rho / (mu - lambd)

        st.write(f"\nUtilisasi: {rho:.2f}, L: {L:.2f}, Lq: {Lq:.2f}, W: {W:.2f}, Wq: {Wq:.2f}")

        rho_vals = np.linspace(0.01, 0.99, 100)
        L_vals = rho_vals / (1 - rho_vals)
        fig, ax = plt.subplots()
        ax.plot(rho_vals, L_vals)
        ax.set_xlabel("ρ")
        ax.set_ylabel("L")
        ax.set_title("Utilisasi vs L")
        st.pyplot(fig)
    else:
        st.error("λ < μ agar sistem stabil")

# =============================
# TAB 4: Turunan Parsial
# =============================
with tab4:
    st.header("4️⃣ Turunan Parsial")
    x, y = sp.symbols('x y')
    fungsi = st.text_input("Masukkan f(x, y):", "x**3 + y + y**2")

    try:
        f = sp.sympify(fungsi)
        # Validasi simbol
        if not (x in f.free_symbols and y in f.free_symbols):
            st.warning("Fungsi harus mengandung variabel x dan y.")
        else:
            fx = sp.diff(f, x)
            fy = sp.diff(f, y)

            x0 = st.number_input("x₀:", value=1.0)
            y0 = st.number_input("y₀:", value=2.0)

            f_val = f.subs({x: x0, y: y0}).evalf()
            fx_val = fx.subs({x: x0, y: y0}).evalf()
            fy_val = fy.subs({x: x0, y: y0}).evalf()

            st.latex(f"f(x, y) = {sp.latex(f)}")
            st.latex(f"\\frac{{\\partial f}}{{\\partial x}} = {sp.latex(fx)}")
            st.latex(f"\\frac{{\\partial f}}{{\\partial y}} = {sp.latex(fy)}")
            st.write(f"Nilai f(x₀, y₀): {f_val}")
            st.write(f"Gradien di titik ({x0}, {y0}): (∂f/∂x = {fx_val}, ∂f/∂y = {fy_val})")

            # Buat meshgrid dan evaluasi fungsi
            X, Y = np.meshgrid(np.linspace(x0 - 2, x0 + 2, 50), np.linspace(y0 - 2, y0 + 2, 50))
            f_np = sp.lambdify((x, y), f, 'numpy')
            Z = f_np(X, Y)
            Z_tangent = float(f_val) + float(fx_val)*(X - x0) + float(fy_val)*(Y - y0)

            # Plot 3D
            fig = plt.figure(figsize=(10, 6))
            ax = fig.add_subplot(111, projection='3d')
            ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7)
            ax.plot_surface(X, Y, Z_tangent, color='red', alpha=0.5)
            ax.set_title("Permukaan dan Bidang Singgung")
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.set_zlabel("f(x, y)")
            st.pyplot(fig)
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
