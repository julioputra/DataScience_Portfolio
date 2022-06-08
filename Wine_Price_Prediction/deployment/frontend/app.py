import streamlit as st
import requests


st.title("Spanish Wine Price Estimator")
year = st.number_input('How vintage is this wine? Please input the year of the wine production', min_value=1900, max_value=2022)
rating = st.slider('How would you rate the wine?', 0.0, 5.0)
body = st.slider('How is the richness of the wine?', 0.0, 5.0)
type_reduced = st.selectbox('What is the type of the wine?', ('Rioja Red', 'Ribera Del Duero Red', 'Red', 'Priorat Red','Other'))
wine_reduced = st.selectbox('What is the name of the wine?', ('Tinto', 'Vina El Pison', 'Unico',
                                                                'Unico Reserva Especial Edicion', 'Pingus',
                                                                "L'Ermita Velles Vinyes Priorat", 'Valbuena 5o', 'Cami Pesseroles',
                                                                'Priorat', 'Gran Reserva',
                                                                'Castillo Ygay Gran Reserva Especial Tinto', 'Ribera del Duero',
                                                                'Flor de Pingus', 'Dalmau Rioja', 'Reserva', 'Rioja Gran Reserva',
                                                                'Toro', 'Rioja Reserva', 'Clos Martinet', 'Finca Dofi',
                                                                'Coleccion Privada', 'Rioja Gran Reserva 904', 'Valdegines',
                                                                'Roda I Reserva Rioja', 'El Viejo', 'Rioja Blanco',
                                                                'Clos del Portal Somni', 'El Puntido', 'Gran Reserva Rioja',
                                                                'Mirto', 'Finca Terrerazo', 'Rioja Graciano', 'Altos de Losada',
                                                                'Vina Alberdi Crianza', 'Corimbo I', 'Preludio', 'Santa Rosa',
                                                                'Roc Nu', 'Rias Baixas Albarino Finca Valinas', 'Treixadura',
                                                                'Nounat', 'Les Brugueres','Other'))
winery_reduced = st.selectbox('What is the Winery?', ('Contino',
                                                        'Artadi',
                                                        'La Rioja Alta',
                                                        'Sierra Cantabria',
                                                        'Matarromera',
                                                        'Vina Pedrosa',
                                                        'Imperial',
                                                        'Losada',
                                                        'Sei Solo',
                                                        'Portal del Priorat',
                                                        'Ramon Bilbao',
                                                        'Matsu',
                                                        'La Vicalanda',
                                                        "Conreria d'Scala Dei",
                                                        'Campillo',
                                                        'Bodegas La Horra',
                                                        'Mustiguillo',
                                                        'Mar de Frades',
                                                        'Enrique Mendoza',
                                                        'Clos Pons',
                                                        'Ramon do Casar',
                                                        'Binigrau',
                                                        'Vinedos de Paganos',
                                                        'Vega Sicilia',
                                                        'Remirez de Ganuza',
                                                        'Alvaro Palacios',
                                                        'Marques de Murrieta',
                                                        'Dominio de Pingus',
                                                        'Martinet',
                                                        'Abadia Retuerta',
                                                        'Vina Sastre',
                                                        'Other'))
region_reduced = st.selectbox('What is the region of the wine?', ('Rioja','Ribera del Duero','Priorato','Toro','Vino de Espana','Rias Baixas','Bierzo','Mallorca','Other'))
# inference
data = {'year': year,
        'rating': rating,
        'body': body,
        'type_reduced': type_reduced,
        'wine_reduced': wine_reduced,
        'winery_reduced': winery_reduced,
        'region_reduced': region_reduced}

URL = "https://h8-ml2-backend-julio.herokuapp.com/"

# komunikasi
r = requests.post(URL, json=data)
res = r.json()
if res['code'] == 200:
    st.title(res['result']['prediction'])