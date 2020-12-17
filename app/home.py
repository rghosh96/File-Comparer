from app import app     # python treats app folder as package bc of __init__
from flask import render_template, request, redirect
import itertools
import plotly
import plotly.graph_objects as go
import os
import json

def compareFiles(file1, file2):
    # open files and save as lists
    with open(file1, 'r') as file1:
            with open(file2, 'r') as file2:
                file1set = file1.read().splitlines()
                file2set = file2.read().splitlines()

    # zip & compare lists, storing line & result in two seperate lists
    lineNum = []
    line1 = []
    line2 = []
    result = []
    print("************* COMPARING **************")
    for one,two in itertools.zip_longest(file1set,file2set, fillvalue='nothing'):
        line1.append(one)
        line2.append(two)
        if one != two:
            result.append("DIFFERENT: (in file 2: " + two + ")")
        else:
            result.append("same")

    for i in range(len(line1)):
        i+= 1
        lineNum.append(i)

        
    # generate table
    data=[go.Table(
        columnorder = [1,2,3,4],
        columnwidth = [30,200,200,100],
        header=dict(values=['L I N E','F I L E 1', 'F I L E 2', 'R E S U L T'],
            line_color='black',
            fill_color='white',
            align='left',
            font_color='black'),
        cells=dict(values=[lineNum, line1, line2, result],
            line_color='white',
            fill_color='rgba(0,0,0,0)',
            align='left',
            font_color='white'))]
    layout = go.Layout(
        paper_bgcolor='black',
        plot_bgcolor='black',
    )

    fig = go.Figure(data=data, layout=layout)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    print(graphJSON)
    return graphJSON


app.config["FILE_UPLOADS"] = os.path.dirname(os.path.realpath(__file__))+"/static/files"


# @app.route("/results")
# def results():
#     if os.path.exists(app.config["FILE_UPLOADS"] + "/file1.txt"):
#         print("exists!")
#     if os.path.exists(app.config["FILE_UPLOADS"] + "/file2.txt"):
#         print("exists!")
#     table = compareFiles(app.config["FILE_UPLOADS"] + "/file1.txt", app.config["FILE_UPLOADS"] + "/file2.txt")
#     return render_template("home.html", table=table)


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        if request.files:
            if "file1" in request.files:
                print(request.files)
                file1 = request.files["file1"]
                # file2 = request.files["file2"]
                # print(file1)
                file1.save(os.path.join(app.config["FILE_UPLOADS"], "file1.txt"))
                # file2.save(os.path.join(app.config["FILE_UPLOADS"], file2.filename))
                # print("file 1 saved!")
            if "file2" in request.files:
                print(request.files)
                file2 = request.files["file2"]
                # file2 = request.files["file2"]
                # print(file1)
                file2.save(os.path.join(app.config["FILE_UPLOADS"], "file2.txt"))
                # file2.save(os.path.join(app.config["FILE_UPLOADS"], file2.filename))
                # print("file 1 saved!")
    file1exists = os.path.exists(app.config["FILE_UPLOADS"] + "/file1.txt")
    file2exists = os.path.exists(app.config["FILE_UPLOADS"] + "/file2.txt")
    print(file1exists)
    print(file2exists)
    print(file1exists and file2exists)


    if (file1exists and file2exists):
        print("both files exist!")
        table = compareFiles(app.config["FILE_UPLOADS"] + "/file1.txt", app.config["FILE_UPLOADS"] + "/file2.txt")
    else:
        data=[go.Table(
        columnorder = [1],
        columnwidth = [500],
        header=dict(values=['E M P T Y  T A B L E'],
            line_color='white',
            fill_color='rgba(0,0,0,0)',
            align='left',
            font_color='white'),
        cells=dict(values=['either one or two files to be compared not found ..'],
            line_color='white',
            fill_color='rgba(0,0,0,0)',
            align='left',
            font_color='white'))]
        layout = go.Layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
        )
        fig = go.Figure(data=data, layout=layout)
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        table = graphJSON

    return render_template("home.html", table=table, file1=file1exists, file2=file2exists)     # flask knows to check templates folder

