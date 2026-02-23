#!/bin/bash
# Script para ejecución automática de monitoreo diario

LOG_DIR="/root/.openclaw/workspace/plant-pwr-investigation/monitoreo"
SCRIPT_PATH="/root/.openclaw/workspace/plant-pwr-investigation/scripts/monitor_diario.py"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="$LOG_DIR/cron_${TIMESTAMP}.log"

echo "🕐 Ejecución automática: $(date)" > "$LOG_FILE"
echo "=================================" >> "$LOG_FILE"

# Ejecutar monitoreo
cd /root/.openclaw/workspace/plant-pwr-investigation
python3 "$SCRIPT_PATH" >> "$LOG_FILE" 2>&1

# Verificar si hay cambios importantes
LAST_LOG="$LOG_DIR/daily_log.json"
if [ -f "$LAST_LOG" ]; then
    # Contar activos en última ejecución
    ACTIVE_COUNT=$(tail -1 "$LAST_LOG" | grep -o '"active":[0-9]*' | cut -d: -f2)
    echo "" >> "$LOG_FILE"
    echo "📊 Resumen cron: $ACTIVE_COUNT dominios activos" >> "$LOG_FILE"
    
    # Aquí podríamos agregar notificaciones si hay cambios drásticos
    if [ "$ACTIVE_COUNT" -lt 4 ]; then
        echo "⚠️  ALERTA: Menos de 4 dominios críticos activos" >> "$LOG_FILE"
    fi
fi

echo "" >> "$LOG_FILE"
echo "✅ Monitoreo completado: $(date)" >> "$LOG_FILE"
