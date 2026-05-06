import streamlit as st
import requests

st.title("🔑 Geni Avaimen Hakija (Väliaikainen työkalu)")

app_id = st.text_input("1. Syötä Geni App ID")
app_secret = st.text_input("2. Syötä Geni App Secret", type="password")

if app_id and app_secret:
    # Luodaan valtuutuslinkki
    auth_url = f"https://www.geni.com/platform/oauth/authorize?client_id={app_id}&response_type=code"
    
    st.markdown("---")
    st.markdown(f"**Vaihe 3:** [**👉 KLIKKAA TÄSTÄ ANTAAKSESI SOVELLUKSELLE LUVAN LUKEA GENIÄ**]({auth_url})")
    
    st.info("💡 **Ohje:** Kun olet klikannut yllä olevaa linkkiä ja painanut Genissä 'Authorize', sinut ohjataan takaisin omaan sovellukseesi. **Katso selaimen yläreunan osoiteriviä!** Osoitteen perässä lukee nyt `?code=jotain...`. Kopioi tuo koodi ja liitä se alle.")

    auth_code = st.text_input("4. Liitä osoiteriviltä kopioimasi 'code' tähän")

    if auth_code:
        if st.button("Hae lopullinen Geni Token"):
            # Vaihdetaan koodi varsinaiseen tokeniin
            token_url = "https://www.geni.com/platform/oauth/request_token"
            payload = {
                "client_id": app_id,
                "client_secret": app_secret,
                "code": auth_code
            }
            response = requests.post(token_url, data=payload)
            
            if response.status_code == 200:
                token_data = response.json()
                st.success("🎉 ONNISTUI! Tässä on lopullinen avaimesi:")
                st.code(token_data.get("access_token"))
                st.write("1. Kopioi yllä oleva koodi talteen.")
                st.write("2. Lisää se Streamlitin asetuksiin (Secrets) nimellä `GENI_ACCESS_TOKEN`.")
                st.write("3. Palauta alkuperäinen Tarinakone-koodi takaisin `geni.py` -tiedostoon!")
            else:
                st.error("Virhe. Koodi saattoi vanhentua tai Genin Callback URL -asetus ei täsmää.")
                st.write(response.text)
