# Create the Network (a Multigraph)

def create_network(filename):
    """
    Given a pickled list of names with format [[name1,name2,...],[name3,name4,name5,...],...] 
    it creates a pickled MultiGraph
    """
    input = open('names_list_file.pickle','rb')
    names_list=pickle.load(input)
    input.close()
    g=nx.MultiGraph()
    for names in names_list:
        if len(names) > 1:
            g.add_edges_from([edge for edge in itertools.combinations(names, 2)])
    output = open('names_multigraph.pickle','wb')
    pickle.dump(g,output)
    output.close()


# # Get degree of top 100 people


def degrees(g):
    """
    Pass a networkx MultiGraph and returns a pickled sorted list of degrees
    """
    
    deg=[[d[0],int(d[1])] for d in hhh.degree_iter()]
    deg = sorted(deg, key=lambda tup: tup[1])

    deg_tuple = [tuple(i) for i in deg[-100:]]
    deg_tuple = tuple(list(reversed(deg_tuple)))

    output = open('Q1','wb') #Answer to Q1.
    pickle.dump(deg_tuple,output)
    output.close()


# # PageRank

def PageRank(g):
    """
    Pass a networkx MultiGraph and returns a sorted list with the PageRank of each node
    """
    number_of_nodes = g.number_of_nodes()
    for node in g.nodes_iter():
        g.node[node]['pr'] = 1./number_of_nodes
    for it in range(10):
        for node in g.nodes_iter():
            g.node[node]['pr'] = (1-0.85)/number_of_nodes +0.85 * sum([g.node[neigh]['pr']/g.degree(neigh) for neigh in g.neighbors_iter(node)])
            
    PR = [[node, g.node[node]['pr']] for node in g.nodes_iter()]
    return sorted(PR, key=lambda tup: tup[1])

    output = open('Q2','wb') #Answer to Q2.
    pickle.dump(PR_tuple,output)
    output.close()


# # FRIENDSHIP

def friendship(g):
    """
    Pass a networkx MultiGraph and returns a the level of friendship between pairs of people
    """
    
    friendship = {} #[[edge, g.number_of_edges(edge[0],edge[1])] for edge in g.edges_iter()]
    
    for edge in g.edges_iter():
        friendship[edge] = g.number_of_edges(edge[0],edge[1])
    
    friendship_list = [[edge, friendship[edge]] for edge in friendship]
    friendship_list = sorted(friendship_list, key=lambda tup: tup[1])
    
    friendship_tuple = [tuple(i) for i in friendship_list[-100:]]
    friendship_tuple = list(reversed(friendship_tuple))

    output = open('Q3','wb') #Answer to Q3.
    pickle.dump(friendship_tuple,output)
    output.close()

