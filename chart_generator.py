import math

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle


# =========================
# PALET WARNA MODERN
# =========================
COLORS = [
    "#E74C3C",
    "#3498DB",
    "#2ECC71",
    "#F39C12",
    "#9B59B6",
    "#E67E22",
    "#1ABC9C",
    "#E91E63",
    "#5D6D7E",
    "#95A5A6",
]

GELAP = "#2C3E50"
ABU = "#7F8C8D"


def _warna_teks(warna):
    r = int(warna[1:3], 16)
    g = int(warna[3:5], 16)
    b = int(warna[5:7], 16)
    terang = 0.299 * r + 0.587 * g + 0.114 * b
    return GELAP if terang > 150 else "white"


def create_chart(site, data, filename):

    if not data:
        return False

    labels = [nama for nama, _ in data][:10]
    values = [nilai for _, nilai in data][:10]
    total = sum(values)
    n = len(values)

    persen = [round(v / total * 100, 1) for v in values]

    # =========================
    # SETUP
    # =========================

    fig, ax = plt.subplots(figsize=(12, 12))
    fig.patch.set_facecolor("white")

    # =========================
    # JUDUL
    # =========================

    fig.text(0.5, 0.955, "TOP 10 APLIKASI",
             ha="center", va="center",
             fontsize=30, fontweight="bold", color=GELAP)

    fig.text(0.5, 0.915, site,
             ha="center", va="center",
             fontsize=17, color=ABU)

    fig.add_artist(Line2D(
        [0.42, 0.58], [0.885, 0.885],
        transform=fig.transFigure,
        color=COLORS[0], linewidth=3
    ))

    # =========================
    # PIE CHART (DONUT)
    # =========================

    explode = [0.06 if i == 0 else 0.015 for i in range(n)]

    wedges, _ = ax.pie(
        values,
        colors=COLORS[:n],
        startangle=90,
        counterclock=False,
        explode=explode,
        wedgeprops=dict(linewidth=4, edgecolor="white")
    )

    # lubang tengah donut
    ax.add_artist(plt.Circle(
        (0, 0), 0.45,
        facecolor="white", edgecolor="white"
    ))

    # highlight aplikasi #1 di tengah
    ukuran = 20 if len(labels[0]) <= 12 else 16

    ax.text(0, 0.16, "#1", ha="center", va="center",
            fontsize=15, fontweight="bold", color=COLORS[0])

    ax.text(0, 0.01, labels[0], ha="center", va="center",
            fontsize=ukuran, fontweight="bold", color=GELAP)

    ax.text(0, -0.16, f"{persen[0]}%", ha="center", va="center",
            fontsize=28, fontweight="bold", color=COLORS[0])

    # =========================
    # LABEL PERSENTASE
    # =========================

    luar = []

    for i, wedge in enumerate(wedges):

        sudut = math.radians((wedge.theta1 + wedge.theta2) / 2)

        if persen[i] >= 4:

            r = 0.72 + explode[i]

            ax.text(
                r * math.cos(sudut),
                r * math.sin(sudut),
                f"{persen[i]}%",
                ha="center", va="center",
                fontsize=15 if persen[i] < 20 else 19,
                fontweight="bold",
                color=_warna_teks(COLORS[i])
            )

        else:

            luar.append((sudut, i))

    # label kecil di luar, disebar supaya tidak bertumpuk

    if luar:

        jarak_min = 0.17

        for tanda in (-1, 1):

            sisi = [
                x for x in luar
                if (1 if math.cos(x[0]) >= 0 else -1) == tanda
            ]

            if not sisi:
                continue

            sisi.sort(key=lambda c: -math.sin(c[0]))

            ys = [1.28 * math.sin(c[0]) for c in sisi]

            for j in range(1, len(ys)):
                if ys[j] > ys[j - 1] - jarak_min:
                    ys[j] = ys[j - 1] - jarak_min

            for (sudut, i), y in zip(sisi, ys):

                x0 = (1.02 + explode[i]) * math.cos(sudut)
                y0 = (1.02 + explode[i]) * math.sin(sudut)

                ax.annotate(
                    f"{labels[i]}  {persen[i]}%",
                    xy=(x0, y0),
                    xytext=(1.15 * tanda, y),
                    ha="left" if tanda > 0 else "right",
                    va="center",
                    fontsize=13, fontweight="bold",
                    color=GELAP,
                    arrowprops=dict(
                        arrowstyle="-",
                        color="#B0BEC5",
                        linewidth=1.3,
                        connectionstyle="angle,angleA=0,angleB=90"
                    )
                )

    # =========================
    # DAFTAR PERINGKAT
    # 5 KIRI + 5 KANAN
    # =========================

    kolom = [
        list(range(min(5, n))),
        list(range(5, n))
    ]

    posisi = [
        {"kotak": 0.09, "teks": 0.125, "pct": 0.47},
        {"kotak": 0.55, "teks": 0.585, "pct": 0.93}
    ]

    y_awal = 0.23
    langkah = 0.048

    for ci, idxs in enumerate(kolom):

        pos = posisi[ci]

        if not idxs:
            continue

        fig.text(
            pos["teks"], y_awal + 0.035,
            f"PERINGKAT {idxs[0] + 1} - {idxs[-1] + 1}",
            ha="left", va="center",
            fontsize=11, fontweight="bold", color=ABU
        )

        for baris, i in enumerate(idxs):

            y = y_awal - baris * langkah

            fig.add_artist(Rectangle(
                (pos["kotak"], y - 0.010),
                0.022, 0.022,
                transform=fig.transFigure,
                facecolor=COLORS[i], edgecolor="none"
            ))

            fig.text(
                pos["teks"], y,
                f"{i + 1}. {labels[i]}",
                ha="left", va="center",
                fontsize=14, fontweight="bold",
                color=GELAP
            )

            fig.text(
                pos["pct"], y,
                f"{persen[i]}%",
                ha="right", va="center",
                fontsize=14, fontweight="bold",
                color=COLORS[i]
            )

    # =========================
    # SIMPAN
    # =========================

    plt.subplots_adjust(
        left=0.03, right=0.97,
        top=0.76, bottom=0.30
    )

    plt.savefig(filename, dpi=300, bbox_inches="tight")
    plt.close()

    return True