from flask import Flask, request, jsonify, current_app
import analyzer

app = Flask(__name__)

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

@app.route('/analyze', methods=['POST'])
def analyze():
    if not 'text' in request.form:
        return jsonify({'error': 'no text provided'}), 400
        
    text = request.form['text']

    if len(text) > 5000:
        return jsonify({'error': 'text exceeds 5000 character limit'}), 400

    mode = modestring_to_enum(request.form['mode'] if 'mode' in request.form else 'normal')
    to = tostring_to_enum(request.form['to'] if 'to' in request.form else 'hiragana')
    romaji_system = romajisystemstring_to_enum(request.form['romaji_system'] if 'romaji_system' in request.form else 'hepburn') 
    print(len(text))
    analisys = analyzer.Analyzer(text, mode, to, romaji_system)
    return analisys.toJSON()