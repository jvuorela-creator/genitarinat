import streamlit as st
import requests

# 1. Sivun asetukset
st.set_page_config(page_title="Historiallinen Sukutarina", page_icon="🕰️", layout="centered")

st.title("🕰️ Historiallinen Sukutarina & Aikajana")
st.write("Syötä esivanhemman perustiedot alle. Tekoäly kirjoittaa tarinan ja rakentaa visuaalisen aikajanan, joka sitoo elämänvaiheet Suomen historian suuriin käännekohtiin.")

# 2. Käyttöliittymä ja lomake
with st.form("tiedot_lomake"):
    nimi = st.text_input("Henkilön nimi", placeholder="Esim. Matti Meikäläinen")
    
    col1, col2 = st.columns(2)
    with col1:
        syntymavuosi = st.text_input("Syntymävuosi (tai arvio)", placeholder="esim. 1835")
        syntymapaikka = st.text_input("Synnyinpaikkakunta", placeholder="esim. Nurmijärvi")
    with col2:
        kuolinvuosi = st.text_input("Kuolinvuosi (tai arvio)", placeholder="esim. 1905")
        kuolinpaikka = st.text_input("Kuolinpaikkakunta", placeholder="esim. Helsinki")
        
    ammatti = st.text_input("Ammatti tai sosiaalinen asema", placeholder="esim. Torppari, seppä, piika...")
    
    # Nappi, joka lähettää lomakkeen
    submit = st.form_submit_button("Luo tarina ja aikajana")

# 3. Logiikka tarinan luontiin
if submit:
    # Tarkistetaan, että ainakin vuodet ja ammatit on täytetty (nimi voi periaatteessa puuttua)
    if not syntymavuosi or not kuolinvuosi or not ammatti:
        st.warning("Täytäthän ainakin syntymävuoden, kuolinvuoden ja ammatin!")
    else:
        # Haetaan OpenAI-avain salaisuuksista
        try:
            openai_key = st.secrets["OPENAI_API_KEY"]
        except KeyError:
            st.error("OpenAI API-avain puuttuu Streamlitin asetuksista (Secrets).")
            st.stop()
            
        # Rakennetaan tekoälyn asiantuntijakehote
        prompt = f"""
        LÄHTÖTIEDOT:
        Nimi: {nimi if nimi else "Tuntematon"}
        Elinaika: {syntymavuosi} ({syntymapaikka}) - {kuolinvuosi} ({kuolinpaikka})
        Ammatti: {ammatti}
        
        OHJEET:
        Olet asiantunteva Suomen historian tutkija ja pedagogi. Tehtäväsi on luoda syötettyjen tietojen pohjalta opettavainen ja elävä katsaus henkilön elämään.

        OSA 1: TARINA (3-4 kappaletta)
        Kirjoita mukaansatempaava tarina henkilön elämästä.
        - Sido henkilön arki tiukasti hänen ammattinsa todellisuuteen tuona aikakautena.
        - Analysoi asuinpaikkakuntien (syntymä- ja kuolinpaikka) merkitystä: millainen ympäristö ja elinkeino siellä vallitsi?
        - Kytke hänen elinvuotensa Suomen historian suuriin linjoihin (esim. nälkävuodet, isoviha, Suomen sota, teollistuminen, sortokaudet).
        
        OSA 2: VISUAALINEN AIKAJANA
        Luo tarinan loppuun otsikko "### ⏳ Elämänpolku ja historian käänteet".
        Rakenna sen alle visuaalisesti selkeä aikajana ranskalaisilla viivoilla. 
        Käytä aikajanalla emoji-kuvakkeita ja lihavoituja vuosilukuja.
        Aseta samalle aikajanalle lomittain henkilön kuviteltuja elämänvaiheita (syntymä, aikuistuminen, muutto/kuolema) ja täsmälleen samaan aikaan oikeasti tapahtuneita valtakunnallisia tai paikallisia historiallisia tapahtumia.
        """
        
        # Kutsutaan OpenAI:ta
        with st.spinner("Tekoäly selaa historiankirjoja ja rakentaa aikajanaa... Tässä menee hetki."):
            try:
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {openai_key}"
                }
                payload = {
                    "model": "gpt-4o",
                    "messages": [
                        {"role": "system", "content": "Olet suomalainen historian ja sukututkimuksen asiantuntija."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.5 # Hieman matalampi lämpötila pitää historiallisen faktan tarkempana
                }
                
                response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    tulos = data["choices"][0]["message"]["content"]
                    
                    st.success("Valmista!")
                    st.markdown("---")
                    st.markdown(tulos)
                else:
                    st.error(f"Virhe OpenAI-yhteydessä: {response.text}")
                    
            except Exception as e:
                st.error(f"Sovelluksessa tapahtui odottamaton virhe: {e}")
