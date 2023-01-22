
<img src="https://cdn-icons-png.flaticon.com/512/1864/1864652.png" width="100">

# Yomi API
Yomi API is a free-to-use Japanese tokenizer and morphological analysis web API. It can take a Japanese text as an input and return a JSON response containing the tokenized text.

## Entry Point

| PATH | Request type |
|------|--------------|
| /analyze/ | POST |

### Query strings

| Name | Required | Description |
|------|----------|----------|
| text | Yes | The text that will be tokenized |
| mode | No | mode of the output `normal`, `spaced`, `okurigana` or `furigana` (default: `normal`) |
| to | No | to which writing system should the text be converted `hiragana`, `katakana` or `romaji` (default: `hiragana`) |
| romaji_system | No | which romanization system (`hepburn`, `kunrei`) should be used when the `to` parameter is set to `romaji` (default: `hepburn`) |

### Examples
Try a [live demo!](https://yssf8.github.io/Yomi-playground/)
##### Simple request using the default settings:
curl:
```powershell
curl -d "text=日本は美しい国だ" https://yomi.onrender.com/analyze
```
python:
```python
import requests
headers = { 'Content-Type': 'application/x-www-form-urlencoded' }
data = 'text=私はレミです'.encode()
response = requests.post('https://yomi.onrender.com/analyze', headers=headers, data=data)
```
##### Request with optional settings:
curl:
```powershell
curl -d "text=日本は美しい国だ&mode=okurigana&to=hiragana&romaji_system=hepburn" https://yomi.onrender.com/analyze
```
python:
```python
import requests
headers = { 'Content-Type': 'application/x-www-form-urlencoded' }
data = 'text=日本は美しい国だ&mode=okurigana&to=hiragana&romaji_system=hepburn'.encode()
response = requests.post('https://yomi.onrender.com/analyze', headers=headers, data=data)
```
#### Response
```json
{
  "converted": "日本(にっぽん)は美しい(うつくしい)国(くに)だ",
  "text": "日本は美しい国だ",
  "words": [
    {
      "lemma": "日本",
      "pos": ["名詞", "固有名詞", "地名", "国"],
      "pronunciation": "日本(にっぽん)",
      "pronunciation_raw": "にっぽん",
      "reading": "日本(にっぽん)",
      "reading_raw": "にっぽん",
      "surface": "日本"
    },
    {
      "lemma": "は",
      "pos": ["助詞", "係助詞", "*", "*"],
      "pronunciation": "は",
      "pronunciation_raw": "わ",
      "reading": "は",
      "reading_raw": "は",
      "surface": "は"
    },
    {
      "lemma": "美しい",
      "pos": ["形容詞", "一般", "*", "*"],
      "pronunciation": "美しい(うつくし゜)",
      "pronunciation_raw": "うつくし゜",
      "reading": "美しい(うつくしい)",
      "reading_raw": "うつくしい",
      "surface": "美しい"
    },
    {
      "lemma": "国",
      "pos": ["名詞",  "普通名詞", "一般", "*"],
      "pronunciation": "国(くに)",
      "pronunciation_raw": "くに",
      "reading": "国(くに)",
      "reading_raw": "くに",
      "surface": "国"
    },
    {
      "lemma": "だ",
      "pos": ["助動詞", "*", "*", "*"],
      "pronunciation": "だ",
      "pronunciation_raw": "だ",
      "reading": "だ",
      "reading_raw": "だ",
      "surface": "だ"
    }
  ]
}
```
### Errors
There are 2 errors that might occur, when the text parameter is empty or it exceeds the 5000 character limit.
Here is the JSON structure for the API errors:
```json
{
  "error": "Description / Details"
}
```

Icon by [freepik](https://www.flaticon.com/de/autoren/freepik)
