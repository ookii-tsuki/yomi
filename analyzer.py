import json
import fugashi
from romkan import to_hepburn, to_kunrei

def katakana_to_hiragana(text):
    return text.translate(str.maketrans({chr(0x30A1 + i): chr(0x3041 + i) for i in range(96)}))

def is_kanji(char):
    return 0x4E00 <= ord(char) <= 0x9FFF

def has_kanji(text):
    for char in text:
        if is_kanji(char):
            return True
    return False

class Mode:
    NORMAL = 0
    SPACED = 1
    OKURIGANA = 2
    FURIGANA = 3

class To:
    ROMAJI = 0
    HIRAGANA = 1
    KATAKANA = 2

class RomajiSystem:
    HEPBURN = 0
    KUNREI = 1

def convert_to_mode(words, converted, mode) -> str:
    if mode == Mode.NORMAL:
        return ''.join(converted)
    elif mode == Mode.SPACED:
        return " ".join(converted)
    elif mode == Mode.OKURIGANA:
        okurigana = str()
        for i in range(len(words)):
            okurigana += f"{words[i].surface}({converted[i]})" if has_kanji(words[i].surface) else words[i].surface
        return okurigana
    else: # mode == Mode.FURIGANA:
        okurigana = str()
        for i in range(len(words)):
            okurigana += f"<ruby>{words[i].surface}<rt>{converted[i]}</rt></ruby>" if has_kanji(words[i].surface) else words[i].surface
        return okurigana

class Element:
    def __init__(self, word: fugashi.UnidicNode, mode: Mode, to: To, romaji_system: RomajiSystem):
        self.surface = word.surface
        self.lemma = word.feature.lemma
        self.pos = [word.feature.pos1, word.feature.pos2, word.feature.pos3, word.feature.pos4]

        if to == To.HIRAGANA:
            self.reading = katakana_to_hiragana(word.feature.kana) if word.feature.kana else word.surface
            self.pronunciation = katakana_to_hiragana(word.feature.pron) if word.feature.pron else word.surface
        elif to == To.KATAKANA:
            self.reading = word.feature.kana if word.feature.kana else word.surface
            self.pronunciation = word.feature.pron if word.feature.pron else word.surface
        elif to == To.ROMAJI:
            self.reading = to_hepburn(word.feature.kana) if word.feature.kana else word.surface if romaji_system == RomajiSystem.HEPBURN else to_kunrei(word.feature.kana) if word.feature.kana else word.surface
            self.pronunciation = to_hepburn(word.feature.pron) if word.feature.pron else word.surface if romaji_system == RomajiSystem.HEPBURN else to_kunrei(word.feature.pron) if word.feature.pron else word.surface

        self.reading_raw = self.reading
        self.pronunciation_raw = self.pronunciation

        self.reading = convert_to_mode([word], [self.reading], mode)
        self.pronunciation = convert_to_mode([word], [self.pronunciation], mode)


class Analyzer:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=None, ensure_ascii=False, separators=(',', ':'))
            
    def __init__(self, text, mode=Mode.NORMAL, to=To.HIRAGANA, romaji_system=RomajiSystem.HEPBURN):
        self.text = text

        tagger = fugashi.Tagger('-Owakati')
        tagger.parse(text)

        words = tagger(text)
                
        if to == To.HIRAGANA:
            hiragana = [katakana_to_hiragana(word.feature.kana) if word.feature.kana else word.surface for word in words]
            self.converted = convert_to_mode(words, hiragana, mode)
        elif to == To.KATAKANA:
            katakana = [word.feature.kana if word.feature.kana else word.surface for word in words]
            self.converted = convert_to_mode(words, katakana, mode)
        elif to == To.ROMAJI:
            romaji = [to_hepburn(word.feature.kana) if word.feature.kana else word.surface for word in words] if romaji_system == RomajiSystem.HEPBURN else [to_kunrei(word.feature.kana) if word.feature.kana else word.surface for word in words]
            self.converted = convert_to_mode(words, romaji, mode)
        
        self.words = []
        for word in words:
            self.words.append(Element(word, mode, to, romaji_system))