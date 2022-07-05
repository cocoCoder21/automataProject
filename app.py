from flask import Flask, render_template, Response, request
import requests
from flask_wtf.csrf import CSRFProtect
from flask_ngrok import run_with_ngrok
import matplotlib.pyplot as plt
from PIL import Image
import base64
import cv2
import os
import io


# This is responsible to provide protection for the website, especially when the user input something.
csrf = CSRFProtect()

app = Flask(__name__)
csrf.init_app(app)

app.config["MAX_CONTENT_LENGTH"] = 3024 * 3024
app.config["UPLOAD_EXTENSIONS"] = ['.jpg', '.png']


@app.route('/')
def Home():
    return render_template('/regex1.html',
                           is_uploaded=False,
                           img_path='',
                           img_size='',
                           img_filename='',
                           img_width=0,
                           img_height=0,
                           img_upload_isvalid=False,
                           predicted_image='',
                           is_predicted=False,
                           is_error=False,
                           is_error_msg=''
                           )

@app.route('/regex2')
def regex2():
    return render_template('/regex2.html',
                           is_uploaded=False,
                           img_path='',
                           img_size='',
                           img_filename='',
                           img_width=0,
                           img_height=0,
                           img_upload_isvalid=False,
                           predicted_image='',
                           is_predicted=False,
                           is_error=False,
                           is_error_msg=''
                           )




if __name__ == '__main__':
    app.run()

# Run the web applicaion using "python app.py"
