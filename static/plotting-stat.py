import matplotlib.pyplot as plt
import numpy as np
import sys
import ast

# Get command line arguments
args = sys.argv[1]
#print("args : ",args)

data = ast.literal_eval(args)

plt.style.use('dark_background')

static_path = "static/"

def plot_data(data):
	plt.clf()
	print("DATA : ", data)
	arr_x = data[2]
	arr_y = []
	for i in range(len(data[2])):
		try:
			if data[1][i][1] in data[2]:
				arr_y.append(float(data[1][i][0]))
			else:
				arr_y.append(0)
		except:
			arr_y.append(0)
	print("arr_y = ",arr_y)
	plt.title("notes de "+str(data[0]), fontsize=20, color="white", fontweight='bold')
	plt.bar(arr_x, arr_y, width=0.4, align='center', color='blue', edgecolor='white', linewidth=1.4)
	plt.savefig(static_path+"user-"+str(data[0])+".png")

plot_data(data)
