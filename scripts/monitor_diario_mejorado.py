#!/usr/bin/env python3
"""
Script de monitoreo mejorado para Plant PWR.
"""

import json
import os
import requests
from datetime import datetime
from urllib.parse import urlparse

# Configuración mejorada
DOMAINS_FILE = "/root/.openclaw/workspace/plant-pwr-investigation/dominios/critical_domains.json"
LOG_FILE = "/root/.openclaw/workspace/plant-pwr-investigation/monitoreo/daily_log.json"

# Headers mejorados para evitar bloqueos
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Cache-Control': 'max-age=0'
}

def load_critical_domains():
    """Carga la lista de dominios críticos"""
    if os.path.exists(DOMAINS_FILE):
        with open(DOMAINS_FILE, 'r') as f:
            return json.load(f)
    return {"critical": [], "high_priority": []}

def check_domain_improved(domain_info):
    """Verifica el estado de un dominio con múltiples intentos"""
    domain = domain_info.get('domain')
    url = domain_info.get('url', f"https://{domain}")
    
    # Intentar múltiples métodos
    test_urls = []
    
    # Si tenemos URL específica, usarla
    if 'url' in domain_info and domain_info['url']:
        test_urls.append(domain_info['url'])
    
    # Intentar con HTTPS
    test_urls.append(f"https://{domain}")
    
    # Intentar con HTTP si HTTPS falla
    test_urls.append(f"http://{domain}")
    
    # Intentar con www
    test_urls.append(f"https://www.{domain}")
    
    for test_url in test_urls:
        try:
            response = requests.get(
                test_url,
                headers=HEADERS,
                timeout=15,
                allow_redirects=True,
                verify=False  # Desactivar verificación SSL temporalmente
            )
            
            if response.status_code < 400:
                return {
                    'domain': domain,
                    'status': 'ACTIVE',
                    'status_code': response.status_code,
                    'final_url': response.url,
                    'tested_url': test_url,
                    'checked_at': datetime.now().isoformat(),
                    'notes': domain_info.get('notes', '')
                }
                
        except requests.exceptions.SSLError:
            # Intentar sin verificación SSL
            try:
                response = requests.get(
                    test_url,
                    headers=HEADERS,
                    timeout=10,
                    allow_redirects=True,
                    verify=False
                )
                if response.status_code < 400:
                    return {
                        'domain': domain,
                        'status': 'ACTIVE_SSL_ISSUE',
                        'status_code': response.status_code,
                        'final_url': response.url,
                        'tested_url': test_url,
                        'checked_at': datetime.now().isoformat(),
                        'notes': f"{domain_info.get('notes', '')} (SSL Issue)"
                    }
            except:
                continue
                
        except requests.exceptions.Timeout:
            continue
        except requests.exceptions.ConnectionError:
            continue
        except:
            continue
    
    # Si todos los intentos fallan
    return {
        'domain': domain,
        'status': 'INACTIVE',
        'status_code': None,
        'final_url': None,
        'tested_url': None,
        'checked_at': datetime.now().isoformat(),
        'notes': domain_info.get('notes', '') + ' - Todos los intentos fallaron'
    }

def main():
    print("🔍 MONITOREO MEJORADO - PLANT PWR")
    print("=" * 50)
    
    # Cargar dominios
    domains_config = load_critical_domains()
    
    # Combinar todos los dominios para monitoreo
    all_domains = []
    
    # Agregar dominios críticos
    for domain_info in domains_config.get('critical', []):
        all_domains.append(domain_info)
    
    # Agregar dominios de alta prioridad (solo dominio, sin URL específica)
    for domain_info in domains_config.get('high_priority', []):
        all_domains.append(domain_info)
    
    print(f"📊 Dominios a monitorear: {len(all_domains)}")
    
    # Verificar cada dominio
    results = []
    active_count = 0
    
    for domain_info in all_domains:
        domain = domain_info.get('domain')
        print(f"\n🔍 Verificando: {domain}")
        
        result = check_domain_improved(domain_info)
        results.append(result)
        
        if result['status'].startswith('ACTIVE'):
            status_icon = "✅"
            active_count += 1
            print(f"   {status_icon} Estado: {result['status']}")
            print(f"   🔗 URL accesible: {result.get('final_url', 'N/A')}")
            if result.get('tested_url'):
                print(f"   🎯 Probado con: {result['tested_url']}")
        else:
            status_icon = "❌"
            print(f"   {status_icon} Estado: {result['status']}")
            print(f"   ⚠️  Notas: {result.get('notes', '')}")
    
    # Guardar resultados
    log_entry = {
        'date': datetime.now().isoformat(),
        'total_domains': len(all_domains),
        'active': active_count,
        'inactive': len(all_domains) - active_count,
        'results': results
    }
    
    # Cargar log anterior si existe
    log_data = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, 'r') as f:
                log_data = json.load(f)
        except:
            log_data = []
    
    # Agregar nuevo log
    log_data.append(log_entry)
    
    # Mantener solo últimos 30 días
    if len(log_data) > 30:
        log_data = log_data[-30:]
    
    # Guardar
    with open(LOG_FILE, 'w') as f:
        json.dump(log_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n📈 RESUMEN FINAL:")
    print(f"   ✅ Activos: {active_count}")
    print(f"   ❌ Inactivos: {len(all_domains) - active_count}")
    print(f"   📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    # Mostrar sitios activos críticos
    critical_active = [r for r in results if r['status'].startswith('ACTIVE') and any(c['domain'] == r['domain'] for c in domains_config.get('critical', []))]
    
    if critical_active:
        print(f"\n🚨 SITIOS CRÍTICOS ACTIVOS ({len(critical_active)}):")
        for result in critical_active:
            print(f"   • {result['domain']} - {result.get('final_url', 'N/A')}")
    
    print(f"\n💾 Log guardado en: {LOG_FILE}")

if __name__ == "__main__":
    # Desactivar warnings de SSL temporalmente
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    main()
