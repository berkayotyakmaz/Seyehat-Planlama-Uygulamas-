"""
Atlas Tema — Modern seyahat teması.
Sıcak krem zemin, okyanus mavisi, terrakotta accent.
"""

RENKLER = {
    # Zemin katmanları
    "bg": "#faf8f5",              # sıcak krem ana zemin
    "bg_alt": "#f2efe9",          # alternatif yüzey
    "surface": "#ffffff",         # kart beyazı
    "inset": "#edeae4",           # input arkaplanı

    # Metin
    "text": "#2c2c2c",            # ana metin
    "text_sec": "#555550",        # ikincil metin
    "text_muted": "#8c8c88",      # soluk metin
    "text_hint": "#b0aea8",       # placeholder
    "text_disabled": "#cccac4",   # devre dışı

    # Çizgiler
    "border": "#d9d6d0",          # genel kenarlık
    "border_light": "#e8e5df",    # hafif kenarlık
    "divider": "#edeae4",         # ayraç

    # Primary — okyanus mavisi
    "primary": "#2d5a7b",
    "primary_dark": "#1e3f58",
    "primary_light": "#e8f0f6",
    "primary_hover": "#3a6d91",

    # Accent — terrakotta / gün batımı
    "accent": "#d4845a",
    "accent_dark": "#b06a42",
    "accent_light": "#fdf0e8",

    # Durum
    "success": "#3a8a6a",
    "success_light": "#e6f3ed",
    "warning": "#c49a3c",
    "warning_light": "#faf3e0",
    "danger": "#c45454",
    "danger_light": "#fceaea",
}


