from flask import Flask, render_template, send_from_directory, url_for, redirect
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
from werkzeug.utils import secure_filename
import os, tempfile
import yaml
from usermapper.usermapper import xmlwriter
from usermapper.mapperdata import get_users 
from flask_bootstrap import Bootstrap
from os import environ, path
from dotenv import load_dotenv

app = Flask(__name__)

bootstrap = Bootstrap(app)

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))
app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
app.config['FLASK_APP'] = environ.get('FLASK_APP')
app.config['FLASK_ENV'] = environ.get('FLASK_ENV')

class MyForm(FlaskForm):
    filename = FileField('Filename: ', validators=[FileRequired(), FileAllowed(['yaml'])])
    submit = SubmitField('Upload')


@app.route("/", methods=('GET','POST'))
def index():
    form = MyForm()
    filename = ""
    if form.validate_on_submit():
        print('submitted')

        basedir = os.path.join(
            os.path.relpath(os.path.dirname(__file__)), 
            'downloads'
        )
        tempdir = tempfile.mkdtemp(dir=basedir)
        filename = os.path.join(tempdir, 'user-mapping.xml')

        configuration = yaml.safe_load(form.filename.data.read())
        structure = get_users(configuration)
        xmlwriter(structure, filename)

        temp_folder = os.path.split(tempdir)[1]

        return redirect (url_for('download_page', temp_folder=temp_folder))

    return render_template('index.html', form=form)


@app.route("/download/<temp_folder>", methods=('GET','POST'))
def download(temp_folder):
    basedir = os.path.join(
        os.path.relpath(os.path.dirname(__file__)), 
        'downloads'
    )
    temp_dir = os.path.join(basedir, temp_folder)
    return send_from_directory(temp_dir, 'user-mapping.xml', as_attachment=True)


@app.route('/download_page/<temp_folder>', methods=('GET','POST'))
def download_page(temp_folder):

    filename = os.path.join(
        os.path.relpath(os.path.dirname(__file__)), 
        'downloads',
        temp_folder,
        'user-mapping.xml'
    )

    with open(filename) as preview:
       data = preview.readlines()
    
    download_url = url_for('download', temp_folder=temp_folder)

    return render_template('download.html', data=data, download_url=download_url)