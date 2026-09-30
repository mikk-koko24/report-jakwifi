APPLICATIONS = {

    # =================
    # VIDEO / STREAMING
    # =================
    "youtube": "YouTube",
    "googlevideo": "YouTube",
    "ytimg": "YouTube",

    "netflix": "Netflix",

    "spotify": "Spotify",
    "scdn": "Spotify",

        "kwai": "Kwai",
    "kwai-pro": "Kwai",
    "kwaipros": "Kwai",

    "snackvideo": "SnackVideo",

    "capcut": "CapCut",

    "mydramawave": "DramaWave",
    "bytedrama": "DramaWave",

        # Entertainment / Video
    "dramawave": "DramaWave",
    "mydramawave": "DramaWave",

    # Short video
    "snackvideo": "SnackVideo",

    # CapCut
    "capcut": "CapCut",

    # Xiaomi Apps
    "miui": "Xiaomi Apps",
    "xiaomi": "Xiaomi Apps",


    # =================
    # SOCIAL MEDIA
    # =================
    "tiktok": "TikTok",
    "tiktokcdn": "TikTok",

    "instagram": "Instagram",
    "cdninstagram": "Instagram",

    "facebook": "Facebook",
    "fbcdn": "Facebook",

    "twitter": "X / Twitter",
    "twimg": "X / Twitter",


    # =================
    # CHAT
    # =================
    "whatsapp": "WhatsApp",
    "telegram": "Telegram",


        # =================
    # FINTECH / PAYMENT
    # =================
    "dana": "DANA",
    "dana.id": "DANA",

    "shopeepay": "ShopeePay",
    "shopee": "ShopeePay",

    "gopay": "GoPay",
    "gojek": "Gojek",


    # =================
    # E-COMMERCE
    # =================
    "tokopedia": "Tokopedia",
    "lazada": "Lazada",


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
    "epicgames": "Epic Games"

}



# Semua ini dibuang,
# bukan aplikasi user

BLOCKED = [

    # CDN / Network
    "cloudflare",
    "akamai",
    "fastly",
    "cloudfront",

    # Infrastruktur
    "amazonaws",
    "azure",
    "microsoft",
    "oracle",

    # Backend
    "api",
    "gateway",
    "service",

    # Tracking
    "analytics",
    "doubleclick",
    "ads",
    "tracking",
    "telemetry"

]



def detect_application(domain):

    domain = domain.lower()


    # buang layanan
    for item in BLOCKED:
        if item in domain:
            return None


    # cari aplikasi
    for key, app in APPLICATIONS.items():

        if key in domain:
            return app


    return None