# modules
import numpy as np
import pandas as pd
from io import StringIO
from datetime import date, timedelta
import streamlit as st
import plotly.express as px


st.title('OPEN COVID (FR) DATASET')

"""
## Données nationales concernant l'épidémie de COVID19
### Sources

* Santé publique France
* Chiffres clés et cas par région
* Données GÉODES
* Agences Régionales de Santé
* Préfectures
* Ministère des Solidarités et de la Santé
* Vidéos / Vidéos en direct
* Points de situation (vidéos + PDF)
* Communiqués de presse

[dépôt des données](https://github.com/opencovid19-fr/data)

---
"""

# Load data
@st.cache(suppress_st_warning=True)
def load_data():
    data = 'https://github.com/opencovid19-fr/data/raw/master/dist/chiffres-cles.csv'
    df0 = pd.read_csv(data, sep=",", low_memory=False)
    # format date
    df0['date'] = df0['date'].str.replace('_','-')
    df0['date'] = pd.to_datetime(df0['date'], errors='coerce')
    return df0

df = load_data()



# gps dict
d_gps = {'France': [46.603354, 1.8883335], 'Charente': [45.6667902, 0.09730504409848517], 'Charente-Maritime': [45.73022675, -0.7212875872563794], 'Corrèze': [45.342904700000005, 1.8176424406120555], 'Creuse': [46.0593485, 2.04890101251091], 'Dordogne': [45.14291985, 0.6321258058651044], 'Gironde': [44.883745950000005, -0.6051264440438711], 'Landes': [44.00996945, -0.6433872354467377], 'Lot-et-Garonne': [44.3691703, 0.45391575832487524], 'Pyrénées-Atlantiques': [43.18718655, -0.728247400084667], 'Deux-Sèvres': [46.53914, -0.29947849341978416], 'Vienne': [46.612116549999996, 0.4654070096639711], 'Haute-Vienne': [45.91901925, 1.203176771876291], 'Île-de-France': [48.6443057, 2.7537863], 'Nouvelle-Aquitaine': [45.4039367, 0.3756199], 'Monde': [44.9863862, 4.5729027], 'Hérault': [43.591422, 3.3553309364095925], 'Haute-Savoie': [46.068820849999994, 6.344536991587102], 'Auvergne-Rhône-Alpes': [45.2968119, 4.6604809], 'Bourgogne-Franche-Comté': [47.0510946, 5.0740568], 'Aisne': [49.453285449999996, 3.606899003594057], 'Doubs': [47.06699155, 6.235622772820445], 'Nord': [50.52896715, 3.0883523694464854], 'Oise': [49.41205455, 2.406487846905477], 'Pas-de-Calais': [50.5144061, 2.258007849773996], 'Somme': [49.96897145, 2.373858954610659], 'Territoire de Belfort': [47.62923095, 6.899301156710882], 'Hauts-de-France': [50.1024606, 2.7247515], 'Grand Est': [48.4845157, 6.113035], "Côte-d'Or": [47.465503350000006, 4.74812234575117], 'Finistère': [48.24511525, -4.044090245241742], 'Loire-Atlantique': [47.34816145, -1.8727461214619257], 'Bas-Rhin': [48.5991783, 7.533818624332648], 'Alpes-Maritimes': [43.9210587, 7.1790785], 'Maine-et-Loire': [47.38863045, -0.3909097146387368], 'Mayenne': [48.1507819, -0.6491273812007092], 'Seine-Maritime': [49.66323745, 0.9401133910609153], 'Guadeloupe': [16.230510250000002, -61.68712602138846], 'Martinique': [14.6367927, -61.01582685063731], 'Guyane': [4.0039882, -52.999998], 'La Réunion': [-21.130737949999997, 55.536480112992315], 'Mayotte': [-12.8253862, 45.148626111147614], 'Centre-Val de Loire': [47.5490251, 1.7324062], 'Normandie': [49.0677708, 0.3138532], 'Pays de la Loire': [47.6594864, -0.8186143], 'Bretagne': [48.2640845, -2.9202408], 'Occitanie': [43.6487851, 2.3435684], "Provence-Alpes-Côte d'Azur": [44.0580563, 6.0638506], 'Corse': [42.188089649999995, 9.068413771427695], 'Ille-et-Vilaine': [48.17276805, -1.6498092420681134], 'Saint-Barthélemy': [17.9036287, -62.811568843006896], 'Saint-Martin': [48.5683066, 6.7539988], 'Morbihan': [47.825981150000004, -2.7633492695588253], 'Sarthe': [48.026928749999996, 0.2538217482247317], 'Ain': [49.453285449999996, 3.606899003594057], 'Ardennes': [49.69801175, 4.671600518245179], 'Aube': [48.3201921, 4.1905396615047525], 'Eure': [49.0756358, 0.9652025944774796], 'Marne': [48.961264, 4.31224359285714], 'Haute-Marne': [48.1329414, 5.252910789751933], 'Meurthe-et-Moselle': [48.95596825, 5.987038299756556], 'Meuse': [49.01296845, 5.428669076639772], 'Moselle': [49.0207259, 6.538035170357949], 'Haut-Rhin': [47.8654746, 7.231543347579764], 'Rhône': [45.8802348, 4.564533629559522], 'Vosges': [48.16378605, 6.382071173595532], 'Allier': [46.36746405, 3.163882848311948], 'Ardèche': [44.815194000000005, 4.3986524702343965], 'Cantal': [45.0497701, 2.699717567737356], 'Drôme': [44.72964575, 5.204559599996514], 'Gard': [43.95995, 4.297637002377168], 'Isère': [45.28979315, 5.634382477386232], 'Loire': [45.75385355, 4.045473682551104], 'Haute-Loire': [45.085724850000005, 3.833826117673291], 'Puy-de-Dôme': [45.7715343, 3.0839934206717934], 'Saône-et-Loire': [46.6557086, 4.55855481835173], 'Savoie': [45.494895150000005, 6.384660381375652], 'Aveyron': [44.315857449999996, 2.5065697302419823], 'Bouches-du-Rhône': [43.5424182, 5.034323560504859], "Côtes-d'Armor": [48.458422150000004, -2.7505868346107736], 'Eure-et-Loir': [48.4474102, 1.3998820185020766], 'Indre-et-Loire': [47.2232046, 0.6866702523286876], 'Haute-Saône': [47.63842335, 6.095114088932768], 'Vaucluse': [43.993864349999996, 5.1818898389002355], 'Hautes-Alpes': [44.6564666, 6.352024584507948], 'Calvados': [49.09076485, -0.24139505722798021], 'Cher': [47.024882399999996, 2.5753333606655704], 'Corse-du-Sud': [41.87340825, 9.0087052196875], 'Haute-Corse': [42.42196975, 9.100906549656115], 'Haute-Garonne': [43.305454600000004, 0.9716791701901577], 'Indre': [46.81210565, 1.5382051557056249], 'Loir-et-Cher': [47.65977515, 1.297183525390464], 'Loiret': [47.9140388, 2.3073794620675887], 'Manche': [49.091895199999996, -1.2454370607545526], 'Paris': [48.8566969, 2.3514616], 'Seine-et-Marne': [48.61902069999999, 3.0418157506708345], 'Yvelines': [48.76203735, 1.8871375621264361], 'Var': [43.4173592, 6.2664620128919], 'Essonne': [48.53034015, 2.239291805668168], 'Hauts-de-Seine': [48.840185899999994, 2.198641221906077], 'Seine-Saint-Denis': [48.9098125, 2.4528634784461856], 'Val-de-Marne': [48.774489349999996, 2.4543321444588204], "Val-d'Oise": [49.07507045, 2.209811443668384], 'Jura': [46.783362499999996, 5.783285726354901], 'Lot': [44.624991800000004, 1.6657742169753669], 'Tarn': [43.7921741, 2.133964772269535], 'Tarn-et-Garonne': [44.080656000000005, 1.2050632958700225], 'Vendée': [46.5040559, -0.7479592], 'Yonne': [47.85512575, 3.6450439257238765], 'Aude': [43.0542733, 2.512471457499548], 'Nièvre': [47.11969705, 3.5448897947227174], 'Orne': [48.57605325, 0.04466171759588161], 'Alpes-de-Haute-Provence': [44.1640832, 6.187851538609079], 'Gers': [43.695527600000005, 0.4101019175237992], 'Polynésie française': [-16.03442485, -146.0490931059517], 'Hautes-Pyrénées': [43.1437925, 0.15866611287926924], 'Pyrénées-Orientales': [42.625894, 2.5065089946931507], 'Lozère': [44.5425706, 3.521114648333333], 'Ariège': [42.9455368, 1.4065544156065486], 'Nouvelle-Calédonie': [-20.454288599999998, 164.55660583077983], 'Wallis et Futuna': [-13.289402, -176.204224]}

