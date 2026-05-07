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
             # ==========================================
               # ==========================================
                # VAIHE A: Haetaan tiedot Genistä
                # ==========================================
                
                puhdas_url = geni_url.split("?")[0]
                raaka_id = puhdas_url.split("/")[-1]
                
                # KORJAUS: Genin pitkät GUID-tunnukset vaativat eteen 'profile-g'
                if raaka_id.isdigit() and len(raaka_id) > 10:
                    geni_id = f"profile-g{raaka_id}"
                elif not raaka_id.startswith("profile-"):
                    geni_id = f"profile-{raaka_id}"
                else:
                    geni_id = raaka_id
                
                headers = {"Authorization": f"Bearer {geni_token}", "Accept": "application/json"}
                api_url = f"https://www.geni.com/api/{geni_id}"
                
                response = requests.get(api_url, headers=headers)
                
                if response.status_code != 200:
                    st.error(f"Geni-tietojen haku epäonnistui (Virhekoodi: {response.status_code}).")
                    st.stop()
                    
                profile = response.json()
                
                # TARKISTUS: Jos Geni palautti tyhjää ("results": [])
                if "results" in profile and len(profile["results"]) == 0:
                    st.error("Geni palautti tyhjän tiedoston.")
                    st.warning("Tämä tarkoittaa yleensä sitä, että profiili on Genissä yksityinen (Private), eikä ohjelmointirajapinnalla ole siihen lukuoikeutta. Kokeile hakea jotain varmasti julkista (Public) esivanhempaa 1800-luvulta!")
                    st.stop()
                
                # TARKISTUS: Onko kyseessä varmasti yksityinen profiili?
                if profile.get("is_private") == True and "name" not in profile:
                    st.error("Tämä on yksityinen profiili (Private). Geni ei salli yksityisten tietojen lukemista ulkoisiin sovelluksiin.")
                    st.stop()
                
                # Poimitaan faktat
                nimi = profile.get("name", "Tuntematon")
                
                birth_data = profile.get("birth", {})
                birth_date = birth_data.get("date", {}).get("formatted_date", "?")
                birth_place = birth_data.get("location", {}).get("place_name", "")
                syntyma = f"{birth_date} {birth_place}".strip()
                
                death_data = profile.get("death", {})
                death_date = death_data.get("date", {}).get("formatted_date", "?")
                death_place = death_data.get("location", {}).get("place_name", "")
                kuolema = f"{death_date} {death_place}".strip()
                
                ammatti = profile.get("occupation", "Tuntematon asema")
                asuinpaikat = profile.get("location", {}).get("place_name", "?")
                perhe = "Puoliso ja lapset (jos kirjattu Geniin)."

                # ==========================================
                # NÄYTETÄÄN HAETUT FAKTAT RUUDULLA
                # ==========================================
                st.info("💡 **Geni-rajapinnan onnistuneesti löytämät faktat:**")
                st.write(f"**Nimi:** {nimi}")
                st.write(f"**Elinaika:** {syntyma} - {kuolema}")
                st.write(f"**Ammatti:** {ammatti}")
                st.write(f"**Paikkakunnat:** {asuinpaikat}")
                st.markdown("---")
# ==========================================
                # NÄYTETÄÄN HAETUT FAKTAT RUUDULLA
                # ==========================================
                st.info("💡 **Tekoälylle lähetettävät faktat:**")
                st.write(f"**Nimi:** {nimi}")
                st.write(f"**Elinaika:** {syntyma} - {kuolema}")
                st.write(f"**Ammatti:** {ammatti}")
                st.write(f"**Paikkakunnat:** {asuinpaikat}")
                st.markdown("---")
                # ==========================================
                # VAIHE B: Rakennetaan kehotus (Prompt)
                # ==========================================
               # ==========================================
                # VAIHE B: Rakennetaan kehotus (Prompt)
                # ==========================================
                prompt = f"""
ROOLI:
Olet asiantunteva Suomen historian tutkija ja kokenut sukututkija. Tehtäväsi on muuttaa kuivat sukututkimusfaktat eläväksi tarinaksi.

LÄHTÖTIEDOT (Syötteet):
Nimi: {nimi}
Elinaika: {syntyma} - {kuolema}
Ammatti / Sosiaalinen asema: {ammatti}
Tärkeimmät asuinpaikat: {asuinpaikat}
Perhe: {perhe}

OHJEET TARINAN KIRJOITTAMISEEN:
0. PÄÄHENKILÖ (KRIITTINEN SÄÄNTÖ): Tarinan on ehdottomasti keskityttävä henkilöön nimeltä {nimi}. Sido hänen nimensä, elämänvaiheensa ja ammattinsa kiinteästi osaksi jokaista kappaletta. Älä kirjoita yleistä historian oppituntia, vaan kuvaa nimenomaan {nimi}-nimisen ihmisen mahdollista arkea tässä historiallisessa viitekehyksessä.
1. Paikallinen konteksti: Analysoi annetut asuinpaikat ja sijoita tarina oikeaan Suomen historialliseen maakuntaan. Kuvaile, miten alueen luonto ja kulttuuri vaikuttivat suoraan hänen ({nimi}) elämäänsä.
2. Ammatti ja arki: Jos ammatti on tiedossa, kerro konkreettisesti, mitä hän teki työkseen. Jos ammattia ei ole, kuvaa tyypillistä tuon ajan maalais- tai kaupunkilaisarkea hänen asuinseudullaan.
3. Aikakausi: Suhteuta hänen elinvuotensa Suomen historian suuriin käännekohtiin (esim. nälkävuodet, sodat) ja pohdi, miten ne ehkä koskettivat hänen perhettään.
4. Tyyli: Kirjoita rikasta, empaattista ja elävää suomea. Älä keksi hänelle valheellisia tekoja, vaan käytä ilmaisuja kuten "{nimi} on saattanut nähdä..." tai "Hänen päiviinsä kuului todennäköisesti...".
5. Muista: Suomi oli osa Ruotsia vuoteen 1809 ja autonominen osa Venäjää vuosina 1809-1917.
6. Konteksti: Yritä päätellä henkilön etunimestä kyseisen nimen taustaa ja kirjoita siitä lyhyesti.
7. Käytä hyödyksi Wikipediaa, jotta voit sitoa henkilön tarinan hänen elinaikaansa
8. Älä koskaan oleta henkilön varallisuutta tai luonteenpiirteitä. Jos ammattia ei ole mainittu, kuvaa ainoastaan alueen yleisiä elinkeinoja.

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
                    "temperature": 0.4
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
