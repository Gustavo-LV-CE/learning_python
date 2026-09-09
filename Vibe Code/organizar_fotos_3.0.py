"""
organizar_fotos.py

Organiza fotografias en carpetas por fecha de captura (segun EXIF),
renombra cada foto con su orden de captura del dia, y genera un
archivo coords.txt con las coordenadas GPS de cada foto.

Uso:
    Coloca este script dentro de la carpeta que contiene todas las fotos
    y corre:
        python organizar_fotos.py

Requiere:
    pip install pillow
    (opcional, para soporte de archivos .heic/.heif)
    pip install pillow-heif
"""

import os
import shutil
from datetime import datetime
from pathlib import Path

from PIL import Image, ExifTags

# Intenta habilitar soporte HEIC/HEIF si la libreria esta disponible
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
    HEIC_SUPPORTED = True
except ImportError:
    HEIC_SUPPORTED = False

SUPPORTED_EXT = {".jpg", ".jpeg", ".png", ".tif", ".tiff"}
if HEIC_SUPPORTED:
    SUPPORTED_EXT |= {".heic", ".heif"}

MESES = {
    1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
    5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
    9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre",
}

# Mapea nombres de tags EXIF a sus IDs, para busqueda legible
TAGS_INV = {v: k for k, v in ExifTags.TAGS.items()}
GPS_TAGS_INV = {v: k for k, v in ExifTags.GPSTAGS.items()}


def obtener_exif(ruta):
    """Devuelve el diccionario EXIF de una imagen, o {} si no tiene."""
    try:
        with Image.open(ruta) as img:
            exif_raw = img.getexif()
            if not exif_raw:
                return {}
            exif = {ExifTags.TAGS.get(k, k): v for k, v in exif_raw.items()}
            # DateTimeOriginal vive en el sub-IFD "Exif" (0x8769)
            exif_ifd = exif_raw.get_ifd(0x8769)
            if exif_ifd:
                exif.update(
                    {ExifTags.TAGS.get(k, k): v for k, v in exif_ifd.items()}
                )
            # Datos GPS estan en un IFD aparte
            gps_ifd = exif_raw.get_ifd(0x8825)  # 0x8825 = GPSInfo
            if gps_ifd:
                exif["GPSInfo"] = {
                    ExifTags.GPSTAGS.get(k, k): v for k, v in gps_ifd.items()
                }
            return exif
    except Exception:
        return {}


def obtener_fecha_captura(exif):
    """Extrae datetime de captura desde EXIF, o None si no existe."""
    valor = exif.get("DateTimeOriginal") or exif.get("DateTime")
    if not valor:
        return None
    try:
        return datetime.strptime(valor, "%Y:%m:%d %H:%M:%S")
    except (ValueError, TypeError):
        return None


def _dms_a_decimal(dms, ref):
    """Convierte coordenadas GPS de grados/minutos/segundos a decimal."""
    try:
        grados, minutos, segundos = [float(x) for x in dms]
    except (TypeError, ValueError):
        return None
    decimal = grados + minutos / 60.0 + segundos / 3600.0
    if ref in ("S", "W"):
        decimal = -decimal
    return decimal


def obtener_coordenadas(exif):
    """Devuelve (lat, lon) en decimal, o None si no hay datos GPS."""
    gps = exif.get("GPSInfo")
    if not gps:
        return None
    lat = gps.get("GPSLatitude")
    lat_ref = gps.get("GPSLatitudeRef")
    lon = gps.get("GPSLongitude")
    lon_ref = gps.get("GPSLongitudeRef")
    if not (lat and lat_ref and lon and lon_ref):
        return None
    lat_dec = _dms_a_decimal(lat, lat_ref)
    lon_dec = _dms_a_decimal(lon, lon_ref)
    if lat_dec is None or lon_dec is None:
        return None
    return round(lat_dec, 6), round(lon_dec, 6)


def nombre_carpeta_fecha(dt):
    return f"{dt.day} de {MESES[dt.month]} {dt.year}"


