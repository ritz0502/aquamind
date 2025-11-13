from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from datetime import datetime, timedelta
import random

app = Flask(__name__)
CORS(app)

# Helper function to generate mock data
def generate_chart_data(days=7, data_type='line'):
    if data_type == 'line':
        return [{'day': f'Day {i+1}', 'value': random.randint(40, 90)} for i in range(days)]
    elif data_type == 'bar':
        return [{'day': f'Day {i+1}', 'value': random.randint(30, 100)} for i in range(days)]
    elif data_type == 'forecast':
        return [
            {
                'day': f'Day {i+1}',
                'temperature': round(random.uniform(20, 28), 1),
                'waveHeight': round(random.uniform(1, 4), 1)
            } for i in range(days)
        ]
    elif data_type == 'activity':
        return [
            {'category': cat, 'count': random.randint(5, 50)}
            for cat in ['Cargo', 'Tankers', 'Fishing', 'Tourism']
        ]
    elif data_type == 'anomaly':
        return [
            {'time': f'{i}:00', 'reading': random.randint(50, 95)}
            for i in range(1, 13)
        ]
    elif data_type == 'health':
        return [
            {'month': month, 'health': random.randint(55, 85)}
            for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        ]

# Pollution Detection Endpoint
@app.route('/api/pollution/run', methods=['POST'])
def pollution_detection():
    try:
        data = request.json
        lat = float(data.get('lat', 0))
        lon = float(data.get('lon', 0))
        depth = float(data.get('depth', 0))
        salinity = float(data.get('salinity', 35))
        temperature = float(data.get('temperature', 25))
        pH = float(data.get('pH', 8.1))
        
        # Simulate pollution score based on parameters
        pollution_score = int(50 + (35 - salinity) * 2 + abs(8.1 - pH) * 10)
        pollution_score = max(0, min(100, pollution_score))
        
        if pollution_score < 40:
            insight = "Low pollution detected. Water quality is excellent for marine life."
        elif pollution_score < 70:
            insight = "Moderate pollution levels detected. Some concern for sensitive species."
        else:
            insight = "High pollution detected. Immediate action recommended to protect ecosystem."
        
        return jsonify({
            'status': 'success',
            'model': 'pollution',
            'results': {
                'score': f'{pollution_score}%',
                'insight': insight,
                'chartData': generate_chart_data(7, 'bar')
            }
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

# Coral Health Endpoint
@app.route('/api/coral/run', methods=['POST'])
def coral_health():
    try:
        data = request.json
        temperature = float(data.get('temperature', 25))
        pH = float(data.get('pH', 8.1))
        depth = float(data.get('depth', 10))
        
        # Simulate coral health score
        health_score = int(85 - abs(26 - temperature) * 5 - abs(8.2 - pH) * 10)
        health_score = max(30, min(100, health_score))
        
        if health_score > 75:
            insight = "Coral health is good. Minimal bleaching risk detected."
        elif health_score > 50:
            insight = "Moderate coral stress detected. Early bleaching signs possible."
        else:
            insight = "Severe coral stress. High bleaching risk - urgent intervention needed."
        
        return jsonify({
            'status': 'success',
            'model': 'coral',
            'results': {
                'health_score': f'{health_score}%',
                'insight': insight,
                'chartData': generate_chart_data(6, 'health')
            }
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

# Ocean Forecast Endpoint
@app.route('/api/forecast/run', methods=['POST'])
def ocean_forecast():
    try:
        data = request.json
        lat = float(data.get('lat', 0))
        temperature = float(data.get('temperature', 25))
        
        # Simulate forecast
        trend = "stable" if abs(lat) < 30 else "warming"
        
        if trend == "stable":
            summary = "Stable Conditions Expected"
            insight = "Ocean conditions expected to remain stable over the next 7 days. Favorable for marine activities."
        else:
            summary = "Temperature Increase Predicted"
            insight = "Gradual warming trend detected. Monitor coral reef areas and adjust conservation strategies."
        
        return jsonify({
            'status': 'success',
            'model': 'forecast',
            'results': {
                'forecast_summary': summary,
                'insight': insight,
                'chartData': generate_chart_data(7, 'forecast')
            }
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

# Human Activity Endpoint
@app.route('/api/activity/run', methods=['POST'])
def human_activity():
    try:
        data = request.json
        lat = float(data.get('lat', 0))
        lon = float(data.get('lon', 0))
        
        # Simulate activity metrics
        ships_detected = random.randint(5, 45)
        ports_nearby = random.randint(0, 5)
        tourism_density = random.randint(1, 10)
        
        if ships_detected > 30:
            insight = "High shipping traffic detected. Increased collision risk for marine mammals."
        elif ships_detected > 15:
            insight = "Moderate marine activity. Regular monitoring recommended."
        else:
            insight = "Low human activity. Minimal disturbance to marine ecosystem."
        
        return jsonify({
            'status': 'success',
            'model': 'activity',
            'results': {
                'ships_detected': ships_detected,
                'ports_nearby': ports_nearby,
                'tourism_density': tourism_density,
                'insight': insight,
                'chartData': generate_chart_data(4, 'activity')
            }
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

# Anomaly Detection Endpoint
@app.route('/api/anomalies/run', methods=['POST'])
def anomaly_detection():
    try:
        data = request.json
        temperature = float(data.get('temperature', 25))
        salinity = float(data.get('salinity', 35))
        pH = float(data.get('pH', 8.1))
        
        # Detect anomalies
        anomalies = []
        risk_level = "Low Risk"
        
        if abs(temperature - 25) > 3:
            anomalies.append(f"Temperature anomaly detected: {temperature}°C (expected ~25°C)")
            risk_level = "Medium Risk"
        
        if abs(salinity - 35) > 3:
            anomalies.append(f"Salinity anomaly detected: {salinity} PSU (expected ~35 PSU)")
            risk_level = "Medium Risk"
        
        if abs(pH - 8.1) > 0.3:
            anomalies.append(f"pH anomaly detected: {pH} (expected ~8.1)")
            risk_level = "High Risk"
        
        if not anomalies:
            anomalies.append("No significant anomalies detected. Parameters within normal ranges.")
            insight = "All ocean parameters are within expected ranges. Ecosystem appears stable."
        else:
            insight = f"{len(anomalies)} anomaly detected. Investigate potential environmental changes."
        
        return jsonify({
            'status': 'success',
            'model': 'anomalies',
            'results': {
                'risk_level': risk_level,
                'anomalies': anomalies,
                'insight': insight,
                'chartData': generate_chart_data(12, 'anomaly')
            }
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

# MEHI (Marine Ecosystem Health Index) Endpoint
@app.route('/api/mehi/run', methods=['POST'])
def mehi_index():
    try:
        data = request.json
        
        # Calculate composite MEHI score from various indicators
        water_quality = random.randint(65, 90)
        biodiversity = random.randint(60, 85)
        coral_health = random.randint(55, 80)
        pollution_level = random.randint(70, 95)
        human_impact = random.randint(50, 75)
        
        mehi_score = int((water_quality + biodiversity + coral_health + pollution_level + human_impact) / 5)
        
        if mehi_score > 80:
            insight = "Excellent ecosystem health. Marine environment is thriving with high biodiversity."
        elif mehi_score > 65:
            insight = "Good ecosystem health. Some areas need attention but overall positive indicators."
        elif mehi_score > 50:
            insight = "Moderate ecosystem health. Several concerning factors require intervention."
        else:
            insight = "Poor ecosystem health. Critical intervention needed to restore marine balance."
        
        radar_data = [
            {'indicator': 'Water Quality', 'value': water_quality},
            {'indicator': 'Biodiversity', 'value': biodiversity},
            {'indicator': 'Coral Health', 'value': coral_health},
            {'indicator': 'Pollution Control', 'value': pollution_level},
            {'indicator': 'Human Impact', 'value': human_impact}
        ]
        
        return jsonify({
            'status': 'success',
            'model': 'mehi',
            'results': {
                'mehi_score': f'{mehi_score}/100',
                'insight': insight,
                'indicators': {
                    'water_quality': f'{water_quality}%',
                    'biodiversity': f'{biodiversity}%',
                    'coral_health': f'{coral_health}%',
                    'pollution_control': f'{pollution_level}%',
                    'human_impact': f'{human_impact}%'
                },
                'radarData': radar_data
            }
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)