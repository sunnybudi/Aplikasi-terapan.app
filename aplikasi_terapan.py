import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import math

# =========================
# SIDEBAR - PETUNJUK
# =========================
st.sidebar.title("\U0001F4D8 Petunjuk Penggunaan")
st.sidebar.markdown("""
Aplikasi ini memiliki 3 model matematika industri:

1. **Simulasi Manual Mesin & Operator**  
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
    "1. Simulasi Manual Mesin & Operator",
    "2. Model Persediaan (EOQ)",
    "3. Model Antrian (M/M/1)",
    "4. Turunan Parsial"
])

# =========================
# TAB 1: Simulasi Manual Mesin & Operator
# =========================
with tab1:
    st.header("1️⃣ Simulasi Manual Jumlah Mesin & Operator")

    target = st.number_input("🎯 Target Produksi Harian (unit)", min_value=1, value=600, step=10)
    jam_kerja = st.number_input("🕒 Jam Kerja per Hari (jam)", min_value=1, value=8)
    kapasitas = st.number_input("⚙️ Kapasitas Mesin & Operator (unit/jam)", value=6)
    biaya_mesin = st.number_input("💰 Biaya Mesin (ribu/hari)", value=300)
    biaya_operator = st.number_input("💰 Biaya Operator (ribu/hari)", value=200)
    kapasitas_harian = kapasitas * jam_kerja

    mesin = st.number_input("🔧 Jumlah Mesin (input manual)", min_value=0, step=1)
    operator = st.number_input("👷 Jumlah Operator (input manual)", min_value=0, step=1)

    pasangan_kerja = min(mesin, operator)
    produksi_aktual = pasangan_kerja * kapasitas_harian
    total_biaya = (mesin * biaya_mesin) + (operator * biaya_operator)

    st.write(f"🔁 Jumlah Pasangan Mesin-Operator: **{pasangan_kerja}**")
    st.write(f"🏭 Total Produksi Aktual: **{produksi_aktual} unit/hari**")
    st.write(f"💵 Total Biaya Harian: **Rp {total_biaya * 1000:,.0f}**")

    fig, ax = plt.subplots()
    ax.bar(["Mesin", "Operator"], [mesin, operator], color=["skyblue", "orange"])
    ax.set_ylabel("Jumlah")
    st.pyplot(fig)

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
