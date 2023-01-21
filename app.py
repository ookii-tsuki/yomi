from flask import Flask, request, jsonify, make_response
import analyzer
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def modestring_to_enum(modestring):
    if modestring == 'normal':
        return analyzer.Mode.NORMAL
    elif modestring == 'spaced':
        return analyzer.Mode.SPACED
    elif modestring == 'okurigana':
        return analyzer.Mode.OKURIGANA
    elif modestring == 'furigana':
        return analyzer.Mode.FURIGANA
    else:
        return analyzer.Mode.NORMAL

def tostring_to_enum(tostring):
    if tostring == 'romaji':
        return analyzer.To.ROMAJI
    elif tostring == 'hiragana':
        return analyzer.To.HIRAGANA
    elif tostring == 'katakana':
        return analyzer.To.KATAKANA
    else:
        return analyzer.To.HIRAGANA
    
def romajisystemstring_to_enum(romajisystemstring):
    if romajisystemstring == 'hepburn':
        return analyzer.RomajiSystem.HEPBURN
    elif romajisystemstring == 'kunrei':
        return analyzer.RomajiSystem.KUNREI
    else:
        return analyzer.RomajiSystem.HEPBURN

def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/analyze', methods=["POST", "OPTIONS"])
def analyze():

    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()

    elif request.method == "POST":
        if not 'text' in request.form:
            return jsonify({'error': 'no text provided'}), 400

        text = request.form['text']

        if len(text) > 5000:
            return jsonify({'error': 'text exceeds 5000 character limit'}), 400

        mode = modestring_to_enum(request.form['mode'] if 'mode' in request.form else 'normal')
        to = tostring_to_enum(request.form['to'] if 'to' in request.form else 'hiragana')
        romaji_system = romajisystemstring_to_enum(request.form['romaji_system'] if 'romaji_system' in request.form else 'hepburn') 

        analisys = analyzer.Analyzer(text, mode, to, romaji_system)

        return _corsify_actual_response(jsonify(analisys.toJSON()))
    else:
        return jsonify({'error': 'invalid request method'}), 400
