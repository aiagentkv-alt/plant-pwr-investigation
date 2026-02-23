#!/usr/bin/env python3
"""
Script de búsqueda diaria automatizada para Plant PWR.
Ejecuta búsquedas en Whoogle y guarda resultados.
"""

import os
import sys
import json
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Configuración
WHOOGLE_URL = "http://localhost:8080"
HEADERS = {'User-Agent': 'Mozilla/5.0'}
LOG_DIR = "/root/.openclaw/workspace/plant-pwr-investigation/monitoreo/logs"
RESULTS_DIR = "/root/.openclaw/workspace/plant-pwr-investigation/evidencia"

def setup_directories():
    """Crear directorios necesarios"""
    os.makedirs(LOG_DIR, exist_ok=True)
    os.makedirs(RESULTS_DIR, exist_ok=True)

def log_message(message):
    """Registrar mensaje en log"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file = os.path.join(LOG_DIR, "whoogle_daily.log")
    
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")
    
    print(f"[{timestamp}] {message}")

def search_whoogle(query, num_results=10):
    """Realizar búsqueda en Whoogle"""
    search_url = f"{WHOOGLE_URL}/search"
    params = {'q': query, 'num': num_results}
    
    try:
        response = requests.get(search_url, params=params, headers=HEADERS, timeout=30)
        
        if response.status_code != 200:
            log_message(f"❌ Error en Whoogle: HTTP {response.status_code} para '{query}'")
            return []
        
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        
        # Buscar contenedores de resultados
        result_containers = soup.find_all('div', class_='ZINbbc')
        
        for container in result_containers[:num_results * 2]:
            # Filtrar secciones no deseadas
            if container.find('details') or container.find('summary'):
                continue
                
            if container.find('span', class_='cAuxJf'):
                continue
            
            # Extraer título
            title_elem = container.find('h3', class_='zBAuLc')
            if not title_elem:
                continue
                
            title_div = title_elem.find('div', class_='ilUpNd UFvD1 aSRlid')
            if title_div:
                title = title_div.get_text(strip=True)
            else:
                title = title_elem.get_text(strip=True)
            
            # Extraer URL
            link_elems = container.find_all('a', href=True)
            external_url = None
            
            for link in link_elems:
                href = link['href']
                if href.startswith('http') and not href.startswith('http://localhost'):
                    external_url = href
                    break
            
            if not external_url:
                continue
            
            # Extraer snippet
            snippet_elem = container.find('div', class_='ilUpNd H66NU aSRlid')
            snippet = ""
            if snippet_elem:
                snippet_text = snippet_elem.get_text(strip=True)
                if '·' in snippet_text:
                    snippet_text = snippet_text.split('·', 1)[-1].strip()
                snippet = snippet_text[:200]
            
            # Extraer dominio
            domain = ""
            try:
                parsed = urlparse(external_url)
                domain = parsed.netloc
            except:
                domain = "unknown"
            
            result = {
                'title': title,
                'url': external_url,
                'domain': domain,
                'snippet': snippet,
                'found_at': datetime.now().isoformat()
            }
            
            results.append(result)
        
        return results
        
    except Exception as e:
        log_message(f"❌ Error en búsqueda '{query}': {type(e).__name__}: {e}")
        return []

def run_daily_search():
    """Ejecutar búsquedas diarias"""
    log_message("🚀 INICIANDO BÚSQUEDA DIARIA AUTOMATIZADA")
    
    # Términos de búsqueda
    search_terms = [
        "Plant PWR Colombia",
        "Plant PWR gotas perros",
        "aceite cannabis mascotas Colombia",
        "zelvatic pets",
        "plantpwr.co",
        "site:instagram.com plant pwr",
        "site:facebook.com plant pwr"
    ]
    
    all_results = []
    
    for query in search_terms:
        log_message(f"🔍 Buscando: '{query}'")
        results = search_whoogle(query, num_results=5)
        
        for result in results:
            result['query'] = query
            all_results.append(result)
        
        log_message(f"   ✅ {len(results)} resultados encontrados")
        
        # Pausa entre búsquedas
        import time
        time.sleep(2)
    
    # Guardar resultados
    if all_results:
        date_str = datetime.now().strftime("%Y%m%d")
        output_file = os.path.join(RESULTS_DIR, f"whoogle_daily_{date_str}.json")
        
        data = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'total_results': len(all_results),
                'search_terms': search_terms,
                'whoogle_url': WHOOGLE_URL
            },
            'results': all_results
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        log_message(f"💾 Resultados guardados en: {output_file}")
        
        # Generar resumen
        generate_summary(all_results, date_str)
    else:
        log_message("⚠️ No se encontraron resultados")
    
    log_message("✅ BÚSQUEDA DIARIA COMPLETADA")

def generate_summary(results, date_str):
    """Generar resumen de resultados"""
    summary_file = os.path.join(LOG_DIR, f"summary_{date_str}.txt")
    
    # Contar por dominio
    domains = {}
    for result in results:
        domain = result['domain']
        if domain not in domains:
            domains[domain] = 0
        domains[domain] += 1
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(f"📊 RESUMEN DE BÚSQUEDA DIARIA - {date_str}\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Total resultados: {len(results)}\n")
        f.write(f"Dominios únicos: {len(domains)}\n\n")
        
        f.write("📈 TOP 10 DOMINIOS:\n")
        for domain, count in sorted(domains.items(), key=lambda x: x[1], reverse=True)[:10]:
            f.write(f"  • {domain}: {count} resultados\n")
        
        f.write("\n🔍 NUEVOS HALLAZGOS POTENCIALES:\n")
        # Aquí se podría agregar lógica para detectar nuevos dominios
        f.write("  (Comparar con base de datos existente)\n")
    
    log_message(f"📋 Resumen generado: {summary_file}")

def main():
    """Función principal"""
    setup_directories()
    log_message("=" * 60)
    log_message("🔎 SISTEMA DE BÚSQUEDA DIARIA - PLANT PWR")
    log_message("=" * 60)
    
    try:
        run_daily_search()
    except Exception as e:
        log_message(f"❌ ERROR CRÍTICO: {type(e).__name__}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
