import pandas as pd
from pathlib import Path

def normalize_country_name(name, mapping):
    """Normalise le nom du pays en anglais"""
    name = name.strip()
    if name in mapping:
        return mapping[name]
    return name

# Dictionnaire complet de normalisation des noms de pays (en anglais)
country_mapping = {
    # Variantes françaises
    "Moldavie": "Moldova",
    "Lituanie": "Lithuania",
    "Tchéquie": "Czech Republic",
    "Allemagne": "Germany",
    "Irlande": "Ireland",
    "Luxembourg": "Luxembourg",
    "Lettonie": "Latvia",
    "Bulgarie": "Bulgaria",
    "Roumanie": "Romania",
    "Slovénie": "Slovenia",
    "France": "France",
    "Portugal": "Portugal",
    "Belgique": "Belgium",
    "Russie": "Russia",
    "Pologne": "Poland",
    "Estonie": "Estonia",
    "Autriche": "Austria",
    "Slovaquie": "Slovakia",
    "Hongrie": "Hungary",
    "Croatie": "Croatia",
    "Grèce": "Greece",
    "Chypre": "Cyprus",
    "Italie": "Italy",
    "Espagne": "Spain",
    "Suisse": "Switzerland",
    "Suède": "Sweden",
    "Norvège": "Norway",
    "Danemark": "Denmark",
    "Finlande": "Finland",
    "Islande": "Iceland",
    "Pays-Bas": "Netherlands",
    "Royaume-Uni": "United Kingdom",
    "Costa Rica": "Costa Rica",
    "Nouvelle-Zélande": "New Zealand",
    "Australie": "Australia",
    "États-Unis": "United States",
    "Canada": "Canada",
    "Mexique": "Mexico",
    "Argentine": "Argentina",
    "Brésil": "Brazil",
    "Chili": "Chile",
    "Colombie": "Colombia",
    "Venezuela": "Venezuela",
    "Pérou": "Peru",
    "Équateur": "Ecuador",
    "Paraguay": "Paraguay",
    "Uruguay": "Uruguay",
    "Bolivie": "Bolivia",
    "Guyane": "Guyana",
    "Surinam": "Suriname",
    "Afrique du Sud": "South Africa",
    "Égypte": "Egypt",
    "Éthiopie": "Ethiopia",
    "Algérie": "Algeria",
    "Maroc": "Morocco",
    "Tunisie": "Tunisia",
    "Libye": "Libya",
    "Soudan": "Sudan",
    "Tanzanie": "Tanzania",
    "Kenya": "Kenya",
    "Cameroun": "Cameroon",
    "Côte d'Ivoire": "Ivory Coast",
    "Ghana": "Ghana",
    "Sénégal": "Senegal",
    "Zambie": "Zambia",
    "Zimbabwe": "Zimbabwe",
    "Malawi": "Malawi",
    "Mozambique": "Mozambique",
    "Angola": "Angola",
    "Pakistan": "Pakistan",
    "Afghanistan": "Afghanistan",
    "Bangladesh": "Bangladesh",
    "Inde": "India",
    "Népal": "Nepal",
    "Sri Lanka": "Sri Lanka",
    "Thaïlande": "Thailand",
    "Laos": "Laos",
    "Cambodge": "Cambodia",
    "Vietnam": "Vietnam",
    "Chine": "China",
    "Japon": "Japan",
    "Corée du Sud": "South Korea",
    "Corée du Nord": "North Korea",
    "Mongolie": "Mongolia",
    "Malaisie": "Malaysia",
    "Indonésie": "Indonesia",
    "Philippines": "Philippines",
    "Birmanie": "Myanmar",
    "Turquie": "Turkey",
    "Irak": "Iraq",
    "Iran": "Iran",
    "Syrie": "Syria",
    "Liban": "Lebanon",
    "Israël": "Israel",
    "Jordanie": "Jordan",
    "Arabie Saoudite": "Saudi Arabia",
    "Émirats arabes unis": "United Arab Emirates",
    "Émirats Arabes Unis": "United Arab Emirates",
    "Qatar": "Qatar",
    "Bahreïn": "Bahrain",
    "Oman": "Oman",
    "Yémen": "Yemen",
    "Koweït": "Kuwait",
    "Azerbaïdjan": "Azerbaijan",
    "Kazakhstan": "Kazakhstan",
    "Ouzbékistan": "Uzbekistan",
    "Tadjikistan": "Tajikistan",
    "Kirghizistan": "Kyrgyzstan",
    "Turkménistan": "Turkmenistan",
    "Géorgie": "Georgia",
    "Arménie": "Armenia",
    "Ukraine": "Ukraine",
    "Biélorussie": "Belarus",
    "Serbie": "Serbia",
    "Bosnie-Herzégovine": "Bosnia and Herzegovina",
    "Monténégro": "Montenegro",
    "Albanie": "Albania",
    "Kosovo": "Kosovo",
    "Malte": "Malta",
    "Guinée équatoriale": "Equatorial Guinea",
    "Gabon": "Gabon",
    "Ouganda": "Uganda",
    "Rwanda": "Rwanda",
    "Burundi": "Burundi",
    "Somalie": "Somalia",
    "Djibouti": "Djibouti",
    "Bénin": "Benin",
    "Togo": "Togo",
    "Mali": "Mali",
    "Mauritanie": "Mauritania",
    "Niger": "Niger",
    "Burkina Faso": "Burkina Faso",
    "Gambie": "Gambia",
    "Guinée-Bissau": "Guinea-Bissau",
    "Guinée": "Guinea",
    "Tchad": "Chad",
    "République centrafricaine": "Central African Republic",
    "Comores": "Comoros",
    "Maurice": "Mauritius",
    "Madagascar": "Madagascar",
    "Haïti": "Haiti",
    "République Dominicaine": "Dominican Republic",
    "Jamaïque": "Jamaica",
    "Trinité-et-Tobago": "Trinidad and Tobago",
    "Cuba": "Cuba",
    "Belize": "Belize",
    "Panama": "Panama",
    "Honduras": "Honduras",
    "Nicaragua": "Nicaragua",
    "El Salvador": "El Salvador",
    "Guatemala": "Guatemala",
    "Groenland": "Greenland",
    "Antigua-et-Barbuda": "Antigua and Barbuda",
    "Sainte-Lucie": "Saint Lucia",
    "Grenade": "Grenada",
    "Dominique": "Dominica",
    "Barbade": "Barbados",
    "Saint-Vincent-et-les-Grenadines": "Saint Vincent and the Grenadines",
    "Fidji": "Fiji",
    "Samoa": "Samoa",
    "Kiribati": "Kiribati",
    "Nauru": "Nauru",
    "Papouasie-Nouvelle-Guinée": "Papua New Guinea",
    "Îles Marshall": "Marshall Islands",
    "Îles Salomon": "Solomon Islands",
    "Vanuatu": "Vanuatu",
    "Tonga": "Tonga",
    "Tuvalu": "Tuvalu",
    "Seychelles": "Seychelles",
    "Andorre": "Andorra",
    "Liechtenstein": "Liechtenstein",
    "Saint-Marin": "San Marino",
    "Lesotho": "Lesotho",
    "Eswatini": "Eswatini",
    "Botswana": "Botswana",
    "Namibie": "Namibia",
    "Soudan du Sud": "South Sudan",
    "République démocratique du Congo": "Democratic Republic of the Congo",
    "Maldives": "Maldives",
    "Timor oriental": "East Timor",
    "Brunei": "Brunei",
    "Singapour": "Singapore",
    "Taïwan": "Taiwan",
    "Hong Kong": "Hong Kong",
    "Erythrée": "Eritrea",
    "Liberia": "Liberia",
    "Sierra Leone": "Sierra Leone",
    "Cap-Vert": "Cape Verde",
    "Cabo Verde": "Cape Verde",
    "São Tomé-et-Príncipe": "São Tomé and Príncipe",
    "Mauritius": "Mauritius",
    "Comores": "Comoros",
    
    # Variantes anglaises/autres
    "Czechia": "Czech Republic",
    "Türkiye": "Turkey",
    "Korea Republic": "South Korea",
    "IR Iran": "Iran",
    "Great-Britain": "United Kingdom",
    "Great Britain": "United Kingdom",
    "USA": "United States",
    "DR Congo": "Democratic Republic of the Congo",
    "Congo DR": "Democratic Republic of the Congo",
    "Democratic Republic of Congo": "Democratic Republic of the Congo",
    "Democratic Republic of the Congo": "Democratic Republic of the Congo",
    "Republic of Congo": "Congo",
    "Republic of the Congo": "Congo",
    "République du Congo": "Congo",
    "Congo": "Congo",
    "Federated States of Micronesia": "Micronesia",
    "Saint Kitts and Nevis": "Saint Kitts and Nevis",
    "States fédérés de Micronésie": "Micronesia",
    "États fédérés de Micronésie": "Micronesia",
    "Kingdom of the Netherlands": "Netherlands",
    "Arabie saoudite": "Saudi Arabia",
    "China PR": "China",
    "Myanmar": "Myanmar",
    
    # Doublons supplémentaires
    "Bhoutan": "Bhutan",
    "Erithrea": "Eritrea",
    "Érythrée": "Eritrea",
    "Ile Maurice": "Mauritius",
    "Île Maurice": "Mauritius",
    "Kyrgyz Republic": "Kyrgyzstan",
    "Kyrgyzstan": "Kyrgyzstan",
    "The Bahamas": "Bahamas",
    "Bahamas": "Bahamas",
    "The Gambia": "Gambia",
    "Gambia": "Gambia",
    "Salomon": "Solomon Islands",
    "Solomon Islands": "Solomon Islands",
    "Salvador": "El Salvador",
    "El Salvador": "El Salvador",
    "Palaos": "Palau",
    "Palau": "Palau",
    "St Kitts and Nevis": "Saint Kitts and Nevis",
    "St Lucia": "Saint Lucia",
    "St Vincent and the Grenadines": "Saint Vincent and the Grenadines",
    "Timor-Leste": "East Timor",
    "East Timor": "East Timor",
    "Micronésie": "Micronesia",
    "Micronesia": "Micronesia",
    "Macédoine du Nord": "North Macedonia",
    "North Macedonia": "North Macedonia",
    "République dominicaine": "Dominican Republic",
    "Dominican Republic": "Dominican Republic",
    "République tchèque": "Czech Republic",
    "Czech Republic": "Czech Republic",
    "République de Irlande": "Ireland",
    "Republic of Ireland": "Ireland",
    "Ireland": "Ireland",
    "République de Moldavie": "Moldova",
    "Republic of Moldova": "Moldova",
    "Moldova": "Moldova",
    "Sao Tomé-et-Principe": "São Tomé and Príncipe",
    "São Tomé and Príncipe": "São Tomé and Príncipe",
    "Trinidad & Tobago": "Trinidad and Tobago",
    "Trinidad and Tobago": "Trinidad and Tobago",
    "Viêt Nam": "Vietnam",
    "Vietnam": "Vietnam",
    "Saint-Christophe-et-Niévès": "Saint Kitts and Nevis",
    "Korea DPR": "North Korea",
    "North Korea": "North Korea",
    "Palestine": "Palestine",
}

