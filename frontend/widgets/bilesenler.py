"""
Atlas bileşenleri — Modern seyahat teması widget'ları.
"""
from PyQt5.QtWidgets import (
    QWidget,
    QFrame,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy,
)
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import (
    QPainter,
    QColor,
    QPen,
    QBrush,
    QFont,
    QFontMetrics,
    QLinearGradient,
)

# ── Renkler ──
BG = QColor("#faf8f5")
BG_ALT = QColor("#f2efe9")
SURFACE = QColor("#ffffff")
TEXT = QColor("#2c2c2c")
TEXT_SEC = QColor("#555550")
TEXT_MUTED = QColor("#8c8c88")
TEXT_HINT = QColor("#b0aea8")
BORDER = QColor("#d9d6d0")
BORDER_LIGHT = QColor("#e8e5df")
DIVIDER = QColor("#edeae4")
PRIMARY = QColor("#2d5a7b")
PRIMARY_DARK = QColor("#1e3f58")
PRIMARY_LIGHT = QColor("#e8f0f6")
ACCENT = QColor("#d4845a")
ACCENT_DARK = QColor("#b06a42")
ACCENT_LIGHT = QColor("#fdf0e8")
SUCCESS = QColor("#3a8a6a")
WARNING = QColor("#c49a3c")
DANGER = QColor("#c45454")

# ── Türkçe ay isimleri ──
AY_ISIMLERI = {
    1: "Ocak", 2: "Şubat", 3: "Mart", 4: "Nisan",
    5: "Mayıs", 6: "Haziran", 7: "Temmuz", 8: "Ağustos",
    9: "Eylül", 10: "Ekim", 11: "Kasım", 12: "Aralık",
}


def tarih_format(dt) -> str:
    return f"{dt.day} {AY_ISIMLERI[dt.month]} {dt.year}"


def tarih_aralik_format(baslangic, bitis) -> str:
    if baslangic.month == bitis.month and baslangic.year == bitis.year:
        return f"{baslangic.day}–{bitis.day} {AY_ISIMLERI[baslangic.month]} {baslangic.year}"
    elif baslangic.year == bitis.year:
        return (f"{baslangic.day} {AY_ISIMLERI[baslangic.month]} – "
                f"{bitis.day} {AY_ISIMLERI[bitis.month]} {bitis.year}")
    return f"{tarih_format(baslangic)} – {tarih_format(bitis)}"


# ============================================================
# METRİK KART — İkon-suz, sade rakam kartı
# ============================================================
class MetrikKart(QFrame):
    def __init__(self, etiket: str, deger: str = "0", altyazi: str = "",
                 accent: bool = False, parent=None):
        super().__init__(parent)
        sol_renk = "#d4845a" if accent else "#2d5a7b"
        self.setStyleSheet(
            "QFrame { background-color: #ffffff; "
            "border: 1px solid #e8e5df; "
            f"border-left: 3px solid {sol_renk}; "
            "border-radius: 8px; }"
        )
        self.setFixedHeight(130)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(6)

        et = QLabel(etiket.upper())
        et.setStyleSheet(
            "color: #8c8c88; font-family: 'Poppins', sans-serif; "
            "font-size: 10px; font-weight: 600; "
            "background: transparent; border: none;"
        )
        layout.addWidget(et)
        layout.addStretch()

        self.deger_lbl = QLabel(str(deger))
        self.deger_lbl.setStyleSheet(
            f"color: {sol_renk}; "
            "font-family: 'Poppins', sans-serif; "
            "font-size: 34px; font-weight: 700; "
            "background: transparent; border: none;"
        )
        layout.addWidget(self.deger_lbl)

        self.alt_lbl = QLabel(altyazi)
        self.alt_lbl.setStyleSheet(
            "color: #8c8c88; font-family: 'Poppins', sans-serif; "
            "font-size: 11px; background: transparent; border: none;"
        )
        layout.addWidget(self.alt_lbl)

        self._accent = accent

    def deger_ayarla(self, deger):
        deger_str = str(deger)
        n = len(deger_str)
        size = 34 if n <= 3 else (28 if n == 4 else 24)
        renk = "#d4845a" if self._accent else "#2d5a7b"
        self.deger_lbl.setStyleSheet(
            f"color: {renk}; font-family: 'Poppins', sans-serif; "
            f"font-size: {size}px; font-weight: 700; "
            "background: transparent; border: none;"
        )
        self.deger_lbl.setText(deger_str)

    def altyazi_ayarla(self, altyazi):
        self.alt_lbl.setText(altyazi)


