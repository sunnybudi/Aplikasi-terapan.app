import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sympy as sp
from scipy.optimize import linprog
import math

st.sidebar.title("📘 Petunjuk Penggunaan")
st.sidebar.markdown("""
Aplikasi ini memiliki 4 model matematika industri:

1. **Optimasi & Jumlah Mesin & Operator**
2. **Model Persediaan EOQ**
3. **Model Antrian (M/M/1)**
4. **Turunan Parsial**
""")

st.title("📊 Aplikasi Model Matematika Industri")

tab1, tab2, tab3, tab4 = st.tabs([
    "1. Optimasi & Jumlah Mesin & Operator",
    "2. Model Persediaan (EOQ)",
    "3. Model Antrian (M/M/1)",
    "4. Turunan Parsial"
])

# =========================
# TAB 1: Optimasi & Integer
# =========================
with tab1:
    st.header("1️⃣ Optimasi & Jumlah Mesin & Operator")

    target = st.number_input("🎯 Target Produksi Harian (unit)", min_value=1, value=600, step=10)
    jam_kerja = st.number_input("🕒 Jam Kerja per Hari", min_value=1, value=8)
    kapasitas = st.number_input("⚙️ Kapasitas Mesin & Operator (unit/jam)", value=6)
    biaya_mesin = st.number_input("💰 Biaya Mesin (ribu/hari)", value=300)
    biaya_operator = st.number_input("💰 Biaya Operator (ribu/hari)", value=200)
    jumlah_mesin_max = st.number_input("🔧 Jumlah Maksimal Mesin", min_value=1, value=10)
    jumlah_operator_max = st.number_input("👷 Jumlah Maksimal Operator", min_value=1, value=20)

    kapasitas_harian = kapasitas * jam_kerja
    c = [biaya_mesin, biaya_operator]
    A_ub = [[-kapasitas_harian, -kapasitas_harian]]
    b_ub = [-target]
    bounds = [(0, jumlah_mesin_max), (0, jumlah_operator_max)]

    res = linprog(c=c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')

    st.subheader("🔍 Optimasi Biaya Mesin & Operator")
    if res.success:
        mesin, operator = res.x
        total_biaya = res.fun
        produksi_mesin = mesin * kapasitas_harian
        produksi_operator = operator * kapasitas_harian
        total_produksi = produksi_mesin + produksi_operator
        biaya_per_unit = (total_biaya * 1000) / total_produksi

        st.success(f"✅ Biaya Minimum: Rp {total_biaya*1000:,.0f}")
        st.write(f"🏭 Total Produksi: **{total_produksi:.0f} unit/hari**")
        st.write(f"💸 Biaya per Unit Produksi: Rp {biaya_per_unit:,.2f}")

        fig, ax = plt.subplots()
        ax.bar(["Mesin", "Operator"], [produksi_mesin, produksi_operator], color=["skyblue", "orange"])
        ax.axhline(target, color='red', linestyle='--', label="Target")
        ax.set_ylabel("Produksi (unit/hari)")
        ax.set_title("Kontribusi Produksi")
        ax.legend()
        st.pyplot(fig)
    else:
        st.error("❌ Gagal menemukan solusi optimal.")

    st.divider()
    st.subheader("🔍 Hitung Jumlah Mesin & Operator (Integer)")
    solusi_ditemukan = False
    for total_personil in range(1, 100):
        produksi = total_personil * kapasitas_harian
        if produksi >= target:
            mesin = total_personil // 2
            operator = total_personil - mesin
            produksi_aktual = (mesin + operator) * kapasitas_harian
            total_biaya = (mesin * biaya_mesin) + (operator * biaya_operator)

            st.success("✅ Solusi Ditemukan")
            st.write(f"🔧 Jumlah Mesin: **{mesin} unit**")
            st.write(f"👷 Jumlah Operator: **{operator} orang**")
            st.write(f"🏭 Total Produksi Aktual: **{produksi_aktual} unit/hari**")
            st.write(f"💵 Total Biaya Harian: **Rp {total_biaya * 1000:,.0f}**")

            fig, ax = plt.subplots()
            ax.bar(["Mesin", "Operator"], [mesin, operator], color=["skyblue", "orange"])
            ax.set_ylabel("Jumlah")
            ax.set_title("Jumlah Mesin & Operator")
            st.pyplot(fig)
            solusi_ditemukan = True
            break
    if not solusi_ditemukan:
        st.error("❌ Tidak ditemukan kombinasi mesin & operator.")

# =========================
# TAB 2: EOQ
# =========================
with tab2:
    st.header("📦 Model Persediaan Bahan Baku (EOQ)")
    D = st.number_input("📅 Permintaan Tahunan (unit bahan baku)", min_value=1, value=10000)
    S = st.number_input("🛒 Biaya Pemesanan per Order (Rp)", min_value=0, value=50000)
    H = st.number_input("🏬 Biaya Penyimpanan per Unit per Tahun (Rp)", min_value=0, value=2000)

    if D > 0 and S > 0 and H > 0:
        EOQ = math.sqrt((2 * D * S) / H)
        frekuensi_pesan = D / EOQ
        siklus_hari = 365 / frekuensi_pesan

        st.success(f"🔢 EOQ (Jumlah Pesan Optimal): {EOQ:.2f} unit")
        st.write(f"📦 Frekuensi Pesan per Tahun: {frekuensi_pesan:.2f} kali")
        st.write(f"⏳ Interval Pemesanan: setiap **{siklus_hari:.0f} hari**")

        Q = np.linspace(1, 2 * EOQ, 100)
        TC = (D / Q) * S + (Q / 2) * H
        fig, ax = plt.subplots()
        ax.plot(Q, TC, label="Total Cost")
        ax.axvline(EOQ, color='red', linestyle='--', label='EOQ')
        ax.set_xlabel("Jumlah Pemesanan (unit)")
        ax.set_ylabel("Total Biaya (Rp)")
        ax.set_title("Kurva Biaya Total vs EOQ")
        ax.legend()
        st.pyplot(fig)
    else:
        st.warning("❗ Semua input harus lebih dari 0.")

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
