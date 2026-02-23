#!/usr/bin/env python3
"""
Script para mostrar resumen completo de la investigación Plant PWR.
"""

import json
import os
from datetime import datetime
import glob

def print_header(text):
    print(f"\n{'='*60}")
    print(f"📊 {text}")
    print(f"{'='*60}")

def load_config():
    config_path = "/root/.openclaw/workspace/plant-pwr-investigation/config.json"
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)
    return {}

def count_files(directory, pattern="*"):
    files = glob.glob(os.path.join(directory, pattern))
    return len(files)

def get_domain_stats():
    critical_path = "/root/.openclaw/workspace/plant-pwr-investigation/dominios/critical_domains.json"
    if os.path.exists(critical_path):
        with open(critical_path, 'r') as f:
            data = json.load(f)
        
        stats = {
            'critical': len(data.get('critical', [])),
            'high_priority': len(data.get('high_priority', [])),
            'to_investigate': len(data.get('to_investigate', [])),
            'competitor': len(data.get('competitor_domains', []))
        }
        stats['total'] = sum(stats.values())
        return stats
    return {'total': 0}

def main():
    print("🔍 RESUMEN COMPLETO - INVESTIGACIÓN PLANT PWR")
    print("=" * 60)
    
    # Cargar configuración
    config = load_config()
    
    # Información del sistema
    print_header("INFORMACIÓN DEL SISTEMA")
    if config:
        sys_info = config.get('system', {})
        print(f"📋 Nombre: {sys_info.get('name', 'N/A')}")
        print(f"🔄 Versión: {sys_info.get('version', 'N/A')}")
        print(f"📅 Creado: {sys_info.get('created', 'N/A')}")
        print(f"📝 Descripción: {sys_info.get('description', 'N/A')}")
    
    # Estadísticas de archivos
    print_header("ESTADÍSTICAS DE ARCHIVOS")
    
    root_dir = "/root/.openclaw/workspace/plant-pwr-investigation"
    directories = {
        '📁 Dominios': 'dominios',
        '📁 Evidencia': 'evidencia',
        '📁 Denuncias': 'denuncias',
        '📁 Análisis': 'analisis',
        '📁 Scripts': 'scripts',
        '📁 Monitoreo': 'monitoreo'
    }
    
    for label, dir_name in directories.items():
        dir_path = os.path.join(root_dir, dir_name)
        if os.path.exists(dir_path):
            file_count = count_files(dir_path, "*")
            print(f"{label}: {file_count} archivos")
    
    # Estadísticas de dominios
    print_header("ESTADÍSTICAS DE DOMINIOS")
    domain_stats = get_domain_stats()
    
    print(f"🌐 TOTAL DOMINIOS: {domain_stats.get('total', 0)}")
    print(f"🔴 Críticos: {domain_stats.get('critical', 0)}")
    print(f"🟡 Alta prioridad: {domain_stats.get('high_priority', 0)}")
    print(f"🟠 Por investigar: {domain_stats.get('to_investigate', 0)}")
    print(f"🔍 Competidor: {domain_stats.get('competitor', 0)}")
    
    # Herramientas configuradas
    print_header("HERRAMIENTAS CONFIGURADAS")
    
    if config and 'tools' in config:
        tools = config['tools']
        
        if tools.get('whoogle', {}).get('enabled'):
            print(f"🔍 Whoogle: ✅ ACTIVO ({tools['whoogle'].get('url', 'N/A')})")
            print(f"   Búsquedas diarias: {'✅' if tools['whoogle'].get('daily_search') else '❌'}")
        
        if tools.get('google_drive', {}).get('enabled'):
            print(f"☁️ Google Drive: ✅ ACTIVO")
            drive_info = tools['google_drive']
            print(f"   Carpeta ID: {drive_info.get('folder_id', 'N/A')}")
            print(f"   Sincronización: {'✅' if drive_info.get('sync_evidence') else '❌'}")
        
        if tools.get('monitoring', {}).get('daily_check'):
            print(f"📊 Monitoreo: ✅ ACTIVO")
            monitor = tools['monitoring']
            print(f"   Intervalo: cada {monitor.get('check_interval_hours', 'N/A')} horas")
            print(f"   Alertas: {'✅' if monitor.get('alert_on_change') else '❌'}")
    
    # Información del competidor
    print_header("INFORMACIÓN DEL COMPETIDOR")
    
    if config and 'targets' in config:
        targets = config['targets']
        competitor = targets.get('primary_competitor', {})
        
        print(f"🎯 Competidor: {competitor.get('name', 'Plant PWR')}")
        print(f"   👤 Dueño: {competitor.get('owner', 'Julian Zuluaga')}")
        print(f"   📍 Ubicación: {competitor.get('location', 'Medellín, Colombia')}")
        print(f"   💰 Rango de precios: {competitor.get('prices_range', '94.900-189.900 COP')}")
        print(f"   📦 Productos: {', '.join(competitor.get('products', ['Aceite cannabis para mascotas']))}")
    
    # Acciones legales
    print_header("ACCIONES LEGALES")
    
    if config and 'legal' in config:
        legal = config['legal']
        
        print(f"⚖️ Autoridades: {', '.join(legal.get('authorities', []))}")
        print(f"🚨 Alerta activa: {legal.get('alert_number', 'N/A')}")
        
        print(f"\n🎯 Próximos pasos legales:")
        for i, step in enumerate(legal.get('next_steps', []), 1):
            print(f"   {i}. {step}")
    
    # Contactos
    print_header("CONTACTOS")
    
    if config and 'contacts' in config:
        contacts = config['contacts']
        
        print(f"👤 Cliente: {contacts.get('client', 'Carlos Calderon - Klean Vet')}")
        print(f"🔍 Investigador: {contacts.get('investigator', 'Charlie (AI Assistant)')}")
        print(f"📧 Email: {contacts.get('email', 'carlos@kleanvet.co')}")
        print(f"🏢 Empresa: {contacts.get('business', 'Cannabian Pharma SAS')}")
    
    # Estado actual
    print_header("ESTADO ACTUAL")
    
    if config and 'status' in config:
        status = config['status']
        
        print(f"📅 Última actualización: {status.get('last_updated', 'N/A')}")
        print(f"🔍 Investigación activa: {'✅' if status.get('active_investigation') else '❌'}")
        print(f"📸 Evidencia recolectada: {'✅' if status.get('evidence_collected') else '❌'}")
        print(f"⚖️ Acciones legales pendientes: {'✅' if status.get('legal_actions_pending') else '❌'}")
        print(f"📊 Monitoreo activo: {'✅' if status.get('monitoring_active') else '❌'}")
    
    # Recomendaciones
    print_header("RECOMENDACIONES")
    
    recommendations = [
        "1. Ejecutar monitoreo diario para verificar cambios",
        "2. Realizar búsqueda Whoogle para nuevos hallazgos",
        "3. Capturar evidencia de sitios críticos",
        "4. Preparar denuncias para autoridades",
        "5. Compartir archivos con Google Drive para respaldo",
        "6. Revisar y actualizar la base de datos semanalmente"
    ]
    
    for rec in recommendations:
        print(f"   {rec}")
    
    print(f"\n{'='*60}")
    print(f"🎯 RESUMEN COMPLETADO: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
