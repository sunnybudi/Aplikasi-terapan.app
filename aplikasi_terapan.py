import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sympy as sp
from scipy.optimize import linprog
import math

# =========================
# SIDEBAR - PETUNJUK
# =========================
st.sidebar.title("📘 Petunjuk Penggunaan")
st.sidebar.markdown("""
Aplikasi ini memiliki 5 model matematika industri:

1. **Optimasi Biaya Mesin & Operator (LP)**  
2. **Hitung Jumlah Mesin & Operator (Integer)**  
3. **Model Persediaan EOQ**  
4. **Model Antrian (M/M/1)**  
5. **Turunan Parsial**

Masukkan data sesuai tab. Hasil & grafik akan muncul secara otomatis.
""")

# =========================
# TAB UTAMA
# =========================
st.title("📊 Aplikasi Model Matematika Industri")

tab1, tab1b, tab2, tab3, tab4 = st.tabs([
    "1. Optimasi Biaya Mesin & Operator",
    "2. Jumlah Mesin & Operator (Integer)",
    "3. Model Persediaan (EOQ)",
    "4. Model Antrian (M/M/1)",
    "5. Turunan Parsial"
])

# =========================
# TAB 1: Optimasi Biaya Mesin & Operator (LP)
# =========================
with tab1:
    st.header("1️⃣ Optimasi Biaya Mesin & Operator")

    target = st.number_input("🎯 Target Produksi Harian (unit)", min_value=1, value=600, step=10)
    jam_kerja = st.number_input("🕒 Jam Kerja per Hari", min_value=1, value=8)

    kapasitas = st.number_input("⚙️ Kapasitas Mesin & Operator (unit/jam)", value=6)
    biaya_mesin = st.number_input("💰 Biaya Mesin (ribu/hari)", value=300)
    biaya_operator = st.number_input("💰 Biaya Operator (ribu/hari)", value=200)
    jumlah_mesin = st.number_input("Jumlah Mesin (unit)", value=10)
    jumlah_operatot = st.number_input("Jumlah Operator (orang)", value=20)

    kapasitas_harian = kapasitas * jam_kerja
    c = [biaya_mesin, biaya_operator]
    A_ub = [[-kapasitas_harian, -kapasitas_harian]]
    b_ub = [-target]
    bounds = [(0, None), (0, None)]

    res = linprog(c=c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')

    if res.success:
        mesin, operator = res.x
        total_biaya = res.fun
        produksi_mesin = mesin * kapasitas_harian
        produksi_operator = operator * kapasitas_harian

        st.success(f"✅ Biaya Minimum: Rp {total_biaya*1000:,.0f}")
        st.write(f"Jumlah Mesin: {mesin:.2f}")
        st.write(f"Jumlah Operator: {operator:.2f}")

        fig, ax = plt.subplots()
        ax.bar(["Mesin", "Operator"], [produksi_mesin, produksi_operator], color=["skyblue", "orange"])
        ax.axhline(target, color='red', linestyle='--', label="Target")
        ax.set_ylabel("Produksi (unit/hari)")
        ax.legend()
        st.pyplot(fig)
    else:
        st.error("❌ Gagal menemukan solusi optimal.")

# =========================
# TAB 1b: Jumlah Mesin & Operator (Integer)
# =========================
with tab1b:
    st.header("2️⃣ Hitung Jumlah Mesin & Operator (Integer)")

    target_int = st.number_input("🎯 Target Produksi Harian", min_value=1, value=600, step=10)
    jam_kerja_int = st.number_input("🕒 Jam Kerja (jam/hari)", min_value=1, value=8)
    kapasitas_int = st.number_input("⚙️ Kapasitas Mesin dan Operator (unit/jam)", value=6.0)

    kapasitas_hari = kapasitas_int * jam_kerja_int

    total_produksi = (jumlah_mesin + jumlah_operator) * kapasitas_hari

    st.success("🔢 Jumlah Minimum Mesin & Operator (Integer)")
    st.write(f"Jumlah Mesin yang dibutuhkan: {jumlah_mesin}")
    st.write(f"Jumlah Operator yang dibutuhkan: {jumlah_operator}")
    st.write(f"Total Produksi per Hari: {total_produksi} unit")

# =========================
# TAB 2: EOQ
# =========================
with tab2:
    st.header("3️⃣ Model Persediaan EOQ")

    D = st.number_input("Permintaan Tahunan (D)", value=1000.0)
    S = st.number_input("Biaya Pemesanan per Order (S)", value=50.0)
    H = st.number_input("Biaya Simpan per Unit per Tahun (H)", value=2.0)

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
        st.warning("Input harus lebih dari 0.")

# =========================
# TAB 3: Antrian M/M/1
# =========================
with tab3:
    st.header("4️⃣ Model Antrian M/M/1")

    lambd = st.number_input("Tingkat Kedatangan (λ)", value=2.0)
    mu = st.number_input("Tingkat Pelayanan (μ)", value=3.0)

    if mu > lambd and lambd > 0:
        rho = lambd / mu
        L = rho / (1 - rho)
        Lq = rho**2 / (1 - rho)
        W = 1 / (mu - lambd)
        Wq = rho / (mu - lambd)

        st.write(f"Utilisasi ρ: {rho:.2f}")
        st.write(f"Rata-rata dalam sistem (L): {L:.2f}")
        st.write(f"Rata-rata dalam antrian (Lq): {Lq:.2f}")
        st.write(f"Waktu dalam sistem (W): {W:.2f}")
        st.write(f"Waktu tunggu (Wq): {Wq:.2f}")

        rho_vals = np.linspace(0.01, 0.99, 100)
        L_vals = rho_vals / (1 - rho_vals)
        fig, ax = plt.subplots()
        ax.plot(rho_vals, L_vals)
        ax.set_xlabel("Utilisasi (ρ)")
        ax.set_ylabel("L")
        ax.set_title("Utilisasi vs Jumlah Rata-rata dalam Sistem (L)")
        st.pyplot(fig)
    else:
        st.error("λ harus < μ agar sistem stabil.")

# =========================
# TAB 4: Turunan Parsial
# =========================
with tab4:
    st.header("5️⃣ Turunan Parsial")

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

        st.latex(f"f(x, y) = {sp.latex(f)}")
        st.latex(f"\\frac{{\\partial f}}{{\\partial x}} = {sp.latex(fx)}")
        st.latex(f"\\frac{{\\partial f}}{{\\partial y}} = {sp.latex(fy)}")
        st.write(f"Nilai f: {f_val}, Gradien: ({fx_val}, {fy_val})")

        X, Y = np.meshgrid(np.linspace(x0-2, x0+2, 50), np.linspace(y0-2, y0+2, 50))
        f_np = sp.lambdify((x, y), f, 'numpy')
        Z = f_np(X, Y)
        Z_tangent = float(f_val) + float(fx_val)*(X - x0) + float(fy_val)*(Y - y0)

        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7)
        ax.plot_surface(X, Y, Z_tangent, color='red', alpha=0.5)
        ax.set_title("Permukaan f(x, y) dan Bidang Singgung di (x₀, y₀)")
        st.pyplot(fig)
    except:
        st.error("⚠️ Fungsi tidak valid. Gunakan sintaks Python seperti `x**2 + y**2`.")