#update df with lat/lon coordinates
for area in df['maille_nom'].unique():
    dfd = df.copy()
    mask = (dfd['maille_nom'] == area)
    df.loc[mask,'lat'] = d_gps[area][0]
    df.loc[mask,'lon'] = d_gps[area][1]
    
#create departement granularity
df_depts = df[df['granularite']=='departement']

#fill na with 0
df_depts.loc[:,'nouvelles_hospitalisations'] = df_depts.loc[:,'nouvelles_hospitalisations'].fillna(0)

### STREAMLIT ###
#################

# sidebar
area = st.sidebar.selectbox(
    'Choisissez la zone à étudier',
     df['maille_nom'].sort_values(ascending=True).unique())

"""
## Données nationales


"""

df_france = df[df['maille_nom'] == 'France']

#st display
'Données calculées le :', date.today()
'Nombre de décès (cumulé)', df_france.tail(1)['deces'].values[0]
'Nouvelles hospitalisations', df_france.tail(1)['nouvelles_hospitalisations'].values[0]
'Nouvelles réanimations', df_france.tail(1)['nouvelles_reanimations'].values[0]

"""
#### Tests positifs par 'Tranche d'âge'
##### (National)
"""

#chargement des données
url = 'https://www.data.gouv.fr/fr/datasets/r/19a91d64-3cd3-42fc-9943-d635491a4d76'
df_P = pd.read_csv(url, sep=";", index_col='jour')

