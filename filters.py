APPLICATIONS = {

    # =================
    # VIDEO / STREAMING
    # =================
    "youtube": "YouTube",
    "googlevideo": "YouTube",
    "ytimg": "YouTube",
    "youtu": "YouTube",

    "netflix": "Netflix",

    "spotify": "Spotify",
    "scdn": "Spotify",

    "kwai": "Kwai",
    "snackvideo": "SnackVideo",

    "capcut": "CapCut",

    "dramawave": "DramaWave",
    "mydramawave": "DramaWave",
    "bytedrama": "DramaWave",

    "vidio": "Vidio",
    "viu": "Viu",
    "wetv": "WeTV",
    "iqiyi": "iQIYI",
    "hotstar": "Disney+ Hotstar",
    "twitch": "Twitch",

    # =================
    # SOCIAL MEDIA
    # =================
    "tiktok": "TikTok",
    "tiktokcdn": "TikTok",
    "snssdk": "TikTok",

    "instagram": "Instagram",
    "cdninstagram": "Instagram",

    "facebook": "Facebook",
    "fbcdn": "Facebook",

    "twitter": "X / Twitter",
    "twimg": "X / Twitter",

    "discord": "Discord",
    "reddit": "Reddit",
    "linkedin": "LinkedIn",
    "pinterest": "Pinterest",

    "line.me": "LINE",
    "linecdn": "LINE",
    "line-scdn": "LINE",

    # =================
    # CHAT
    # =================
    "whatsapp": "WhatsApp",
    "telegram": "Telegram",

    # =================
    # FINTECH / PAYMENT
    # =================
    "dana": "DANA",
    "shopeepay": "ShopeePay",
    "shopee": "ShopeePay",
    "gopay": "GoPay",
    "gojek": "Gojek",
    "grab": "Grab",
    "grabpay": "Grab",
    "ovo": "OVO",
    "linkaja": "LinkAja",
    "bca": "BCA",
    "mandiri": "Mandiri",
    "seabank": "SeaBank",

    # =================
    # E-COMMERCE
    # =================
    "tokopedia": "Tokopedia",
    "lazada": "Lazada",
    "bukalapak": "Bukalapak",
    "blibli": "Blibli",
    "traveloka": "Traveloka",
    "tiket.com": "Tiket.com",

    # =================
    # GAME
    # =================
    "mobilelegends": "Mobile Legends",
    "moonton": "Mobile Legends",
    "pubg": "PUBG Mobile",
    "krafton": "PUBG Mobile",
    "freefire": "Free Fire",
    "garena": "Free Fire",
    "steam": "Steam",
    "riot": "Riot Games",
    "epicgames": "Epic Games",
    "roblox": "Roblox",
    "genshin": "Genshin Impact",
    "supercell": "Supercell",
    "minecraft": "Minecraft",

    # =================
    # EDUKASI / LAINNYA
    # =================
    "ruangguru": "Ruangguru",
    "zenius": "Zenius",
    "duolingo": "Duolingo",
    "zoom": "Zoom",
    "miui": "Xiaomi Apps",
    "xiaomi": "Xiaomi Apps"
}


def detect_application(domain):

    domain = domain.lower()

    # =========================
    # CEK APLIKASI DULU!
    # supaya api.tiktok.com,
    # api.whatsapp.com, dll
    # tetap terhitung
    # =========================

    for key, app in APPLICATIONS.items():

        if key in domain:
            return app

    # tidak cocok aplikasi mana pun
    # (CDN, tracking, dll otomatis
    # dibuang karena tidak ada
    # di daftar aplikasi)

    return None
