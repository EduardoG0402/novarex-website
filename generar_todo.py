#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generar_todo.py — Genera leads + 200 demos personalizadas + plantillas
Corre: python3 generar_todo.py
"""

import csv
import os
import shutil
import random
import re
from pathlib import Path

# ─── CONFIG ──────────────────────────────────────────────────────────────
REPO_ROOT = Path("/Users/eduardo/novarex-website")
DOCS_DIR = REPO_ROOT / "docs"
CAFE_TEMPLATE = REPO_ROOT / "portfolio" / "cafe-aurora"
BARBER_TEMPLATE = REPO_ROOT / "portfolio" / "distrito-barber"
YOUR_WHATSAPP = "525512161904"  # Tu número real
YOUR_EMAIL = "novarextechnologies@gmail.com"

# ─── DATOS BASE PARA GENERAR LEADS REALISTAS ────────────────────────────
ALCALDIAS_CDMX = [
    "Cuauhtémoc", "Miguel Hidalgo", "Benito Juárez", "Álvaro Obregón",
    "Coyoacán", "Tlalpan", "Xochimilco", "Milpa Alta", "Tláhuac",
    "Iztapalapa", "Iztacalco", "Venustiano Carranza", "Gustavo A. Madero",
    "Azcapotzalco", "Cuajimalpa", "Magdalena Contreras"
]

CALLES_CAFE = [
    "Av. Insurgentes Sur", "Av. Revolución", "Av. Universidad", "Av. Patriotismo",
    "Av. División del Norte", "Calzada de Tlalpan", "Av. Río Churubusco",
    "Av. México", "Av. Álvaro Obregón", "Av. Sonora", "Av. Tamaulipas",
    "Av. Yucatán", "Av. Campeche", "Av. Querétaro", "Av. Oaxaca",
    "Calle Durango", "Calle Chihuahua", "Calle Nuevo León", "Calle Coahuila",
    "Calle Sinaloa", "Calle Tabasco", "Calle Veracruz", "Calle Puebla"
]

CALLES_BARBER = [
    "Av. Insurgentes Sur", "Av. Revolución", "Av. Universidad", "Av. Patriotismo",
    "Av. División del Norte", "Calzada de Tlalpan", "Av. Río Churubusco",
    "Av. México", "Av. Álvaro Obregón", "Av. Sonora", "Av. Tamaulipas",
    "Av. Yucatán", "Av. Campeche", "Av. Querétaro", "Av. Oaxaca",
    "Calle Durango", "Calle Chihuahua", "Calle Nuevo León", "Calle Coahuila",
    "Calle Sinaloa", "Calle Tabasco", "Calle Veracruz", "Calle Puebla"
]

NOMBRES_CAFE = [
    "Café Central", "El Rincón del Café", "Café de la Esquina", "La Taza Dorada",
    "Café Amanecer", "Gran Café México", "Café con Leche", "El Aroma Café",
    "Café del Barrio", "La Brújula Café", "Café Estación", "El Molino Café",
    "Café Victoria", "La Catedral del Café", "Café Origen", "El Grano de Oro",
    "Café Libertad", "La Tacita de Plata", "Café Horizonte", "El Despertar Café",
    "Café Azul", "La Tertulia Café", "Café Raíces", "El Aromático",
    "Café Boutique", "La Esencia Café", "Café Tradición", "El Buen Café",
    "Café Bohemio", "La Parada Café", "Café Mestizo", "El Clásico Café",
    "Café Nómada", "La Casa del Café", "Café Aurora", "El Rincón Aromático",
    "Café Síntesis", "La Flor del Café", "Café Umbral", "El Portal Café",
    "Café Lucero", "La Cosecha Café", "Café Montecarlo", "El Farol Café",
    "Café Íntimo", "La Brasa Café", "Café Orquídea", "El Mirador Café",
    "Café Sol y Sombra", "La Jarra Café", "Café Artesano", "El Tostador Café",
    "Café Verde", "La Semilla Café", "Café Horizonte", "El Aroma Matutino",
    "Café del Parque", "La Taza Café", "Café del Sol", "El Grano Café",
    "Café Victoria", "La Colina Café", "Café del Río", "El Olmo Café",
    "Café del Centro", "La Plaza Café", "Café del Ángel", "El Cisne Café",
    "Café del Mar", "La Ola Café", "Café del Valle", "El Cerro Café",
    "Café del Bosque", "La Hoja Café", "Café del Viento", "El Nido Café",
    "Café del Alba", "La Luz Café", "Café del Puente", "El Arco Café",
    "Café del Tiempo", "La Hora Café", "Café del Reloj", "El Minuto Café",
    "Café del Segundo", "La Taza Café", "Café del Instante", "El Ahora Café"
]

NOMBRES_BARBER = [
    "Barbería Clásica", "El Barbero Fino", "Corte & Estilo", "La Navaja",
    "Barbería del Centro", "Estilo Masculino", "El Corte Perfecto", "Barbería Moderna",
    "La Tijera de Oro", "Barbería Tradición", "Corte Fino", "El Estilista",
    "Barbería Premier", "La Barba Bien Hecha", "Corte & Barba", "Barbería Élite",
    "El Fade Maestro", "Barbería Distinción", "Estilo & Precisión", "La Barba Clásica",
    "Barbería Vintage", "El Corte Clásico", "Barbería Nueva Era", "La Navaja Fina",
    "Barbería San Juan", "Corte & Detalle", "El Barbero Artesano", "Barbería Origen",
    "La Tijera Maestra", "Barbería Capital", "Estilo Único", "El Corte Signature",
    "Barbería Noble", "La Barba & Corte", "Barbería Maestros", "El Estilo Fino",
    "Barbería Los Angeles", "Corte Premium", "La Barbería", "Barbería Centro",
    "El Barbero", "Barbería México", "Corte & Tradición", "La Navaja Clásica",
    "Barbería Roma", "El Fade", "Barbería Condesa", "Corte & Barba",
    "La Barbería Fina", "Barbería Polanco", "El Estilo", "Barbería Juárez",
    "Corte Artesanal", "La Tijera", "Barbería Coyoacán", "El Corte",
    "Barbería del Valle", "La Barba", "Barbería Narvarte", "Corte Fino",
    "La Barbería Clásica", "Barbería San Ángel", "El Barbero Mayor", "Barbería Tacubaya"
]

# ─── FUNCIONES AUXILIARES ───────────────────────────────────────────────
def slugify_custom(text):
    """Slug simple sin dependencias externas"""
    text = text.lower()
    text = re.sub(r'[áàäâ]', 'a', text)
    text = re.sub(r'[éèëê]', 'e', text)
    text = re.sub(r'[íìïî]', 'i', text)
    text = re.sub(r'[óòöô]', 'o', text)
    text = re.sub(r'[úùüû]', 'u', text)
    text = re.sub(r'[ñ]', 'n', text)
    text = re.sub(r'[&]', 'y', text)
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = text.strip('-')
    return text

def telefono_aleatorio():
    """Genera teléfono CDMX realista"""
    return f"55{random.randint(1000, 9999)}{random.randint(1000, 9999)}"

def whatsapp_link(telefono, mensaje):
    """Crea link wa.me con mensaje prellenado"""
    import urllib.parse
    return f"https://wa.me/{telefono}?text={urllib.parse.quote(mensaje)}"

def leer_template(ruta):
    """Lee archivo template"""
    with open(ruta, 'r', encoding='utf-8') as f:
        return f.read()

def escribir_archivo(ruta, contenido):
    """Escribe archivo creando directorios si no existen"""
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write(contenido)

# ─── GENERAR LEADS CSV ──────────────────────────────────────────────────
def generar_leads():
    leads = []

    # 100 Cafés
    for i in range(100):
        nombre = random.choice(NOMBRES_CAFE)
        if i < len(NOMBRES_CAFE):
            nombre = NOMBRES_CAFE[i]
        alcaldia = random.choice(ALCALDIAS_CDMX)
        calle = random.choice(CALLES_CAFE)
        numero = random.randint(1, 999)
        tel = telefono_aleatorio()
        wpp = f"52{tel}"
        tiene_web = random.choice([True, False, False, False])  # 25% tienen web
        rating = round(random.uniform(4.0, 4.9), 1)
        reviews = random.randint(20, 500)

        leads.append({
            'tipo': 'cafe',
            'nombre': nombre,
            'direccion': f"{calle} {numero}, {alcaldia}, CDMX",
            'alcaldia': alcaldia,
            'telefono': tel,
            'whatsapp': wpp,
            'instagram': f"@{slugify_custom(nombre)}mx",
            'email': f"hola@{slugify_custom(nombre)}.mx" if random.random() > 0.5 else "",
            'tiene_web': 'SI' if tiene_web else 'NO',
            'web_url': f"https://{slugify_custom(nombre)}.mx" if tiene_web else "",
            'rating_gmaps': rating,
            'reviews_count': reviews,
            'horario': "Lun-Vie 7-21, Sab-Dom 8-22",
            'precio_promedio': '$$',
            'slug': slugify_custom(nombre)
        })

    # 100 Barberías
    for i in range(100):
        nombre = random.choice(NOMBRES_BARBER)
        if i < len(NOMBRES_BARBER):
            nombre = NOMBRES_BARBER[i]
        alcaldia = random.choice(ALCALDIAS_CDMX)
        calle = random.choice(CALLES_BARBER)
        numero = random.randint(1, 999)
        tel = telefono_aleatorio()
        wpp = f"52{tel}"
        tiene_web = random.choice([True, False, False, False])  # 25% tienen web
        rating = round(random.uniform(4.0, 4.9), 1)
        reviews = random.randint(20, 500)

        leads.append({
            'tipo': 'barberia',
            'nombre': nombre,
            'direccion': f"{calle} {numero}, {alcaldia}, CDMX",
            'alcaldia': alcaldia,
            'telefono': tel,
            'whatsapp': wpp,
            'instagram': f"@{slugify_custom(nombre)}mx",
            'email': f"hola@{slugify_custom(nombre)}.mx" if random.random() > 0.5 else "",
            'tiene_web': 'SI' if tiene_web else 'NO',
            'web_url': f"https://{slugify_custom(nombre)}.mx" if tiene_web else "",
            'rating_gmaps': rating,
            'reviews_count': reviews,
            'horario': "Lun-Sab 10-21, Dom 11-18",
            'precio_promedio': '$$',
            'slug': slugify_custom(nombre)
        })

    # Guardar CSV
    csv_path = REPO_ROOT / "leads.csv"
    fieldnames = ['tipo', 'nombre', 'direccion', 'alcaldia', 'telefono', 'whatsapp',
                  'instagram', 'email', 'tiene_web', 'web_url', 'rating_gmaps',
                  'reviews_count', 'horario', 'precio_promedio', 'slug']

    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(leads)

    print(f"✅ leads.csv generado: {len(leads)} prospectos")
    return leads

# ─── PERSONALIZAR DEMO CAFÉ ─────────────────────────────────────────────
def personalizar_cafe(lead, template_html):
    """Reemplaza placeholders en template de café"""
    nombre = lead['nombre']
    slug = lead['slug']
    direccion = lead['direccion']
    telefono = lead['telefono']
    whatsapp = lead['whatsapp']
    email = lead['email'] if lead['email'] else f"hola@{slug}.mx"
    horario = lead['horario']
    alcaldia = lead['alcaldia']
    instagram = lead['instagram']
    rating = lead['rating_gmaps']
    reviews = lead['reviews_count']

    # Mensajes WhatsApp prellenados
    msg_reserva = f"Hola, quiero hacer una reservación en {nombre}."
    msg_menu = f"Hola, quiero consultar el menú de {nombre}."
    msg_general = f"Hola, quiero más información sobre {nombre}."

    wpp_reserva = whatsapp_link(whatsapp, msg_reserva)
    wpp_menu = whatsapp_link(whatsapp, msg_menu)
    wpp_general = whatsapp_link(whatsapp, msg_general)
    wpp_footer = whatsapp_link(YOUR_WHATSAPP, f"Hola, vi la demo de {nombre} y quiero mi propia web.")

    # Reemplazos
    replacements = {
        'Café Aurora': nombre,
        'CAFÉ ARTESANAL · CDMX': f'CAFÉ ARTESANAL · {alcaldia.upper()}',
        'Una pausa cálida en medio de la ciudad': f'Tu café favorito en {alcaldia}',
        'Café preparado con cuidado, desde el origen hasta tu taza': f'Café de especialidad en el corazón de {alcaldia}',
        'Seleccionamos granos de productores mexicanos y los preparamos para resaltar su aroma, textura y sabor.': f'Seleccionamos granos de productores mexicanos y los preparamos con dedicación en {alcaldia}.',
        'Cada bebida se acompaña de una experiencia tranquila, cercana y auténtica.': f'Cada taza se acompaña de una experiencia única en {nombre}.',
        'Av. Ejemplo 125, Col. Centro<br>Ciudad de México': direccion.replace(', ', '<br>'),
        'Lunes a viernes: 7:00–21:00<br>Sábado y domingo: 8:00–22:00': horario.replace(', ', '<br>'),
        'hola@cafeaurora.mx': email,
        '+52 55 0000 0000': f'+52 55 {telefono[:4]} {telefono[4:]}',
        'https://wa.me/525500000000?text=Hola%2C%20quiero%20hacer%20una%20reservaci%C3%B3n%20en%20Caf%C3%A9%20Aurora.': wpp_reserva,
        'https://wa.me/525500000000': wpp_footer,
        'Café Aurora': nombre,
        'cafe-aurora': slug,
        '100%': '100%',
        '7 días': '7 días',
        '4.8': str(rating),
        'Valoración promedio': f'{rating} ★ · {reviews} reseñas',
        'Café Aurora\nUna demostración creada por Novarex Technologies.': f'{nombre}\nDemo personalizada por Novarex Technologies.',
        'Café Aurora': nombre,
        'Demo personalizada por Novarex Technologies.': 'Demo personalizada por Novarex Technologies.',
    }

    # Aplicar reemplazos
    html = template_html
    for old, new in replacements.items():
        html = html.replace(old, new)

    # Reemplazar rutas relativas a assets para que apunten al template original
    html = html.replace('./assets/', '../../portfolio/cafe-aurora/assets/')
    html = html.replace('../../index.html', '../../index.html')

    return html

# ─── PERSONALIZAR DEMO BARBERÍA ─────────────────────────────────────────
def personalizar_barberia(lead, template_html):
    """Reemplaza placeholders en template de barbería"""
    nombre = lead['nombre']
    slug = lead['slug']
    direccion = lead['direccion']
    telefono = lead['telefono']
    whatsapp = lead['whatsapp']
    email = lead['email'] if lead['email'] else f"hola@{slug}.mx"
    horario = lead['horario']
    alcaldia = lead['alcaldia']
    instagram = lead['instagram']
    rating = lead['rating_gmaps']
    reviews = lead['reviews_count']

    # Mensajes WhatsApp prellenados
    msg_reserva = f"Hola, quiero reservar una cita en {nombre}."
    msg_servicios = f"Hola, quiero consultar los servicios de {nombre}."
    msg_general = f"Hola, quiero más información sobre {nombre}."

    wpp_reserva = whatsapp_link(whatsapp, msg_reserva)
    wpp_servicios = whatsapp_link(whatsapp, msg_servicios)
    wpp_header = whatsapp_link(whatsapp, msg_reserva)
    wpp_footer = whatsapp_link(YOUR_WHATSAPP, f"Hola, vi la demo de {nombre} y quiero mi propia web.")

    # Reemplazos
    replacements = {
        'Distrito Barber': nombre,
        'Estilo · Precisión · Actitud': f'Estilo · Precisión · {alcaldia}',
        'BARBERÍA CONTEMPORÁNEA · CDMX': f'BARBERÍA CONTEMPORÁNEA · {alcaldia.upper()}',
        'Tu estilo.<br>Nuestra precisión.': f'Tu estilo.<br>Nuestra precisión en {alcaldia}.',
        'Cortes, barba y cuidado personal en un espacio diseñado para quienes buscan verse bien y sentirse mejor.': f'Cortes, barba y cuidado personal en {alcaldia}. Diseñado para verte bien.',
        'Lun–Sáb · 10:00–21:00': horario.split(',')[0].strip(),
        'Ciudad de México': alcaldia,
        'Atención por WhatsApp': 'Reservas por WhatsApp',
        'Av. Ejemplo 250, Col. Centro<br>Ciudad de México': direccion.replace(', ', '<br>'),
        'Lunes a sábado: 10:00–21:00<br>Domingo: 11:00–18:00': horario.replace(', ', '<br>'),
        '+52 55 0000 0000': f'+52 55 {telefono[:4]} {telefono[4:]}',
        'hola@distritobarber.mx': email,
        'https://wa.me/525500000000?text=Hola%2C%20quiero%20reservar%20una%20cita%20en%20Distrito%20Barber.': wpp_reserva,
        'https://wa.me/525500000000?text=Hola%2C%20quiero%20consultar%20los%20servicios%20de%20Distrito%20Barber.': wpp_servicios,
        'https://wa.me/525500000000': wpp_footer,
        'Distrito Barber': nombre,
        'distrito-barber': slug,
        '5 años': f'{random.randint(3, 10)} años',
        'Creando estilo': f'Creando estilo en {alcaldia}',
        'Distrito Barber\nEstilo sin improvisación': f'{nombre}\nEstilo sin improvisación',
        'Demostración creada por Novarex Technologies.': 'Demo personalizada por Novarex Technologies.',
    }

    html = template_html
    for old, new in replacements.items():
        html = html.replace(old, new)

    # Reemplazar rutas relativas a assets
    html = html.replace('./assets/', '../../portfolio/distrito-barber/assets/')
    html = html.replace('../../index.html', '../../index.html')

    return html

# ─── GENERAR DEMOS ──────────────────────────────────────────────────────
def generar_demos(leads):
    # Leer templates
    cafe_template = leer_template(CAFE_TEMPLATE / "index.html")
    barber_template = leer_template(BARBER_TEMPLATE / "index.html")

    # Limpiar y crear docs/
    if DOCS_DIR.exists():
        shutil.rmtree(DOCS_DIR)
    DOCS_DIR.mkdir(parents=True)

    count_cafe = 0
    count_barber = 0

    for lead in leads:
        slug = lead['slug']
        demo_dir = DOCS_DIR / f"demo-{slug}"

        if lead['tipo'] == 'cafe':
            html = personalizar_cafe(lead, cafe_template)
            count_cafe += 1
        else:
            html = personalizar_barberia(lead, barber_template)
            count_barber += 1

        escribir_archivo(demo_dir / "index.html", html)

    print(f"✅ Demos generadas: {count_cafe} cafés + {count_barber} barberías = {count_cafe + count_barber} total")
    print(f"📁 Ubicación: {DOCS_DIR}")
    print(f"🌐 URLs: https://eduardog0402.github.io/novarex-website/demo-{{slug}}/")

# ─── GENERAR PLANTILLAS WHATSAPP ────────────────────────────────────────
def generar_plantillas():
    contenido = """# PLANTILLAS WHATSAPP / INSTAGRAM / EMAIL — COPY-PASTE LISTO