# nettoyage des données
df_P = df_P.rename(columns={'cl_age90':'cl_age'})
df_P.cl_age = df_P.cl_age.astype('int')
df_P.dep = df_P.dep.astype('str')
df_P = df_P[(df_P.P == 1) & (df_P.cl_age > 0)]

# graph
'Échantillon de Tests positifs analysés : ',len(df_P)

df_P['cl_age_txt'] = df_P['cl_age'].apply(lambda x:str(x-9)+'-'+str(x))

fig0 = px.bar(df_P['cl_age_txt'].value_counts())
st.plotly_chart(fig0)

"""
#### France : Évolution des 'Nouvelles hospitalisations'
##### (animation)
"""
df_anim = df_depts
df_anim['dt_str'] = df_anim['date'].apply(lambda x: x.strftime("%d-%b-%Y"))

col1, col2 = st.beta_columns(2)

date1 = col1.date_input('Date de début')
date2 = col2.date_input('Date de fin')
df_anim = df_anim[(df_anim['date'] >= pd.to_datetime(date1)) & (df_anim['date'] <= pd.to_datetime(date2))]

try:
	fig1= px.scatter_mapbox(df_anim, lat="lat", lon="lon", 
						size="nouvelles_hospitalisations", hover_name="maille_nom",
						animation_frame="dt_str", 
						zoom=4, center={'lat':48.862725,'lon':2.287592}, 
						height=800,
						mapbox_style="open-street-map")

	st.plotly_chart(fig1)
except KeyError:
	st.write('Dates incorrectes')

"""
## Données sur la 'zone' sélectionnée
"""

# st_display
'Vous avez choisi: ', area

# création du df_area
df_area = df[df['maille_nom'] == area]

'Données calculées le :', date.today()
'Nombre de décès (cumulé)', df_area.tail(1)['deces'].values[0]
'Nouvelles hospitalisations', df_area.tail(1)['nouvelles_hospitalisations'].values[0]
'Nouvelles réanimations', df_area.tail(1)['nouvelles_reanimations'].values[0]

# plotly chart 1
df_last10 = df_area.tail(10)
df1 = df_last10.melt(id_vars='date', value_vars=['nouvelles_hospitalisations', 'nouvelles_reanimations'])
fig1 = px.line(df1, x='date' , y='value' , color='variable')

# plotly chart 2
df2 = df_area.melt(id_vars='date', value_vars=['deces','hospitalises'])
fig2 = px.line(df2, x='date' , y='value' , color='variable')

# plotly chart 3
df3 = df_area
fig3 = px.line(df3, x='date', y='reanimation')


"""
#### Les 10 derniers jours (Nouvelles hospitalisations, Nouvelles réanimations) 
##### par zone:
"""
area

# fig 1 : hosp/reas last10 days
st.plotly_chart(fig1)

"""
#### Décès, Hospitalisés 
##### par zone:
"""
area

# fig2 : ['deces','hospitalises']
st.plotly_chart(fig2)

"""
#### Réanimations
##### par zone:
"""
area

# fig3 : ['reanimation']
st.plotly_chart(fig3)