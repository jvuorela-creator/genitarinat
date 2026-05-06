import streamlit as st
import requests
import urllib.parse

st.set_page_config(page_title="Geni Avain", page_icon="🔑")

# ==========================================
# 1. LAITA OMAT TIETOSI SUORAAN TÄHÄN (lainausmerkkien sisään)
# ==========================================
APP_ID = "2029"
APP_SECRET = "pUV0t2qb0RZhPEFdcuzx6zIT4rd5N1igGrE2XfFO"
CALLBACK_URL = "https://genitarinat.streamlit.app/"

st.title("🔑 Geni Avaimen Hakija (Automaattinen)")

if APP_ID == "LAITA_OMA_APP_ID_TÄHÄN":
    st.warning("Muokkaa koodiin omat tietosi (App ID, Secret ja osoite) ensin!")
    st.stop()

# Luodaan valtuutuslinkki
safe_callback = urllib.parse.quote(CALLBACK_URL, safe='')
auth_url = f"https://www.geni.com/platform/oauth/authorize?client_id={APP_ID}&response_type=code&redirect_uri={safe_callback}"

st.markdown(f"### 👉 [1. KLIKKAA TÄSTÄ ANTAMASSA LUPA]({auth_url})")
st.write("Kun klikkaat linkkiä ja hyväksyt pyynnön, Geni palauttaa sinut tälle sivulle. Koodi hoitaa loput automaattisesti.")

st.markdown("---")

# 2. AUTOMAATTINEN KOODIN SIEPPAUS
# Streamlit lukee osoiterivin automaattisesti kun sivu latautuu uudelleen
if "code" in st.query_params:
    auth_code = st.query_params["code"]
    st.info("Koodi siepattu onnistuneesti osoiteriviltä! Vaihdetaan se avaimeksi...")
    
    token_url = "https://www.geni.com/platform/oauth/request_token"
    payload = {
        "client_id": APP_ID,
        "client_secret": APP_SECRET,
        "code": auth_code,
        "redirect_uri": CALLBACK_URL
    }
    
    response = requests.post(token_url, data=payload)
    
    if response.status_code == 200:
        token_data = response.json()
        st.success("🎉 LOPULTAKIN ONNISTUI! Tässä on lopullinen avaimesi:")
        st.code(token_data.get("access_token"))
        st.write("Ota avain talteen Streamlitin Secrets-asetuksiin! Tämän jälkeen voit palauttaa varsinaisen Tarinakone-koodin tähän tiedostoon.")
        
        # Tyhjennetään osoiterivi, ettei sivu mene jumiin päivitettäessä
        st.query_params.clear()
    else:
        st.error("Geni hylkäsi pyynnön. Varmista koodista, että CALLBACK_URL on täsmälleen sama kuin Genin asetuksissa (esim. kauttaviiva lopussa).")
        st.write(response.json())
        st.query_params.clear()
