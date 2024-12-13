import pymysql
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('registration.html')

@app.route('/register', methods=['POST'])
def register():
    # Retrieve form data
    name = request.form.get("full_name")
    email = request.form.get("email")
    password = request.form.get("password")
    cpassword = request.form.get("cpassword")
    
    if password != cpassword:
        return render_template("registration.html", msg="Passwords do not match.")
    
    try:
        database = pymysql.connect(
            user='root',
            password='root',   
            database='database1'
        )
        
        cursor = database.cursor()
        query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s);"
        cursor.execute(query, (name, email, password))
        database.commit()
        cursor.close()
        database.close()

        return render_template('dashboard.html', name=name)
    
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        return render_template("registration.html", msg=e)


@app.route('/showdatabase')
def showdatabase():
    database = pymysql.connect(
            user='root',
            password='root',   
            database='database1'
        )
        
    cursor = database.cursor()
    cursor.execute("select * from users")
    data =  cursor.fetchall()
    return render_template('displaydata.html', data=data)

@app.route('/login', methods=['post'])
def login():
    database = pymysql.connect(
            user='root',
            password='root',   
            database='database1'
        )
        
    cursor = database.cursor()
    email = request.form.get('email')
    password=request.form.get('password')
    query=f"select * from users where email = '{email}'"
    print(query)
    cursor.execute(query)
    result=cursor.fetchall()
    print(result)
    database.commit()
    if(len(result)==0):
        return render_template('login.html',msg="user not exist")
    if(result[0][2]!=password):    
        return render_template('login.html',msg1="password not match")
    return render_template('dashboard.html',name=result[0][0])

@app.route('/gotologin')
def gotologin():
    return render_template('login.html')

    
if __name__ == '__main__':
    app.run(debug=True)
