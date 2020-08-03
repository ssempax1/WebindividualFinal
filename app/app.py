from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'gradesData'
mysql.init_app(app)


@app.route('/')
def signin():
    user = {'username': "Ssempax's Project"}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblGradesImport')
    result = cursor.fetchall()
    return render_template('index.html', title='Grades Sign in ', user=user, grades=result)


@app.route('/enroll')
def enroll():
    user = {'username': "Ssempax's Project"}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblGradesImport')
    result = cursor.fetchall()
    return render_template('enroll.html', title='Enroll Form', user=user, grade=result)


@app.route('/home', methods=['GET'])
def index():
    user = {'username': "Ssempax's Project"}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblGradesImport')
    result = cursor.fetchall()
    return render_template('home.html', title='Home', user=user, grade=result)


@app.route('/view/<int:grade_id>', methods=['GET'])
def record_view(grade_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblGradesImport WHERE id=%s', grade_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', grade=result[0])


@app.route('/edit/<int:grade_id>', methods=['GET'])
def form_edit_get(grade_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblGradesImport WHERE id=%s', grade_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', grade=result[0])


@app.route('/edit/<int:grade_id>', methods=['POST'])
def form_update_post(grade_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Last_name'), request.form.get('First_name'), request.form.get('SSN'),
                 request.form.get('Test1'), request.form.get('Test2'),
                 request.form.get('Test3'), request.form.get('Test4'),
                 request.form.get('Final'), request.form.get('Grade'), grade_id)
    sql_update_query = """UPDATE tblGradesImport t SET t.Last_name = %s, t.First_name = %s, t.SSN = %s, t.Test1 = 
    %s, t.Test2 = %s, t.Test3 = %s, t.Test4 = %s ,t.Final = %s, t.Grade =%s   WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/grades/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New grade Form')


@app.route('/grades/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Last_name'), request.form.get('First_name'), request.form.get('SSN'),
                 request.form.get('Test1'), request.form.get('Test2'),
                 request.form.get('Test3'), request.form.get('Test4'),
                 request.form.get('Final'), request.form.get('Grade'))
    sql_insert_query = """INSERT INTO tblGradesImport (Last_name,First_name,Test1,Test2,Test3,Test4,Final, Grade) 
                VALUES (%s, %s,%s, %s,%s, %s,%s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/delete/<int:grade_id>', methods=['POST'])
def form_delete_post(grade_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblGradesImport WHERE id = %s """
    cursor.execute(sql_delete_query, grade_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/grades', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblGradesImport')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/grades/<int:grade_id>', methods=['GET'])
def api_retrieve(grade_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblGradesImport WHERE id=%s', grade_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/grades/<int:grade_id>', methods=['PUT'])
def api_edit(grade_id) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['Last_name'], content['First_name'], content['SSN'],
                 content['Test1'], content['Test2'],
                 content['Test3'], content['Test4'],
                 content['Final'], content['Grade'], grade_id)
    sql_update_query = """UPDATE tblGradesImport t SET  t.Last_name = %s, t.First_name = %s, t.SSN = %s, 
         t.Test1 = %s, t.Test2 = %s, t.Test3 = %s, t.Test4 = %s, t.Final = %s, t.Grade = %s WHERE t.id = %s"""
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/grades/', methods=['POST'])
def api_add() -> str:
    content = request.json

    cursor = mysql.get_db().cursor()
    inputData = (content['Last_name'], content['First_name'], content['SSN'],
                 content['Test1'], content['Test2'],
                 content['Test3'], content['Test4'],
                 content['Final'], request.form.get('Grade'))
    sql_insert_query = """INSERT INTO tblGradesImport (Last_name,First_name,Test1,Test2,Test3,Test4,Final, Grade) 
                VALUES (%s, %s,%s, %s,%s, %s,%s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


@app.route('/api/grades/<int:grade_id>', methods=['DELETE'])
def api_delete(grade_id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblGradesImport WHERE id = %s """
    cursor.execute(sql_delete_query, grade_id)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
