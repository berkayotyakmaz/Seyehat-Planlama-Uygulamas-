"""
Raporlar sayfası — İstatistikler, şehir dağılımı, CSV export.
"""
import csv

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QFrame,
    QPushButton,
    QFileDialog,
    QMessageBox,
)
from PyQt5.QtCore import Qt

from backend import VeriYoneticisi
from frontend.widgets.bilesenler import (
    SayfaHeader,
    MetrikKart,
    KategoriBarYatay,
    Kart,
    tarih_aralik_format,
)


class RaporlarSayfasi(QWidget):
    def __init__(self, vy: VeriYoneticisi, aktif_kullanici=None, parent=None):
        super().__init__(parent)
        self.vy = vy
        self.aktif_kullanici = aktif_kullanici
        self._arayuz_olustur()
        self.yenile()

    @property
    def _kid(self):
        return self.aktif_kullanici.kullanici_id if self.aktif_kullanici else None

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
            kategori="RAPORLAR",
            baslik="Analiz",
            altyazi="Seyahat istatistikleri ve raporlar.",
        )
        self.layout.addWidget(header)
        self.layout.addSpacing(20)

        # Export
        export_row = QHBoxLayout()
        export_row.addStretch()
        export_btn = QPushButton("CSV Export")
        export_btn.setObjectName("IkincilButon")
        export_btn.setFixedHeight(34)
        export_btn.setCursor(Qt.PointingHandCursor)
        export_btn.clicked.connect(self._csv_export)
        export_row.addWidget(export_btn)
        self.layout.addLayout(export_row)
        self.layout.addSpacing(14)

        # Metrikler
        self.layout.addWidget(self._section_baslik("Genel İstatistikler"))
        self.layout.addSpacing(10)

        metrik_row = QHBoxLayout()
        metrik_row.setSpacing(14)

        self.m_toplam = MetrikKart("Toplam Seyahat", "0")
        self.m_sure = MetrikKart("Ort. Süre", "0", "gün", accent=True)
        self.m_harcama = MetrikKart("Gerçekleşen Harcama", "0")
        self.m_sehir = MetrikKart("Farklı Şehir", "0")

        metrik_row.addWidget(self.m_toplam)
        metrik_row.addWidget(self.m_sure)
        metrik_row.addWidget(self.m_harcama)
        metrik_row.addWidget(self.m_sehir)

        self.layout.addLayout(metrik_row)
        self.layout.addSpacing(28)

        # Şehir dağılımı
        self.layout.addWidget(self._section_baslik("En Çok Ziyaret Edilen Şehirler"))
        self.layout.addSpacing(10)

        self.sehir_kart = Kart(baslik="Şehir Dağılımı", alt_baslik="Seyahat sayısına göre")
        self.sehir_bar = KategoriBarYatay({})
        self.sehir_kart.layout.addWidget(self.sehir_bar)
        self.layout.addWidget(self.sehir_kart)
        self.layout.addSpacing(28)

        # Geçmiş
        self.layout.addWidget(self._section_baslik("Seyahat Geçmişi"))
        self.layout.addSpacing(10)

        self.gecmis_container = QVBoxLayout()
        self.gecmis_container.setSpacing(8)
        self.layout.addLayout(self.gecmis_container)

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
        ist = self.vy.genel_istatistikler(self._kid)
        self.m_toplam.deger_ayarla(str(ist["toplam_seyahat"]))

        ort = self.vy.ortalama_sure(self._kid)
        self.m_sure.deger_ayarla(f"{ort:.1f}")
        self.m_sure.altyazi_ayarla("gün ortalama")

        harcama = ist["gerceklesen_harcama"]
        if harcama >= 1000:
            self.m_harcama.deger_ayarla(f"{harcama/1000:.1f}K")
        else:
            self.m_harcama.deger_ayarla(str(int(harcama)))
        planli = ist["planlanan_butce"]
        self.m_harcama.altyazi_ayarla(
            f"{int(harcama):,} TL  (+{int(planli):,} TL planlı)".replace(",", ".")
        )

        dagilim = self.vy.sehir_dagilimi(self._kid)
        self.m_sehir.deger_ayarla(str(len(dagilim)))

        self.sehir_bar.dagilim = dagilim
        n = len(dagilim) if dagilim else 1
        self.sehir_bar.setMinimumHeight(n * 44 + 10)
        self.sehir_bar.update()

        # Geçmiş
        while self.gecmis_container.count():
            item = self.gecmis_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        gecmis = self.vy.gecmis_seyahatler(self._kid)
        if not gecmis:
            bos = QLabel("Henüz tamamlanmış seyahat yok.")
            bos.setStyleSheet(
                "color: #b0aea8; font-family: 'Poppins', sans-serif; "
                "font-size: 13px; font-style: italic; "
                "background: transparent; border: none; padding: 12px 0;"
            )
            self.gecmis_container.addWidget(bos)
        else:
            for s in gecmis:
                satir = QFrame()
                satir.setStyleSheet(
                    "QFrame { background-color: #ffffff; "
                    "border: 1px solid #e8e5df; border-radius: 8px; }"
                )
                row = QHBoxLayout(satir)
                row.setContentsMargins(16, 12, 16, 12)
                row.setSpacing(14)

                yer = QLabel(s.gidis_yeri)
                yer.setStyleSheet(
                    "color: #2c2c2c; font-family: 'Poppins', sans-serif; "
                    "font-size: 15px; font-weight: 700; "
                    "background: transparent; border: none;"
                )
                row.addWidget(yer)

                tarih = QLabel(tarih_aralik_format(s.tarih, s.donus_tarihi))
                tarih.setStyleSheet(
                    "color: #8c8c88; font-family: 'Poppins', sans-serif; "
                    "font-size: 11px; background: transparent; border: none;"
                )
                row.addWidget(tarih)

                gun = QLabel(f"{s.gun_sayisi()} gün")
                gun.setStyleSheet(
                    "color: #2d5a7b; font-family: 'Poppins', sans-serif; "
                    "font-size: 11px; font-weight: 600; "
                    "background: transparent; border: none;"
                )
                row.addWidget(gun)

                if s.konaklama:
                    butce = QLabel(f"{int(s.toplam_butce()):,} TL".replace(",", "."))
                    butce.setStyleSheet(
                        "color: #d4845a; font-family: 'Poppins', sans-serif; "
                        "font-size: 11px; font-weight: 600; "
                        "background: transparent; border: none;"
                    )
                    row.addWidget(butce)

                row.addStretch()
                self.gecmis_container.addWidget(satir)

    def _csv_export(self):
        dosya, _ = QFileDialog.getSaveFileName(
            self, "CSV Olarak Kaydet", "seyahatler.csv",
            "CSV Dosyası (*.csv)"
        )
        if not dosya:
            return

        tum = self.vy.tum_seyahatler(self._kid)
        with open(dosya, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow([
                "ID", "Gidiş Yeri", "Gidiş Tarihi", "Dönüş Tarihi",
                "Gün Sayısı", "Otel", "Gecelik Fiyat", "Konaklama Bütçesi",
                "Durum", "Notlar",
            ])
            for s in tum:
                writer.writerow([
                    s.seyahat_id,
                    s.gidis_yeri,
                    s.tarih.strftime("%d.%m.%Y"),
                    s.donus_tarihi.strftime("%d.%m.%Y"),
                    s.gun_sayisi(),
                    s.konaklama.otel_adi if s.konaklama else "",
                    s.konaklama.fiyat if s.konaklama else "",
                    s.toplam_butce(),
                    s.durum_metni(),
                    s.notlar,
                ])

        QMessageBox.information(self, "Export", f"CSV dosyası kaydedildi:\n{dosya}")
