from flask import Flask, jsonify, request, render_template, redirect, flash
import re
from dict.tables import tables_dict
import pandas as pd
from database.services import upload_df_to_database, get_metric


app = Flask(__name__)


@app.route('/')
def init():
    """_summary_
    """
    return "<p>Hello, Welcome to My Globant's Coding challenge!</p>"


@app.route('/uploadFile')
def uploadFile():
    return render_template("uploadFile.html")


@app.route('/success', methods=['POST'])
def answerUploadFile():
    if request.method == 'POST':
        f = request.files['file']

        if f.filename == '':
            flash('No selected file')
            return redirect(request.url)

        f.save(f.filename)
        fileType = (re.search('^(departments|hired_employees|jobs).*',
                    f.filename).group(1))

    if fileType not in tables_dict:
        return jsonify(status_code=405,
                       content={'error': 'Filename not expected for upload'})

    tcolumns = list(tables_dict[fileType].keys())
    df = pd.read_csv(f.filename, names=tcolumns, dtype={
                     t: 'str' for t in tcolumns})

    nrows = len(df.index)
    print("numero de registros: ", nrows)
    if nrows < 1 or nrows > 1000:
        return jsonify(status_code=405,
                       content={'error':
                                'The number of lines should be between 1 and 1000'})

    upload_df_to_database(df, fileType)

    return render_template("answerUploadFile.html",
                           name=f.filename,
                           type=fileType,
                           columns=tcolumns,
                           rows=nrows)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
