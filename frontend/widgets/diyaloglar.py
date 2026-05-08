"""
Diyaloglar — Seyahat ekleme/düzenleme, plan düzenleme (Atlas tema).
"""
from datetime import datetime

from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QDateEdit,
    QComboBox,
    QTextEdit,
    QPushButton,
    QFrame,
    QDoubleSpinBox,
    QMessageBox,
    QWidget,
)
from PyQt5.QtCore import Qt, QDate

from backend import Seyahat, Konaklama, Plan


class SeyahatDiyalog(QDialog):
    def __init__(self, seyahat: Seyahat = None, parent=None):
        super().__init__(parent)
        self.seyahat = seyahat
        self.setWindowTitle("Seyahat Düzenle" if seyahat else "Yeni Seyahat")
        self.setFixedSize(520, 640)
        self.setModal(True)
        self._arayuz_olustur()

    def _arayuz_olustur(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(0)

        baslik = QLabel("Seyahat Düzenle" if self.seyahat else "Yeni Seyahat")
        baslik.setStyleSheet(
            "color: #2c2c2c; font-family: 'Poppins', sans-serif; "
            "font-size: 24px; font-weight: 700; "
            "background: transparent; border: none;"
        )
        layout.addWidget(baslik)
        layout.addSpacing(16)

        # Gidiş yeri
        layout.addWidget(self._etiket("Gidiş Yeri"))
        layout.addSpacing(4)
        self.gidis_yeri_input = QLineEdit()
        self.gidis_yeri_input.setPlaceholderText("Şehir veya ülke adı")
        self.gidis_yeri_input.setFixedHeight(40)
        if self.seyahat:
            self.gidis_yeri_input.setText(self.seyahat.gidis_yeri)
        layout.addWidget(self.gidis_yeri_input)
        layout.addSpacing(14)

        # Tarihler
        tarih_row = QHBoxLayout()
        tarih_row.setSpacing(14)

        sol = QVBoxLayout()
        sol.addWidget(self._etiket("Gidiş Tarihi"))
        sol.addSpacing(4)
        self.tarih_input = QDateEdit()
        self.tarih_input.setCalendarPopup(True)
        self.tarih_input.setDisplayFormat("dd.MM.yyyy")
        self.tarih_input.setFixedHeight(40)
        if self.seyahat:
            self.tarih_input.setDate(QDate(
                self.seyahat.tarih.year, self.seyahat.tarih.month, self.seyahat.tarih.day))
        else:
            self.tarih_input.setDate(QDate.currentDate())
        sol.addWidget(self.tarih_input)

        sag = QVBoxLayout()
        sag.addWidget(self._etiket("Dönüş Tarihi"))
        sag.addSpacing(4)
        self.donus_input = QDateEdit()
        self.donus_input.setCalendarPopup(True)
        self.donus_input.setDisplayFormat("dd.MM.yyyy")
        self.donus_input.setFixedHeight(40)
        if self.seyahat:
            self.donus_input.setDate(QDate(
                self.seyahat.donus_tarihi.year, self.seyahat.donus_tarihi.month,
                self.seyahat.donus_tarihi.day))
        else:
            self.donus_input.setDate(QDate.currentDate().addDays(3))
        sag.addWidget(self.donus_input)

        tarih_row.addLayout(sol)
        tarih_row.addLayout(sag)
        layout.addLayout(tarih_row)
        layout.addSpacing(14)

        # Konaklama
        layout.addWidget(self._etiket("Konaklama (opsiyonel)"))
        layout.addSpacing(4)

        self.otel_input = QLineEdit()
        self.otel_input.setPlaceholderText("Otel adı (boş bırakılabilir)")
        self.otel_input.setFixedHeight(40)
        layout.addWidget(self.otel_input)
        layout.addSpacing(10)

        kon_row = QHBoxLayout()
        kon_row.setSpacing(14)

        fiyat_col = QVBoxLayout()
        fiyat_col.addWidget(self._etiket("Gecelik Fiyat"))
        fiyat_col.addSpacing(4)
        self.fiyat_input = QDoubleSpinBox()
        self.fiyat_input.setRange(0, 999999)
        self.fiyat_input.setDecimals(0)
        self.fiyat_input.setSuffix(" TL")
        self.fiyat_input.setFixedHeight(40)
        fiyat_col.addWidget(self.fiyat_input)

        oda_col = QVBoxLayout()
        oda_col.addWidget(self._etiket("Oda Tipi"))
        oda_col.addSpacing(4)
        self.oda_combo = QComboBox()
        self.oda_combo.addItems(["Standart", "Tek Kişilik", "Çift Kişilik", "Suite"])
        self.oda_combo.setFixedHeight(40)
        oda_col.addWidget(self.oda_combo)

        kon_row.addLayout(fiyat_col)
        kon_row.addLayout(oda_col)
        layout.addLayout(kon_row)
        layout.addSpacing(10)

        self.adres_input = QLineEdit()
        self.adres_input.setPlaceholderText("Adres (opsiyonel)")
        self.adres_input.setFixedHeight(40)
        layout.addWidget(self.adres_input)
        layout.addSpacing(14)

        # Notlar
        layout.addWidget(self._etiket("Notlar"))
        layout.addSpacing(4)
        self.notlar_input = QTextEdit()
        self.notlar_input.setPlaceholderText("Notlarınız...")
        self.notlar_input.setFixedHeight(60)
        if self.seyahat:
            self.notlar_input.setPlainText(self.seyahat.notlar)
        layout.addWidget(self.notlar_input)

        # Mevcut konaklama
        if self.seyahat and self.seyahat.konaklama:
            k = self.seyahat.konaklama
            self.otel_input.setText(k.otel_adi)
            self.fiyat_input.setValue(k.fiyat)
            self.adres_input.setText(k.adres)
            idx = self.oda_combo.findText(k.oda_tipi)
            if idx >= 0:
                self.oda_combo.setCurrentIndex(idx)

        layout.addStretch()

        # Butonlar
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        iptal_btn = QPushButton("İptal")
        iptal_btn.setFixedHeight(42)
        iptal_btn.setCursor(Qt.PointingHandCursor)
        iptal_btn.setStyleSheet(
            "QPushButton { background-color: #ffffff; color: #2d5a7b; "
            "border: 1px solid #2d5a7b; border-radius: 6px; "
            "font-family: 'Poppins'; font-size: 13px; font-weight: 600; "
            "padding: 0 24px; } "
            "QPushButton:hover { background-color: #e8f0f6; }"
        )
        iptal_btn.clicked.connect(self.reject)

        kaydet_btn = QPushButton("Kaydet")
        kaydet_btn.setFixedHeight(42)
        kaydet_btn.setCursor(Qt.PointingHandCursor)
        kaydet_btn.setStyleSheet(
            "QPushButton { background-color: #2d5a7b; color: #ffffff; "
            "border: none; border-radius: 6px; "
            "font-family: 'Poppins'; font-size: 13px; font-weight: 600; "
            "padding: 0 24px; } "
            "QPushButton:hover { background-color: #3a6d91; }"
        )
        kaydet_btn.clicked.connect(self._kaydet)

        btn_row.addWidget(iptal_btn)
        btn_row.addWidget(kaydet_btn)
        layout.addLayout(btn_row)

    def _etiket(self, metin: str) -> QLabel:
        lbl = QLabel(metin)
        lbl.setStyleSheet(
            "color: #555550; font-family: 'Poppins', sans-serif; "
            "font-size: 11px; font-weight: 600; "
            "background: transparent; border: none;"
        )
        return lbl

    def _kaydet(self):
        gidis_yeri = self.gidis_yeri_input.text().strip()
        if not gidis_yeri:
            QMessageBox.warning(self, "Uyarı", "Gidiş yeri boş olamaz.")
            return

        qd_tarih = self.tarih_input.date()
        qd_donus = self.donus_input.date()
        tarih = datetime(qd_tarih.year(), qd_tarih.month(), qd_tarih.day())
        donus = datetime(qd_donus.year(), qd_donus.month(), qd_donus.day())

        if donus < tarih:
            QMessageBox.warning(self, "Uyarı", "Dönüş tarihi gidiş tarihinden önce olamaz.")
            return

        otel = self.otel_input.text().strip()
        konaklama = None
        if otel:
            konaklama = Konaklama(
                otel_adi=otel,
                fiyat=self.fiyat_input.value(),
                adres=self.adres_input.text().strip(),
                oda_tipi=self.oda_combo.currentText(),
            )

        self.sonuc = {
            "gidis_yeri": gidis_yeri,
            "tarih": tarih,
            "donus_tarihi": donus,
            "konaklama": konaklama,
            "notlar": self.notlar_input.toPlainText().strip(),
        }
        self.accept()


class PlanDuzenleDiyalog(QDialog):
    def __init__(self, plan: Plan, parent=None):
        super().__init__(parent)
        self.plan = plan
        self.setWindowTitle(f"Gün {plan.gun} — Plan Düzenle")
        self.setFixedSize(480, 520)
        self.setModal(True)
        self._arayuz_olustur()

    def _arayuz_olustur(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(0)

        baslik = QLabel(f"Gün {self.plan.gun}")
        baslik.setStyleSheet(
            "color: #2c2c2c; font-family: 'Poppins', sans-serif; "
            "font-size: 24px; font-weight: 700; "
            "background: transparent; border: none;"
        )
        layout.addWidget(baslik)

        if self.plan.tarih:
            from frontend.widgets.bilesenler import tarih_format
            tarih_lbl = QLabel(tarih_format(self.plan.tarih))
            tarih_lbl.setStyleSheet(
                "color: #8c8c88; font-family: 'Poppins', sans-serif; "
                "font-size: 12px; background: transparent; border: none;"
            )
            layout.addWidget(tarih_lbl)

        layout.addSpacing(16)

        # Rota
        layout.addWidget(self._etiket("Rota (her satıra bir yer)"))
        layout.addSpacing(4)
        self.rota_input = QTextEdit()
        self.rota_input.setPlaceholderText("Sultanahmet\nAyasofya\nTopkapı Sarayı")
        self.rota_input.setFixedHeight(120)
        self.rota_input.setPlainText("\n".join(self.plan.rota))
        layout.addWidget(self.rota_input)
        layout.addSpacing(14)

        # Aktiviteler
        layout.addWidget(self._etiket("Aktiviteler (her satıra bir aktivite)"))
        layout.addSpacing(4)
        self.aktivite_input = QTextEdit()
        self.aktivite_input.setPlaceholderText("Sabah kahvaltısı\nMüze gezisi\nAkşam yemeği")
        self.aktivite_input.setFixedHeight(120)
        self.aktivite_input.setPlainText("\n".join(self.plan.aktiviteler))
        layout.addWidget(self.aktivite_input)

        layout.addStretch()

        # Butonlar
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        iptal_btn = QPushButton("İptal")
        iptal_btn.setFixedHeight(42)
        iptal_btn.setCursor(Qt.PointingHandCursor)
        iptal_btn.setStyleSheet(
            "QPushButton { background-color: #ffffff; color: #2d5a7b; "
            "border: 1px solid #2d5a7b; border-radius: 6px; "
            "font-family: 'Poppins'; font-size: 13px; font-weight: 600; "
            "padding: 0 24px; } "
            "QPushButton:hover { background-color: #e8f0f6; }"
        )
        iptal_btn.clicked.connect(self.reject)

        kaydet_btn = QPushButton("Kaydet")
        kaydet_btn.setFixedHeight(42)
        kaydet_btn.setCursor(Qt.PointingHandCursor)
        kaydet_btn.setStyleSheet(
            "QPushButton { background-color: #2d5a7b; color: #ffffff; "
            "border: none; border-radius: 6px; "
            "font-family: 'Poppins'; font-size: 13px; font-weight: 600; "
            "padding: 0 24px; } "
            "QPushButton:hover { background-color: #3a6d91; }"
        )
        kaydet_btn.clicked.connect(self._kaydet)

        btn_row.addWidget(iptal_btn)
        btn_row.addWidget(kaydet_btn)
        layout.addLayout(btn_row)

    def _etiket(self, metin: str) -> QLabel:
        lbl = QLabel(metin)
        lbl.setStyleSheet(
            "color: #555550; font-family: 'Poppins', sans-serif; "
            "font-size: 11px; font-weight: 600; "
            "background: transparent; border: none;"
        )
        return lbl

    def _kaydet(self):
        rota_text = self.rota_input.toPlainText().strip()
        akt_text = self.aktivite_input.toPlainText().strip()

        self.sonuc_rota = [r.strip() for r in rota_text.split("\n") if r.strip()]
        self.sonuc_aktiviteler = [a.strip() for a in akt_text.split("\n") if a.strip()]
        self.accept()
