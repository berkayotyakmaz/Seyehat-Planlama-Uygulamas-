"""
Seyahat Detay sayfası — Konaklama + günlük planlar.
"""
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QFrame,
    QPushButton,
    QSizePolicy,
    QMessageBox,
)
from PyQt5.QtCore import Qt, pyqtSignal

from backend import VeriYoneticisi
from frontend.widgets.bilesenler import (
    SayfaHeader,
    DurumRozeti,
    GunlukPlanKart,
    Kart,
    tarih_aralik_format,
    tarih_format,
)
from frontend.widgets.diyaloglar import PlanDuzenleDiyalog, SeyahatDiyalog


class SeyahatDetaySayfasi(QWidget):
    geri_istendi = pyqtSignal()
    veri_degisti = pyqtSignal()

    def __init__(self, vy: VeriYoneticisi, parent=None):
        super().__init__(parent)
        self.vy = vy
        self.seyahat = None
        self._arayuz_olustur()

    def _arayuz_olustur(self):
        dis = QVBoxLayout(self)
        dis.setContentsMargins(0, 0, 0, 0)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)

        self.icerik = QWidget()
        self.layout = QVBoxLayout(self.icerik)
        self.layout.setContentsMargins(40, 32, 40, 32)
        self.layout.setSpacing(0)

        self.scroll.setWidget(self.icerik)
        dis.addWidget(self.scroll)

    def seyahat_yukle(self, seyahat_id: int):
        self.seyahat = self.vy.seyahat_getir(seyahat_id)
        self._icerigi_olustur()

    def yenile(self):
        if self.seyahat:
            self.seyahat = self.vy.seyahat_getir(self.seyahat.seyahat_id)
            self._icerigi_olustur()

    def _temizle(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._layout_temizle(item.layout())

    def _layout_temizle(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._layout_temizle(item.layout())

    def _icerigi_olustur(self):
        self._temizle()
        s = self.seyahat
        if not s:
            return

        # Geri butonu
        geri_btn = QPushButton("← Seyahatler")
        geri_btn.setObjectName("IkincilButon")
        geri_btn.setFixedHeight(32)
        geri_btn.setFixedWidth(140)
        geri_btn.setCursor(Qt.PointingHandCursor)
        geri_btn.clicked.connect(self.geri_istendi.emit)
        self.layout.addWidget(geri_btn)
        self.layout.addSpacing(14)

        # Header
        header = SayfaHeader(
            kategori="SEYAHAT DETAY",
            baslik=s.gidis_yeri,
            altyazi=tarih_aralik_format(s.tarih, s.donus_tarihi),
            sag_metin=f"{s.gun_sayisi()} GÜN",
        )
        self.layout.addWidget(header)
        self.layout.addSpacing(14)

        # Rozet + düzenle
        ust_row = QHBoxLayout()
        rozet = DurumRozeti.from_seyahat(s)
        ust_row.addWidget(rozet)
        ust_row.addStretch()

        if not s.gecmis_mi():
            duzenle_btn = QPushButton("Düzenle")
            duzenle_btn.setObjectName("IkincilButon")
            duzenle_btn.setFixedHeight(32)
            duzenle_btn.setCursor(Qt.PointingHandCursor)
            duzenle_btn.clicked.connect(self._duzenle)
            ust_row.addWidget(duzenle_btn)

        self.layout.addLayout(ust_row)
        self.layout.addSpacing(20)

        # Geçmiş bilgi notu
        if s.gecmis_mi():
            bilgi = QLabel("Bu seyahat tamamlandı.")
            bilgi.setStyleSheet(
                "background-color: #f2efe9; color: #8c8c88; "
                "border: none; border-radius: 8px; "
                "padding: 12px 18px; font-family: 'Poppins', sans-serif; "
                "font-size: 12px; font-weight: 500;"
            )
            self.layout.addWidget(bilgi)
            self.layout.addSpacing(14)

        # Konaklama
        self.layout.addWidget(self._section_baslik("Konaklama"))
        self.layout.addSpacing(8)

        if s.konaklama:
            kon_kart = Kart(baslik=s.konaklama.otel_adi, alt_baslik=s.konaklama.oda_tipi)

            detaylar = QVBoxLayout()
            detaylar.setSpacing(6)

            if s.konaklama.adres:
                detaylar.addWidget(self._bilgi_satir("Adres", s.konaklama.adres))

            fiyat_str = f"{int(s.konaklama.fiyat):,} TL / gece".replace(",", ".")
            detaylar.addWidget(self._bilgi_satir("Gecelik Fiyat", fiyat_str))

            toplam = s.konaklama.toplam_fiyat(s.gun_sayisi())
            toplam_str = f"{int(toplam):,} TL".replace(",", ".")
            detaylar.addWidget(self._bilgi_satir("Toplam Maliyet", toplam_str))

            kon_kart.layout.addLayout(detaylar)
            self.layout.addWidget(kon_kart)
        else:
            bos = QLabel("Konaklama bilgisi eklenmemiş.")
            bos.setStyleSheet(
                "color: #b0aea8; font-family: 'Poppins', sans-serif; "
                "font-size: 13px; font-style: italic; "
                "background: transparent; border: none; padding: 12px 0;"
            )
            self.layout.addWidget(bos)

        self.layout.addSpacing(24)

        # Notlar
        if s.notlar:
            self.layout.addWidget(self._section_baslik("Notlar"))
            self.layout.addSpacing(8)
            notlar_lbl = QLabel(s.notlar)
            notlar_lbl.setWordWrap(True)
            notlar_lbl.setStyleSheet(
                "color: #555550; font-family: 'Poppins', sans-serif; "
                "font-size: 13px; "
                "background-color: #e8f0f6; border: none; border-radius: 8px; "
                "padding: 16px 20px;"
            )
            self.layout.addWidget(notlar_lbl)
            self.layout.addSpacing(24)

        # Günlük planlar
        self.layout.addWidget(self._section_baslik("Günlük Planlar"))
        self.layout.addSpacing(10)

        for plan in s.planlar:
            plan_row = QHBoxLayout()
            plan_row.setSpacing(8)

            plan_kart = GunlukPlanKart(plan)
            plan_kart.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            plan_row.addWidget(plan_kart, 1)

            if not s.gecmis_mi():
                duzenle = QPushButton("Düzenle")
                duzenle.setFixedSize(72, 30)
                duzenle.setCursor(Qt.PointingHandCursor)
                duzenle.clicked.connect(
                    lambda _, g=plan.gun: self._plan_duzenle(g))
                plan_row.addWidget(duzenle, 0, Qt.AlignTop)

            self.layout.addLayout(plan_row)
            self.layout.addSpacing(10)

        self.layout.addStretch()

    def _section_baslik(self, metin: str) -> QLabel:
        lbl = QLabel(metin)
        lbl.setStyleSheet(
            "color: #2c2c2c; font-family: 'Poppins', sans-serif; "
            "font-size: 16px; font-weight: 700; "
            "background: transparent; border: none;"
        )
        return lbl

    def _bilgi_satir(self, etiket: str, deger: str) -> QWidget:
        w = QWidget()
        w.setStyleSheet("background: transparent; border: none;")
        row = QHBoxLayout(w)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(12)

        et = QLabel(etiket)
        et.setStyleSheet(
            "color: #8c8c88; font-family: 'Poppins', sans-serif; "
            "font-size: 11px; font-weight: 600; "
            "background: transparent; border: none;"
        )
        et.setFixedWidth(120)
        row.addWidget(et)

        dg = QLabel(deger)
        dg.setStyleSheet(
            "color: #2c2c2c; font-family: 'Poppins', sans-serif; "
            "font-size: 13px; font-weight: 500; "
            "background: transparent; border: none;"
        )
        row.addWidget(dg, 1)
        return w

    def _duzenle(self):
        if not self.seyahat:
            return
        dlg = SeyahatDiyalog(seyahat=self.seyahat, parent=self)
        if dlg.exec_() == SeyahatDiyalog.Accepted:
            r = dlg.sonuc
            try:
                self.vy.seyahat_guncelle(
                    seyahat_id=self.seyahat.seyahat_id,
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

    def _plan_duzenle(self, gun: int):
        if not self.seyahat:
            return
        plan = None
        for p in self.seyahat.planlar:
            if p.gun == gun:
                plan = p
                break
        if not plan:
            return

        dlg = PlanDuzenleDiyalog(plan, parent=self)
        if dlg.exec_() == PlanDuzenleDiyalog.Accepted:
            self.vy.plan_guncelle(
                self.seyahat.seyahat_id,
                gun,
                dlg.sonuc_rota,
                dlg.sonuc_aktiviteler,
            )
            self.veri_degisti.emit()
            self.yenile()
