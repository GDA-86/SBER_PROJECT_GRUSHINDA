import pandas as pd
import pickle
from flask import Flask, jsonify, render_template, request
from models.my_functions2model import gda_main_proc

app = Flask(__name__)


#  Проверка работы сервера
@app.route('/test', methods=['GET'])
def test_server():
    return jsonify({'status': 'ok', 'message': 'Flask server is running'})


# Отображение формы и обработка данных
@app.route('/predict', methods=['GET', 'POST']) # type: ignore
def predict():
    if request.method == 'GET':
        return render_template('index.html')

    if request.method == 'POST':
        try:
            # Извлекаем все полей из формы с валидацией типов
            input_data = {
                'session_id': request.form.get('session_id'),
                'client_id': request.form.get('client_id'),
                'visit_date': request.form.get('visit_date'),
                'visit_time': request.form.get('visit_time'),
                'visit_number': int(request.form.get('visit_number')), # type: ignore
                'utm_source': request.form.get('utm_source'),
                'utm_medium': request.form.get('utm_medium'),
                'utm_campaign': request.form.get('utm_campaign'),
                'utm_adcontent': request.form.get('utm_adcontent'),
                'utm_keyword': request.form.get('utm_keyword'),
                'device_category': request.form.get('device_category'),
                'device_os': request.form.get('device_os'),
                'device_brand': request.form.get('device_brand'),
                'device_model': request.form.get('device_model'),
                'device_screen_resolution': request.form.get('device_screen_resolution'),
                'device_browser': request.form.get('device_browser'),
                'geo_country': request.form.get('geo_country'),
                'geo_city': request.form.get('geo_city'),
            }


            with open('models/model_v1.pkl', 'rb') as f: model = pickle.load(f)

            lo_sessions = pd.DataFrame(list(input_data))
            lo_hits = pd.DataFrame(list({'1': '1'})) # так определена ф-ия (
            
            X = gda_main_proc(lo_sessions, lo_hits, mode=2)

            
                #Получаем предсказания
            prediction = model.predict(X)          # Классы (0 или 1)

            return jsonify(
                {
                    'status': 'success',
                    'received_data': input_data,
                    'prediction': prediction,
                }
            )

        except (ValueError, TypeError) as e:
            return (
                jsonify(
                    {'status': 'error', 'message': f'Ошибка при вводе данных: {e}'}
                ),
                400,
            )


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
