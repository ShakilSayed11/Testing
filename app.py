import os
from flask import Flask, render_template, request, jsonify
from supabase import create_client, Client
import datetime

app = Flask(__name__)

# Supabase credentials from environment variables
SUPABASE_URL = os.getenv('https://dwcbvbpwkfmydeucsydj.supabase.co')
SUPABASE_KEY = os.getenv('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR3Y2J2YnB3a2ZteWRldWNzeWRqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjI4NTQ2NTMsImV4cCI6MjAzODQzMDY1M30.g688zmPnGmwu9oBt7YrfUmtivDohDyiEYPQP-lz16GI')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def index():
    response = supabase.table('attendance').select('*').execute()
    data = response.data

    if not data:
        return "No data found in the attendance table."
    
    current_date = datetime.date.today().strftime('%d-%b')

    return render_template('index.html', data=data, current_date=current_date)

@app.route('/update', methods=['POST'])
def update():
    record_id = request.form.get('id')
    date_column = request.form.get('date_column')
    new_value = request.form.get('new_value')

    response = supabase.table('attendance').update({date_column: new_value}).eq('id', record_id).execute()
    
    if response.error:
        return jsonify({'status': 'error', 'message': str(response.error)})
    
    return jsonify({'status': 'success', 'data': response.data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

