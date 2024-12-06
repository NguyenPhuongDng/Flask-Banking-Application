"""
This is a Banking Application to predict wherether any new person
seeking loans will default or NOT. This app takes the following
inputs to predict the result:
['income', 'othdebt', 'debtinc', 'creddebt', 'employ']
"""

import pickle
import pandas as pd
from flask import Flask, render_template, request

with open("SVM_model_Banking_Application.pkl", "rb") as source:
    model = pickle.load(source)

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    """
    Defining the actions based on the "GET" and "POST" requests
    in the index.html
    """

    col = ['income', 'othdebt', 'debtinc', 'creddebt', 'employ']
    if request.method == "GET":
        return render_template("index.html")

    else:
        input = request.form.to_dict()
        input_data = {key: float(input[key]) for key in col}
        form_inputs = pd.DataFrame(input_data, index=[0])
        prediction = model.predict(form_inputs.astype(float))
        result = "Default" if prediction[0] == 1 else "No Default"
        return result


if __name__ == "__main__":
    app.run(debug=True)