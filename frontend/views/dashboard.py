"""
Dashboard sayfası — Metrikler + yaklaşan seyahatler.
"""
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QFrame,
    QPushButton,
)
from PyQt5.QtCore import Qt, pyqtSignal

from backend import VeriYoneticisi
from frontend.widgets.bilesenler import (
    MetrikKart,
    HeroKart,
    DurumRozeti,
    tarih_aralik_format,
)


class DashboardSayfasi(QWidget):
    seyahat_secildi = pyqtSignal(int)

    def __init__(self, vy: VeriYoneticisi, aktif_kullanici=None, parent=None):
        super().__init__(parent)
        self.vy = vy
        self.aktif_kullanici = aktif_kullanici
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

        # Hero kart
        ad = self.aktif_kullanici.ad if self.aktif_kullanici else "Seyyah"
        self.hero = HeroKart(
            baslik=f"Hoş Geldin, {ad}",
            altyazi="Yolculuğunu planla, anılarını biriktir.",
        )
        self.layout.addWidget(self.hero)
        self.layout.addSpacing(28)

        # Metrik kartlar
        self.layout.addWidget(self._section_baslik("İstatistikler"))
        self.layout.addSpacing(10)

        metrik_row = QHBoxLayout()
        metrik_row.setSpacing(14)

        self.m_toplam = MetrikKart("Toplam Seyahat", "0", "Tüm seyahatler")
        self.m_aktif = MetrikKart("Aktif Seyahat", "0", "Şu an devam eden", accent=True)
        self.m_yaklasan = MetrikKart("Yaklaşan", "0", "Gelecek seyahatler")
        self.m_harcama = MetrikKart("Toplam Harcama", "0", "Konaklama toplamı")

        metrik_row.addWidget(self.m_toplam)
        metrik_row.addWidget(self.m_aktif)
        metrik_row.addWidget(self.m_yaklasan)
        metrik_row.addWidget(self.m_harcama)

        self.layout.addLayout(metrik_row)
        self.layout.addSpacing(28)

        # Yaklaşan seyahatler
        self.layout.addWidget(self._section_baslik("Yaklaşan Seyahatler"))
        self.layout.addSpacing(10)

        self.yaklasan_container = QVBoxLayout()
        self.yaklasan_container.setSpacing(10)
        self.layout.addLayout(self.yaklasan_container)

        self.layout.addStretch()

        scroll.setWidget(icerik)
        dis.addWidget(scroll)

    def _section_baslik(self, metin: str) -> QLabel:
        lbl = QLabel(metin)
        lbl.setStyleSheet(
            "color: #2c2c2c; font-family: 'Poppins', sans-serif; "
            "font-size: 16px; font-weight: 700; "
            "background: transparent; border: none;"
        )
        return lbl

    def yenile(self):
        ist = self.vy.genel_istatistikler()
        self.m_toplam.deger_ayarla(str(ist["toplam_seyahat"]))
        self.m_aktif.deger_ayarla(str(ist["aktif_seyahat"]))
        self.m_yaklasan.deger_ayarla(str(ist["yaklasan_seyahat"]))

        harcama = ist["toplam_harcama"]
        if harcama >= 1000:
            harcama_str = f"{harcama/1000:.1f}K"
        else:
            harcama_str = str(int(harcama))
        self.m_harcama.deger_ayarla(harcama_str)
        self.m_harcama.altyazi_ayarla(f"{int(harcama):,} TL".replace(",", "."))

        self.hero.metrikleri_ayarla([
            ("Toplam", str(ist["toplam_seyahat"])),
            ("Aktif", str(ist["aktif_seyahat"])),
            ("Yaklaşan", str(ist["yaklasan_seyahat"])),
            ("Harcama", harcama_str),
        ])

        # Yaklaşan seyahatler
        while self.yaklasan_container.count():
            item = self.yaklasan_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        gelecek = self.vy.gelecek_seyahatler()
        aktif = self.vy.aktif_seyahatler()
        liste = aktif + gelecek

        if not liste:
            bos = QLabel("Yaklaşan seyahat bulunmuyor.")
            bos.setStyleSheet(
                "color: #b0aea8; font-family: 'Poppins', sans-serif; "
                "font-size: 13px; font-style: italic; "
                "background: transparent; border: none; padding: 20px 0;"
            )
            self.yaklasan_container.addWidget(bos)
        else:
            for s in liste[:5]:
                kart = self._seyahat_kart(s)
                self.yaklasan_container.addWidget(kart)

    def _seyahat_kart(self, seyahat) -> QFrame:
        kart = QFrame()
        kart.setStyleSheet(
            "QFrame { background-color: #ffffff; "
            "border: 1px solid #e8e5df; "
            "border-radius: 8px; }"
        )
        kart.setCursor(Qt.PointingHandCursor)

        layout = QHBoxLayout(kart)
        layout.setContentsMargins(20, 14, 20, 14)
        layout.setSpacing(14)

        # Sol accent bar
        bar = QFrame()
        bar.setFixedSize(3, 48)
        bar.setStyleSheet(
            "background-color: #d4845a; border: none; border-radius: 1px;")
        layout.addWidget(bar, 0, Qt.AlignVCenter)

        # Bilgi
        sol = QVBoxLayout()
        sol.setSpacing(3)

        yer = QLabel(seyahat.gidis_yeri)
        yer.setStyleSheet(
            "color: #2c2c2c; font-family: 'Poppins', sans-serif; "
            "font-size: 17px; font-weight: 700; "
            "background: transparent; border: none;"
        )
        sol.addWidget(yer)

        tarih = QLabel(tarih_aralik_format(seyahat.tarih, seyahat.donus_tarihi))
        tarih.setStyleSheet(
            "color: #8c8c88; font-family: 'Poppins', sans-serif; "
            "font-size: 12px; background: transparent; border: none;"
        )
        sol.addWidget(tarih)

        meta = f"{seyahat.gun_sayisi()} gün"
        if seyahat.konaklama:
            meta += f"  ·  {seyahat.konaklama.otel_adi}"
        meta_lbl = QLabel(meta)
        meta_lbl.setStyleSheet(
            "color: #b0aea8; font-family: 'Poppins', sans-serif; "
            "font-size: 11px; background: transparent; border: none;"
        )
        sol.addWidget(meta_lbl)

        layout.addLayout(sol, 1)

        rozet = DurumRozeti.from_seyahat(seyahat)
        layout.addWidget(rozet, 0, Qt.AlignVCenter)

        detay_btn = QPushButton("Detay")
        detay_btn.setObjectName("IkincilButon")
        detay_btn.setFixedSize(72, 32)
        detay_btn.setCursor(Qt.PointingHandCursor)
        detay_btn.clicked.connect(
            lambda _, sid=seyahat.seyahat_id: self.seyahat_secildi.emit(sid))
        layout.addWidget(detay_btn, 0, Qt.AlignVCenter)

        return kart
