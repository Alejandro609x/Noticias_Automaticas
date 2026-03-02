# noticias_ciber_x_final.py

import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from googletrans import Translator
import tweepy
import gzip
import json

# ==============================
# CONFIGURACIÓN
# ==============================

# RSS feeds de noticias
RSS_FEEDS = [
    "https://feeds.feedburner.com/TheHackersNews",
    "https://www.bleepingcomputer.com/feed/"
]

# Cuentas X a monitorear
CUENTAS_X = [
    "H4ckmanac",
    "AnonymousMex_",
    "adrxx_Chronus",
    "SonoraCiber",
]

# Correo
EMAIL_REMITENTE = "ale609jandro609@gmail.com"
EMAIL_DESTINO = "asalazarl@finanzas.cdmx.gob.mx"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
APP_PASSWORD = "TOKENGENERADA"

# API de X
BEARER_TOKEN = "TOKEN_X"

# Número máximo de artículos por feed
MAX_ARTICULOS = 5

translator = Translator()

# ==============================
# FUNCIONES
# ==============================

def obtener_noticias():
    noticias = []
    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:MAX_ARTICULOS]:
            noticias.append({
                "titulo": entry.title,
                "link": entry.link,
                "contenido": None
            })
    return noticias

def extraer_texto(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "lxml")
        parrafos = soup.find_all("p")
        texto = " ".join([p.get_text() for p in parrafos])
        return texto[:3000]
    except Exception as e:
        return f"No se pudo extraer contenido: {e}"

def traducir_al_espanol(texto):
    try:
        trad = translator.translate(texto, dest="es")
        return trad.text
    except:
        return texto

def resumir_texto(texto):
    oraciones = texto.split(".")
    resumen = ".".join(oraciones[:3])
    if len(resumen.strip()) == 0:
        resumen = texto[:200] + "..."
    return resumen

def obtener_tweets_cuenta(username, max_tweets=5):
    resultado = []
    try:
        client = tweepy.Client(bearer_token=BEARER_TOKEN)
        user = client.get_user(username=username)
        user_id = user.data.id
        tweets = client.get_users_tweets(id=user_id, max_results=max_tweets, tweet_fields=["created_at"])
        if tweets.data:
            for t in tweets.data:
                resultado.append({
                    "titulo": f"Tweet de @{username}",
                    "link": f"https://x.com/{username}/status/{t.id}",
                    "contenido": t.text
                })
    except Exception as e:
        print(f"[!] No se pudieron obtener tweets de @{username}: {e}")
    return resultado

def obtener_cves_recientes(max_cves=5):
    try:
        url = "https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-recent.json.gz"
        r = requests.get(url, stream=True)
        with gzip.GzipFile(fileobj=r.raw) as f:
            data = json.load(f)
        cves = []
        for item in data["CVE_Items"][:max_cves]:
            cve_id = item["cve"]["CVE_data_meta"]["ID"]
            desc = item["cve"]["description"]["description_data"][0]["value"]
            cves.append({"id": cve_id, "desc": desc})
        return cves
    except Exception as e:
        print(f"[!] Error obteniendo CVEs: {e}")
        return []

def generar_reporte(noticias, cves):
    reporte_html = f"<h2>🛡️ Reporte Diario de Ciberseguridad</h2>"
    reporte_html += f"<p>Fecha: {datetime.now().strftime('%d/%m/%Y')}</p>"

    # Noticias
    reporte_html += "<h3>📢 Noticias recientes</h3><ul>"
    for n in noticias:
        if n["contenido"] is None:
            n["contenido"] = extraer_texto(n["link"])
        contenido = traducir_al_espanol(n["contenido"])
        resumen = resumir_texto(contenido)
        reporte_html += f"<li><b>{n['titulo']}</b><br>{resumen}<br><a href='{n['link']}'>Fuente</a></li>"
    reporte_html += "</ul>"

    # CVEs
    reporte_html += "<h3>⚠️ CVEs recientes</h3><ul>"
    for c in cves:
        reporte_html += f"<li><b>{c['id']}</b>: {c['desc']}</li>"
    reporte_html += "</ul>"

    reporte_html += "<p>Este reporte se genera automáticamente para alertar sobre novedades en ciberseguridad.</p>"
    return reporte_html

def enviar_correo(reporte_html):
    msg = MIMEMultipart("alternative")
    msg["From"] = EMAIL_REMITENTE
    msg["To"] = EMAIL_DESTINO
    msg["Subject"] = "Reporte diario de ciberseguridad"
    msg.attach(MIMEText(reporte_html, "html"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_REMITENTE, APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("[+] Correo enviado correctamente")
    except Exception as e:
        print(f"[!] Error enviando correo: {e}")

# ==============================
# MAIN
# ==============================

def main():
    noticias = obtener_noticias()

    # Agregar tweets de X
    for cuenta in CUENTAS_X:
        noticias += obtener_tweets_cuenta(cuenta)

    # Obtener CVEs recientes
    cves = obtener_cves_recientes()

    # Generar y enviar reporte
    reporte = generar_reporte(noticias, cves)
    enviar_correo(reporte)

if __name__ == "__main__":
    main()
