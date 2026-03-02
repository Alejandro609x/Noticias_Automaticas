# 📄 README - Noticias de Ciberseguridad y CVEs

## 🔹 Propósito

Estos scripts fueron desarrollados para **mantenerse siempre actualizado en ciberseguridad**, recopilando información relevante de **noticias, CVEs recientes y tweets de expertos en seguridad**.

* `noticiasciber.py`: usa la **API de X (Twitter) con créditos** para obtener publicaciones de cuentas especializadas en ciberseguridad.
* `noticiashacking.py`: obtiene noticias y CVEs **sin depender de X**, ideal para entornos sin créditos o restricciones de API.

El objetivo es generar un **reporte diario en español**, resumido y traducido, que se envía automáticamente por correo electrónico a los responsables de seguridad o áreas de auditoría.

---

## 🔹 Requisitos mínimos

* Python 3.11+
* Sistema con conexión a Internet
* **Correo Gmail habilitado con App Password** de 16 caracteres
* Dependencias de Python:

```bash
pip install feedparser beautifulsoup4 requests lxml googletrans==4.0.0-rc1 tweepy
```

> `tweepy` solo es necesario para `noticiasciber.py` con X.

---

## 🔹 Instalación

1. Clonar o descargar el proyecto:

```bash
git clone https://github.com/usuario/NoticiasCiber.git
cd NoticiasCiber
```

2. Crear un entorno virtual (opcional pero recomendado):

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

> Alternativamente, instalar manualmente con el comando indicado en **Requisitos mínimos**.

---

## 🔹 Configuración

1. **Correo electrónico**:

En ambos scripts, reemplaza:

```python
EMAIL_REMITENTE = "tu_correo@gmail.com"
EMAIL_DESTINO = "destino@empresa.gob.mx"
APP_PASSWORD = "TU_APP_PASSWORD_DE_16_CARACTERES"
```

2. **X API (solo `noticiasciber.py`)**:

* Genera tu app en [X Developer Portal](https://developer.twitter.com/)
* Obtén el **Bearer Token** con créditos disponibles
* Pega tu token en:

```python
BEARER_TOKEN = "TU_BEARER_TOKEN_DE_X"
```

> Asegúrate de no usar la Consumer Key ni Secret Key para este script.

3. **Fuentes de noticias**:

* `noticiashacking.py` permite agregar **RSS o URLs normales**.
* Modifica la lista `FUENTES`:

```python
FUENTES = [
    "https://feeds.feedburner.com/TheHackersNews",
    "https://www.bleepingcomputer.com/feed/",
    "https://www.securityweek.com/rss",
    "https://www.profesionalhacking.com/noticias"
]
```

* El script detecta automáticamente si es RSS o HTML.

---

## 🔹 Uso

### Ejecutar `noticiasciber.py` (con X API)

```bash
python noticiasciber.py
```

* Obtiene noticias de RSS, tweets de cuentas X y CVEs recientes.
* Traduce y resume al español.
* Envía el **reporte diario** al correo configurado.

---

### Ejecutar `noticiashacking.py` (sin X)

```bash
python noticiashacking.py
```

* Obtiene noticias de RSS y páginas normales.
* Incluye los CVEs más recientes.
* Traduce y resume automáticamente.
* Envía el reporte al correo configurado.

---

## 🔹 Personalización

* **Número de artículos por fuente**:

```python
MAX_ARTICULOS = 5
```

* **Número de CVEs**:

```python
max_cves = 5
```

* **Agregar nuevas fuentes RSS o URLs**: solo agregar a `FUENTES`.

---

## 🔹 Características

* Traduce automáticamente contenido al español
* Resume artículos y CVEs para lectura rápida
* Envío automático de correo HTML diario
* Manejo de errores robusto: si falla alguna fuente, el script sigue funcionando
* `noticiasciber.py` usa **API oficial de X**, pero requiere créditos
* `noticiashacking.py` es **100% gratuito**, sin depender de X

---

## 🔹 Sugerencias de uso en el trabajo

* Ejecutar diariamente vía **cron job** o **Tareas programadas**
* Revisar los CVEs críticos y noticias resumidas para **actualización rápida**
* Mantener lista de fuentes actualizada con feeds confiables
* Para X, asegurar que la cuenta tenga **créditos disponibles** para lectura de tweets

---

## 🔹 Contacto / Soporte

Este script fue desarrollado para **uso interno en auditoría y ciberseguridad**.
Para dudas sobre configuración o nuevas fuentes:

* Correo del responsable: `asalazarl@finanzas.cdmx.gob.mx`
* Autor: Alejandro Salazar Luis
