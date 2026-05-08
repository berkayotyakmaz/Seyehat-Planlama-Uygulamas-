"""
Login Penceresi — Atlas tema, modern seyahat tasarımı.
"""
from PyQt5.QtWidgets import (
    QDialog,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFrame,
    QCheckBox,
    QSizePolicy,
)
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import (
    QPainter,
    QColor,
    QPen,
    QFont,
    QLinearGradient,
    QBrush,
)

from backend import AuthYoneticisi

PRIMARY = QColor("#2d5a7b")
PRIMARY_DARK = QColor("#1e3f58")
ACCENT = QColor("#d4845a")
TEXT = QColor("#2c2c2c")
TEXT_MUTED = QColor("#8c8c88")
BG = QColor("#faf8f5")
SURFACE = QColor("#ffffff")
BORDER = QColor("#d9d6d0")


class _SolPanel(QWidget):
    """Login sol panel — gradient arka plan + marka."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(520)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w = self.width()
        h = self.height()

        # Gradient arka plan
        grad = QLinearGradient(0, 0, w, h)
        grad.setColorAt(0, PRIMARY_DARK)
        grad.setColorAt(0.6, PRIMARY)
        grad.setColorAt(1, QColor("#3a7ca5"))
        p.fillRect(self.rect(), QBrush(grad))

        # Dekoratif daireler
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(255, 255, 255, 6))
        p.drawEllipse(int(w * 0.5), -60, 300, 300)
        p.drawEllipse(-80, int(h * 0.6), 250, 250)
        p.drawEllipse(int(w * 0.3), int(h * 0.7), 200, 200)

        margin = 52

        # Accent çizgi
        p.setBrush(ACCENT)
        p.drawRoundedRect(QRectF(margin, 72, 32, 3), 1.5, 1.5)

        # Küçük etiket
        p.setPen(QColor(255, 255, 255, 140))
        font = QFont("Poppins", 10, QFont.Bold)
        if not font.exactMatch():
            font = QFont("Segoe UI", 10, QFont.Bold)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 1.5)
        p.setFont(font)
        p.drawText(QRectF(margin, 84, w - margin * 2, 20),
                   Qt.AlignLeft, "SEYAHAT PLANLAMA")

        # Büyük başlık
        p.setPen(QColor(255, 255, 255))
        font = QFont("Poppins", 44, QFont.Bold)
        if not font.exactMatch():
            font = QFont("Segoe UI", 44, QFont.Bold)
        p.setFont(font)
        p.drawText(QRectF(margin, 114, w - margin * 2, 60),
                   Qt.AlignLeft | Qt.AlignVCenter, "Yol Defteri")

        # Slogan
        p.setPen(QColor(255, 255, 255, 180))
        font = QFont("Poppins", 16)
        if not font.exactMatch():
            font = QFont("Segoe UI", 16)
        p.setFont(font)
        p.drawText(QRectF(margin, 210, w - margin * 2, 28),
                   Qt.AlignLeft, "Yolculuğunu planla,")
        p.drawText(QRectF(margin, 238, w - margin * 2, 28),
                   Qt.AlignLeft, "anılarını biriktir.")

        # Özellikler
        ozellikler = [
            "Seyahat planı oluşturma",
            "Konaklama bilgisi yönetimi",
            "Günlük rota ve aktivite planlama",
            "Detaylı raporlar ve analiz",
        ]

        ozellik_y = 310
        for i, oz in enumerate(ozellikler):
            y = ozellik_y + i * 38

            # Daire bullet
            p.setBrush(ACCENT)
            p.setPen(Qt.NoPen)
            p.drawEllipse(int(margin), int(y - 5), 6, 6)

            p.setPen(QColor(255, 255, 255, 210))
            font = QFont("Poppins", 12)
            if not font.exactMatch():
                font = QFont("Segoe UI", 12)
            p.setFont(font)
            p.drawText(margin + 18, y, oz)

        # Footer
        p.setPen(QColor(255, 255, 255, 80))
        font = QFont("Poppins", 9)
        if not font.exactMatch():
            font = QFont("Segoe UI", 9)
        p.setFont(font)
        p.drawText(QRectF(margin, h - 40, w - margin * 2, 16),
                   Qt.AlignLeft, "© 2026 Yol Defteri")
        p.drawText(QRectF(margin, h - 40, w - margin * 2, 16),
                   Qt.AlignRight, "v1.0")


class LoginPenceresi(QDialog):
    def __init__(self, auth: AuthYoneticisi, parent=None):
        super().__init__(parent)
        self.auth = auth
        self.dogrulanan_kullanici = None

        self.setWindowTitle("Yol Defteri — Giriş")
        self.setFixedSize(1080, 680)
        self.setModal(True)
        self._arayuz_olustur()

    def _arayuz_olustur(self):
        ana = QHBoxLayout(self)
        ana.setContentsMargins(0, 0, 0, 0)
        ana.setSpacing(0)

        ana.addWidget(_SolPanel())

        # Sağ form
        sag = QFrame()
        sag.setStyleSheet("background-color: #faf8f5;")
        sag_layout = QVBoxLayout(sag)
        sag_layout.setContentsMargins(52, 64, 52, 48)
        sag_layout.setSpacing(0)

        # Kategori
        kat = QLabel("GİRİŞ")
        kat.setStyleSheet(
            "color: #d4845a; font-family: 'Poppins', sans-serif; "
            "font-size: 10px; font-weight: 700; "
            "background: transparent; border: none;"
        )
        sag_layout.addWidget(kat)
        sag_layout.addSpacing(12)

        baslik = QLabel("Hoş Geldin")
        baslik.setStyleSheet(
            "color: #2c2c2c; font-family: 'Poppins', sans-serif; "
            "font-size: 36px; font-weight: 700; "
            "background: transparent; border: none;"
        )
        sag_layout.addWidget(baslik)

        alt = QLabel("Devam etmek için hesabına giriş yap.")
        alt.setStyleSheet(
            "color: #8c8c88; font-family: 'Poppins', sans-serif; "
            "font-size: 13px; "
            "background: transparent; border: none;"
        )
        sag_layout.addWidget(alt)
        sag_layout.addSpacing(28)

        # Form
        sag_layout.addWidget(self._etiket("KULLANICI ADI"))
        sag_layout.addSpacing(6)

        self.kul_input = QLineEdit()
        self.kul_input.setPlaceholderText("kullanıcı adınızı girin")
        self.kul_input.setFixedHeight(44)
        self.kul_input.setStyleSheet(self._input_stil())
        self.kul_input.returnPressed.connect(lambda: self.sifre_input.setFocus())
        sag_layout.addWidget(self.kul_input)
        sag_layout.addSpacing(18)

        sag_layout.addWidget(self._etiket("ŞİFRE"))
        sag_layout.addSpacing(6)

        self.sifre_input = QLineEdit()
        self.sifre_input.setPlaceholderText("••••••••")
        self.sifre_input.setEchoMode(QLineEdit.Password)
        self.sifre_input.setFixedHeight(44)
        self.sifre_input.setStyleSheet(self._input_stil())
        self.sifre_input.returnPressed.connect(self._giris_yap)
        sag_layout.addWidget(self.sifre_input)
        sag_layout.addSpacing(10)

        self.goster_chk = QCheckBox("Şifreyi göster")
        self.goster_chk.setStyleSheet(
            "QCheckBox { color: #8c8c88; font-family: 'Poppins', sans-serif; "
            "font-size: 11px; font-weight: 500; "
            "background: transparent; border: none; spacing: 8px; }"
            "QCheckBox::indicator { width: 16px; height: 16px; "
            "border: 1px solid #d9d6d0; border-radius: 4px; "
            "background-color: #ffffff; }"
            "QCheckBox::indicator:checked { background-color: #2d5a7b; "
            "border: 1px solid #2d5a7b; }"
        )
        self.goster_chk.toggled.connect(self._sifre_goster)
        sag_layout.addWidget(self.goster_chk)
        sag_layout.addSpacing(20)

        # Hata kutusu
        self.hata_lbl = QLabel("")
        self.hata_lbl.setStyleSheet(
            "background-color: #fceaea; color: #c45454; "
            "border: 1px solid #c45454; border-radius: 6px; "
            "padding: 12px 16px; "
            "font-family: 'Poppins', sans-serif; font-size: 12px; font-weight: 500;"
        )
        self.hata_lbl.setVisible(False)
        sag_layout.addWidget(self.hata_lbl)

        # Giriş butonu
        self.giris_btn = QPushButton("Oturum Aç")
        self.giris_btn.setFixedHeight(48)
        self.giris_btn.setCursor(Qt.PointingHandCursor)
        self.giris_btn.setStyleSheet(
            "QPushButton { background-color: #2d5a7b; color: #ffffff; "
            "border: none; border-radius: 8px; "
            "font-family: 'Poppins', sans-serif; font-size: 14px; "
            "font-weight: 600; } "
            "QPushButton:hover { background-color: #3a6d91; }"
        )
        self.giris_btn.clicked.connect(self._giris_yap)
        sag_layout.addWidget(self.giris_btn)

        sag_layout.addSpacing(20)

        # İpucu
        ipucu = QLabel(
            "<span style=\"color:#8c8c88; font-family:'Poppins',sans-serif; "
            "font-size:10px; font-weight:600;\">VARSAYILAN ERİŞİM</span><br><br>"
            "<span style=\"color:#2c2c2c; font-family:'Poppins',sans-serif; "
            "font-size:13px; font-weight:500;\">"
            "admin <span style='color:#d4845a;'>·</span> admin123</span>"
        )
        ipucu.setStyleSheet(
            "background-color: #e8f0f6; "
            "border: none; border-radius: 8px; "
            "padding: 14px 18px;"
        )
        sag_layout.addWidget(ipucu)

        sag_layout.addStretch()

        footer = QLabel("© 2026 Yol Defteri")
        footer.setStyleSheet(
            "color: #b0aea8; font-family: 'Poppins', sans-serif; "
            "font-size: 10px; background: transparent; border: none;"
        )
        footer.setAlignment(Qt.AlignCenter)
        sag_layout.addWidget(footer)

        ana.addWidget(sag, 1)

    def _etiket(self, metin: str) -> QLabel:
        lbl = QLabel(metin)
        lbl.setStyleSheet(
            "color: #555550; font-family: 'Poppins', sans-serif; "
            "font-size: 11px; font-weight: 600; "
            "background: transparent; border: none;"
        )
        return lbl

    def _input_stil(self) -> str:
        return (
            "QLineEdit { background-color: #ffffff; "
            "border: 1px solid #d9d6d0; border-radius: 8px; "
            "padding: 0 14px; "
            "color: #2c2c2c; font-family: 'Poppins', sans-serif; font-size: 14px; "
            "selection-background-color: #2d5a7b; selection-color: #ffffff; } "
            "QLineEdit:focus { border: 2px solid #2d5a7b; "
            "background-color: #ffffff; } "
            "QLineEdit:hover { border: 1px solid #2d5a7b; }"
        )

    def _sifre_goster(self, checked: bool):
        self.sifre_input.setEchoMode(
            QLineEdit.Normal if checked else QLineEdit.Password
        )

    def _hata_goster(self, mesaj: str):
        self.hata_lbl.setText(mesaj)
        self.hata_lbl.setVisible(True)

    def _giris_yap(self):
        kul = self.kul_input.text().strip()
        sifre = self.sifre_input.text()

        if not kul:
            self._hata_goster("Kullanıcı adı boş olamaz.")
            self.kul_input.setFocus()
            return
        if not sifre:
            self._hata_goster("Şifre boş olamaz.")
            self.sifre_input.setFocus()
            return

        kullanici = self.auth.dogrula(kul, sifre)
        if kullanici is None:
            self._hata_goster("Kullanıcı adı veya şifre hatalı.")
            self.sifre_input.clear()
            self.sifre_input.setFocus()
            return

        self.dogrulanan_kullanici = kullanici
        self.accept()
