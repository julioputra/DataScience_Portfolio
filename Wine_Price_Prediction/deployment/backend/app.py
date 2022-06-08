from flask import Flask, jsonify, request
import pickle
import pandas as pd

app = Flask(__name__)

PRICE = [*range(5, 3500, 1)]
columns = ['year', 'rating', 'body', 'type_reduced', 'wine_reduced', 'winery_reduced', 'region_reduced']

with open("winsorizers.pkl", "rb") as a:
    winsorizer = pickle.load(a)

with open("imputer.pkl", "rb") as b:
    imputer = pickle.load(b)

with open("wine_pipe.pkl", "rb") as f:
    model_wine = pickle.load(f)

@app.route("/", methods=["GET", "POST"])
def wine_inference():
    if request.method == 'POST':
        data = request.json
        new_data = [data['year'],
                    data['rating'],
                    data['body'],
                    data['type_reduced'],
                    data['wine_reduced'],
                    data['winery_reduced'],
                    data['region_reduced']]
        new_data = pd.DataFrame([new_data], columns=columns)
        data_winsor = winsorizer.fit_transform(new_data)
        data_imp = imputer.fit_transform(data_winsor)
        res = model_wine.predict(data_imp)
        response = {'code':200, 'status':'OK',
                    'result':{'prediction': str(res[0])}}
        print(response)
        return jsonify(response)
    return "Silahkan gunakan method post untuk mengakses model wine"


   