import pickle
import pandas as pd
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

with open("SVM_model_Banking_Application.pkl", "rb") as source:
    model = pickle.load(source)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bank_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employ = db.Column(db.Float, nullable=False)
    creddebt = db.Column(db.Float, nullable=False)
    debtinc = db.Column(db.Float, nullable=False)
    income = db.Column(db.Float, nullable=False)
    othdebt = db.Column(db.Float, nullable=False)
    result = db.Column(db.String(50), nullable=False)


with app.app_context():
    db.create_all()

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

        new_application = Application(
            employ=form_inputs['employ'][0],
            creddebt=form_inputs['creddebt'][0],
            debtinc=form_inputs['debtinc'][0],
            income=form_inputs['income'][0],
            othdebt=form_inputs['othdebt'][0],
            result=result
        )
        db.session.add(new_application)
        db.session.commit()

        return result

@app.route("/check_db")
def check_db():
    """
    """
    try:
        # Truy vấn để lấy số lượng bảng trong cơ sở dữ liệu SQLite
        result = db.session.execute(text("SELECT count(name) FROM sqlite_master WHERE type='table';"))
        num_tables = result.fetchone()[0]
        return f"Kết nối thành công, số bảng là: {num_tables}"
    except Exception as e:
        return f"Lỗi kết nối: {e}"
if __name__ == "__main__":
    app.run(debug=True)