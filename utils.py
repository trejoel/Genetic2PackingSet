from igraph import *
import itertools

def GML2Ma(F):
   print(F)

def readCactus(F):
	cac=Graph.Read_GML(F)
	return cac

def getLen(G):
	myAM=G.get_adjacency()
	lenAM=len(myAM[0])
	return lenAM

#this function returns the list of all vertices in a graph
def getListVertices(G):
	return [v.index for v in G.vs]


#return the neighbors of vertex v from graph G
def getNeighbors(G,v):
	#return G.neighbors(v, mode="out")
	return G.neighbors(v)


#this function returns the neighborhood at distance two 
#of the current vertex
def getN2(G,v):
	listN2=list()
	listN2=G.neighbors(v)
	lenN=len(listN2)
	for i in range(0,lenN):
		listAux=G.neighbors(listN2[i])
		lenAux=len(listAux)
		for j in range(0,lenAux):
			if (not listAux[j] in listN2 and listAux[j]!=v):
				listN2.append(listAux[j])
	return listN2

def howMany2PinN2(G,v):
	listN2=getN2(G,v)
	lenN2=len(listN2)
	cont=0;
	for i in range(0,lenN2):
		if (G.vs.select(listN2[i])["color"]==['black']):
			cont=cont+1
	return cont

#this condition verify if there is not a black vertex at distance two of a
#given black vertex	

def Max2PCondition(G,v):
	retVal=True
	if (G.vs.select(v)["color"]==['black']):
		blackNeighbors=howMany2PinN2(G,v)
		if (blackNeighbors>0):
			print(blackNeighbors)
			retVal=False
	else: # v is not included in the 2-packing set:
		blackNeighbors=howMany2PinN2(G,v)
		if (blackNeighbors==0):# there exists no black vertex at distance two from v
			print(blackNeighbors)
			retVal=False
	return retVal

#this function verifies that graph G is a maximal 2-packing
def verify2packing(cac):
	listVertices=getListVertices(cac)
	for i in range(0,len(listVertices)):
		if (not Max2PCondition(cac,listVertices[i])):
			return False
	return True


def createTestMatrix(G):
	myAM=G.get_adjacency()
	listAM=list()
	lenAM=len(myAM[0])
	for i in range(0,lenAM):
		listAM.append(myAM[i])
	return listAM

def matrixWithDiagonal(G):
	myList=createTestMatrix(G)
	myLen=len(myList)
	for i in range(0,myLen):
		myList[i][i]=1
	return myList

def allWhite(G):
	lenG=getLen(G)
	for i in range(0,lenG):
		G.vs.select(i)["color"]='white'

def ColorOutput(G,myList):
	lenG=getLen(G)
	for i in range(0,lenG):
		if (myList[i]==1):
			G.vs.select(i)["color"]='black'
	return G

#subset operations

# return all binary subsets of length n
def binarySubsets(n):
	lst=list(itertools.product([0,1],repeat=n))
	return lst

	
