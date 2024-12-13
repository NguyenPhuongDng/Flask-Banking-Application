import pickle
import pandas as pd
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from spark_funcion import get_analytics_data

with open("SVM_model_Banking_Application.pkl", "rb") as source:
    model = pickle.load(source)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bank_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=True)
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
        try:
            name = input.get("name")
            age = int(input.get("age", 0)) if input.get("age") else None
            input_data = {key: float(input[key]) for key in col}
        except ValueError:
            return render_template("error.html")
        
        form_inputs = pd.DataFrame(input_data, index=[0])
        prediction = model.predict(form_inputs.astype(float))
        result = "Default" if prediction == 1 else "No Default"

        try:
            new_application = Application(
                name=name,
                age=age,
                employ=form_inputs['employ'][0],
                creddebt=form_inputs['creddebt'][0],
                debtinc=form_inputs['debtinc'][0],
                income=form_inputs['income'][0],
                othdebt=form_inputs['othdebt'][0],
                result=result
            )
            db.session.add(new_application)
            db.session.commit()
        except: return render_template("error.html")

        return render_template("result.html", result=result)

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
    
@app.route("/view_table/<table_name>")
def view_table(table_name):
    # access http://127.0.0.1:5000/view_table/Application 
    try:
        # Thực hiện truy vấn
        result = db.session.execute(text(f"SELECT * FROM {table_name}"))
        # Lấy danh sách cột từ kết quả
        columns = result.keys()
        # Chuyển đổi kết quả truy vấn thành danh sách dictionary
        data = [dict(zip(columns, row)) for row in result]
        return render_template("view_table.html", table_name=table_name, data=data)
    except Exception as e:
        return f"Lỗi: {e}"
    
@app.route("/analysis")
def analytics():
    db_path = "instance/bank_app.db"
    table_name = "Application"
    data = get_analytics_data(db_path, table_name)

    return render_template("analytics.html", data=data)
    
if __name__ == "__main__":
    app.run(debug=True)