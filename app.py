import os
import sys
import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from deob.deob import deobfuscate
except ImportError:
    pass

app = Flask(__name__)
CORS(app) # Cho phép GitHub Pages gọi API vào đây

@app.route('/api/deobfuscate', methods=['POST'])
def handle_deobfuscate():
    data = request.get_json()
    if not data or 'code' not in data:
        return jsonify({'error': 'Vui lòng cung cấp mã Lua.'}), 400

    try:
        result = deobfuscate(data['code'])
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e), 'traceback': traceback.format_exc()}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
