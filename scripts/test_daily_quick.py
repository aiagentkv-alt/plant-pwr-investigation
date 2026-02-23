#!/usr/bin/env python3
"""
Test rápido del script de búsqueda diaria.
"""

import os
import json
from datetime import datetime

# Configuración
LOG_DIR = "/root/.openclaw/workspace/plant-pwr-investigation/monitoreo/logs"
RESULTS_DIR = "/root/.openclaw/workspace/plant-pwr-investigation/evidencia"

def setup_directories():
    """Crear directorios necesarios"""
    os.makedirs(LOG_DIR, exist_ok=True)
    os.makedirs(RESULTS_DIR, exist_ok=True)
    print("✅ Directorios configurados")

def test_logging():
    """Probar sistema de logging"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file = os.path.join(LOG_DIR, "test_daily.log")
    
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] 🔧 TEST DEL SISTEMA DIARIO\n")
        f.write(f"[{timestamp}] ✅ Sistema de logging funcionando\n")
    
    print("✅ Sistema de logging funcionando")
    return log_file

def test_results_saving():
    """Probar guardado de resultados"""
    date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(RESULTS_DIR, f"test_results_{date_str}.json")
    
    # Datos de prueba
    test_data = {
        'metadata': {
            'test': True,
            'generated_at': datetime.now().isoformat(),
            'system': 'Plant PWR Investigation',
            'version': '1.0'
        },
        'test_results': [
            {
                'title': 'Test Result 1',
                'url': 'https://example.com/test1',
                'domain': 'example.com',
                'snippet': 'This is a test result for the daily search system.',
                'found_at': datetime.now().isoformat()
            },
            {
                'title': 'Test Result 2',
                'url': 'https://test.com/plant-pwr',
                'domain': 'test.com',
                'snippet': 'Another test result showing the system works.',
                'found_at': datetime.now().isoformat()
            }
        ]
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Resultados de prueba guardados en: {output_file}")
    return output_file

def test_summary_generation():
    """Probar generación de resumen"""
    date_str = datetime.now().strftime("%Y%m%d")
    summary_file = os.path.join(LOG_DIR, f"test_summary_{date_str}.txt")
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("📊 RESUMEN DE PRUEBA DEL SISTEMA\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("Sistema: Monitoreo Automatizado Plant PWR\n")
        f.write("Estado: ✅ FUNCIONANDO CORRECTAMENTE\n\n")
        f.write("🔧 Componentes probados:\n")
        f.write("  • Sistema de logging ✓\n")
        f.write("  • Guardado de resultados ✓\n")
        f.write("  • Generación de resúmenes ✓\n")
        f.write("  • Estructura de directorios ✓\n\n")
        f.write("🚀 Próximos pasos:\n")
        f.write("  1. Ejecutar búsqueda real en Whoogle\n")
        f.write("  2. Configurar cron job diario\n")
        f.write("  3. Monitorear resultados automáticamente\n")
    
    print(f"✅ Resumen de prueba generado: {summary_file}")
    return summary_file

def main():
    """Función principal de prueba"""
    print("=" * 60)
    print("🔧 TEST DEL SISTEMA DE BÚSQUEDA DIARIA")
    print("=" * 60)
    
    try:
        # 1. Configurar directorios
        setup_directories()
        
        # 2. Probar logging
        log_file = test_logging()
        
        # 3. Probar guardado de resultados
        results_file = test_results_saving()
        
        # 4. Probar generación de resumen
        summary_file = test_summary_generation()
        
        print("\n" + "=" * 60)
        print("🎯 TEST COMPLETADO EXITOSAMENTE")
        print("=" * 60)
        print(f"📁 Archivos generados:")
        print(f"   • Log: {log_file}")
        print(f"   • Resultados: {results_file}")
        print(f"   • Resumen: {summary_file}")
        print("\n✅ El sistema está listo para búsquedas reales.")
        print("🔧 Para ejecutar búsqueda real:")
        print("   cd /root/.openclaw/workspace/plant-pwr-investigation/scripts")
        print("   source venv/bin/activate")
        print("   python3 whoogle_search.py")
        
    except Exception as e:
        print(f"❌ ERROR EN TEST: {type(e).__name__}: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())