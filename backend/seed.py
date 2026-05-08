"""
Seed verisi - 6 örnek seyahat (geçmiş + aktif + gelecek karışık).
"""
from datetime import datetime, timedelta

from .seyahat import Seyahat
from .konaklama import Konaklama
from .plan import Plan
from .veri_yoneticisi import VeriYoneticisi


def seed_gerekli_mi(vy: VeriYoneticisi) -> bool:
    return len(vy.tum_seyahatler()) == 0


def seed_uygula(vy: VeriYoneticisi) -> None:
    bugun = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    # 1. Kapadokya - geçmiş (1 ay önce, 3 gün)
    kap_baslangic = bugun - timedelta(days=30)
    kap_bitis = kap_baslangic + timedelta(days=2)
    kapadokya = Seyahat(
        seyahat_id=1,
        gidis_yeri="Kapadokya",
        tarih=kap_baslangic,
        donus_tarihi=kap_bitis,
        konaklama=Konaklama("Cave Hotel", 1500, "Göreme Merkez", "Çift Kişilik"),
        planlar=[
            Plan(1, kap_baslangic,
                 ["Göreme", "Uçhisar"],
                 ["Balon turu", "Kahvaltı", "Peri bacaları gezisi"]),
            Plan(2, kap_baslangic + timedelta(days=1),
                 ["Göreme Açıkhava Müzesi", "Avanos"],
                 ["Müze gezisi", "Çömlek atölyesi", "Akşam yemeği"]),
            Plan(3, kap_baslangic + timedelta(days=2),
                 ["Derinkuyu", "Ihlara Vadisi"],
                 ["Yeraltı şehri turu", "Vadi yürüyüşü"]),
        ],
        notlar="Harika bir deneyimdi! Balon turu unutulmaz.",
    )

    # 2. Antalya - geçmiş (2 hafta önce, 5 gün)
    ant_baslangic = bugun - timedelta(days=14)
    ant_bitis = ant_baslangic + timedelta(days=4)
    antalya = Seyahat(
        seyahat_id=2,
        gidis_yeri="Antalya",
        tarih=ant_baslangic,
        donus_tarihi=ant_bitis,
        konaklama=Konaklama("Sea View Resort", 2200, "Konyaaltı Sahili", "Suite"),
        planlar=[
            Plan(1, ant_baslangic,
                 ["Düden Şelalesi", "Kaleiçi"],
                 ["Şelale gezisi", "Tarihi sokaklar yürüyüşü"]),
            Plan(2, ant_baslangic + timedelta(days=1),
                 ["Aspendos", "Side"],
                 ["Antik tiyatro gezisi", "Side harabeleri"]),
            Plan(3, ant_baslangic + timedelta(days=2),
                 ["Konyaaltı Plajı"],
                 ["Plaj günü", "Yüzme", "Güneşlenme"]),
            Plan(4, ant_baslangic + timedelta(days=3),
                 ["Olimpos", "Yanartaş"],
                 ["Olimpos harabeleri", "Yanartaş gece gezisi"]),
            Plan(5, ant_baslangic + timedelta(days=4),
                 ["Antalya Müzesi"],
                 ["Müze gezisi", "Hediyelik alışveriş", "Dönüş hazırlığı"]),
        ],
        notlar="Deniz harikaydı, Aspendos çok etkileyici.",
    )

    # 3. İstanbul (iş gezisi) - aktif (bugün başladı, 4 gün)
    ist_baslangic = bugun
    ist_bitis = bugun + timedelta(days=3)
    istanbul = Seyahat(
        seyahat_id=3,
        gidis_yeri="İstanbul",
        tarih=ist_baslangic,
        donus_tarihi=ist_bitis,
        konaklama=Konaklama("Bosphorus Hotel", 3000, "Beşiktaş, Boğaz kenarı", "Suite"),
        planlar=[
            Plan(1, ist_baslangic,
                 ["Konferans Merkezi", "Taksim"],
                 ["Konferans katılımı", "Akşam yemeği"]),
            Plan(2, ist_baslangic + timedelta(days=1),
                 ["Sultanahmet", "Ayasofya", "Topkapı Sarayı"],
                 ["Tarihi alan gezisi", "Öğle yemeği"]),
            Plan(3, ist_baslangic + timedelta(days=2),
                 ["Galata Kulesi", "Karaköy", "Balat"],
                 ["Fotoğraf turu", "Kahve molası"]),
            Plan(4, ist_baslangic + timedelta(days=3),
                 ["Kapalıçarşı", "Mısır Çarşısı"],
                 ["Alışveriş", "Dönüş"]),
        ],
        notlar="İş gezisi ama biraz gezi de yapmalı.",
    )

    # 4. Bodrum - yaklaşan (2 hafta sonra, 7 gün)
    bod_baslangic = bugun + timedelta(days=14)
    bod_bitis = bod_baslangic + timedelta(days=6)
    bodrum = Seyahat(
        seyahat_id=4,
        gidis_yeri="Bodrum",
        tarih=bod_baslangic,
        donus_tarihi=bod_bitis,
        konaklama=Konaklama("Beach Resort", 1800, "Bodrum Merkez", "Çift Kişilik"),
        planlar=[
            Plan(1, bod_baslangic,
                 ["Bodrum Kalesi"],
                 ["Varış ve yerleşme", "Kale gezisi"]),
            Plan(2, bod_baslangic + timedelta(days=1),
                 ["Bodrum Antik Tiyatro", "Marina"],
                 ["Antik tiyatro gezisi", "Marina yürüyüşü"]),
            Plan(3, bod_baslangic + timedelta(days=2),
                 ["Bitez Plajı"],
                 ["Yat turu", "Plaj"]),
            Plan(4, bod_baslangic + timedelta(days=3),
                 ["Gümüşlük"],
                 ["Gümüşlük gezisi", "Balık yemeği"]),
            Plan(5, bod_baslangic + timedelta(days=4),
                 ["Türkbükü"],
                 ["Plaj günü"]),
            Plan(6, bod_baslangic + timedelta(days=5),
                 ["Bodrum Sualtı Müzesi"],
                 ["Müze gezisi", "Alışveriş"]),
            Plan(7, bod_baslangic + timedelta(days=6),
                 [],
                 ["Dönüş hazırlığı"]),
        ],
    )

    # 5. Trabzon - yaklaşan (1 ay sonra, 4 gün)
    trb_baslangic = bugun + timedelta(days=30)
    trb_bitis = trb_baslangic + timedelta(days=3)
    trabzon = Seyahat(
        seyahat_id=5,
        gidis_yeri="Trabzon",
        tarih=trb_baslangic,
        donus_tarihi=trb_bitis,
        konaklama=Konaklama("Karadeniz Otel", 1200, "Trabzon Merkez", "Tek Kişilik"),
        planlar=[
            Plan(1, trb_baslangic,
                 ["Uzungöl"],
                 ["Uzungöl gezisi", "Doğa yürüyüşü"]),
            Plan(2, trb_baslangic + timedelta(days=1),
                 ["Sümela Manastırı"],
                 ["Manastır gezisi", "Fotoğraf"]),
            Plan(3, trb_baslangic + timedelta(days=2),
                 ["Ayder Yaylası"],
                 ["Yayla gezisi", "Termal banyo"]),
            Plan(4, trb_baslangic + timedelta(days=3),
                 ["Trabzon Merkez", "Atatürk Köşkü"],
                 ["Şehir turu", "Dönüş"]),
        ],
    )

    # 6. Eskişehir - yaklaşan (3 hafta sonra, 2 gün), konaklama yok
    esk_baslangic = bugun + timedelta(days=21)
    esk_bitis = esk_baslangic + timedelta(days=1)
    eskisehir = Seyahat(
        seyahat_id=6,
        gidis_yeri="Eskişehir",
        tarih=esk_baslangic,
        donus_tarihi=esk_bitis,
        konaklama=None,
        planlar=[
            Plan(1, esk_baslangic,
                 ["Odunpazarı", "Porsuk Çayı"],
                 ["Tarihi evler gezisi", "Gondol turu"]),
            Plan(2, esk_baslangic + timedelta(days=1),
                 ["Sazova Parkı", "Bilim Deney Merkezi"],
                 ["Park gezisi", "Bilim merkezi", "Dönüş"]),
        ],
    )

    for s in [kapadokya, antalya, istanbul, bodrum, trabzon, eskisehir]:
        vy.seyahat_ekle_hazir(s)
