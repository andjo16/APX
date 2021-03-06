# -*- coding: utf-8 -*-
"""Vertex cover with triangles.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tnK0rW978-9fVbqdDmBGo9EveajjzEFq
"""

# Fetch and import APX wrapper class
#!wget -q https://raw.githubusercontent.com/rasmus-pagh/apx/main/apx.py -O apx.py
#!wget -q https://raw.githubusercontent.com/andjo16/APX/master/Assignment2/apx2.py -O apx.py
#import apx
import apx2
from importlib import reload
reload(apx2)
from apx2 import DataFile, LinearProgram, np

"""# Find triangles in graph

"""

def triangleFinder(graph):
  triangles = []
  for e1 in graph:
    for e2 in graph: #for every pair of edges
      common = set(e1) & set(e2)
      if len(common)==1: #if they have a common node
        u = list(set(e1)-common)[0]
        v = list(set(e2)-common)[0]
        if [u,v] in graph: #and if theiir non-common nodes are connected
          tmp = set((u,v,list(common)[0]))
          if tmp not in triangles: #then the three nodes to the set of triangles
            triangles.append(set((u,v,list(common)[0])))
  
  return triangles

"""# Triangle aware LP for approximating VC

"""

def vertexCoverTriangles():
  filenames = []
  LPres = []
  roundedres = []
  for filename in DataFile.graph_files:
    graph = DataFile(filename)
    vertex_cover_lp = LinearProgram('min')
    objective = {}
    #Find triangles
    triangles = triangleFinder(graph)
    for (u,v) in graph:
      vertex_cover_lp.add_constraint({u: 1, v: 1}, 1)
      objective[u] = 1.0
      objective[v] = 1.0
    #Add additional constraints for triangles
    for (u,v,w) in triangles:
      vertex_cover_lp.add_constraint({u: 1, v: 1, w:1}, 2)
    
    vertex_cover_lp.set_objective(objective)
    value, solution = vertex_cover_lp.solve()
    rounded_value, rounded_solution = 0, {}
    for x in solution:
      r = int(np.round(solution[x] + 1e-10))
      rounded_solution[x] = r
      rounded_value += r
    filenames.append(filename)
    LPres.append(value)
    roundedres.append(rounded_value)

    print(f'Graph: {filename}')
    print(f'LP optimal value: {value}\n{solution}')
    print(f'Rounded LP value: {rounded_value}\n{rounded_solution}')
    print()
  return (filenames,LPres, roundedres)

"""# Orignal LP for approximating VC
Only used for comparing with triangle aware solution.

This code is not functionally changed from the given LP for approximating VC.
"""

def vertexCover():
  filenames = []
  LPres = []
  roundedres = []
  for filename in DataFile.graph_files:
    graph = DataFile(filename)
    vertex_cover_lp = LinearProgram('min')
    objective = {}
    for (u,v) in graph:
      vertex_cover_lp.add_constraint({u: 1, v: 1}, 1)
      objective[u] = 1.0
      objective[v] = 1.0

    vertex_cover_lp.set_objective(objective)
    value, solution = vertex_cover_lp.solve()
    rounded_value, rounded_solution = 0, {}
    for x in solution:
      r = int(np.round(solution[x] + 1e-10))
      rounded_solution[x] = r
      rounded_value += r
    filenames.append(filename)
    LPres.append(value)
    roundedres.append(rounded_value)

    print(f'Graph: {filename}')
    print(f'LP optimal value: {value}\n{solution}')
    print(f'Rounded LP value: {rounded_value}\n{rounded_solution}')
    print()

  return (filenames,LPres, roundedres)

"""Used for comparison in report"""

def createTable(cover, covertriangles):
  print("\\begin{center}\n\t\\begin{tabular}{ c | c | c | c | c | c | c}\\label{tab:compare}\n\t\t&  \multicolumn{3}{c|}{Vertex cover} & \multicolumn{3}{c}{Vertex cover triangles}\\\\")
  print("\t\t Name & LP & Rounded & Ratio & LP & Rounded & Ratio\\\\");
  print("\t\t\\hline")
  for i in range(len(cover[0])):
    print("\t\t " + str(cover[0][i][:-4])+ " & %.5f & %d & %.5f & %.5f & %d & %.5f \\\\" % (cover[1][i], cover[2][i], cover[2][i]/cover[1][i], covertriangles[1][i], covertriangles[2][i], covertriangles[2][i]/covertriangles[1][i]));
  print("\t\\end{tabular}\n\\end{center}")

print("---------Vertex Cover---------")
VC = vertexCover()
print("---------Vertex Cover with Triangles---------")
VCT = vertexCoverTriangles()

createTable(VC,VCT)