# ============================================================
# MASTHEAD — Sidebar üst logo
# ============================================================
class Masthead(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(90)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w = self.width()

        # Accent çizgi
        p.setPen(Qt.NoPen)
        p.setBrush(ACCENT)
        p.drawRoundedRect(QRectF(24, 20, 28, 3), 1.5, 1.5)

        # Ana isim
        p.setPen(QColor("#ffffff"))
        font = QFont("Poppins", 20, QFont.Bold)
        if not font.exactMatch():
            font = QFont("Segoe UI", 20, QFont.Bold)
        p.setFont(font)
        p.drawText(QRectF(24, 30, w - 48, 30),
                   Qt.AlignLeft | Qt.AlignVCenter, "Yol Defteri")

        # Alt etiket
        p.setPen(QColor(255, 255, 255, 100))
        font = QFont("Poppins", 9)
        if not font.exactMatch():
            font = QFont("Segoe UI", 9)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 1.5)
        p.setFont(font)
        p.drawText(QRectF(24, 62, w - 48, 16),
                   Qt.AlignLeft | Qt.AlignVCenter, "SEYAHAT PLANLAMA")


# ============================================================
# SAYFA HEADER — Sayfa üst başlık
# ============================================================
class SayfaHeader(QWidget):
    def __init__(self, kategori: str, baslik: str, altyazi: str = "",
                 sag_metin: str = "", parent=None):
        super().__init__(parent)
        self.kategori = kategori
        self.baslik = baslik
        self.altyazi = altyazi
        self.sag_metin = sag_metin
        self.setFixedHeight(110)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w = self.width()
        h = self.height()

        # Kategori tag
        p.setPen(ACCENT)
        font = QFont("Poppins", 10, QFont.Bold)
        if not font.exactMatch():
            font = QFont("Segoe UI", 10, QFont.Bold)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 1.5)
        p.setFont(font)
        p.drawText(0, 22, self.kategori)

        # Sağ metin
        if self.sag_metin:
            p.setPen(TEXT_MUTED)
            fm = QFontMetrics(font)
            sx = w - fm.horizontalAdvance(self.sag_metin)
            p.drawText(sx, 22, self.sag_metin)

        # Başlık
        p.setPen(TEXT)
        font = QFont("Poppins", 32, QFont.Bold)
        if not font.exactMatch():
            font = QFont("Segoe UI", 32, QFont.Bold)
        font.setLetterSpacing(QFont.AbsoluteSpacing, -0.5)
        p.setFont(font)
        p.drawText(QRectF(0, 32, w, 44),
                   Qt.AlignLeft | Qt.AlignVCenter, self.baslik)

        # Altyazı
        if self.altyazi:
            p.setPen(TEXT_MUTED)
            font = QFont("Poppins", 13)
            if not font.exactMatch():
                font = QFont("Segoe UI", 13)
            p.setFont(font)
            p.drawText(QRectF(0, 78, w, 22),
                       Qt.AlignLeft | Qt.AlignVCenter, self.altyazi)

        # Alt çizgi
        p.setPen(QPen(BORDER_LIGHT, 1))
        p.drawLine(0, h - 1, w, h - 1)


