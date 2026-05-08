"""
Seyahatler sayfası — Kart grid + filtre + CRUD.
"""
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QFrame,
    QPushButton,
    QLineEdit,
    QComboBox,
    QMessageBox,
    QSizePolicy,
)
from PyQt5.QtCore import Qt, pyqtSignal

from backend import VeriYoneticisi
from frontend.widgets.bilesenler import (
    SayfaHeader,
    DurumRozeti,
    tarih_aralik_format,
)
from frontend.widgets.diyaloglar import SeyahatDiyalog


class SeyahatlerSayfasi(QWidget):
    seyahat_secildi = pyqtSignal(int)
    veri_degisti = pyqtSignal()

    def __init__(self, vy: VeriYoneticisi, parent=None):
        super().__init__(parent)
        self.vy = vy
        self._filtre = "tumu"
        self._arama = ""
        self._arayuz_olustur()
        self.yenile()

    def _arayuz_olustur(self):
        dis = QVBoxLayout(self)
        dis.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        icerik = QWidget()
        self.layout = QVBoxLayout(icerik)
        self.layout.setContentsMargins(40, 32, 40, 32)
        self.layout.setSpacing(0)

        header = SayfaHeader(
            kategori="SEYAHATLER",
            baslik="Seyahatlerim",
            altyazi="Tüm seyahat planlarınız bir arada.",
        )
        self.layout.addWidget(header)
        self.layout.addSpacing(20)

        # Toolbar
        toolbar = QHBoxLayout()
        toolbar.setSpacing(10)

        self.arama_input = QLineEdit()
        self.arama_input.setPlaceholderText("Seyahat ara...")
        self.arama_input.setFixedHeight(38)
        self.arama_input.setMaximumWidth(280)
        self.arama_input.textChanged.connect(self._arama_degisti)
        toolbar.addWidget(self.arama_input)

        self.filtre_combo = QComboBox()
        self.filtre_combo.addItems(["Tümü", "Aktif", "Yaklaşan", "Geçmiş"])
        self.filtre_combo.setFixedHeight(38)
        self.filtre_combo.setFixedWidth(130)
        self.filtre_combo.currentIndexChanged.connect(self._filtre_degisti)
        toolbar.addWidget(self.filtre_combo)

        toolbar.addStretch()

        yeni_btn = QPushButton("  Yeni Seyahat  ")
        yeni_btn.setObjectName("PrimaryButon")
        yeni_btn.setFixedHeight(38)
        yeni_btn.setCursor(Qt.PointingHandCursor)
        yeni_btn.setStyleSheet(
            "QPushButton { background-color: #2d5a7b; color: #ffffff; "
            "border: none; border-radius: 6px; "
            "font-family: 'Poppins', sans-serif; font-size: 13px; "
            "font-weight: 600; padding: 0 22px; } "
            "QPushButton:hover { background-color: #3a6d91; }"
        )
        yeni_btn.clicked.connect(self._yeni_seyahat)
        toolbar.addWidget(yeni_btn)

        self.layout.addLayout(toolbar)
        self.layout.addSpacing(16)

        self.grid_container = QVBoxLayout()
        self.grid_container.setSpacing(14)
        self.layout.addLayout(self.grid_container)

        self.layout.addStretch()

        scroll.setWidget(icerik)
        dis.addWidget(scroll)

    def _arama_degisti(self, text):
        self._arama = text.strip().lower()
        self._kartlari_guncelle()

    def _filtre_degisti(self, idx):
        filtreler = ["tumu", "aktif", "yaklasan", "gecmis"]
        self._filtre = filtreler[idx]
        self._kartlari_guncelle()

    def yenile(self):
        self._kartlari_guncelle()

    def _kartlari_guncelle(self):
        while self.grid_container.count():
            item = self.grid_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                while item.layout().count():
                    sub = item.layout().takeAt(0)
                    if sub.widget():
                        sub.widget().deleteLater()

        tum = self.vy.tum_seyahatler()
        if self._filtre == "aktif":
            tum = [s for s in tum if s.aktif_mi()]
        elif self._filtre == "yaklasan":
            tum = [s for s in tum if s.gelecek_mi()]
        elif self._filtre == "gecmis":
            tum = [s for s in tum if s.gecmis_mi()]

        if self._arama:
            tum = [s for s in tum if self._arama in s.gidis_yeri.lower()]

        if not tum:
            bos = QLabel("Seyahat bulunamadı.")
            bos.setStyleSheet(
                "color: #b0aea8; font-family: 'Poppins', sans-serif; "
                "font-size: 14px; font-style: italic; "
                "background: transparent; border: none; padding: 40px 0;"
            )
            bos.setAlignment(Qt.AlignCenter)
            self.grid_container.addWidget(bos)
            return

        row_layout = None
        for i, s in enumerate(tum):
            if i % 2 == 0:
                row_layout = QHBoxLayout()
                row_layout.setSpacing(14)
                self.grid_container.addLayout(row_layout)
            kart = self._kart_olustur(s)
            row_layout.addWidget(kart)

        if len(tum) % 2 == 1:
            row_layout.addStretch()

    def _kart_olustur(self, seyahat) -> QFrame:
        kart = QFrame()
        kart.setStyleSheet(
            "QFrame { background-color: #ffffff; "
            "border: 1px solid #e8e5df; "
            "border-radius: 10px; }"
        )
        kart.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        kart.setCursor(Qt.PointingHandCursor)

        layout = QVBoxLayout(kart)
        layout.setContentsMargins(22, 18, 22, 18)
        layout.setSpacing(8)

        # Yer + rozet
        ust = QHBoxLayout()
        yer = QLabel(seyahat.gidis_yeri)
        yer.setStyleSheet(
            "color: #2c2c2c; font-family: 'Poppins', sans-serif; "
            "font-size: 20px; font-weight: 700; "
            "background: transparent; border: none;"
        )
        ust.addWidget(yer)
        ust.addStretch()
        rozet = DurumRozeti.from_seyahat(seyahat)
        ust.addWidget(rozet)
        layout.addLayout(ust)

        # Tarih
        tarih = QLabel(tarih_aralik_format(seyahat.tarih, seyahat.donus_tarihi))
        tarih.setStyleSheet(
            "color: #8c8c88; font-family: 'Poppins', sans-serif; "
            "font-size: 12px; background: transparent; border: none;"
        )
        layout.addWidget(tarih)

        # Ayraç
        ayrac = QFrame()
        ayrac.setFixedHeight(1)
        ayrac.setStyleSheet("background-color: #edeae4;")
        layout.addWidget(ayrac)

        # Meta
        meta_row = QHBoxLayout()
        meta_row.setSpacing(16)

        gun_lbl = QLabel(f"{seyahat.gun_sayisi()} gün")
        gun_lbl.setStyleSheet(
            "color: #2d5a7b; font-family: 'Poppins', sans-serif; "
            "font-size: 12px; font-weight: 700; "
            "background: transparent; border: none;"
        )
        meta_row.addWidget(gun_lbl)

        if seyahat.konaklama:
            otel_lbl = QLabel(seyahat.konaklama.otel_adi)
            otel_lbl.setStyleSheet(
                "color: #8c8c88; font-family: 'Poppins', sans-serif; "
                "font-size: 11px; background: transparent; border: none;"
            )
            meta_row.addWidget(otel_lbl)

            butce = seyahat.toplam_butce()
            butce_lbl = QLabel(f"{int(butce):,} TL".replace(",", "."))
            butce_lbl.setStyleSheet(
                "color: #d4845a; font-family: 'Poppins', sans-serif; "
                "font-size: 11px; font-weight: 600; "
                "background: transparent; border: none;"
            )
            meta_row.addWidget(butce_lbl)
        else:
            bos = QLabel("Konaklama yok")
            bos.setStyleSheet(
                "color: #b0aea8; font-family: 'Poppins', sans-serif; "
                "font-size: 11px; font-style: italic; "
                "background: transparent; border: none;"
            )
            meta_row.addWidget(bos)

        meta_row.addStretch()
        layout.addLayout(meta_row)

        # Butonlar
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        detay_btn = QPushButton("Detay")
        detay_btn.setObjectName("IkincilButon")
        detay_btn.setFixedSize(72, 30)
        detay_btn.setCursor(Qt.PointingHandCursor)
        detay_btn.clicked.connect(
            lambda _, sid=seyahat.seyahat_id: self.seyahat_secildi.emit(sid))

        duzenle_btn = QPushButton("Düzenle")
        duzenle_btn.setFixedSize(80, 30)
        duzenle_btn.setCursor(Qt.PointingHandCursor)
        duzenle_btn.clicked.connect(
            lambda _, sid=seyahat.seyahat_id: self._duzenle(sid))
        if seyahat.gecmis_mi():
            duzenle_btn.setEnabled(False)

        sil_btn = QPushButton("Sil")
        sil_btn.setObjectName("TehlikeButon")
        sil_btn.setFixedSize(50, 30)
        sil_btn.setCursor(Qt.PointingHandCursor)
        sil_btn.clicked.connect(
            lambda _, sid=seyahat.seyahat_id: self._sil(sid))

        btn_row.addWidget(detay_btn)
        btn_row.addWidget(duzenle_btn)
        btn_row.addWidget(sil_btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        return kart

    def _yeni_seyahat(self):
        dlg = SeyahatDiyalog(parent=self)
        if dlg.exec_() == SeyahatDiyalog.Accepted:
            r = dlg.sonuc
            self.vy.seyahat_ekle(
                gidis_yeri=r["gidis_yeri"],
                tarih=r["tarih"],
                donus_tarihi=r["donus_tarihi"],
                konaklama=r["konaklama"],
                notlar=r["notlar"],
            )
            self.veri_degisti.emit()
            self.yenile()

    def _duzenle(self, seyahat_id: int):
        s = self.vy.seyahat_getir(seyahat_id)
        if not s:
            return
        dlg = SeyahatDiyalog(seyahat=s, parent=self)
        if dlg.exec_() == SeyahatDiyalog.Accepted:
            r = dlg.sonuc
            try:
                self.vy.seyahat_guncelle(
                    seyahat_id=seyahat_id,
                    gidis_yeri=r["gidis_yeri"],
                    tarih=r["tarih"],
                    donus_tarihi=r["donus_tarihi"],
                    konaklama=r["konaklama"],
                    notlar=r["notlar"],
                )
                self.veri_degisti.emit()
                self.yenile()
            except ValueError as ex:
                QMessageBox.warning(self, "Hata", str(ex))

    def _sil(self, seyahat_id: int):
        s = self.vy.seyahat_getir(seyahat_id)
        if not s:
            return
        cevap = QMessageBox.question(
            self, "Seyahat Sil",
            f"'{s.gidis_yeri}' seyahatini silmek istediğinize emin misiniz?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No,
        )
        if cevap == QMessageBox.Yes:
            self.vy.seyahat_sil(seyahat_id)
            self.veri_degisti.emit()
            self.yenile()
