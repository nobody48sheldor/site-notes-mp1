import matplotlib.pyplot as plt
import numpy as np
import sys
import ast

# Get command line arguments
args = sys.argv[1:]

# Initialize variables for list and string
data = None
db = None

# Process arguments
if len(args) >= 2:
    try:
        # The first argument is expected to be a list in string format
        data = ast.literal_eval(args[0])
        
        # The second argument is expected to be a string
        db = args[1]

        print(f"Received list: {data}")
        print(f"Received string: {db}")

    except (ValueError, SyntaxError) as e:
        print(f"Error parsing input: {e}")
else:
    print("Insufficient arguments provided. Please provide a list and a string.")


plt.style.use('dark_background')

static_path = "static/"

def plot_data(data,db):
	plt.clf()
	arr_x = np.linspace(0,20,41)
	arr_y = [0 for i in arr_x]
	for i in data:
		arr_y[int(2*i[0])] += 1
	m = max(arr_y)
	arr_y0 = np.array(arr_y)
	arr_y = np.array([None if i==0 else i for i in arr_y])
	print(arr_y)
	plt.xlim(0,20)
	plt.ylim(0, m+1)
	plt.title("distribution de : "+db, fontsize=30, color="white", fontweight='bold')
	plt.bar(arr_x, arr_y0, width=0.4, align='center', color='blue', edgecolor='white', linewidth=1.4)
	plt.savefig(static_path+db+".png")

plot_data(data,db)
