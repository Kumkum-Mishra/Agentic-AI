# Streamlit Cloud पर "1/requirements.txt" error ठीक करें

Error आता था क्योंकि पहले path में स्पेस था। अब UI में वो सेक्शन edit करने को मिलता ही नहीं – इसलिए fix सिर्फ repo में सही फाइल रखना है।

---

**Advanced settings में Requirements file नहीं मिलता:** नए UI में वहाँ सिर्फ Python version और Secrets होते हैं। Cloud खुद `requirements.txt` ढूंढता है (पहले ऐप वाले फोल्डर में, फिर repo जड़ पर)। इसलिए **नया deploy मत बनाओ** – बस नीचे वाला कदम करो।

---

## 2. जाँच करें कि repo की जड़ पर फाइल है

GitHub पर जाएं:  
`https://github.com/Kumkum-Mishra/Agentic-AI`

वहाँ **जड़** पर (Assessment 1 के बाहर) एक फाइल **`requirements.txt`** दिखनी चाहिए। अगर नहीं दिखती तो लोकल में ये चलाएं और push करें:

```bash
cd "K:\GitHub\Agentic-AI"
git add requirements.txt
git status
git commit -m "Add requirements at root for Cloud"
git push origin main
```

---

## संक्षेप

- **Advanced settings** में Requirements file का फील्ड नहीं होता – edit करने की जरूरत नहीं।
- **GitHub repo की जड़** पर `requirements.txt` होनी चाहिए (Assessment 1 के बाहर)। Cloud पहले ऐप वाले फोल्डर में ढूंढता है, फिर जड़ पर – Assessment 1 में अब requirements.txt नहीं है तो जड़ वाली use होगी।
- पुरानी ऐप पर **Reboot app** करो; नया deploy बनाना जरूरी नहीं।
