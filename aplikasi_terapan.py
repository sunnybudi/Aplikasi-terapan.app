import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from scipy.optimize import linprog
import math

# =========================
# SIDEBAR - PETUNJUK
# =========================
st.sidebar.title("\U0001F4D8 Petunjuk Penggunaan")
st.sidebar.markdown("""
Aplikasi ini memiliki 4 model matematika industri:

1. **Optimasi & Jumlah Mesin & Operator**  
2. **Model Persediaan EOQ**  
3. **Model Antrian (M/M/1)**  
4. **Turunan Parsial**

Masukkan data sesuai tab. Hasil & grafik akan muncul secara otomatis.
""")

# =========================
# TAB UTAMA
# =========================
st.title("\U0001F4CA Aplikasi Model Matematika Industri")

tab1, tab2, tab3, tab4 = st.tabs([
    "1. Optimasi & Jumlah Mesin & Operator",
    "2. Model Persediaan (EOQ)",
    "3. Model Antrian (M/M/1)",
    "4. Turunan Parsial"
])

# =========================
# TAB 1: Optimasi & Jumlah Mesin & Operator
# =========================
with tab1:
    st.header("1️⃣ Optimasi & Jumlah Mesin & Operator")

    mode = st.radio("Pilih Mode", ["Optimasi Biaya (LP)", "Jumlah Mesin & Operator (Integer)"])

    target = st.number_input("🎯 Target Produksi Harian (unit)", min_value=1, value=600, step=10)
    jam_kerja = st.number_input("🕒 Jam Kerja per Hari (jam)", min_value=1, value=8)
    kapasitas = st.number_input("⚙️ Kapasitas Mesin & Operator (unit/jam)", value=6)
    biaya_mesin = st.number_input("💰 Biaya Mesin (ribu/hari)", value=300)
    biaya_operator = st.number_input("💰 Biaya Operator (ribu/hari)", value=200)
    kapasitas_harian = kapasitas * jam_kerja

    if mode == "Optimasi Biaya (LP)":
        st.subheader("Optimasi Biaya dengan Linear Programming")

        bounds = [(0, None), (0, None)]
        c = [biaya_mesin, biaya_operator]
        A_ub = [[-kapasitas_harian, -kapasitas_harian]]
        b_ub = [-target]

        res = linprog(c=c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')

        if res.success:
            mesin, operator = res.x
            total_biaya = res.fun
            total_produksi = (mesin + operator) * kapasitas_harian
            biaya_per_unit = (total_biaya * 1000) / total_produksi

            st.success(f"✅ Biaya Minimum: Rp {total_biaya * 1000:,.0f}")
            st.write(f"🏭 Total Produksi: **{total_produksi:.0f} unit/hari**")
            st.write(f"💸 Biaya per Unit Produksi: Rp {biaya_per_unit:,.2f}")

            fig, ax = plt.subplots()
            ax.bar(["Mesin", "Operator"], [mesin, operator], color=["skyblue", "orange"])
            ax.set_ylabel("Jumlah Unit")
            st.pyplot(fig)
        else:
            st.error("❌ Gagal menemukan solusi optimal.")

    elif mode == "Jumlah Mesin & Operator (Integer)":
        st.subheader("Perhitungan Jumlah Mesin & Operator (Integer)")

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
                st.pyplot(fig)

                solusi_ditemukan = True
                break

        if not solusi_ditemukan:
            st.error("❌ Tidak ditemukan kombinasi mesin & operator untuk target tersebut.")

# =========================
# TAB 2: EOQ
# =========================
with tab2:
    st.header("📦 Model Persediaan EOQ")
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

        Q = np.linspace(1, 2 * EOQ, 100)
        TC = (D / Q) * S + (Q / 2) * H

        fig, ax = plt.subplots()
        ax.plot(Q, TC)
        ax.axvline(EOQ, color='red', linestyle='--')
        ax.set_xlabel("Jumlah Pesanan")
        ax.set_ylabel("Total Biaya")
        st.pyplot(fig)
    else:
        st.warning("Input harus lebih besar dari 0")

# =========================
# TAB 3: M/M/1 Queueing
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
    else:
        st.warning("λ harus < μ dan > 0")

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
        ax.set_title("f(x, y) dan Bidang Singgung di (x₀, y₀)")
        st.pyplot(fig)
    except:
        st.error("Fungsi tidak valid. Gunakan format Python: x**2 + y**2")
