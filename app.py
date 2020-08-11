# coding:utf-8
from flask import Flask, render_template, request, redirect, url_for, make_response,jsonify
from werkzeug.utils import secure_filename
import os
import cv2
import time
import sys
from test import get_poem
from datetime import timedelta
import click
from flask_sqlalchemy import SQLAlchemy

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.send_file_max_age_default = timedelta(seconds=1)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')
@app.cli.command()
def forge():
    db.create_all()
    user = [
        {'image_path': 'static/images/1.jpg', 'generated_poems': 'test1'},
        {'image_path': 'static/images/2.jpg', 'generated_poems': 'test2'},
        {'image_path': 'static/images/3.jpg', 'generated_poems': 'test3'}
    ]

    for u in user:
        u = User(image_path=u['image_path'], generated_poems=u['generated_poems'])
        db.session.add(u)

    db.session.commit()
    click.echo('Done.')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(50))
    generated_poems=db.Column(db.String(500))

@app.route('/', methods=['POST', 'GET'])  
def upload():
    user_data1 = User.query.order_by(User.id.desc()).first()
    now_id=user_data1.id
    user_data2= User.query.get(now_id-1)
    user_data3=User.query.get(now_id-2)

    if request.method == 'POST':
        f = request.files['file']
 
        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "please use (png、PNG、jpg、JPG、bmp) type image!"})
 
        user_input = request.form.get("name")
 
        basepath = os.path.dirname(__file__)  
 
        upload_path = os.path.join(basepath, 'static/images/temp', secure_filename(f.filename))  
        f.save(upload_path)
 
        img = cv2.imread(upload_path)

        cv2.imwrite(os.path.join(basepath, 'static/images/temp', 'test.jpg'), img)
        poem_output=get_poem(os.path.join(basepath,'static/images/temp/test.jpg'))
        new_id=now_id
        str_id=str(new_id)+'.jpg'
        image_path=os.path.join('static/images',str_id)
        true_path=os.path.join(basepath,image_path)
        cv2.imwrite(true_path, img)

        user_data=User(image_path=image_path,generated_poems=poem_output)
        db.session.add(user_data)
        db.session.commit()





        return render_template('upload_ok.html',poem_output=poem_output,user_data1=user_data1,user_data2=user_data2,user_data3=user_data3,val1=time.time())
 
    return render_template('upload.html',user_data1=user_data1,user_data2=user_data2,user_data3=user_data3)

if __name__ == '__main__':
    # app.debug = True
    app.run(host='0.0.0.0', port=5000, debug=True)
 
 

