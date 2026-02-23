#!/usr/bin/env python3
"""
Script de monitoreo diario mejorado para Plant PWR.
Versión: 2.0 - Con múltiples intentos y headers realistas
"""

import json
import os
import requests
from datetime import datetime
import urllib3

# Configuración
DOMAINS_FILE = "/root/.openclaw/workspace/plant-pwr-investigation/dominios/critical_domains.json"
LOG_FILE = "/root/.openclaw/workspace/plant-pwr-investigation/monitoreo/daily_log.json"

# Headers realistas para evitar bloqueos
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'
}

def load_domains():
    """Carga dominios desde archivo JSON"""
    if os.path.exists(DOMAINS_FILE):
        with open(DOMAINS_FILE, 'r') as f:
            return json.load(f)
    return {"critical": [], "high_priority": []}

def check_domain_smart(domain_info):
    """Verifica dominio con múltiples estrategias"""
    domain = domain_info.get('domain')
    url = domain_info.get('url', f"https://{domain}")
    
    # Estrategias de prueba
    test_strategies = [
        lambda: try_url(url),  # URL específica primero
        lambda: try_url(f"https://{domain}"),
        lambda: try_url(f"http://{domain}"),
        lambda: try_url(f"https://www.{domain}"),
        lambda: try_url(f"http://www.{domain}")
    ]
    
    for strategy in test_strategies:
        result = strategy()
        if result and result['status_code'] < 400:
            return result
    
    # Todos fallaron
    return {
        'domain': domain,
        'status': 'INACTIVE',
        'status_code': None,
        'final_url': None,
        'checked_at': datetime.now().isoformat()
    }

def try_url(url):
    """Intenta acceder a una URL"""
    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10,
            allow_redirects=True,
            verify=False  # Temporal para SSL issues
        )
        return {
            'domain': url.split('//')[-1].split('/')[0],
            'status': 'ACTIVE',
            'status_code': response.status_code,
            'final_url': response.url,
            'checked_at': datetime.now().isoformat()
        }
    except:
        return None

def main():
    print("🔍 MONITOREO DIARIO - PLANT PWR v2.0")
    print("=" * 50)
    
    # Desactivar warnings SSL
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    # Cargar dominios
    data = load_domains()
    all_domains = data.get('critical', []) + data.get('high_priority', [])
    
    print(f"📊 Dominios a monitorear: {len(all_domains)}")
    
    # Verificar cada dominio
    results = []
    active_count = 0
    
    for domain_info in all_domains:
        domain = domain_info.get('domain')
        print(f"\n🔍 {domain}: ", end='')
        
        result = check_domain_smart(domain_info)
        results.append({**result, 'priority': domain_info.get('priority', 'UNKNOWN')})
        
        if result['status'] == 'ACTIVE':
            print("✅ ACTIVO")
            active_count += 1
        else:
            print("❌ INACTIVO")
    
    # Guardar resultados
    log_entry = {
        'date': datetime.now().isoformat(),
        'total': len(all_domains),
        'active': active_count,
        'inactive': len(all_domains) - active_count,
        'results': results
    }
    
    # Manejar archivo de log
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, 'r') as f:
                logs = json.load(f)
        except:
            logs = []
    
    logs.append(log_entry)
    if len(logs) > 30:
        logs = logs[-30:]
    
    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)
    
    # Mostrar resumen
    print(f"\n📈 RESUMEN:")
    print(f"   ✅ Activos: {active_count}/{len(all_domains)}")
    print(f"   ❌ Inactivos: {len(all_domains) - active_count}/{len(all_domains)}")
    
    # Sitios críticos activos
    critical_active = [r for r in results if r['status'] == 'ACTIVE' and r.get('priority') == 'CRITICAL']
    if critical_active:
        print(f"\n🚨 SITIOS CRÍTICOS ACTIVOS ({len(critical_active)}):")
        for r in critical_active:
            print(f"   • {r['domain']}")
    
    print(f"\n💾 Log guardado: {LOG_FILE}")
    print(f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M')}")

if __name__ == "__main__":
    main()