# ============================================================
# HERO KART — Dashboard büyük kart
# ============================================================
class HeroKart(QWidget):
    def __init__(self, baslik: str, altyazi: str, metrikler: list = None,
                 parent=None):
        super().__init__(parent)
        self.baslik = baslik
        self.altyazi = altyazi
        self.metrikler = metrikler or []
        self.setMinimumHeight(220)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def metrikleri_ayarla(self, metrikler: list):
        self.metrikler = metrikler
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w = self.width()
        h = self.height()

        # Gradient arka plan
        grad = QLinearGradient(0, 0, w, h)
        grad.setColorAt(0, PRIMARY_DARK)
        grad.setColorAt(1, PRIMARY)
        p.setBrush(QBrush(grad))
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(self.rect(), 12, 12)

        # Dekoratif daireler (seyahat hissi)
        p.setBrush(QColor(255, 255, 255, 8))
        p.drawEllipse(int(w * 0.7), -40, 200, 200)
        p.drawEllipse(int(w * 0.8), int(h * 0.3), 160, 160)

        sol_x = 36
        sol_w = int(w * 0.52)

        # Küçük etiket
        p.setPen(QColor(ACCENT.red(), ACCENT.green(), ACCENT.blue(), 220))
        font = QFont("Poppins", 10, QFont.Bold)
        if not font.exactMatch():
            font = QFont("Segoe UI", 10, QFont.Bold)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 1.5)
        p.setFont(font)
        p.drawText(sol_x, 44, "YOL DEFTERİ")

        # Başlık
        p.setPen(QColor(255, 255, 255))
        font = QFont("Poppins", 28, QFont.Bold)
        if not font.exactMatch():
            font = QFont("Segoe UI", 28, QFont.Bold)
        p.setFont(font)

        fm = QFontMetrics(font)
        kelimeler = self.baslik.split()
        satirlar, kalan = [], ""
        for k in kelimeler:
            test = kalan + (" " if kalan else "") + k
            if fm.horizontalAdvance(test) <= sol_w:
                kalan = test
            else:
                if kalan:
                    satirlar.append(kalan)
                kalan = k
        if kalan:
            satirlar.append(kalan)
        satirlar = satirlar[:2]

        y = 60
        for satir in satirlar:
            p.drawText(sol_x, y + 30, satir)
            y += 36

        # Altyazı
        p.setPen(QColor(255, 255, 255, 160))
        font = QFont("Poppins", 13)
        if not font.exactMatch():
            font = QFont("Segoe UI", 13)
        p.setFont(font)
        p.drawText(QRectF(sol_x, y + 12, sol_w, 22), Qt.AlignLeft, self.altyazi)

        # Sağ taraf metrikler 2x2
        m = self.metrikler[:4]
        if len(m) >= 4:
            sag_x = int(w * 0.56)
            sag_w = w - sag_x - 36
            cell_w = sag_w / 2
            cell_h = (h - 70) / 2
            grid_y = 40

            for i, (etiket, deger) in enumerate(m):
                row = i // 2
                col = i % 2
                cx = sag_x + col * cell_w
                cy = grid_y + row * cell_h

                # Etiket
                p.setPen(QColor(255, 255, 255, 120))
                font = QFont("Poppins", 9, QFont.Bold)
                if not font.exactMatch():
                    font = QFont("Segoe UI", 9, QFont.Bold)
                font.setLetterSpacing(QFont.AbsoluteSpacing, 1)
                p.setFont(font)
                p.drawText(int(cx), int(cy + 14), etiket.upper())

                # Değer
                p.setPen(QColor(255, 255, 255))
                font = QFont("Poppins", 32, QFont.Bold)
                if not font.exactMatch():
                    font = QFont("Segoe UI", 32, QFont.Bold)
                p.setFont(font)
                p.drawText(int(cx), int(cy + 52), str(deger))

                # Accent çizgi
                p.setPen(Qt.NoPen)
                p.setBrush(QColor(ACCENT.red(), ACCENT.green(), ACCENT.blue(), 180))
                p.drawRoundedRect(QRectF(cx, cy + 60, 20, 2), 1, 1)


# ============================================================
# AVATAR — Daire içinde baş harf
# ============================================================
class Avatar(QWidget):
    PALETLER = [
        QColor("#2d5a7b"), QColor("#d4845a"), QColor("#3a8a6a"),
        QColor("#c49a3c"), QColor("#8b6eb0"),
    ]

    def __init__(self, ad: str, boyut: int = 40, parent=None):
        super().__init__(parent)
        self.ad = ad.strip()
        self.bas_harf = self.ad[0].upper() if self.ad else "?"
        self.setFixedSize(boyut, boyut)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w = self.width()
        h = self.height()

        renk = self.PALETLER[hash(self.ad) % len(self.PALETLER)]

        p.setBrush(renk)
        p.setPen(Qt.NoPen)
        p.drawEllipse(1, 1, w - 2, h - 2)

        p.setPen(QColor(255, 255, 255))
        font = QFont("Poppins", int(w * 0.38), QFont.Bold)
        if not font.exactMatch():
            font = QFont("Segoe UI", int(w * 0.38), QFont.Bold)
        p.setFont(font)
        p.drawText(self.rect(), Qt.AlignCenter, self.bas_harf)