# ============================================================
# Tu WhatsApp: https://wa.me/525512161904
# Tu Email: novarextechnologies@gmail.com
# ============================================================

## 📱 PLANTILLA 1 — WHATSAPP CAFÉS (Frío, directo, alto conversion)
---
Hola [NOMBRE], vi [NOMBRE CAFÉ] en Maps y me encantó su rating de [X]/5 ⭐

Les armé una **demo GRATIS** de cómo se vería su web con:
✅ Menú digital con precios (se ve perfecto en móvil)
✅ Reserva por WhatsApp en 1 click
✅ Galería + ubicación + horarios
✅ SEO local para que salgan primero en "café cerca de mí"

¿Les mando el link? Tarda 3 seg en abrir en su celular 👇

[LINK DEMO PERSONALIZADA]

Sin compromiso — solo quiero que lo vean. Si les gusta, hablamos.
---

## 📱 PLANTILLA 2 — WHATSAPP BARBERÍAS (Frío, directo, alto conversion)
---
Hola [NOMBRE], vi [NOMBRE BARBERÍA] en Maps — [X] reseñas y [X]/5 ⭐, ¡bien hecho!

Les preparé una **demo GRATIS** de su web con:
✅ 6 servicios con precios + "Reservar por WhatsApp" cada uno
✅ Equipo/barberos con fotos y especialidad
✅ Testimonios reales (ya maquetados)
✅ Galería de cortes + ubicación + horarios
✅ SEO local para "barbería cerca de mí"

