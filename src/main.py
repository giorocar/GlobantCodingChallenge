from flask import Flask, jsonify, request, render_template, redirect, flash
import re
from src.dict.tables import tables_dict
import pandas as pd
from src.database.services import upload_df_to_database, get_metric
from src.data_quality.data_quality import generate_filter_codes


app = Flask(__name__)


@app.route('/')
def init():
    """_summary_
    """
    return "<p>Hello, Welcome to My Globant's Coding challenge!</p>"


# @app.route('/uploadFile')
# def uploadFile():
#     return render_template("uploadFile.html")


@app.route('/uploadFile', methods=['POST'])
def uploadFile():
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

    content_response = {'file': f.filename,
                        'type': fileType,
                        'columns': tcolumns,
                        'rows': nrows}

    if nrows < 1 or nrows > 1000:
        return jsonify(status_code=405,
                       content={'error':
                                'The number of lines should be between 1 and 1000'})

    codeline = generate_filter_codes(df, fileType)
    loc = {'df': df}
    exec(codeline, globals(), loc)

    df_ok = loc['df_ok']
    df_failed = loc['df_failed']
    upload_df_to_database(df_ok, fileType)
    ok_inserts = len(df_ok.index)
    fail_rows = len(df_failed.index)

    if fail_rows == 0:
        content_response['result'] = 'All the records have been uploaded'
        content_response['nrows_inserted'] = ok_inserts
    else:
        content_response[
            'result'] = f'Errors founded on records failed, successfully uploaded {ok_inserts} registers'
        if ok_inserts > 0:
            content_response['nrows_inserted'] = ok_inserts
        df_failed = df_failed.fillna('').to_dict(orient="records")
        content_response['rows_failed'] = df_failed
        content_response['nrows_failed'] = fail_rows

    return jsonify(status_code=200, content=content_response)


@app.route('/metrics', methods=['GET'])
def metrics():

    query_input = request.args.get('query')
    query_type = ['num_emp_hired_x_job_dpto',
                  'list_emp_hired_x_dpto']
    if query_input not in query_type:
        return jsonify(status_code=405,
                       content={'error': f'The query {query_input} is not available'})
    try:
        results = get_metric(query_input)
        return jsonify(status_code=200, content=results)
    except Exception as e:
        return e


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
