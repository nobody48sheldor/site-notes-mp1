import os
import sys
from flask import Flask, render_template, request, url_for, redirect
from dotenv import load_dotenv

load_dotenv("./.flaskenv")

app = Flask(__name__)

GRADES_DICT= {"DS-1-maths": [[(14,1), (12,2), (5,4), (3,3)], 4], "DS-1-physique": [[(17,1), (12,2), (5,4)], 3]}

Cont =  {"username": "Arnaud", "grades": GRADES_DICT}

@app.route("/")
def index(user_prompt="Hi Arnaud !"):
	return( render_template("home.html", Cont=Cont) )

@app.route("/", methods=["GET", "POST"])
def add_grade():
	new_grade = request.form.get("grade",None)
	id_grade = request.form.get("id_grade",None)
	DS_add = request.form.get("DS_add",None)
	if (new_grade == "") or (id_grade == "") or (new_grade == None) or (id_grade == None) or (DS_add == "") or (DS_add == None):
		return( render_template("home.html", Cont=Cont) )
	new_grade = int(new_grade )
	id_grade = int(id_grade )
	print(3*"\n")
	print(new_grade, id_grade)
	print(3*"\n")
	if not (id_grade in [i[1] for i in Cont["grades"][DS_add][0] ]):
		Cont["grades"][DS_add][0].append((new_grade, id_grade))
		Cont["grades"][DS_add][0].sort()
		Cont["grades"][DS_add][0].reverse()
		Cont["grades"][DS_add][1] += 1
	return( render_template("index.html", Cont=Cont, DS="DS-1-maths") )
	

@app.route("/DS/<ds>")
def get_grades(ds):
	print(2*"\n")
	print(ds)
	print(2*"\n")
	return(render_template("index.html", Cont=Cont, DS=str(ds)) )

@app.route("/DS/<ds>", methods=["GET", "POST"])
def get_and_post_grades(ds):
	print(2*"\n")
	print(ds)
	print(2*"\n")
	new_grade = request.form.get("grade",None)
	id_grade = request.form.get("id_grade",None)
	DS_add = request.form.get("DS_add",None)
	print(new_grade)
	print(id_grade)
	if (new_grade == "") or (id_grade == "") or (new_grade == None) or (id_grade == None):
		return( render_template("home.html", Cont=Cont) )
	if (DS_add == "") or (DS_add == None):
		DS_add = ds
	new_grade = int(new_grade )
	id_grade = int(id_grade )
	print(3*"\n")
	print(new_grade, id_grade)
	print(3*"\n")
	if not (id_grade in [i[1] for i in Cont["grades"][DS_add][0] ]):
		Cont["grades"][DS_add][0].append((new_grade, id_grade))
		Cont["grades"][DS_add][0].sort()
		Cont["grades"][DS_add][0].reverse()
		Cont["grades"][DS_add][1] += 1
	return(render_template("index.html", Cont=Cont, DS=str(ds)) )

if __name__ == "__main__":
	app.run(debug=True)
