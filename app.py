from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

app = Flask(__name__)
app.secret_key = "pop_cards_tr_secret_key"

user_data = {
    "username": "MüzikSever",
    "points": 100,
    "inventory": []
}

posts_feed = []
leaderboard = [
    {"username": "MüzikSever", "points": 100, "cards_count": 0}
]

# T-POP TAM KADRO KART KATALOĞU (Görseller Google & Ajans veri bağlantılıdır)
cards_catalog = [
    # --- MANIFEST (6 Üye) ---
    {"id": "manifest_sueda", "name": "Sueda Uluca", "artist": "Manifest", "role": "Main Vocal (Ana Vokal)", "price": 100, "image": "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=500", "rarity": "Efsanevi"},
    {"id": "manifest_lidya", "name": "Lidya Pınar", "artist": "Manifest", "role": "Lead Vocal (Lider Vokal)", "price": 85, "image": "https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e?w=500", "rarity": "Nadir"},
    {"id": "manifest_hilal", "name": "Hilal Yelekçi", "artist": "Manifest", "role": "Lead Dancer (Lider Dansçı)", "price": 85, "image": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=500", "rarity": "Nadir"},
    {"id": "manifest_esin", "name": "Esin Bahat", "artist": "Manifest", "role": "Main Dancer (Ana Dansçı)", "price": 90, "image": "https://images.unsplash.com/photo-1508214751196-bcfd4ca60f91?w=500", "rarity": "Efsanevi"},
    {"id": "manifest_mina", "name": "Mina Solak", "artist": "Manifest", "role": "Sub Vocal & Dance", "price": 75, "image": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=500", "rarity": "Yaygın"},
    {"id": "manifest_zeynep", "name": "Zeynep Sude Oktay", "artist": "Manifest", "role": "Sub Vocal", "price": 75, "image": "https://images.unsplash.com/photo-1488426862026-3ee34a7d66df?w=500", "rarity": "Yaygın"},

    # --- RADİKAL (4 Üye) ---
    {"id": "radikal_vedat", "name": "Vedat Çelik", "artist": "Radikal", "role": "Ana Vokal & Söz/Beste", "price": 100, "image": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=500", "rarity": "Efsanevi"},
    {"id": "radikal_yusa", "name": "Yuşa Akbıyık", "artist": "Radikal", "role": "Baş Dansçı (Maknae)", "price": 85, "image": "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?w=500", "rarity": "Nadir"},
    {"id": "radikal_yusuf", "name": "Yusuf Emre (Yemre)", "artist": "Radikal", "role": "Yardımcı Vokal", "price": 80, "image": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=500", "rarity": "Nadir"},
    {"id": "radikal_ibrahim", "name": "İbrahim Can Kaya (CJ)", "artist": "Radikal", "role": "Ana Dansçı & Rapçi", "price": 85, "image": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=500", "rarity": "Nadir"},

    # --- CRUSH (7 Üye) ---
    {"id": "crush_oguzhan", "name": "Oğuzhan Çiftçi", "artist": "CRUSH", "role": "Lider & Ana Vokal", "price": 95, "image": "https://images.unsplash.com/photo-1501196354995-cbb51c65aaea?w=500", "rarity": "Efsanevi"},
    {"id": "crush_batu", "name": "Batu Cengiz", "artist": "CRUSH", "role": "Lead Vocal", "price": 80, "image": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=500", "rarity": "Nadir"},
    {"id": "crush_baris", "name": "Barış Çağan Yüksekkaya", "artist": "CRUSH", "role": "Main Rap & Dance", "price": 85, "image": "https://images.unsplash.com/photo-1513956589380-bad6acb9b9d4?w=500", "rarity": "Nadir"},
    {"id": "crush_mirac", "name": "Miraç Fırat", "artist": "CRUSH", "role": "Sub Vocal", "price": 75, "image": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=500", "rarity": "Yaygın"},
    {"id": "crush_milan", "name": "Milan Önder", "artist": "CRUSH", "role": "Visual & Sub Vocal", "price": 75, "image": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=500", "rarity": "Yaygın"},
    {"id": "crush_arda", "name": "Arda Soydoğan", "artist": "CRUSH", "role": "Lead Dancer", "price": 75, "image": "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?w=500", "rarity": "Yaygın"},
    {"id": "crush_efe", "name": "Efe Şan", "artist": "CRUSH", "role": "Sub Dancer", "price": 70, "image": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=500", "rarity": "Yaygın"},

    # --- KARM6 (6 Üye) ---
    {"id": "karm6_cesuku", "name": "Cem Suha Kurt (CeSuKu)", "artist": "KARM6", "role": "Rap & Vokal (Ateşin Alevi)", "price": 95, "image": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=500", "rarity": "Efsanevi"},
    {"id": "karm6_ada", "name": "Ada Atılgan", "artist": "KARM6", "role": "Ana Vokal (Ateşin Kıvılcımı)", "price": 90, "image": "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=500", "rarity": "Efsanevi"},
    {"id": "karm6_ezgi", "name": "Ezgi Akliman", "artist": "KARM6", "role": "Vokal (Ateşin Kalbi)", "price": 80, "image": "https://images.unsplash.com/photo-1524504388940-b1c1722653e1?w=500", "rarity": "Nadir"},
    {"id": "karm6_erdeniz", "name": "Erdeniz Telli", "artist": "KARM6", "role": "Baş Dansçı (Ateşin Sıcaklığı)", "price": 85, "image": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=500", "rarity": "Nadir"},
    {"id": "karm6_adilcan", "name": "Adilcan Bilgin", "artist": "KARM6", "role": "Lider Vokal (Ateşin Dumanı)", "price": 85, "image": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=500", "rarity": "Nadir"},
    {"id": "karm6_ozlem", "name": "Özlem Naz Gözcü", "artist": "KARM6", "role": "Vokal & Görsel (Ateşin Işığı)", "price": 80, "image": "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=500", "rarity": "Nadir"},

    # --- AURA (4 Üye) ---
    {"id": "aura_asli", "name": "Aslı Göztaşı", "artist": "Aura", "role": "Ana Vokal (A-slı)", "price": 90, "image": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=500", "rarity": "Efsanevi"},
    {"id": "aura_suzy", "name": "Suzy (Umut) Roumenov", "artist": "Aura", "role": "Baş Dansçı (U-mut)", "price": 85, "image": "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=500", "rarity": "Nadir"},
    {"id": "aura_meri", "name": "Meri (Raziye) Aslan", "artist": "Aura", "role": "Vokal & Dans (R-aziye)", "price": 75, "image": "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=500", "rarity": "Yaygın"},
    {"id": "aura_esra", "name": "Esra (Aylin) Mutlu", "artist": "Aura", "role": "Sahne Enerjisi (A-ylin)", "price": 75, "image": "https://images.unsplash.com/photo-1524504388940-b1c1722653e1?w=500", "rarity": "Yaygın"}
]

songs_catalog = [
    {"id": 1, "title": "HAYRAN", "artist": "Radikal", "reward_points": 40, "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4"},
    {"id": 2, "title": "CRUSH - Sahne Şovu", "artist": "CRUSH", "reward_points": 50, "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerMeltdowns.mp4"},
    {"id": 3, "title": "KARM6 - Ta Burama", "artist": "KARM6", "reward_points": 45, "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4"},
    {"id": 4, "title": "Manifest - Çıkış Klibi", "artist": "Manifest", "reward_points": 45, "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4"}
]

def sync_leaderboard():
    for user in leaderboard:
        if user["username"] == user_data["username"]:
            user["points"] = user_data["points"]
            user["cards_count"] = len(user_data["inventory"])
    leaderboard.sort(key=lambda x: (x["points"], x["cards_count"]), reverse=True)

@app.route("/")
def index():
    sync_leaderboard()
    return render_template("index.html", user=user_data, posts=posts_feed, leaderboard=leaderboard)

@app.route("/post_share", methods=["POST"])
def post_share():
    username = request.form.get("username") or "AnonimPopçu"
    user_data["username"] = username
    artist = request.form.get("artist")
    caption = request.form.get("caption")
    image_url = request.form.get("image_url") or "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=500"
    
    new_post = {
        "id": len(posts_feed) + 1,
        "username": username,
        "artist": artist,
        "caption": caption,
        "image": image_url,
        "likes": 0,
        "timestamp": "Şimdi"
    }
    posts_feed.insert(0, new_post)
    user_data["points"] += 50
    flash("Gönderin başarıyla akışta paylaşıldı ve +50 Puan kazandın! 🔥", "success")
    return redirect(url_for("index"))

@app.route("/store")
def store():
    return render_template("store.html", user=user_data, cards=cards_catalog)

@app.route("/buy/<card_id>", methods=["POST"])
def buy_card(card_id):
    card = next((c for c in cards_catalog if c["id"] == card_id), None)
    if card:
        if card_id in user_data["inventory"]:
            flash("Bu üye kartına zaten sahipsin!", "warning")
        elif user_data["points"] >= card["price"]:
            user_data["points"] -= card["price"]
            user_data["inventory"].append(card_id)
            flash(f"Tebrikler! {card['artist']} grubundan {card['name']} kartını satın aldın! 🎴", "success")
        else:
            flash("Yeterli puanın yok! Şarkı izleyerek puan kazanabilirsin.", "danger")
    return redirect(url_for("store"))

@app.route("/player")
def player():
    return render_template("player.html", user=user_data, songs=songs_catalog)

@app.route("/api/add_points", methods=["POST"])
def add_points_api():
    data = request.get_json()
    points_to_add = int(data.get("points", 0))
    user_data["points"] += points_to_add
    sync_leaderboard()
    return jsonify({"status": "success", "new_points": user_data["points"]})

if __name__ == "__main__":
    app.run(debug=True)
