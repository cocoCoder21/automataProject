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
    sample = f"static/images/dfa_cover.png"
    return render_template('/regex1.html', sample=sample)

@app.route('/regex2')
def regex2():
    return render_template('/regex2.html')


# ============================ DFA 1 ============================

# # Required [4]: a aa ab aba  /  b bb ba baa
# # a [optional] bb ba [optional] baa
#
# #Check if the substring is one of the combinations --> [(a,]
# #Ends with aba or baa

@csrf.exempt
@app.route('/rgx1', methods=['POST'])
def r1():
    if request.method == "POST":
        answer = 'valid'
        strng = request.form['rgx1_input']
        strng = strng.lower().strip()
        file_strng = strng
        print(strng)

        # 1.  Regex 1 : (a + b)(a + b)*(aa + bb)(ab + ba)(a + b)*(aba + baa)
        sublist = ['aaaab', 'baaab', 'abbab', 'bbbab', 'aaaba', 'baaba', 'abbba', 'bbbba']


        print(strng)
        if strng[-3:] == 'aba' or strng[-3:] == 'baa':
                strng = strng[:-3]

                if any(substr in strng for substr in sublist):
                    answer ='valid'
                else:
                    answer ="invalid"
        else:
                answer ='invalid'

        print(answer)

        #FILE CHANGING
        file_Samples = ["aaababaa","abbaabab","baaabbabbbaba","bbbabaabbabba"]

        if file_strng in file_Samples:
            sample = f"static/images/{file_strng}.gif"
        else:
            sample = f"static/images/cannot.png"

    return render_template('/regex1.html', answer=answer, sample=sample, str= file_strng)



# ============================ DFA 2 ============================

# # First 2 letters must be aa or bb
# #Check if the input ends with the required values in expression 4 & 5 exist
# #Check if [aba, aaa, or ab] exist and return index
# #Check the remaining string if it contains a only or b only
# depending on the required value chosen in expression 4

@csrf.exempt
@app.route('/rgx2', methods=['POST'])
def r2():
    if request.method == "POST":
        answer = 'valid'
        strng = request.form['rgx2_input']
        strng = str(strng).lower().strip()
        file_strng = strng
        print(strng)

        # 1.  Regex 1 : (a + b)(a + b)*(aa + bb)(ab + ba)(a + b)*(aba + baa)
        # Function that finds [aba, aaa, ba]

        #     (aa + bb) (a + b)* (aba + aaa + ba) (bb* + aa*) (a + b + aa)
        # 2.  (11 + 00) (1 + 0)* (101 + 111 + 01) (00* + 11*) (1 + 0 + 11)

        exp3 = ['101', '111', '01']

        def check_midSubstring(s, exp4):

            if s.rfind('01') > max(s.rfind('101'), s.rfind('111')):
                idx = s.rfind('01')
                idx += 2

            else:
                idx = max(s.rfind('101'), s.rfind('111'))
                idx += 3

            s = s[idx:]

            if s == "":
                return 'Valid'

            elif exp4 == '1' and "0" in s:
                return 'Invalid'

            elif exp4 == '0' and "1" in s:
                return 'Invalid'

            else:
                return 'Valid'


        # Check required strings according to expression 1
        if strng[:2] == '11' or strng[:2] == '00':
            strng = strng[2:]

            # Check required strings according to expression 4 & 5 (3 STRINGS)
            if strng.endswith('011') or strng.endswith('111'):
                exp4 = strng[-3:]
                strng = strng[:-3]

                if any(substr in strng for substr in exp3):
                    answer = check_midSubstring(strng, exp4[0])

                elif strng == '10':
                    answer= 'Valid'

                else:
                    print(strng)
                    answer = 'Invalid'


            # Check required strings according to expression 4 & 5 (2 STRINGS)
            elif strng.endswith('11') or strng.endswith('10') or strng.endswith('01') or strng.endswith('00'):
                exp4 = strng[-2:]
                strng = strng[:-2]

                if any(substr in strng for substr in exp3):
                    answer = check_midSubstring(strng, exp4[0])
                else:
                    answer ='Invalid'

            else:
                print("check end: ", strng)
                answer ='Invalid'

        else:
            answer ='invalid'

    print(answer)
    # FILE CHANGING

    file_Samples = ["11101011","000110", "11111111", "10101000", "1110001"]

    if file_strng in file_Samples:
        sample = f"static/images/'{file_strng}'.gif"
    else:
        sample = f"static/images/cannot.png"

    return render_template('/regex2.html', answer=answer, sample=sample,  str= file_strng)




if __name__ == '__main__':
    app.run()

# Run the web applicaion using "python app.py"
