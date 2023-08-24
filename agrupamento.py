import requests
import os

api_key = os.environ.get("API-OPENROUTE")
base_url = 'https://api.openrouteservice.org/optimization'

# Dados que entram
sede = [-42.8268461,-5.0700164]
coord_pac_g = [('-5.0835298', '-42.8165683'), ('-5.0651632', '-42.7936305'), ('-5.0442248', '-42.8310981'), ('-5.0502492', '-42.8189285'), ('-5.0395227', '-42.829918'), ('-5.0652146', '-42.7938826'), ('-5.0925823', '-42.7966214'), ('-5.0775346', '-42.8141138'), ('-5.0705826', '-42.8296627'), ('-5.0593186', '-42.8149973'), ('-5.0608146', '-42.7863733'), ('-5.0758626', '-42.7846063'), ('-5.0865104', '-42.8205631'), ('-5.0596706', '-42.8277191'), ('-5.0528064', '-42.8183544'), ('-5.1401542', '-42.7926263'), ('-5.1511816', '-42.7805975'), ('-5.116329', '-42.7546262'), ('-5.1285821', '-42.7840148'), ('-5.0937283', '-42.7479283'), ('-5.1010805', '-42.7393168'), ('-5.1375676', '-42.8032882'), ('-5.1142868', '-42.7989141'), ('-5.1046203', '-42.7611874'), ('-5.092503', '-42.736583')]
coord_pac_p = [('-5.0888927', '-42.8142082'), ('-5.057743', '-42.818781'), ('-5.0653836', '-42.7993096'), ('-5.0340124', '-42.8152407')]

qtd = len(coord_pac_g)
jobs_bigs = [{"id": i+1, "location": [float(lon), float(lat)], "skills":[2]} for i, (lat, lon) in enumerate(coord_pac_g)]
jobs_smalls = [{"id": i+qtd, "location": [float(lon), float(lat)], "skills":[1]} for i, (lat, lon) in enumerate(coord_pac_p)]
jobs = jobs_bigs+jobs_smalls

headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

data = {
    "jobs": jobs,
    "vehicles": [{"id":1,"profile":"driving-car","start":sede,"end":sede},
                 {"id":2,"profile":"driving-car","start":sede,"end":sede},
                 {"id":3,"profile":"driving-car","start":sede,"end":sede}]
}


response = requests.post(base_url, json=data, headers=headers)

if response.status_code == 200:
    optimized_route = response.json()
    print(optimized_route)
else:
    print(f"Request failed with status code: {response.status_code}")
    print(response.text)