# ============================================================
# KART — Genel amaçlı kart
# ============================================================
class Kart(QFrame):
    def __init__(self, baslik: str = None, alt_baslik: str = None,
                 accent: bool = False, parent=None):
        super().__init__(parent)
        self.setObjectName("Kart")

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(24, 20, 24, 20)
        self.layout.setSpacing(12)

        if baslik:
            ust = QHBoxLayout()
            ust.setContentsMargins(0, 0, 0, 0)
            ust.setSpacing(0)

            if accent:
                marker = QFrame()
                marker.setFixedSize(3, 24)
                marker.setStyleSheet(
                    "background-color: #d4845a; border: none; border-radius: 1px;")
                ust.addWidget(marker, 0, Qt.AlignVCenter)
                ust.addSpacing(10)

            baslik_l = QVBoxLayout()
            baslik_l.setSpacing(2)
            baslik_l.setContentsMargins(0, 0, 0, 0)

            self.baslik_lbl = QLabel(baslik)
            self.baslik_lbl.setObjectName("KartBaslik")
            baslik_l.addWidget(self.baslik_lbl)

            if alt_baslik:
                self.alt_baslik_lbl = QLabel(alt_baslik)
                self.alt_baslik_lbl.setObjectName("KartAltBaslik")
                baslik_l.addWidget(self.alt_baslik_lbl)

            ust.addLayout(baslik_l)
            ust.addStretch()
            self.layout.addLayout(ust)

            ayrac = QFrame()
            ayrac.setFixedHeight(1)
            ayrac.setStyleSheet("background-color: #edeae4;")
            self.layout.addWidget(ayrac)


# ============================================================
# KATEGORİ BAR
# ============================================================
class KategoriBarYatay(QWidget):
    def __init__(self, dagilim: dict, parent=None):
        super().__init__(parent)
        self.dagilim = dagilim
        n = len(dagilim) if dagilim else 1
        self.setMinimumHeight(n * 44 + 10)

    def paintEvent(self, e):
        if not self.dagilim:
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w = self.width()

        sirali = sorted(self.dagilim.items(), key=lambda x: -x[1])
        max_v = max(v for _, v in sirali) if sirali else 1

        kat_w = 140
        sag_w = 50
        bar_x = kat_w + 12
        bar_w = w - bar_x - sag_w - 12

        satir_y = 6
        for i, (kategori, sayi) in enumerate(sirali):
            # Kategori adı
            p.setPen(TEXT)
            font = QFont("Poppins", 12, QFont.DemiBold)
            if not font.exactMatch():
                font = QFont("Segoe UI", 12, QFont.DemiBold)
            p.setFont(font)
            p.drawText(QRectF(0, satir_y, kat_w, 32),
                       Qt.AlignLeft | Qt.AlignVCenter, kategori)

            # Bar arka plan
            p.setPen(Qt.NoPen)
            p.setBrush(BORDER_LIGHT)
            p.drawRoundedRect(QRectF(bar_x, satir_y + 11, bar_w, 10), 5, 5)

            # Bar dolu
            dolu_w = max((sayi / max_v) * bar_w, 8)
            renk = ACCENT if i == 0 else PRIMARY
            p.setBrush(renk)
            p.drawRoundedRect(QRectF(bar_x, satir_y + 11, dolu_w, 10), 5, 5)

            # Sayı
            p.setPen(TEXT)
            font = QFont("Poppins", 14, QFont.Bold)
            if not font.exactMatch():
                font = QFont("Segoe UI", 14, QFont.Bold)
            p.setFont(font)
            p.drawText(QRectF(bar_x + bar_w + 8, satir_y, sag_w, 32),
                       Qt.AlignRight | Qt.AlignVCenter, str(sayi))

            satir_y += 44


# ============================================================
# ROZET
# ============================================================
class Rozet(QLabel):
    STILLER = {
        "basari": (
            "background-color: #e6f3ed; color: #3a8a6a; "
            "border: none;"
        ),
        "uyari": (
            "background-color: #faf3e0; color: #c49a3c; "
            "border: none;"
        ),
        "tehlike": (
            "background-color: #fceaea; color: #c45454; "
            "border: none;"
        ),
        "notr": (
            "background-color: #f2efe9; color: #8c8c88; "
            "border: none;"
        ),
        "primary": (
            "background-color: #e8f0f6; color: #2d5a7b; "
            "border: none;"
        ),
    }

    def __init__(self, metin: str, tip: str = "basari", parent=None):
        super().__init__(metin, parent)
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumHeight(26)
        self.setMinimumWidth(80)

        renk_stil = self.STILLER.get(tip, self.STILLER["notr"])
        self.setStyleSheet(
            f"QLabel {{ {renk_stil} "
            f"border-radius: 4px; "
            f"padding: 4px 12px; "
            f"font-family: 'Poppins', sans-serif; "
            f"font-size: 10px; font-weight: 700; }}"
        )


