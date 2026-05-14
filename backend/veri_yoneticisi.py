"""
Seyahat Veri Yöneticisi - JSON kalıcılık ile tüm seyahatleri yönetir.
Konaklama ve Plan'lar seyahat içinde nested olarak saklanır.
"""
import json
import os
import shutil
import tempfile
from datetime import datetime
from typing import Dict, List, Optional

from .seyahat import Seyahat
from .konaklama import Konaklama
from .plan import Plan


def _bugun() -> datetime:
    """Bugünün başlangıç anı — tek noktada tanımlı (race-condition önler)."""
    return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)


class VeriYoneticisi:
    """Seyahat verilerini JSON dosyasında yönetir."""

    def __init__(self, veri_klasoru: str = "data"):
        self.veri_klasoru = veri_klasoru
        os.makedirs(veri_klasoru, exist_ok=True)

        self.seyahatler_dosya = os.path.join(veri_klasoru, "seyahatler.json")

        self._seyahatler: Dict[int, Seyahat] = {}
        self._sonraki_id = 1

        self._yukle()

    # ── Kalıcılık ──

    def _yukle(self) -> None:
        if not os.path.exists(self.seyahatler_dosya):
            return
        try:
            with open(self.seyahatler_dosya, "r", encoding="utf-8") as f:
                veri = json.load(f)
            for d in veri:
                s = Seyahat.from_dict(d)
                self._seyahatler[s.seyahat_id] = s
            if self._seyahatler:
                self._sonraki_id = max(self._seyahatler) + 1
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as ex:
            # Bozuk dosyayı sessizce yutma — yedekle ki yeni yazımla ezilmesin.
            yedek = (
                self.seyahatler_dosya
                + ".bozuk."
                + datetime.now().strftime("%Y%m%d_%H%M%S")
            )
            try:
                shutil.copy2(self.seyahatler_dosya, yedek)
                print(
                    f"[VeriYoneticisi] UYARI: Veri dosyası bozuk ({ex}). "
                    f"Yedek: {yedek}"
                )
            except OSError as kopyala_hatasi:
                raise RuntimeError(
                    f"Seyahat verisi bozuk ve yedeklenemedi. "
                    f"Manuel müdahale gerekli: {self.seyahatler_dosya}"
                ) from kopyala_hatasi
            self._seyahatler = {}
            self._sonraki_id = 1

    def kaydet(self) -> None:
        """Atomik yazım: temp dosyaya yaz, os.replace ile değiştir."""
        os.makedirs(self.veri_klasoru, exist_ok=True)
        veri = [s.to_dict() for s in self._seyahatler.values()]

        dir_ = os.path.dirname(self.seyahatler_dosya) or "."
        fd, tmp_yol = tempfile.mkstemp(
            prefix=".seyahatler_", suffix=".tmp", dir=dir_
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(veri, f, ensure_ascii=False, indent=2)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp_yol, self.seyahatler_dosya)
        except Exception:
            try:
                os.unlink(tmp_yol)
            except OSError:
                pass
            raise

    # ── Seyahat CRUD ──

    def seyahat_ekle(
        self,
        gidis_yeri: str,
        tarih: datetime,
        donus_tarihi: datetime,
        kullanici_id: int = 1,
        konaklama: Konaklama | None = None,
        notlar: str = "",
    ) -> Seyahat:
        if not gidis_yeri.strip():
            raise ValueError("Gidiş yeri boş olamaz.")
        if donus_tarihi < tarih:
            raise ValueError("Dönüş tarihi gidiş tarihinden önce olamaz.")

        seyahat = Seyahat(
            seyahat_id=self._sonraki_id,
            gidis_yeri=gidis_yeri,
            tarih=tarih,
            donus_tarihi=donus_tarihi,
            kullanici_id=kullanici_id,
            konaklama=konaklama,
            notlar=notlar,
        )
        seyahat.planlari_olustur()
        self._seyahatler[seyahat.seyahat_id] = seyahat
        self._sonraki_id += 1
        self.kaydet()
        return seyahat

    def seyahat_ekle_hazir(self, seyahat: Seyahat) -> Seyahat:
        """Seed için: hazır Seyahat nesnesini ekler. ID çakışmasını reddeder."""
        if seyahat.seyahat_id in self._seyahatler:
            raise ValueError(
                f"ID çakışması: {seyahat.seyahat_id} zaten kullanımda."
            )
        self._seyahatler[seyahat.seyahat_id] = seyahat
        self._sonraki_id = max(self._sonraki_id, seyahat.seyahat_id + 1)
        self.kaydet()
        return seyahat

    def seyahat_guncelle(
        self,
        seyahat_id: int,
        gidis_yeri: str,
        tarih: datetime,
        donus_tarihi: datetime,
        konaklama: Konaklama | None = None,
        notlar: str = "",
    ) -> Seyahat:
        s = self._seyahatler.get(seyahat_id)
        if not s:
            raise ValueError(f"Seyahat bulunamadı (ID: {seyahat_id}).")
        if s.gecmis_mi():
            raise ValueError("Geçmiş seyahatler düzenlenemez.")
        if donus_tarihi < tarih:
            raise ValueError("Dönüş tarihi gidiş tarihinden önce olamaz.")

        s.gidis_yeri = gidis_yeri.strip()
        s.tarih = tarih
        s.donus_tarihi = donus_tarihi
        s.konaklama = konaklama
        s.notlar = notlar.strip()
        s.planlari_olustur()
        self.kaydet()
        return s

    def seyahat_sil(self, seyahat_id: int) -> bool:
        if seyahat_id not in self._seyahatler:
            return False
        del self._seyahatler[seyahat_id]
        self.kaydet()
        return True

    def seyahat_getir(self, seyahat_id: int) -> Optional[Seyahat]:
        return self._seyahatler.get(seyahat_id)

    def plan_guncelle(
        self,
        seyahat_id: int,
        gun: int,
        rota: list[str],
        aktiviteler: list[str],
    ):
        """Belirli bir günün planını günceller. Geçmiş seyahatlerde reddeder."""
        s = self._seyahatler.get(seyahat_id)
        if not s:
            raise ValueError("Seyahat bulunamadı.")
        if s.gecmis_mi():
            raise ValueError("Geçmiş seyahatlerin planları düzenlenemez.")
        for p in s.planlar:
            if p.gun == gun:
                p.rota = rota
                p.aktiviteler = aktiviteler
                self.kaydet()
                return
        raise ValueError(f"Gün {gun} bulunamadı.")

    # ── Sorgular (kullanıcıya göre filtreleme) ──

    def _kullaniciya_ait(
        self, kullanici_id: Optional[int]
    ) -> List[Seyahat]:
        """kullanici_id None → tümü; aksi halde sahibine ait olanlar."""
        tum = list(self._seyahatler.values())
        if kullanici_id is None:
            return tum
        return [s for s in tum if s.kullanici_id == kullanici_id]

    def tum_seyahatler(
        self, kullanici_id: Optional[int] = None
    ) -> List[Seyahat]:
        return sorted(
            self._kullaniciya_ait(kullanici_id),
            key=lambda s: s.tarih,
            reverse=True,
        )

    def aktif_seyahatler(
        self, kullanici_id: Optional[int] = None
    ) -> List[Seyahat]:
        bugun = _bugun()
        return [
            s for s in self._kullaniciya_ait(kullanici_id)
            if s.tarih <= bugun <= s.donus_tarihi
        ]

    def gelecek_seyahatler(
        self, kullanici_id: Optional[int] = None
    ) -> List[Seyahat]:
        bugun = _bugun()
        return sorted(
            [s for s in self._kullaniciya_ait(kullanici_id)
             if s.tarih > bugun],
            key=lambda s: s.tarih,
        )

    def gecmis_seyahatler(
        self, kullanici_id: Optional[int] = None
    ) -> List[Seyahat]:
        bugun = _bugun()
        return sorted(
            [s for s in self._kullaniciya_ait(kullanici_id)
             if s.donus_tarihi < bugun],
            key=lambda s: s.tarih,
            reverse=True,
        )

    # ── İstatistik ──

    def genel_istatistikler(
        self, kullanici_id: Optional[int] = None
    ) -> dict:
        """
        Gerçekleşen harcama = geçmiş + aktif (yaşandı/yaşanıyor).
        Planlanan bütçe   = gelecek seyahatlerin konaklama maliyeti.
        Toplam bütçe      = ikisinin toplamı.
        """
        tum = self._kullaniciya_ait(kullanici_id)
        bugun = _bugun()

        gerceklesen = 0.0
        planlanan = 0.0
        aktif_sayi = 0
        gelecek_sayi = 0

        for s in tum:
            butce = s.toplam_butce()
            if s.donus_tarihi < bugun:
                gerceklesen += butce
            elif s.tarih > bugun:
                planlanan += butce
                gelecek_sayi += 1
            else:
                gerceklesen += butce
                aktif_sayi += 1

        return {
            "toplam_seyahat": len(tum),
            "aktif_seyahat": aktif_sayi,
            "yaklasan_seyahat": gelecek_sayi,
            "gerceklesen_harcama": gerceklesen,
            "planlanan_butce": planlanan,
            "toplam_butce": gerceklesen + planlanan,
        }

    def sehir_dagilimi(
        self, kullanici_id: Optional[int] = None
    ) -> dict:
        """En çok gidilen şehirler."""
        dagilim: dict[str, int] = {}
        for s in self._kullaniciya_ait(kullanici_id):
            dagilim[s.gidis_yeri] = dagilim.get(s.gidis_yeri, 0) + 1
        return dagilim

    def ortalama_sure(
        self, kullanici_id: Optional[int] = None
    ) -> float:
        tum = self._kullaniciya_ait(kullanici_id)
        if not tum:
            return 0
        return sum(s.gun_sayisi() for s in tum) / len(tum)
