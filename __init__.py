import os
import sys
from flask import Flask, render_template, request, url_for, redirect
from dotenv import load_dotenv
#import numpy as np
#import matplotlib.pyplot as plt
from math import sqrt

#plt.style.use('dark_background')

load_dotenv("./.flaskenv")

app = Flask(__name__)

def average(L):
	S = 0
	for i in L:
		S += i[0]
	return(float(str(S/len(L))[:4]))

def ecart_type(L):
	S = 0
	avg = average(L)
	for i in L:
		S += (i[0] - avg)**2
	return(float(str( sqrt( S/len(L)) )[:4] ))


# init DB
GRADES_DICT= {}
DBs = [f[:-4] for f in os.listdir("static/db/")]

def get_data(db):
	with open("static/db/"+db+".csv") as database:
		L = database.readlines()
		if (L == []) or (L == ["\n"]):
			return([])
		data = [tuple( [float(string.strip()) for string in line.split(';') ]) for line in L]
	return(data)

def write_data(db, L):
	with open("static/db/"+db+".csv", "w") as database:
		database.writelines([str(item[0])+";"+str(item[1])+"\n" for item in L] )

for db in DBs:
	data = get_data(db)
	GRADES_DICT[db] = [data, len(data), average(data), ecart_type(data)] 

print(2*"\n",DBs,2*"\n")
print(2*"\n",GRADES_DICT,2*"\n")




#GRADES_DICT= {"DS-1-maths": [[(14,1), (12,2), (5,4), (3,3)], 4], "DS-1-physique": [[(17,1), (12,2), (5,4)], 3]}


Cont =  {"usermessage": ["welcome !"], "grades": GRADES_DICT}

@app.route("/")
def index(user_prompt="Hi, welcome !"):
	return( render_template("home.html", Cont=Cont) )

@app.route("/", methods=["GET", "POST"])
def index_user(user_prompt="Hi, welcome !"):
	user = request.form.get("user",None)
	return( redirect("http://127.0.0.1:5000/USER/"+user) )

@app.route("/DS/<ds>")
def get_grades(ds):	
	Cont["grades"][ds][0] = get_data(ds)
	Cont["grades"][ds][1] = len(Cont["grades"][ds][0])
	Cont["grades"][ds][2] = average(Cont["grades"][ds][0])
	Cont["grades"][ds][3] = ecart_type(Cont["grades"][ds][0])
	return(render_template("index.html", Cont=Cont, DS=str(ds)) )

@app.route("/DS/<ds>", methods=["GET", "POST"])
def get_and_post_grades(ds):
	new_grade = request.form.get("grade",None)
	id_grade = request.form.get("id_grade",None)
	DS_add = request.form.get("DS_add",None)
	if (new_grade == "") or (id_grade == "") or (new_grade == None) or (id_grade == None):
		return( render_template("home.html", Cont=Cont) )
	if (DS_add == "") or (DS_add == None):
		DS_add = ds
	new_grade = float(new_grade )
	id_grade = float(id_grade )
	if id_grade in [i[1] for i in Cont["grades"][DS_add][0] ]:
		indice = -1
		for i in range(len(Cont["grades"][DS_add][0])):
			if Cont["grades"][DS_add][0][i][1] == id_grade:
				indice = i
		if indice != (-1):
			Cont["grades"][DS_add][0].pop(indice)
		Cont["grades"][DS_add][1] -= 1
	if not (id_grade in [i[1] for i in Cont["grades"][DS_add][0] ]):
		Cont["grades"][DS_add][0].append((new_grade, id_grade))
		Cont["grades"][DS_add][0].sort()
		Cont["grades"][DS_add][0].reverse()
		Cont["grades"][DS_add][1] += 1
		Cont["grades"][DS_add][2] = average(Cont["grades"][DS_add][0])
		Cont["grades"][DS_add][3] = ecart_type(Cont["grades"][DS_add][0])
		write_data(DS_add, Cont["grades"][DS_add][0])
		#plot_data(DS_add)
		os.system("python3 static/plotting.py '"+str(Cont["grades"][DS_add][0])+"' '"+DS_add+"'")
		return(render_template("index.html", Cont=Cont, DS=str(ds)) )

@app.route("/USER/<user>", methods=["GET", "POST"])
def stats(user):
	user_grade = []
	for DSs in Cont["grades"]:
		for i in Cont["grades"][DSs][0]:
			if i[1] == float(user):
				user_grade.append((i[0], DSs))
	cmd = "python3 static/plotting-stat.py '"+"[" + user + "," + "["
	for i in range(len(user_grade) -1):
		cmd = cmd + "("+str(user_grade[i][0])+","+'"'+str(user_grade[i][1])+'"'+")"+","
	cmd = cmd + "("+str(user_grade[-1][0])+","+'"'+str(user_grade[-1][1])+'"'+")"+ "],["
	for i in range(len(Cont["grades"]) -1):
		cmd = cmd +'"'+ list(Cont["grades"].keys())[i]+'"' + ","
	cmd = cmd + '"'+list(Cont["grades"].keys())[-1]+'"' + "]]'"
	print(cmd)
	os.system(cmd)
	return(render_template("user.html", Cont=Cont, user=user, user_grade=user_grade) )
	

if __name__ == "__main__":
	app.run(debug=True)
