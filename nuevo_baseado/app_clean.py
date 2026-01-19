from flask import Flask, request, redirect, url_for, render_template_string
import os

app = Flask(__name__)

@app.route('/redirigir_tipo_llenado', methods=['POST'])
def redirigir_tipo_llenado():
    tipo = request.form.get('tipo')
    user_id = request.form.get('user_id')
    fila_idx = request.form.get('fila_idx')
    print(f"DEBUG tipo recibido: '{tipo}' (tipo: {type(tipo)})")
    print(f"DEBUG user_id recibido: '{user_id}' (tipo: {type(user_id)})")
    print(f"DEBUG fila_idx recibido: '{fila_idx}' (tipo: {type(fila_idx)})")
    
    # Convertir tipo a string y limpiar espacios
    tipo_str = str(tipo).strip().lower() if tipo is not None else ''
    
    if tipo_str == 'ptp':
        # Redirigir a la selección de tipo de llenado para PtP
        return redirect(url_for('seleccion_llenado_ptp', user_id=user_id, fila_idx=fila_idx))
    elif tipo_str == 'ptmp':
        # Redirigir a la selección de tipo de llenado para PtMP
        return redirect(url_for('seleccion_llenado_ptmp', user_id=user_id, fila_idx=fila_idx))
    elif tipo_str == 'diseno_solucion':
        # 🎯 LLENADO AUTOMÁTICO DE DISEÑO DE SOLUCIÓN - Redirigir a procesar
        print("🎯 LLENADO AUTOMÁTICO DE DISEÑO DE SOLUCIÓN - Redirigiendo a procesar")
        print(f"🔍 Parámetros recibidos: user_id='{user_id}', fila_idx='{fila_idx}', tipo='{tipo_str}'")
        
        # Redirigir a la función procesar con los parámetros correctos
        return redirect(url_for('procesar', user_id=user_id, fila_idx=fila_idx, tipo='diseno_solucion', llenado_automatico='true'))
    elif tipo_str == 'site_survey':
        # Redirigir a site survey
        return redirect(url_for('site_survey', user_id=user_id, fila_idx=fila_idx))
    else:
        return f"Tipo de llenado no reconocido: {tipo_str}"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
