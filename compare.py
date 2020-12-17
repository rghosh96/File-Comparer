import itertools
import plotly.graph_objects as go

# open files and save as lists
with open('one.txt', 'r') as file1:
        with open('two.txt', 'r') as file2:
            file1set = file1.read().splitlines()
            file2set = file2.read().splitlines()

# zip & compare lists, storing line & result in two seperate lists
lineNum = []
line = []
result = []
print("************* COMPARING **************")
for one,two in itertools.zip_longest(file1set,file2set, fillvalue='nothing'):
    line.append(one)
    if one != two:
        result.append("DIFFERENT: (in file 2: " + two + ")")
    else:
        result.append("same")

for i in range(len(line)):
    i+= 1
    lineNum.append(i)

print(line)
print(result)
    
# generate table
fig = go.Figure(data=[go.Table(
    columnorder = [1,2,3],
    columnwidth = [30,200,100],
    header=dict(values=['line','line content', 'result'],
        line_color='white',
        fill_color='lightgray',
        align='left',
        font_color='white'),
    cells=dict(values=[lineNum, line, result],
        line_color='white',
        fill_color='lavenderblush',
        align='left',
        font_color='darkgray'))
])
fig.show()
