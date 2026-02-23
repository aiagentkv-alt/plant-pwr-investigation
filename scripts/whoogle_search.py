#!/usr/bin/env python3
"""
Script para realizar búsquedas automatizadas en Whoogle.
"""

import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup
import re

WHOOGLE_URL = "http://localhost:8080"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def search_whoogle(query, num_results=10):
    """
    Realiza una búsqueda en Whoogle y extrae resultados.
    
    Args:
        query: Término de búsqueda
        num_results: Número máximo de resultados a extraer
    
    Returns:
        Lista de resultados con título, URL y snippet
    """
    print(f"🔍 Buscando: '{query}'")
    
    # Construir URL de búsqueda
    search_url = f"{WHOOGLE_URL}/search"
    params = {
        'q': query,
        'num': num_results
    }
    
    try:
        response = requests.get(search_url, params=params, headers=HEADERS, timeout=15)
        
        if response.status_code != 200:
            print(f"❌ Error en Whoogle: HTTP {response.status_code}")
            return []
        
        # Parsear HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extraer resultados (Whoogle usa estructura específica)
        results = []
        
        # Buscar contenedores de resultados - Whoogle usa divs con clase ZINbbc
        result_containers = soup.find_all('div', class_='ZINbbc')
        
        for container in result_containers[:num_results * 2]:  # Get more to filter
            # Skip if it's "People also search for" or other non-result sections
            if container.find('details') or container.find('summary'):
                continue
                
            # Skip if it's an image section
            if container.find('span', class_='cAuxJf'):
                continue
            
            result = {}
            
            # Extraer título - Buscar en h3 con clase específica
            title_elem = container.find('h3', class_='zBAuLc')
            if title_elem:
                # Dentro del h3, buscar el div con el texto
                title_div = title_elem.find('div', class_='ilUpNd UFvD1 aSRlid')
                if title_div:
                    result['title'] = title_div.get_text(strip=True)
                else:
                    result['title'] = title_elem.get_text(strip=True)
            
            # Extraer URL - Buscar enlaces externos
            link_elems = container.find_all('a', href=True)
            external_url = None
            
            for link in link_elems:
                href = link['href']
                # Check if it looks like an external URL (contains common domains)
                if any(domain in href for domain in ['plantpwr', 'instagram', 'facebook', 'mercadolibre', 'ispetshope', 'http://', 'https://']):
                    if href.startswith('http') and not href.startswith('http://localhost'):
                        external_url = href
                        break
            
            if external_url:
                result['url'] = external_url
                
                # También extraer dominio para análisis
                from urllib.parse import urlparse
                try:
                    parsed = urlparse(external_url)
                    result['domain'] = parsed.netloc
                except:
                    result['domain'] = 'unknown'
            
            # Extraer snippet/descripción - Buscar divs con clase específica
            snippet_elem = container.find('div', class_='ilUpNd H66NU aSRlid')
            if snippet_elem:
                snippet_text = snippet_elem.get_text(strip=True)
                # Filter out date information
                if '·' in snippet_text:
                    snippet_text = snippet_text.split('·', 1)[-1].strip()
                result['snippet'] = snippet_text[:200]
            
            # Extraer URL mostrada (no el enlace real)
            url_elem = container.find('div', class_='ilUpNd BamJPe aSRlid XR4uSe')
            if url_elem:
                result['display_url'] = url_elem.get_text(strip=True)
            
            # Only add if we have both title and URL
            if result.get('title') and result.get('url'):
                results.append(result)
                
                # Stop if we have enough results
                if len(results) >= num_results:
                    break
        
        print(f"✅ {len(results)} resultados encontrados")
        return results
        
    except Exception as e:
        print(f"❌ Error en búsqueda: {type(e).__name__}: {e}")
        return []