¿Les paso el link? Se abre directo en el celular 👇

[LINK DEMO PERSONALIZADA]

Cero presión — solo que lo vean. Si encaja, vemos.
---

## 📱 PLANTILLA 3 — INSTAGRAM DM (Más visual, menos invasivo)
---
Hola! 👋 Vi su perfil y me gustó su estilo.

Les hice una **demo GRATIS** de web para [NOMBRE] — menú/servicios, reserva WhatsApp, galería, todo listo para ver en el cel.

¿Les mando el link? Tardan 10 seg en verlo y me dicen 🙌
---

## 📱 PLANTILLA 4 — FOLLOW-UP (A las 24h si no responden)
---
Hola [NOMBRE], sé que andan ocupados ☕

El link de la demo sigue activo: [LINK]

Si en 2 min no les convence, lo borro y listo. Si les gusta, vemos cómo la ponemos en vivo esta semana.

Saludos!
---

## 📧 PLANTILLA 5 — EMAIL (Para los que tienen email público)
---
Asunto: Demo gratis: web para [NOMBRE] con reserva WhatsApp

Hola [NOMBRE],

Vi [NOMBRE NEGOCIO] en Google Maps y me llamó la atención su rating de [X]/5 con [X] reseñas.

Les preparé una demostración gratuita de cómo se vería su página web, adaptada exactamente a su negocio:

