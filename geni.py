import streamlit as st
import requests
import urllib.parse

st.title("🔑 Geni Avaimen Hakija (Pomminvarma versio)")

app_id = st.text_input("1. Syötä Geni App ID")
app_secret = st.text_input("2. Syötä Geni App Secret", type="password")
callback_url = st.text_input("3. Syötä tarkka Callback URL (Sama kuin Genin asetuksissa, esim. https://minun-sovellus.streamlit.app/)")

if app_id and app_secret and callback_url:
    # Koodataan URL turvalliseen muotoon
    safe_callback = urllib.parse.quote(callback_url, safe='')
    
    # Luodaan valtuutuslinkki, jossa Callback URL on pakotettu
    auth_url = f"https://www.geni.com/platform/oauth/authorize?client_id={app_id}&response_type=code&redirect_uri={safe_callback}"
    
    st.markdown("---")
    st.markdown(f"**Vaihe 4:** [**👉 KLIKKAA TÄSTÄ HAKEAKSESI UUSI KOODI**]({auth_url})")
    
    st.info("💡 **Muista!** Koodi on kertakäyttöinen. Jos sivu latautuu uudelleen, hae aina uusi koodi yllä olevasta linkistä.")

    auth_code = st.text_input("5. Liitä osoiteriviltä uusi 'code=' koodi tähän")

    if auth_code:
        if st.button("Hae lopullinen Geni Token"):
            token_url = "https://www.geni.com/platform/oauth/request_token"
            payload = {
                "client_id": app_id,
                "client_secret": app_secret,
                "code": auth_code,
                "redirect_uri": callback_url
            }
            response = requests.post(token_url, data=payload)
            
            if response.status_code == 200:
                token_data = response.json()
                st.success("🎉 ONNISTUI! Tässä on lopullinen avaimesi:")
                st.code(token_data.get("access_token"))
            else:
                st.error("Edelleen virhe. Tarkista syötteet alta:")
                st.write(response.json())
