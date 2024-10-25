import os
import sys
from flask import Flask, render_template, request, url_for, redirect
from dotenv import load_dotenv
#import numpy as np
#import matplotlib.pyplot as plt

plt.style.use('dark_background')

load_dotenv("./.flaskenv")

app = Flask(__name__)


# init DB
GRADES_DICT= {}
DBs = [f[:-4] for f in os.listdir("db/")]

def get_data(db):
	with open("static/db/"+db+".csv") as database:
		L = database.readlines()
		print(L, "dakldazkjkl")
		if (L == []) or (L == ["\n"]):
			return([])
		data = [tuple( [float(string.strip()) for string in line.split(';') ]) for line in L]
	return(data)

def write_data(db, L):
	with open("static/db/"+db+".csv", "w") as database:
		database.writelines([str(item[0])+";"+str(item[1])+"\n" for item in L] )

for db in DBs:
	data = get_data(db)
	GRADES_DICT[db] = [data, len(data)] 

print(2*"\n",DBs,2*"\n")
print(2*"\n",GRADES_DICT,2*"\n")


"""
def plot_data(db):
	plt.clf()
	arr_x = np.linspace(0,20,41)
	arr_y = [0 for i in arr_x]
	for i in Cont["grades"][db][0]:
		arr_y[int(2*i[0])] += 1
	m = max(arr_y)
	arr_y0 = np.array(arr_y)
	arr_y = np.array([None if i==0 else i for i in arr_y])
	print(arr_y)
	plt.xlim(0,20)
	plt.ylim(0, m+1)
	plt.scatter(arr_x, arr_y, color="red")
	plt.plot(arr_x, arr_y0, color="blue")
	plt.savefig("static/"+db+".png")
"""
			
	

#GRADES_DICT= {"DS-1-maths": [[(14,1), (12,2), (5,4), (3,3)], 4], "DS-1-physique": [[(17,1), (12,2), (5,4)], 3]}


Cont =  {"usermessage": ["welcome !"], "grades": GRADES_DICT}

@app.route("/")
def index(user_prompt="Hi, welcome !"):
	return( render_template("home.html", Cont=Cont) )

@app.route("/", methods=["GET", "POST"])
def add_grade():
	new_grade = request.form.get("grade",None)
	id_grade = request.form.get("id_grade",None)
	DS_add = request.form.get("DS_add",None)
	if (new_grade == "") or (id_grade == "") or (new_grade == None) or (id_grade == None) or (DS_add == "") or (DS_add == None):
		return( render_template("home.html", Cont=Cont) )
	new_grade = float(new_grade )
	id_grade = float(id_grade )
	if not (id_grade in [i[1] for i in Cont["grades"][DS_add][0] ]):
		Cont["grades"][DS_add][0].append((new_grade, id_grade))
		Cont["grades"][DS_add][0].sort()
		Cont["grades"][DS_add][0].reverse()
		Cont["grades"][DS_add][1] += 1
		write_data(DS_add, Cont["grades"][DS_add][0])
		#plot_data(DS_add)
		os.system("python3 static/plotting.py '"+str(Cont["grades"][DS_add][0])+"' '"+DS_add+"'")
	return( render_template("index.html", Cont=Cont, DS="DS-1-maths") )
	

@app.route("/DS/<ds>")
def get_grades(ds):	
	Cont["grades"][ds][0] = get_data(ds)
	Cont["grades"][ds][1] = len(Cont["grades"][ds][0])
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
	if not (id_grade in [i[1] for i in Cont["grades"][DS_add][0] ]):
		Cont["grades"][DS_add][0].append((new_grade, id_grade))
		Cont["grades"][DS_add][0].sort()
		Cont["grades"][DS_add][0].reverse()
		Cont["grades"][DS_add][1] += 1
		write_data(DS_add, Cont["grades"][DS_add][0])
		#plot_data(DS_add)
		os.system("python3 static/plotting.py '"+str(Cont["grades"][DS_add][0])+"' '"+DS_add+"'")
	return(render_template("index.html", Cont=Cont, DS=str(ds)) )

if __name__ == "__main__":
	app.run(debug=True)