# Charger tous les fichiers CSV
data_folder = Path("c:/Carthagéo/Geozone/Data")
files = {
    "Alcohol": "Alcohol.csv",
    "Army": "Army.csv",
    "Capital City - Numeric": "Capital City - Numeric.csv",
    "Capital City - Ratio": "Capital City - Ratio.csv",
    "Chinese diaspora": "Chinese diaspora.csv",
    "Density": "Density.csv",
    "EEZ": "EEZ.csv",
    "FIFA": "FIFA.csv",
    "Happiness": "Happiness.csv",
    "Homicide rate": "Homicide rate.csv",
    "HDI": "IDH.csv",
    "Individual GDP": "Individual GDP.csv",
    "Life expectancy": "Life expentancy.csv",
    "Obesity": "Obesity.csv",
    "Olympics": "Olympics.csv",
    "Superficy (asc)": "Superficy (asc).csv",
}

# Dictionnaire pour stocker tous les classements par pays
rankings_data = {}

# Traiter chaque fichier
for col_name, filename in files.items():
    filepath = data_folder / filename
    if filepath.exists():
        print(f"Processing {filename}...")
        df = pd.read_csv(filepath)
        
        # Nettoyer les noms de pays (supprimer les espaces inutiles)
        df['Country'] = df['Country'].str.strip()
        
        # Normaliser les noms de pays
        df['Country'] = df['Country'].apply(lambda x: normalize_country_name(x, country_mapping))
        
        # Ajouter les classements au dictionnaire
        for _, row in df.iterrows():
            country = row['Country']
            rank = row['Rank']
            if country not in rankings_data:
                rankings_data[country] = {}
            rankings_data[country][col_name] = rank
    else:
        print(f"File not found: {filename}")

# Créer le dataframe final
all_countries = sorted(rankings_data.keys())
final_data = []

for country in all_countries:
    row = {"Country": country}
    for col_name in files.keys():
        value = rankings_data[country].get(col_name, "NULL")
        row[col_name] = value
    final_data.append(row)

# Créer le dataframe avec l'ordre des colonnes
columns = ["Country"] + list(files.keys())
result_df = pd.DataFrame(final_data)
result_df = result_df[columns]

# Sauvegarder en CSV
output_path = Path("c:/Carthagéo/Geozone/Rankings.csv")
result_df.to_csv(output_path, index=False, encoding='utf-8')

print(f"\n✓ Fichier Rankings.csv créé avec succès!")
print(f"Nombre de pays: {len(all_countries)}")
print(f"Chemin: {output_path}")
print(f"\nPremières lignes:")
print(result_df.head(15))
print(f"\nTotal: {len(result_df)} pays")