ANA_STIL = f"""
/* ── GENEL ────────────────────────────────────────── */
QWidget {{
    background-color: {RENKLER['bg']};
    color: {RENKLER['text']};
    font-family: "Poppins", "DM Sans", "Segoe UI", sans-serif;
    font-size: 13px;
}}

QMainWindow {{
    background-color: {RENKLER['bg']};
}}

QToolTip {{
    background-color: {RENKLER['primary_dark']};
    color: #ffffff;
    border: none;
    padding: 7px 12px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 500;
}}

/* ── SIDEBAR ──────────────────────────────────────── */
#Sidebar {{
    background-color: {RENKLER['primary_dark']};
    border: none;
}}

#Sidebar QLabel {{
    background: transparent;
    border: none;
}}

QPushButton#MenuButon {{
    background-color: transparent;
    color: rgba(255,255,255,0.65);
    text-align: left;
    padding-left: 24px;
    padding-right: 24px;
    border: none;
    border-left: 3px solid transparent;
    border-radius: 0;
    font-family: "Poppins", "DM Sans", sans-serif;
    font-size: 13px;
    font-weight: 500;
}}

QPushButton#MenuButon:hover {{
    background-color: rgba(255,255,255,0.08);
    color: rgba(255,255,255,0.9);
}}

QPushButton#MenuButon:checked {{
    background-color: rgba(255,255,255,0.1);
    color: #ffffff;
    font-weight: 600;
    border-left: 3px solid {RENKLER['accent']};
}}

#KullaniciKart {{
    background-color: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 8px;
}}

#KullaniciKart QLabel {{
    background: transparent;
    border: none;
}}

#KullaniciAd {{
    color: #ffffff;
    font-weight: 600;
    font-size: 12px;
    font-family: "Poppins", sans-serif;
}}

#KullaniciDurum {{
    color: rgba(255,255,255,0.5);
    font-size: 10px;
    font-family: "Poppins", sans-serif;
    text-transform: uppercase;
    font-weight: 500;
}}

#PlanRozet {{
    background-color: {RENKLER['accent']};
    color: #ffffff;
    border: none;
    border-radius: 4px;
    padding: 2px 8px;
    font-size: 9px;
    font-weight: 700;
    font-family: "Poppins", sans-serif;
    min-width: 44px;
}}

#MenuBaslik {{
    color: rgba(255,255,255,0.35);
    font-family: "Poppins", sans-serif;
    font-size: 9px;
    font-weight: 700;
    text-transform: uppercase;
    background: transparent;
    border: none;
}}

/* ── SAYFA BAŞLIKLARI ─────────────────────────────── */
#SayfaBaslik {{
    color: {RENKLER['text']};
    background: transparent;
    border: none;
    font-family: "Poppins", "DM Sans", sans-serif;
    font-size: 32px;
    font-weight: 700;
}}

#SayfaAltBaslik {{
    color: {RENKLER['text_muted']};
    background: transparent;
    border: none;
    font-family: "Poppins", sans-serif;
    font-size: 13px;
    font-weight: 400;
}}

/* ── KARTLAR ──────────────────────────────────────── */
#Kart {{
    background-color: {RENKLER['surface']};
    border: 1px solid {RENKLER['border_light']};
    border-radius: 8px;
}}

#Kart QLabel {{
    background: transparent;
    border: none;
}}

#KartBaslik {{
    color: {RENKLER['text']};
    font-family: "Poppins", sans-serif;
    font-size: 17px;
    font-weight: 700;
    background: transparent;
    border: none;
}}

#KartAltBaslik {{
    color: {RENKLER['text_muted']};
    font-family: "Poppins", sans-serif;
    font-size: 12px;
    background: transparent;
    border: none;
}}

/* ── BUTONLAR ─────────────────────────────────────── */
QPushButton {{
    background-color: {RENKLER['surface']};
    color: {RENKLER['text']};
    border: 1px solid {RENKLER['border']};
    padding: 6px 16px;
    border-radius: 6px;
    font-family: "Poppins", sans-serif;
    font-size: 12px;
    font-weight: 600;
    min-height: 28px;
}}

QPushButton:hover {{
    background-color: {RENKLER['bg_alt']};
    border: 1px solid {RENKLER['text_muted']};
}}

QPushButton:disabled {{
    background-color: {RENKLER['inset']};
    color: {RENKLER['text_disabled']};
    border: 1px solid {RENKLER['border_light']};
}}

QPushButton#PrimaryButon {{
    background-color: {RENKLER['primary']};
    background: {RENKLER['primary']};
    color: #ffffff;
    border: 1px solid {RENKLER['primary']};
    padding-left: 22px;
    padding-right: 22px;
}}

QPushButton#PrimaryButon:hover {{
    background-color: {RENKLER['primary_hover']};
    background: {RENKLER['primary_hover']};
    border: 1px solid {RENKLER['primary_hover']};
    color: #ffffff;
}}

QPushButton#IkincilButon {{
    background-color: {RENKLER['surface']};
    color: {RENKLER['primary']};
    border: 1px solid {RENKLER['primary']};
    padding-left: 18px;
    padding-right: 18px;
}}

QPushButton#IkincilButon:hover {{
    background-color: {RENKLER['primary_light']};
    color: {RENKLER['primary']};
}}

QPushButton#TehlikeButon {{
    background-color: transparent;
    color: {RENKLER['danger']};
    border: 1px solid {RENKLER['border']};
    padding-left: 14px;
    padding-right: 14px;
}}

QPushButton#TehlikeButon:hover {{
    background-color: {RENKLER['danger']};
    color: #ffffff;
    border: 1px solid {RENKLER['danger']};
}}

/* ── FORM ALANLARI ────────────────────────────────── */
QLineEdit, QSpinBox, QDateEdit, QComboBox, QTextEdit, QDoubleSpinBox {{
    background-color: {RENKLER['surface']};
    border: 1px solid {RENKLER['border']};
    border-radius: 6px;
    padding-left: 12px;
    padding-right: 12px;
    color: {RENKLER['text']};
    selection-background-color: {RENKLER['primary']};
    selection-color: #ffffff;
    font-family: "Poppins", sans-serif;
    font-size: 13px;
}}

/* İç butonları sıfırla (ok, takvim, spin vs.) */
QSpinBox::up-button, QSpinBox::down-button,
QDoubleSpinBox::up-button, QDoubleSpinBox::down-button,
QDateEdit::up-button, QDateEdit::down-button {{
    background: transparent;
    border: none;
    width: 20px;
    padding: 0;
    margin: 0;
}}

QSpinBox::up-arrow, QDoubleSpinBox::up-arrow, QDateEdit::up-arrow {{
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-bottom: 5px solid {RENKLER['text_muted']};
    width: 0;
    height: 0;
}}

QSpinBox::down-arrow, QDoubleSpinBox::down-arrow, QDateEdit::down-arrow {{
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid {RENKLER['text_muted']};
    width: 0;
    height: 0;
}}

QDateEdit::drop-down {{
    border: none;
    width: 28px;
    background: transparent;
    padding: 0;
    margin: 0;
    subcontrol-origin: padding;
    subcontrol-position: center right;
}}

QLineEdit:focus, QSpinBox:focus, QDateEdit:focus,
QComboBox:focus, QTextEdit:focus, QDoubleSpinBox:focus {{
    border: 2px solid {RENKLER['primary']};
    background-color: #ffffff;
}}

QLineEdit:hover, QSpinBox:hover, QDateEdit:hover,
QComboBox:hover, QTextEdit:hover, QDoubleSpinBox:hover {{
    border: 1px solid {RENKLER['primary']};
}}

QComboBox::drop-down {{
    border: none;
    width: 28px;
    background: transparent;
}}

QComboBox::down-arrow {{
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid {RENKLER['text_muted']};
    margin-right: 12px;
    width: 0;
    height: 0;
}}

QComboBox QAbstractItemView {{
    background-color: {RENKLER['surface']};
    border: 1px solid {RENKLER['border']};
    border-radius: 6px;
    selection-background-color: {RENKLER['primary_light']};
    selection-color: {RENKLER['primary']};
    color: {RENKLER['text']};
    padding: 4px;
    outline: 0;
}}

QLabel#FormEtiket {{
    color: {RENKLER['text_sec']};
    font-family: "Poppins", sans-serif;
    font-size: 11px;
    font-weight: 600;
    background: transparent;
    border: none;
}}

/* ── SCROLLBAR ────────────────────────────────────── */
QScrollBar:vertical {{
    background: transparent;
    width: 8px;
    border: none;
    margin: 4px 2px;
}}

QScrollBar::handle:vertical {{
    background: {RENKLER['border']};
    border-radius: 4px;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background: {RENKLER['text_muted']};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
    background: none;
}}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
    background: none;
}}

QScrollBar:horizontal {{
    background: transparent;
    height: 8px;
    border: none;
    margin: 2px 4px;
}}

QScrollBar::handle:horizontal {{
    background: {RENKLER['border']};
    border-radius: 4px;
    min-width: 30px;
}}

QScrollBar::handle:horizontal:hover {{
    background: {RENKLER['text_muted']};
}}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0;
    background: none;
}}

QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
    background: none;
}}

/* ── DİYALOG ──────────────────────────────────────── */
QDialog {{
    background-color: {RENKLER['bg']};
}}

QMessageBox {{
    background-color: {RENKLER['surface']};
}}

QMessageBox QLabel {{
    color: {RENKLER['text']};
    font-family: "Poppins", sans-serif;
    font-size: 13px;
    background: transparent;
    border: none;
}}

QMessageBox QPushButton {{
    min-width: 90px;
    min-height: 32px;
    padding: 4px 16px;
}}

/* ── AYIRAÇLAR ────────────────────────────────────── */
QFrame#Ayirici {{
    background-color: {RENKLER['border']};
    max-height: 1px;
    min-height: 1px;
    border: none;
}}

QFrame#AyiriciInce {{
    background-color: {RENKLER['divider']};
    max-height: 1px;
    min-height: 1px;
    border: none;
}}
"""