def nombre_disponible(carpeta, nombre_base, ext):
    """Evita sobrescribir si el archivo destino ya existe."""
    candidato = carpeta / f"{nombre_base}{ext}"
    contador = 1
    while candidato.exists():
        candidato = carpeta / f"{nombre_base}_{contador}{ext}"
        contador += 1
    return candidato


def main():
    carpeta_actual = Path.cwd()
    script_nombre = Path(__file__).name

    con_fecha = []   # (ruta, datetime, coords)
    sin_fecha = []    # (ruta, coords)

    archivos = [
        f for f in carpeta_actual.iterdir()
        if f.is_file()
        and f.suffix.lower() in SUPPORTED_EXT
        and f.name != script_nombre
    ]

    if not archivos:
        print("No se encontraron fotos compatibles en esta carpeta.")
        return

    print(f"Analizando {len(archivos)} foto(s)...")

    for ruta in archivos:
        exif = obtener_exif(ruta)
        fecha = obtener_fecha_captura(exif)
        coords = obtener_coordenadas(exif)
        if fecha:
            con_fecha.append((ruta, fecha, coords))
        else:
            sin_fecha.append((ruta, coords))

    # Agrupar por fecha (solo dia, sin hora)
    grupos = {}
    for ruta, fecha, coords in con_fecha:
        clave = fecha.date()
        grupos.setdefault(clave, []).append((ruta, fecha, coords))

    # Acumula bloques para el archivo de resumen en la raiz
    bloques_resumen = []  # (fecha_date, nombre_fecha, [lineas])

    # Procesar cada grupo de fecha (ordenados cronologicamente)
    for clave in sorted(grupos.keys()):
        fotos = grupos[clave]
        fotos.sort(key=lambda x: x[1])  # ordenar por hora exacta
        nombre_fecha = nombre_carpeta_fecha(fotos[0][1])
        carpeta_fecha = carpeta_actual / nombre_fecha
        carpeta_fecha.mkdir(exist_ok=True)

        lineas_coords = []
        for idx, (ruta, fecha, coords) in enumerate(fotos, start=1):
            ext = ruta.suffix.lower()
            destino = nombre_disponible(carpeta_fecha, str(idx), ext)
            shutil.move(str(ruta), str(destino))
            if coords:
                lat, lon = coords
                lineas_coords.append(f"{idx} - {lat}, {lon}")
            else:
                lineas_coords.append(f"{idx} - sin GPS")

        nombre_txt = f"coords {nombre_fecha}.txt"
        with open(carpeta_fecha / nombre_txt, "w", encoding="utf-8") as f:
            f.write("\n".join(lineas_coords) + "\n")

        bloques_resumen.append((clave, nombre_fecha, lineas_coords))
        print(f"  {carpeta_fecha.name}: {len(fotos)} foto(s) organizadas.")

    # Procesar fotos sin fecha
    if sin_fecha:
        carpeta_sf = carpeta_actual / "Sin fecha"
        carpeta_sf.mkdir(exist_ok=True)
        lineas_coords = []
        for ruta, coords in sin_fecha:
            destino = nombre_disponible(carpeta_sf, ruta.stem, ruta.suffix.lower())
            shutil.move(str(ruta), str(destino))
            if coords:
                lat, lon = coords
                lineas_coords.append(f"{destino.name} - {lat}, {lon}")
            else:
                lineas_coords.append(f"{destino.name} - sin GPS")

        with open(carpeta_sf / "coords sin fecha.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(lineas_coords) + "\n")

        bloques_resumen.append((None, "Sin fecha", lineas_coords))
        print(f"  Sin fecha: {len(sin_fecha)} foto(s) movidas.")

    # Escribir archivo de resumen en la raiz
    if bloques_resumen:
        partes = []
        for _, nombre_fecha, lineas in bloques_resumen:
            partes.append(nombre_fecha + "\n" + "\n".join(lineas))
        with open(carpeta_actual / "Resumen de coords.txt", "w", encoding="utf-8") as f:
            f.write("\n\n".join(partes) + "\n")
        print("  Resumen de coords.txt creado.")

    print("\nListo.")


if __name__ == "__main__":
    main()