def search_plant_pwr_variations():
    """Busca variaciones de términos relacionados con Plant PWR"""
    search_terms = [
        # Términos principales
        "Plant PWR aceite mascotas",
        "Plant PWR gotas perros",
        "Plant PWR cannabis veterinario",
        "Plant PWR Colombia precio",
        
        # Términos alternativos
        "Zelvatic Pets aceite",
        "Zelvatic Pets cannabis",
        "Zelvatic Pets mascotas",
        
        # Términos genéricos (para detectar nuevos competidores)
        "aceite cannabis perros comprar",
        "cannabis veterinario Colombia",
        "gotas CBD mascotas Medellín",
        
        # Búsquedas específicas por ciudad
        "Plant PWR Medellín",
        "Plant PWR Bogotá",
        "Plant PWR Cali",
        
        # Búsquedas en plataformas específicas
        "site:facebook.com Plant PWR",
        "site:instagram.com Plant PWR",
        "site:mercadolibre.com.co aceite cannabis mascotas"
    ]
    
    all_results = []
    
    for term in search_terms:
        print(f"\n{'='*50}")
        print(f"🔎 TÉRMINO: {term}")
        print(f"{'='*50}")
        
        results = search_whoogle(term, num_results=5)
        
        for result in results:
            result['search_term'] = term
            result['found_at'] = datetime.now().isoformat()
            all_results.append(result)
            
            print(f"   📝 {result.get('title', 'Sin título')[:60]}...")
            print(f"   🔗 {result.get('domain', 'Sin dominio')}")
            if result.get('snippet'):
                print(f"   📋 {result.get('snippet')[:80]}...")
        
        # Pausa entre búsquedas para no sobrecargar
        import time
        time.sleep(2)
    
    return all_results

def save_results(results, filename=None):
    """Guarda los resultados en un archivo JSON"""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"/root/.openclaw/workspace/plant-pwr-investigation/analisis/whoogle_results_{timestamp}.json"
    
    data = {
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'total_results': len(results),
            'whoogle_url': WHOOGLE_URL
        },
        'results': results
    }
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Resultados guardados en: {filename}")
    return filename

def analyze_results(results):
    """Analiza los resultados para extraer información útil"""
    print(f"\n📊 ANÁLISIS DE {len(results)} RESULTADOS")
    print("=" * 50)
    
    # Extraer dominios únicos
    domains = set()
    for result in results:
        if 'domain' in result:
            domains.add(result['domain'])
    
    print(f"🌐 Dominios únicos encontrados: {len(domains)}")
    print("\n📋 TOP 10 DOMINIOS:")
    domain_count = {}
    for result in results:
        domain = result.get('domain')
        if domain:
            domain_count[domain] = domain_count.get(domain, 0) + 1
    
    # Ordenar por frecuencia
    sorted_domains = sorted(domain_count.items(), key=lambda x: x[1], reverse=True)
    
    for domain, count in sorted_domains[:10]:
        print(f"   • {domain}: {count} menciones")
    
    # Buscar nuevos dominios potenciales de Plant PWR
    print(f"\n🔍 BUSCANDO NUEVOS DOMINIOS SOSPECHOSOS:")
    suspicious_keywords = ['plantpwr', 'zelvatic', 'cannabis', 'mascota', 'veterinaria']
    new_domains = []
    
    for domain in domains:
        domain_lower = domain.lower()
        if any(keyword in domain_lower for keyword in suspicious_keywords):
            print(f"   ⚠️  SOSPECHOSO: {domain}")
            new_domains.append(domain)
    
    return {
        'total_domains': len(domains),
        'top_domains': sorted_domains[:10],
        'suspicious_domains': new_domains
    }

def main():
    print("🔍 SISTEMA DE BÚSQUEDA WHOOGLE - PLANT PWR")
    print("=" * 60)
    
    # Probar conexión a Whoogle
    print("🔗 Probando conexión a Whoogle...")
    try:
        response = requests.get(WHOOGLE_URL, timeout=5)
        if response.status_code == 200:
            print("✅ Whoogle conectado correctamente")
        else:
            print(f"⚠️  Whoogle responde con código: {response.status_code}")
    except:
        print("❌ No se puede conectar a Whoogle")
        print("   Verifica que esté corriendo en localhost:8080")
        return
    
    # Realizar búsquedas
    print(f"\n🚀 INICIANDO BÚSQUEDAS AUTOMATIZADAS")
    print(f"{'='*60}")
    
    results = search_plant_pwr_variations()
    
    if results:
        # Guardar resultados
        filename = save_results(results)
        
        # Analizar resultados
        analysis = analyze_results(results)
        
        print(f"\n🎯 RESUMEN FINAL:")
        print(f"   📊 Total resultados: {len(results)}")
        print(f"   🌐 Dominios únicos: {analysis['total_domains']}")
        print(f"   ⚠️  Dominios sospechosos: {len(analysis['suspicious_domains'])}")
        
        if analysis['suspicious_domains']:
            print(f"\n🚨 NUEVOS DOMINIOS PARA INVESTIGAR:")
            for domain in analysis['suspicious_domains']:
                print(f"   • {domain}")
    else:
        print("❌ No se encontraron resultados")

if __name__ == "__main__":
    main()
