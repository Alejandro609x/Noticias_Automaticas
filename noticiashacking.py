# noticias_ciber_avanzado.py

import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from googletrans import Translator
import gzip
import json

# ==============================
# CONFIGURACIÓN
# ==============================

# Fuentes de noticias (RSS o URLs normales)
FUENTES = [
    "https://feeds.feedburner.com/TheHackersNews",  # RSS
    "https://www.bleepingcomputer.com/feed/",       # RSS
    "https://www.securityweek.com/rss",             # RSS
    "https://www.example.com/noticias-ciber"        # URL normal (HTML)
]

# Correo
EMAIL_REMITENTE = "usuario@gmail.com"
EMAIL_DESTINO = "usuario@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
APP_PASSWORD = "codigodeseguridad16caracteres"

# Número máximo de artículos por fuente
MAX_ARTICULOS = 5

translator = Translator()

# ==============================
# FUNCIONES
# ==============================

# Detecta si la fuente es RSS
def es_rss(url):
    return url.endswith(".xml") or "feed" in url or "rss" in url

# Obtener noticias desde RSS
def obtener_noticias_rss(url):
    noticias = []
    try:
        feed = feedparser.parse(url)
        for entry in feed.entries[:MAX_ARTICULOS]:
            noticias.append({
                "titulo": entry.title,
                "link": entry.link,
                "contenido": None
            })
    except Exception as e:
        print(f"[!] Error leyendo RSS {url}: {e}")
    return noticias

# Obtener noticias desde página web normal (HTML)
def obtener_noticias_html(url):
    noticias = []
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "lxml")
        # Extrae los primeros MAX_ARTICULOS encabezados <h2> o <h3> con enlace
        articulos = soup.find_all(["h2", "h3"], limit=MAX_ARTICULOS)
        for art in articulos:
            a_tag = art.find("a")
            if a_tag and a_tag.get("href"):
                link = a_tag["href"]
                if not link.startswith("http"):
                    # Construye link completo si es relativo
                    link = requests.compat.urljoin(url, link)
                noticias.append({
                    "titulo": a_tag.get_text(strip=True),
                    "link": link,
                    "contenido": None
                })
    except Exception as e:
        print(f"[!] Error leyendo HTML {url}: {e}")
    return noticias

# Extraer contenido de un artículo
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

# Traducir al español
def traducir_al_espanol(texto):
    try:
        trad = translator.translate(texto, dest="es")
        return trad.text
    except:
        return texto

# Resumir texto
def resumir_texto(texto):
    oraciones = texto.split(".")
    resumen = ".".join(oraciones[:3])
    if len(resumen.strip()) == 0:
        resumen = texto[:200] + "..."
    return resumen

# Obtener CVEs recientes
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

# Generar reporte HTML
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

# Enviar correo
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
    noticias = []
    for fuente in FUENTES:
        if es_rss(fuente):
            noticias += obtener_noticias_rss(fuente)
        else:
            noticias += obtener_noticias_html(fuente)

    cves = obtener_cves_recientes()
    reporte = generar_reporte(noticias, cves)
    enviar_correo(reporte)

if __name__ == "__main__":
    main()