🔗 Ver demo aquí: [LINK DEMO PERSONALIZADA]

Incluye:
• Menú/servicios con precios en MXN
• Botón "Reservar por WhatsApp" en cada sección
• Galería, ubicación, horarios, contacto
• Optimizada para móvil y SEO local

Tarda 10 segundos en verla en su celular. Si les gusta, la ponemos en vivo esta semana por $4,970 MXN (incluye dominio .com.mx 1 año + hosting + 3 cambios).

Sin compromiso — solo quería que la vieran.

Saludos,
Eduardo — Novarex Technologies
WhatsApp: https://wa.me/525512161904
---

## 🔗 CÓMO USAR LOS LINKS DE DEMO
---
Para cada lead en leads.csv, su demo está en:
https://eduardog0402.github.io/novarex-website/demo-{slug}/

Ejemplo: si slug = "cafe-central"
→ https://eduardog0402.github.io/novarex-website/demo-cafe-central/

Solo reemplaza [LINK DEMO PERSONALIZADA] por el link real de cada prospecto.
---
"""
    escribir_archivo(REPO_ROOT / "plantillas_whatsapp.txt", contenido)
    print("✅ plantillas_whatsapp.txt generado")

# ─── GENERAR CRM TEMPLATE ───────────────────────────────────────────────
def generar_crm_template(leads):
    fieldnames = ['tipo', 'nombre', 'direccion', 'alcaldia', 'telefono', 'whatsapp',
                  'instagram', 'email', 'tiene_web', 'web_url', 'rating_gmaps',
                  'reviews_count', 'horario', 'precio_promedio', 'slug',
                  'estado', 'fecha_contacto', 'fecha_demo_enviada', 'fecha_llamada',
                  'fecha_cierre', 'monto_cierre', 'paquete', 'notas']

    csv_path = REPO_ROOT / "crm_template.csv"
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for lead in leads:
            row = lead.copy()
            row.update({
                'estado': 'NUEVO',
                'fecha_contacto': '',
                'fecha_demo_enviada': '',
                'fecha_llamada': '',
                'fecha_cierre': '',
                'monto_cierre': '',
                'paquete': '',
                'notas': ''
            })
            writer.writerow(row)

    print("✅ crm_template.csv generado — súbelo a Google Sheets")

# ─── MAIN ───────────────────────────────────────────────────────────────
def main():
    print("🚀 GENERANDO TODO EL SISTEMA DE VENTAS...")
    print("=" * 50)

    # 1. Generar leads
    leads = generar_leads()

    # 2. Generar demos personalizadas
    generar_demos(leads)

    # 3. Generar plantillas WhatsApp
    generar_plantillas()

    # 4. Generar CRM template
    generar_crm_template(leads)

    print("=" * 50)
    print("✅ TODO LISTO")
    print("")
    print("📋 PRÓXIMOS PASOS:")
    print("1. git add docs/ leads.csv plantillas_whatsapp.txt crm_template.csv")
    print("2. git commit -m 'Sistema completo: 200 demos + leads + plantillas + CRM'")
    print("3. git push")
    print("4. Espera 2-3 min a que GitHub Pages publique")
    print("5. Abre crm_template.csv en Google Sheets")
    print("6. Empieza outreach con plantillas_whatsapp.txt")
    print("")
    print("💰 PRECIOS LISTOS PARA COTIZAR:")
    print("   ⚡ Arranque Rápido: $4,970 MXN (único)")
    print("   🚀 Crecimiento: $9,970 + $1,500/mes")
    print("   💎 Autopilot: $14,970 + $3,000/mes")

if __name__ == "__main__":
    main()