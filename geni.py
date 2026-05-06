<!DOCTYPE html>
<html lang="fi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Esivanhemman Tarina - SUKU</title>
    <!-- PWA Manifesti -->
    <link rel="manifest" href="/manifest.json">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f4f4f9;
            color: #333;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .header {
            width: 100%;
            background-color: #2c3e50;
            color: white;
            text-align: center;
            padding: 1rem 0;
            font-size: 1.2rem;
        }
        .header a {
            color: #f1c40f;
            text-decoration: none;
            font-weight: bold;
        }
        .container {
            max-width: 600px;
            width: 90%;
            background: white;
            padding: 2rem;
            margin-top: 2rem;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        input[type="text"] {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
        }
        button {
            width: 100%;
            padding: 10px;
            background-color: #27ae60;
            color: white;
            border: none;
            border-radius: 4px;
            font-size: 1.1rem;
            cursor: pointer;
        }
        button:hover {
            background-color: #219653;
        }
        #result {
            margin-top: 2rem;
            line-height: 1.6;
            white-space: pre-wrap; /* Säilyttää kappalejaot */
        }
        .loader {
            display: none;
            text-align: center;
            font-style: italic;
            color: #666;
            margin-top: 10px;
        }
    </style>
</head>
<body>

    <div class="header">
        <a href="https://www.sukulehti.fi" target="_blank">SUKU -lehti | www.sukulehti.fi</a>
    </div>

    <div class="container">
        <h2>Herätä esivanhempasi eloon</h2>
        <p>Liitä alle Geni-profiilin linkki (esim. https://www.geni.com/people/Nimi/123456789) ja tekoäly luo historiallisen tarinan.</p>
        
        <input type="text" id="geniUrl" placeholder="Liitä Geni-URL tähän...">
        <button onclick="generateStory()">Luo tarina</button>
        
        <div id="loader" class="loader">Haetaan tietoja ja kirjoitetaan tarinaa... Tässä voi kestää hetki.</div>
        <div id="result"></div>
    </div>

    <script>
        async function generateStory() {
            const urlInput = document.getElementById('geniUrl').value;
            const resultDiv = document.getElementById('result');
            const loader = document.getElementById('loader');

            if (!urlInput.includes('geni.com/people/')) {
                alert('Tarkista, että syötit kelvollisen Geni-linkin.');
                return;
            }

            // Näytetään latausteksti
            resultDiv.innerHTML = '';
            loader.style.display = 'block';

            try {
                // Kutsutaan Netlify-funktiota
                const response = await fetch('/.netlify/functions/getStory', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ url: urlInput })
                });

                const data = await response.json();

                if (response.ok) {
                    resultDiv.innerHTML = `<h3>Tarina:</h3><p>${data.story}</p>`;
                } else {
                    resultDiv.innerHTML = `<p style="color:red;">Virhe: ${data.error}</p>`;
                }
            } catch (error) {
                resultDiv.innerHTML = `<p style="color:red;">Yhteysvirhe. Yritä myöhemmin uudelleen.</p>`;
            } finally {
                loader.style.display = 'none';
            }
        }

        // PWA Service Workerin rekisteröinti (mahdollistaa asennuksen puhelimeen)
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('/sw.js').catch(err => {
                    console.log('Service Worker rekisteröinti epäonnistui:', err);
                });
            });
        }
    </script>
</body>
</html>
