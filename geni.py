import streamlit as st
import requests
import urllib.parse

st.title("🔑 Geni Avaimen Hakija (Lomakeversio)")

# Luodaan valtuutuslinkki heti alkuun
app_id_temp = st.text_input("A. Syötä App ID tähän saadaksesi linkin (jos sinulla ei ole vielä uutta koodia)")
callback_url_temp = st.text_input("B. Syötä Callback URL tähän (esim. https://sovellus.streamlit.app/)")

if app_id_temp and callback_url_temp:
    safe_callback = urllib.parse.quote(callback_url_temp, safe='')
    auth_url = f"https://www.geni.com/platform/oauth/authorize?client_id={app_id_temp}&response_type=code&redirect_uri={safe_callback}"
    st.markdown(f"**👉 [KLIKKAA TÄSTÄ HAKEAKSESI UUDEN KOODIN OSOITERIVILLE]({auth_url})**")

st.markdown("---")
st.write("Kun olet saanut uuden koodin osoiteriville, täytä alla oleva lomake. Streamlit ei nyt päivitä sivua kesken kaiken.")

# Lukittu lomake alkaa
with st.form("geni_form"):
    app_id = st.text_input("1. Geni App ID")
    app_secret = st.text_input("2. Geni App Secret", type="password")
    callback_url = st.text_input("3. Callback URL (Täsmälleen sama kuin yllä)")
    auth_code = st.text_input("4. Liitä uusi 'code=' tähän")
    
    # Tämä nappi lähettää tiedot vasta kun sitä painetaan
    submit_button = st.form_submit_button("Hae lopullinen Geni Token")

if submit_button:
    if app_id and app_secret and callback_url and auth_code:
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
            st.success("🎉 LOPULTAKIN ONNISTUI! Tässä on avaimesi:")
            st.code(token_data.get("access_token"))
        else:
            st.error("Geni hylkäsi pyynnön.")
            st.write(response.json())
    else:
        st.warning("Täytä lomakkeen kaikki neljä kenttää ennen lähetystä.")
