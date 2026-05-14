"""
Ana Pencere — Atlas tema, koyu sidebar + içerik yığını.
"""
from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
    QButtonGroup,
    QFrame,
    QMessageBox,
    QApplication,
)
from PyQt5.QtCore import Qt

from backend import VeriYoneticisi
from frontend.widgets.bilesenler import Masthead, Avatar
from frontend.views.dashboard import DashboardSayfasi
from frontend.views.seyahatler import SeyahatlerSayfasi
from frontend.views.seyahat_detay import SeyahatDetaySayfasi
from frontend.views.raporlar import RaporlarSayfasi


class AnaPencere(QMainWindow):
    def __init__(self, vy: VeriYoneticisi, aktif_kullanici=None):
        super().__init__()
        self.vy = vy
        self.aktif_kullanici = aktif_kullanici
        self.logout_istendi = False

        self.setWindowTitle("Yol Defteri — Seyahat Planlama")
        self.setMinimumSize(1180, 760)
        self.resize(1380, 880)

        self._arayuz_olustur()

    def _arayuz_olustur(self):
        merkez = QWidget()
        ana = QHBoxLayout(merkez)
        ana.setContentsMargins(0, 0, 0, 0)
        ana.setSpacing(0)

        sidebar = self._sidebar_olustur()
        ana.addWidget(sidebar)

        icerik_sarici = QWidget()
        icerik_sarici.setStyleSheet("background-color: #faf8f5;")
        icerik_layout = QVBoxLayout(icerik_sarici)
        icerik_layout.setContentsMargins(0, 0, 0, 0)
        icerik_layout.setSpacing(0)

        self.yigin = QStackedWidget()

        self.sayfa_dashboard = DashboardSayfasi(self.vy, self.aktif_kullanici)
        self.sayfa_seyahatler = SeyahatlerSayfasi(self.vy, self.aktif_kullanici)
        self.sayfa_detay = SeyahatDetaySayfasi(self.vy, self.aktif_kullanici)
        self.sayfa_raporlar = RaporlarSayfasi(self.vy, self.aktif_kullanici)

        self.sayfa_seyahatler.seyahat_secildi.connect(self._seyahat_detay_goster)
        self.sayfa_seyahatler.veri_degisti.connect(self._tumunu_yenile)
        self.sayfa_detay.geri_istendi.connect(self._seyahatler_sayfasina_don)
        self.sayfa_detay.veri_degisti.connect(self._tumunu_yenile)
        self.sayfa_dashboard.seyahat_secildi.connect(self._seyahat_detay_goster)

        self.yigin.addWidget(self.sayfa_dashboard)   # 0
        self.yigin.addWidget(self.sayfa_seyahatler)  # 1
        self.yigin.addWidget(self.sayfa_detay)        # 2
        self.yigin.addWidget(self.sayfa_raporlar)     # 3

        icerik_layout.addWidget(self.yigin)
        ana.addWidget(icerik_sarici, 1)

        self.setCentralWidget(merkez)
        self.yigin.setCurrentIndex(0)

    def _sidebar_olustur(self) -> QFrame:
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(250)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 16)
        layout.setSpacing(0)

        layout.addWidget(Masthead())
        layout.addSpacing(24)

        layout.addWidget(self._menu_baslik("MENÜ"))

        self.buton_grubu = QButtonGroup(self)
        self.buton_grubu.setExclusive(True)

        self._menu_butonu_ekle(layout, "Dashboard", 0)
        self._menu_butonu_ekle(layout, "Seyahatler", 1)
        self._menu_butonu_ekle(layout, "Raporlar", 3)

        self.buton_grubu.button(0).setChecked(True)

        layout.addStretch()

        # Kullanıcı kartı
        kart_sarici = QHBoxLayout()
        kart_sarici.setContentsMargins(14, 0, 14, 0)

        kullanici_kart = QFrame()
        kullanici_kart.setObjectName("KullaniciKart")

        kk_layout = QHBoxLayout(kullanici_kart)
        kk_layout.setContentsMargins(12, 12, 12, 12)
        kk_layout.setSpacing(10)

        if self.aktif_kullanici:
            ad_str = self.aktif_kullanici.ad
            rol_str = self.aktif_kullanici.rol.upper()
        else:
            ad_str = "Kullanıcı"
            rol_str = "MİSAFİR"

        avatar = Avatar(ad_str, boyut=36)

        kullanici_bilgi = QVBoxLayout()
        kullanici_bilgi.setSpacing(2)
        kullanici_bilgi.setContentsMargins(0, 0, 0, 0)

        ust_satir = QHBoxLayout()
        ust_satir.setSpacing(8)
        ust_satir.setContentsMargins(0, 0, 0, 0)

        ad = QLabel(ad_str)
        ad.setObjectName("KullaniciAd")

        plan = QLabel("SEYYAH")
        plan.setObjectName("PlanRozet")
        plan.setAlignment(Qt.AlignCenter)
        plan.setMinimumWidth(48)
        plan.setMinimumHeight(18)

        ust_satir.addWidget(ad)
        ust_satir.addWidget(plan)
        ust_satir.addStretch()

        durum = QLabel(rol_str)
        durum.setObjectName("KullaniciDurum")

        kullanici_bilgi.addLayout(ust_satir)
        kullanici_bilgi.addWidget(durum)

        kk_layout.addWidget(avatar)
        kk_layout.addLayout(kullanici_bilgi)
        kk_layout.addStretch()

        cikis_btn = QPushButton("✕")
        cikis_btn.setFixedSize(28, 28)
        cikis_btn.setCursor(Qt.PointingHandCursor)
        cikis_btn.setToolTip("Çıkış yap")
        cikis_btn.setStyleSheet(
            "QPushButton { background-color: transparent; "
            "color: rgba(255,255,255,0.4); border: 1px solid rgba(255,255,255,0.15); "
            "border-radius: 6px; font-size: 12px; padding: 0; } "
            "QPushButton:hover { color: #ffffff; "
            "background-color: #c45454; border: 1px solid #c45454; }"
        )
        cikis_btn.clicked.connect(self._cikis_yap)
        kk_layout.addWidget(cikis_btn, 0, Qt.AlignVCenter)

        kart_sarici.addWidget(kullanici_kart)
        layout.addLayout(kart_sarici)

        return sidebar

    def _menu_baslik(self, metin: str) -> QLabel:
        lbl = QLabel(metin)
        lbl.setObjectName("MenuBaslik")
        lbl.setContentsMargins(24, 0, 24, 10)
        return lbl

    def _menu_butonu_ekle(self, layout, metin: str, indeks: int):
        btn = QPushButton(metin)
        btn.setObjectName("MenuButon")
        btn.setCheckable(True)
        btn.setFixedHeight(40)
        btn.setCursor(Qt.PointingHandCursor)
        btn.clicked.connect(lambda _, i=indeks: self._sayfa_degistir(i))
        self.buton_grubu.addButton(btn, indeks)
        layout.addWidget(btn)

    def _cikis_yap(self):
        cevap = QMessageBox.question(
            self, "Oturum Sonlandır",
            "Oturumu kapatıp giriş ekranına dönmek istediğinize emin misiniz?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No,
        )
        if cevap == QMessageBox.Yes:
            # main.py'daki loop bunu görüp login ekranını yeniden açacak.
            self.logout_istendi = True
            self.close()

    def _sayfa_degistir(self, indeks: int):
        self.yigin.setCurrentIndex(indeks)
        sayfa = self.yigin.widget(indeks)
        if hasattr(sayfa, "yenile"):
            sayfa.yenile()

    def _seyahat_detay_goster(self, seyahat_id: int):
        self.sayfa_detay.seyahat_yukle(seyahat_id)
        self.yigin.setCurrentIndex(2)

    def _seyahatler_sayfasina_don(self):
        self.yigin.setCurrentIndex(1)
        self.buton_grubu.button(1).setChecked(True)
        self.sayfa_seyahatler.yenile()

    def _tumunu_yenile(self):
        for i in range(self.yigin.count()):
            sayfa = self.yigin.widget(i)
            if hasattr(sayfa, "yenile"):
                sayfa.yenile()
