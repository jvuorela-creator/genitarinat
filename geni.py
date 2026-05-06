import streamlit as st
import requests

# 1. Sivun asetukset ja SUKU-lehden yläpalkki
st.set_page_config(page_title="Esivanhemman Tarina - SUKU", page_icon="📜")
st.markdown(
    """
    <div style='text-align: center; background-color: #2c3e50; padding: 15px; margin-bottom: 20px; border-radius: 5px;'>
        <a href='https://www.sukulehti.fi' target='_blank' style='color: #f1c40f; text-decoration: none; font-weight: bold; font-size: 1.2rem;'>SUKU -lehti | www.sukulehti.fi</a>
    </div>
    """, 
    unsafe_allow_html=True
)

st.title("Herätä esivanhempasi eloon")
st.write("Liitä alle Geni-profiilin linkki, niin tekoäly luo faktojen pohjalta elävän historiallisen tarinan.")

# 2. Käyttöliittymän syöttökenttä
geni_url = st.text_input("Geni-URL (esim. https://www.geni.com/people/Nimi/123456789)")

# 3. Logiikka, kun nappia painetaan
if st.button("Luo tarina"):
    if "geni.com/people/" not in geni_url:
        st.error("Tarkista, että syötit kelvollisen Geni-linkin.")
    else:
        with st.spinner("Haetaan tietoja ja kirjoitetaan tarinaa... Tässä voi kestää hetki."):
            try:
                # Erotetaan Geni ID linkistä
                geni_id = geni_url.split("/")[-1]
                
                # Haetaan API-avaimet Streamlitin salaisuuksista (Secrets)
                geni_token = st.secrets["GENI_ACCESS_TOKEN"]
                openai_key = st.secrets["OPENAI_API_KEY"]

                # ==========================================
                # VAIHE A: Haetaan tiedot Genistä
                # ==========================================
              # ==========================================
                # VAIHE A: Haetaan tiedot Genistä
                # ==========================================
                
                # 1. SIIVOTAAN URL: Poistetaan kaikki kysymysmerkin jälkeinen "roska"
                puhdas_url = geni_url.split("?")[0]
                
                # 2. Poimitaan varsinainen ID
                geni_id = puhdas_url.split("/")[-1]
                
                headers = {"Authorization": f"Bearer {geni_token}", "Accept": "application/json"}
                api_url = f"https://www.geni.com/api/{geni_id}"
                
                response = requests.get(api_url, headers=headers)
                
                if response.status_code != 200:
                    # Näytetään tarkempi virheviesti, joka auttaa vianetsinnässä
                    st.error(f"Geni-tietojen haku epäonnistui (Virhekoodi: {response.status_code}).")
                    st.write(f"Yritettiin hakea tunnuksella: {geni_id}")
                    st.write("Varmista, että profiili on julkinen ja API-avain on voimassa.")
                    st.stop()

                # ==========================================
                # VAIHE B: Rakennetaan kehotus (Prompt)
                # ==========================================
                prompt = f"""
ROOLI:
Olet asiantunteva Suomen historian tutkija, paikallishistorian asiantuntija ja kokenut sukututkija. Tehtäväsi on muuttaa kuivat sukututkimusfaktat eläväksi, kunnioittavaksi ja historiallisesti tarkaksi tarinaksi, joka auttaa lukijaa ymmärtämään esivanhempansa arkea.

LÄHTÖTIEDOT (Syötteet):
Nimi: {nimi}
Elinaika: {syntyma} - {kuolema}
Ammatti / Sosiaalinen asema: {ammatti}
Tärkeimmät asuinpaikat: {asuinpaikat}
Perhe: {perhe}

OHJEET TARINAN KIRJOITTAMISEEN:
1. Paikallinen ja alueellinen konteksti (TÄRKEIN): Analysoi annetut asuinpaikat ja sijoita tarina oikeaan Suomen historialliseen maakuntaan. Kuvaile kyseisen alueen tyypillistä elinkeinoa, luontoa ja kulttuuria.
2. Aikakauden suuret linjat: Suhteuta henkilön elinvuodet Suomen historian suuriin käännekohtiin.
3. Ammatti ja arjen kuvaus: Mitä kyseisen ammatin/aseman edustaja teki työkseen kyseisellä vuosisadalla?
4. Tyyli ja sävy: Kirjoita mukaansatempaavaa, rikasta ja elävää suomen kieltä. Älä keksi henkilölle tekoja, joita ei ole syötteessä.
5. Rakenne: Jaa tarina 3-4 selkeään kappaleeseen (Johdanto, Ammatti, Historia, Kuolema ja perintö).
"""

                # ==========================================
                # VAIHE C: Lähetetään tekoälylle (OpenAI)
                # ==========================================
                openai_url = "https://api.openai.com/v1/chat/completions"
                openai_headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {openai_key}"
                }
                openai_payload = {
                    "model": "gpt-4o",
                    "messages": [
                        {"role": "system", "content": "Olet suomalainen historioitsija."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.7
                }
                
                ai_response = requests.post(openai_url, headers=openai_headers, json=openai_payload)
                if ai_response.status_code != 200:
                    st.error(f"Tekoälyn rajapinta palautti virheen: {ai_response.text}")
                    st.stop()
                    
                ai_data = ai_response.json()
                tarina = ai_data["choices"][0]["message"]["content"]
                
                # ==========================================
                # VAIHE D: Näytetään valmis tarina
                # ==========================================
                st.success("Tarinan luonti onnistui!")
                st.markdown("### Tarina:")
                st.write(tarina)
                
            except Exception as e:
                st.error(f"Sovelluksessa tapahtui odottamaton virhe: {e}")