# ============================================================
# DURUM ROZETİ
# ============================================================
class DurumRozeti(Rozet):
    @classmethod
    def from_seyahat(cls, seyahat, parent=None):
        if seyahat.gecmis_mi():
            return cls("GEÇMİŞ", "notr", parent)
        if seyahat.aktif_mi():
            return cls("AKTİF", "basari", parent)
        kalan = seyahat.kalan_gun()
        if kalan is not None:
            return cls(f"{kalan} GÜN KALDI", "uyari", parent)
        return cls("YAKLAŞIYOR", "primary", parent)


# ============================================================
# GÜNLÜK PLAN KARTI
# ============================================================
class GunlukPlanKart(QFrame):
    def __init__(self, plan, parent=None):
        super().__init__(parent)
        self.setStyleSheet(
            "QFrame { background-color: #ffffff; "
            "border: 1px solid #e8e5df; "
            "border-left: 3px solid #2d5a7b; "
            "border-radius: 8px; }"
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 14, 20, 14)
        layout.setSpacing(8)

        # Gün başlığı
        gun_row = QHBoxLayout()
        gun_lbl = QLabel(f"Gün {plan.gun}")
        gun_lbl.setStyleSheet(
            "color: #2d5a7b; font-family: 'Poppins', sans-serif; "
            "font-size: 14px; font-weight: 700; "
            "background: transparent; border: none;"
        )
        gun_row.addWidget(gun_lbl)

        if plan.tarih:
            tarih_lbl = QLabel(tarih_format(plan.tarih))
            tarih_lbl.setStyleSheet(
                "color: #8c8c88; font-family: 'Poppins', sans-serif; "
                "font-size: 11px; "
                "background: transparent; border: none;"
            )
            gun_row.addStretch()
            gun_row.addWidget(tarih_lbl)

        layout.addLayout(gun_row)

        ayrac = QFrame()
        ayrac.setFixedHeight(1)
        ayrac.setStyleSheet("background-color: #edeae4;")
        layout.addWidget(ayrac)

        # Rota
        if plan.rota:
            rota_baslik = QLabel("Rota")
            rota_baslik.setStyleSheet(
                "color: #d4845a; font-family: 'Poppins', sans-serif; "
                "font-size: 10px; font-weight: 700; "
                "background: transparent; border: none;"
            )
            layout.addWidget(rota_baslik)

            for i, yer in enumerate(plan.rota, 1):
                rota_item = QLabel(f"  {i}.  {yer}")
                rota_item.setStyleSheet(
                    "color: #2c2c2c; font-family: 'Poppins', sans-serif; "
                    "font-size: 12px; "
                    "background: transparent; border: none;"
                )
                layout.addWidget(rota_item)

        # Aktiviteler
        if plan.aktiviteler:
            if plan.rota:
                layout.addSpacing(4)
            akt_baslik = QLabel("Aktiviteler")
            akt_baslik.setStyleSheet(
                "color: #d4845a; font-family: 'Poppins', sans-serif; "
                "font-size: 10px; font-weight: 700; "
                "background: transparent; border: none;"
            )
            layout.addWidget(akt_baslik)

            for akt in plan.aktiviteler:
                akt_item = QLabel(f"  •  {akt}")
                akt_item.setStyleSheet(
                    "color: #555550; font-family: 'Poppins', sans-serif; "
                    "font-size: 12px; "
                    "background: transparent; border: none;"
                )
                layout.addWidget(akt_item)

        if not plan.rota and not plan.aktiviteler:
            bos = QLabel("Henüz plan eklenmemiş")
            bos.setStyleSheet(
                "color: #b0aea8; font-family: 'Poppins', sans-serif; "
                "font-size: 12px; font-style: italic; "
                "background: transparent; border: none;"
            )
            layout.addWidget(bos)


# ============================================================
# Yardımcı
# ============================================================
class Ayirici(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Ayirici")
        self.setFixedHeight(1)


class AyiriciInce(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("AyiriciInce")
        self.setFixedHeight(1)
