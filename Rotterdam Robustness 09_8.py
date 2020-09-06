# -*- coding: utf-8 -*-
"""
Created on Mon May 11 13:27:01 2020

@author: alexandra.akosa
"""

import csv                                                             
import networkx as nx
# import cairo 
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import * 
import time
import statistics 
from operator import itemgetter


def displayNetwork(g, visual_style={}):
    nx.draw(g, **visual_style)
    plt.savefig('rotterdamnetwork.png')
    display(Image(filename='img/temp.png'))
    
def displayPlot(plt):
    plt.savefig("img/temp_plot.png")
    display(Image(filename='img/temp_plot.png'))
    
visual_style ={}
visual_style["node_size"] = 10

def nx_remove_frac(network,frac):
    #print('before:', nx.info(network))
    s = int(len(network.nodes)* frac) #number of nodes to be removed 
    #print ('s:', s)
    num_nodeslist = list(range(0,(len(network.nodes) -1))) #making num of nodes in orginial network iterable    
    #print('num original', len(num_nodeslist))
    list_removednodes = []
    for it in range(s):
        it = np.random.choice(num_nodeslist,1)
        list_removednodes.append(int(it))
        num_nodeslist.remove(it)
    nodelistafter = [i for j, i in enumerate(network.nodes) if j not in list_removednodes] # list of original nodes - removed nodes (based on position nums in the list)
    subnetwork = network.subgraph(nodelistafter)
    return subnetwork
    #print('after:', nx.info(subnetwork))
    #print(len(nodelistafter))
    #print('num original after', len(num_nodeslist))
    #print('removed list', len(list_removednodes))
    #print('after:', nx.info(network))
    
def nx_remove_between (network,topn): #removes the top n of the sorted betweenness list 
    sorted_betweenness = sorted(betweenness_dict.items(),key=itemgetter(1),reverse=True)
    nodelist = set(list(network.nodes))
    blist = sorted_betweenness[:topn]
    for b in blist:
#        print(b[0])
        #nodelist.remove(b[0])
        nodelist = nodelist - set([b[0]])
    nodelistafter = list(nodelist) 
    subnetwork = network.subgraph(nodelistafter)
    #print(list(set(network.nodes)-set(subnetwork.nodes)))
    return subnetwork 
    
def nx_remove_closeness(network, topn):
    sorted_closeness = sorted(closeness_dict.items(),key=itemgetter(1),reverse=True)
    #print(sorted_closeness)
    nodelist = set(list(network.nodes))
    #nodelist = list(network.nodes)
    #print(nodelist)
    clist = sorted_closeness[:topn]
    #print (clist )
    for c in clist:
    #    print(c[0])
        nodelist = nodelist - set([c[0]])
        #nodelist.remove(c[0])
    nodelistafter =list( nodelist) 
    #nodelistafter = nodelist 
    subnetwork = network.subgraph(nodelistafter)
    #print(list(set(network.nodes)-set(subnetwork.nodes)))
    return subnetwork  

def nx_remove_degree (network, topn):
    sorted_degree = sorted(degree_dict.items(),key=itemgetter(1),reverse=True)
#    print(sorted_degree)
    nodelist = set(list(network.nodes))
#   print(nodelist)
    dlist = sorted_degree[:topn]
    for d in dlist:
       #print(d,set([d[0]]))
       nodelist = nodelist - set([d[0]])
       #print(nodelist)
    #   print(set(d[0]).isdisjoint(set(nodelist)))
     #  nodelist.remove(d[0])
    nodelistafter =list( nodelist) 
#    print(len(nodelistafter))
    subnetwork = network.subgraph(nodelistafter)
#    print((list(set(network.nodes)-set(subnetwork.nodes))))
#   print(subnetwork.nodes)
    return subnetwork 

def nx_spatialrisk (network, n_risk):
    risknodes = floodrisk_ids
    nodelist = set(list(network.nodes))
    rmodlist =[]
    #print(n_risk)
    risklist = risknodes[:n_risk]
    # print('risklist contains', len(risklist)) 
    for r in risklist:
        rmodlist.append([r,'NA'])
    for rm in rmodlist:
        nodelist = nodelist - set([rm[0]])
        # print('length of nodelist after risk removal', len(nodelist))
    # #   print(set(d[0]).isdisjoint(set(nodelist)))
    #   #  nodelist.remove(d[0])
    nodelistafter =list( nodelist) 
    # print(len(nodelistafter))
    subnetwork = network.subgraph(nodelistafter)
    # print((list(set(network.nodes)-set(subnetwork.nodes))))
    # print(subnetwork.nodes)
    return subnetwork 

with open('Rotterdam_nx_nodes.csv', 'r') as nodecsv:    # Read in the nodelist file             
    nodereader = csv.reader(nodecsv)                                       
    nodes = [n for n in nodereader ][1:]                                  
node_ids = [n[0] for n in nodes]      # Get a list of just the node names (the first item in each row)
#print(node_ids)

with open('Station Nodes_Rotterdam_clip.csv', 'r') as stationscsv:
    stationreader = csv.reader(stationscsv)
    stations = [s for s in stationreader][1:]
station_ids = [s[0] for s in stations]
#print(station_ids)

with open('flood risk nodes_150m.csv','r') as floodriskcsv:
    floodriskreader = csv.reader(floodriskcsv)
    floodrisknodes = [ f for f in floodriskreader][1:]
floodrisk_ids = [f[0] for f in floodrisknodes]
#print(floodrisk_ids)    
    
with open('Rotterdam_nx_edges.csv', 'r') as edgecsv:       # Read in the edgelist file                  
    edgereader = csv.reader(edgecsv)                                   
    edges = [e for e in edgereader][1:]     #list of row lists including all info
edge_from_to =  [[e[0],e[1]] for e in edges]                   
edge_list= [tuple(e) for e in edge_from_to]
#print(edge_from_to)
#print(edge_list)

#print(set(station_ids).isdisjoint(set(node_ids)))

RG = nx.Graph() # Initialize a Graph object                                                        
RG.add_nodes_from(node_ids) # Add nodes to the Graph                             
RG.add_edges_from(edge_list) # Add edges to the Graph  
#print(nx.info(RG)) # Print information about the Graph  
remove = ['']
RG.remove_nodes_from(remove) #remove blank nodes

################################################################################

node_xcord_dict ={}
node_ycord_dict = {}

for node in nodes:
    node_xcord_dict[node[0]] = node[1]
    node_ycord_dict[node[0]]= node[2]
    
nx.set_node_attributes(RG,node_xcord_dict,'x_coordinate')
nx.set_node_attributes(RG,node_ycord_dict,'y_coordinate')

degree_dict = nx.degree_centrality(RG)
nx.set_node_attributes(RG,degree_dict,'degree') 

betweenness_dict = nx.betweenness_centrality(RG)
nx.set_node_attributes(RG,betweenness_dict, 'betweenness')

closeness_dict = nx.closeness_centrality(RG)
nx.set_node_attributes(RG,closeness_dict,'closeness') 

sorted_bw = sorted(betweenness_dict.items(),key=itemgetter(1),reverse=True)
sorted_close = sorted(closeness_dict.items(),key=itemgetter(1),reverse=True)
sorted_degree = sorted(degree_dict.items(),key=itemgetter(1),reverse=True)
#print('Top 20 nodes by betweenness centrality:')

#num=0
#for b in sorted_close[:20]:
#    num+=1
#    print(num,':',b)
#    
#num=0
#for b in sorted_degree[:20]:
#    num+=1
#    print(num,':',b)

#with open ('degree_scores_RC.csv', 'w', newline='') as csvfile: 
#            thewriter = csv.writer(csvfile)
#            for b in sorted_degree:
#                thewriter.writerow(b)
#    
#print (betweenness_dict)
  

#nx_remove_degree(RG,75)
#displayNetwork(br,visual_style) 
#    

#########################################################################################
edge_id_dict = {}
edge_connections_dict ={}
edge_pressure_dict = {}
edge_material_dict = {}

#print(RG.edges())

for edge in edges: 
    edge_id_dict[edge[0], edge[1]] = edge[2]
    edge_connections_dict[edge[0], edge[1]] = edge[3]
    edge_pressure_dict[edge[0], edge[1]] = edge[5]
    edge_material_dict[edge[0], edge[1]] = edge[6]
##    
nx.set_edge_attributes(RG,edge_id_dict,'edge_id') 
nx.set_edge_attributes(RG,edge_connections_dict, 'edge_connections_count') 
nx.set_edge_attributes(RG,edge_pressure_dict, 'edge_pressure') 
nx.set_edge_attributes(RG,edge_material_dict, 'edge_material') 

#displayNetwork(nx_remove_frac(RG,0),visual_style)

#displayNetwork(RG,visual_style)

#print(nx.number_connected_components(RG))
RG2 = (max(nx.connected_component_subgraphs(RG),key=len)) #ensure full connectivity (compensates for an incomplete clip)
#print(nx.number_connected_components(RG2))
#print(nx.number_connected_components(nx_remove_frac(RG2,0)))   
#print(len(RG2)) # 1580
#print(len(RG)) #1820
#print(nx.info(RG2)) 
#displayNetwork(RG2,visual_style)

#
#nlist = []
#elist = []
#subgraphs = list(nx.connected_component_subgraphs(nx_remove_frac(RG2,.0)))
#for s in subgraphs:
#    if set(station_ids).isdisjoint(set(s.nodes)) == False:
#        nlist.append(s)
#for n in nlist: 
#    print('node count sub', len(n))
#    if len(n.nodes) > 1:  #filter out single node graphs 
#        print('edges:',len(n.edges))
#        for e in n.edges():
#            elist.append(int(n.edges[e]["edge_connections_count"]))        
#print('number subgraphs', len(nlist))
#print('total edges of graphs larger than 1 node:',len(elist))
#print('list of connection count', elist)            
#print('sum count connections', sum(elist))
            
#for e in RG2.edges():
#    print(e,RG.edges[e]['edge_id'],RG.edges[e]['edge_connections_count'],RG.edges[e]['edge_pressure'],RG.edges[e]['edge_material'])

#elist =[]
#for e in RG2.edges():
#    elist.append(int(RG2.edges[e]["edge_connections_count"]))
#print(sum(elist)) # 6741, RG2 = 5488

#print(RG.nodes())
#for n in RG.nodes():
#    print(n,RG.node[n]['x_coordinate'],RG.node[n]['y_coordinate']) 


##################################################################################

def plot_servicelevel_per_q(network,q_range,samples=1, mode="random"): 
    if mode == "random": 
        qlist=[]
        frac_list = []
        service_list = []
        for q in q_range:  
            nlist = []
            elist =[]
            stationlist =[]
            s = 0
            for i in range(samples):         
                g_before = network
                g_after = nx_remove_frac(g_before, q)
                subgraphs = list(nx.connected_component_subgraphs(g_after)) # conneced subgraphs after removal
            for s in subgraphs:
                if set(station_ids).isdisjoint(set(s.nodes)) == False:
                    nlist.append(s)     #list of subgraphs with a station
            for n in nlist: 
                if len(n.nodes) > 1:  #filter out single node graphs 
                    for station in station_ids:                         # to get count of stations serving customers
                        if list(n.nodes).count(station) > 0:
                            stationlist.append(list(n.nodes).count(station))                    
                    for e in n.edges():
                        elist.append(int(n.edges[e]["edge_connections_count"]))
            qlist.append([q,len(subgraphs),len(nlist),sum(elist),len(stationlist)])     
        print(qlist)
        for q in qlist: 
            frac_list.append(q[0])
            service_list.append(q[3]) 
        #print(qlist)
        print(frac_list)
        print(service_list)
        plt.clf()
        plt.plot(frac_list,service_list, color="red")
        plt.tick_params(axis='both', which='major', labelsize=20)
        plt.tick_params(axis='both', which='minor', labelsize=20)
        plt.xlabel('fraction of removal', fontsize=15)
        plt.ylabel('serviced customers', fontsize=15)
        plt.ylim(0,max(service_list))
        plt.xlim((min(q_range),max(q_range)))
        plt.title('Customers with access to a station', fontsize =19)
#        frac_list.sort()
#        service_list.sort()
#        slope,intercept = np.polyfit(np.asarray(frac_list),np.asarray(service_list),1)
#        print('random slope is:', slope)
#        plt.plot(np.asarray(frac_list),slope*np.asarray(frac_list) + intercept)
        plt.subplots_adjust(bottom=0.2)
        plt.subplots_adjust(left=0.15)
        displayPlot(plt)
    elif mode == "betweenness":
        topnlist = []
        qlist = []
        x_list = []
        y_list = []
        for q in q_range: 
            #topnlist.append(int(q*100))
            topnlist.append(int(len(network.nodes)* q))
        #print(topnlist)
        for ntop in topnlist:
            nlist = [] # list of subgraphs with a station per top n attack 
            elist = [] # number of connections per node in n list of subgraphs with stations  
            stationlist = [] #amount of stations serving connections 
            g_before = network
            g_after = nx_remove_between (g_before,ntop)
            subgraphs = list(nx.connected_component_subgraphs(g_after))
            for s in subgraphs:
                if set(station_ids).isdisjoint(set(s.nodes)) == False:
                    nlist.append(s)  
            for n in nlist: 
                if len(n.nodes) > 1:  #filter out single node graphs 
                    for station in station_ids:                         # to get count of stations serving customers
                        if list(n.nodes).count(station) > 0:
                            stationlist.append(list(n.nodes).count(station))
                    for e in n.edges():
                        elist.append(int(n.edges[e]["edge_connections_count"]))
            qlist.append([ntop,len(subgraphs),len(nlist), sum(elist),len(stationlist)])      # list of topn , subgraphs, subgraphs w/stations, sum of connections
        print(qlist)
        for q in qlist: 
            x_list.append(q[0])
            y_list.append(q[3])   
        print(x_list)
        print(y_list)
        plt.clf()
        plt.plot(x_list,y_list, color="red")
        plt.tick_params(axis='both', which='major', labelsize=20)
        plt.tick_params(axis='both', which='minor', labelsize=20)
        plt.xlabel('removed top n by betweenness', fontsize=15)
        plt.ylabel('serviced customers', fontsize=15)
        plt.ylim((0,max(y_list)))
        plt.xlim(0,max(x_list))
        plt.title('Customers with access to a station', fontsize =19)
        #x_list.sort()
        #y_list.sort()
        #slope,intercept = np.polyfit(np.log(x_list),np.log(y_list),1)
        #print('betwenness slope is:', slope)
        #plt.plot(np.asarray(x_list),slope*np.asarray(y_list) + intercept)
        plt.subplots_adjust(bottom=0.2)
        plt.subplots_adjust(left=0.15)
        displayPlot(plt)
    elif mode == "closeness":
        topnlist = []
        qlist = []
        x_list = []
        y_list = []
        for q in q_range: 
            #topnlist.append(int(q*100))
            topnlist.append(int(len(network.nodes)* q))
        #print(topnlist)
        for ntop in topnlist:
            nlist = [] # list of subgraphs with a station per top n attack 
            elist = [] # number of connections per node in n list of subgraphs with stations  
            stationlist=[]
            g_before = network
            g_after = nx_remove_closeness (g_before,ntop)
            subgraphs = list(nx.connected_component_subgraphs(g_after))
            for s in subgraphs:
                if set(station_ids).isdisjoint(set(s.nodes)) == False:
                    nlist.append(s)  
            for n in nlist: 
                if len(n.nodes) > 1:  #filter out single node graphs 
                    for station in station_ids:                         # to get count of stations serving customers
                        if list(n.nodes).count(station) > 0:
                            stationlist.append(list(n.nodes).count(station))
                    for e in n.edges():
                        elist.append(int(n.edges[e]["edge_connections_count"]))
            qlist.append([ntop,len(subgraphs),len(nlist),sum(elist),len(stationlist)])      # list of topn , subgraphs, subgraphs w/stations, sum of connections
        print(qlist)
        for q in qlist: 
            x_list.append(q[0])
            y_list.append(q[3])        
        print(x_list)
        print(y_list)
        plt.clf()
        plt.plot(x_list,y_list, color="red")
        plt.tick_params(axis='both', which='major', labelsize=20)
        plt.tick_params(axis='both', which='minor', labelsize=20)
        plt.xlabel('removed top n by closeness', fontsize=15)
        plt.ylabel('serviced customers', fontsize=15)
        plt.ylim((0,max(y_list)))
        plt.xlim(0,max(x_list))
        plt.title('Customers with access to a station', fontsize =19)
#        x_list.sort()
#        y_list.sort()
        #slope,intercept = np.polyfit(np.log(x_list),np.log(y_list),1)
        #print('closeness slope is:', slope)        
        plt.subplots_adjust(bottom=0.2)
        plt.subplots_adjust(left=0.15)
        displayPlot(plt)
    elif mode == "degree":
        topnlist = []
        qlist = []
        x_list = []
        y_list = []
        for q in q_range: 
            #topnlist.append(int(q*100))
            topnlist.append(int(len(network.nodes)* q))
        # print(topnlist)
        for ntop in topnlist:
            nlist = [] # list of subgraphs with a station per top n attack 
            elist = [] # number of connections per node in n list of subgraphs with stations  
            stationlist = []
            g_before = network
            g_after = nx_remove_degree(g_before,ntop)
            subgraphs = list(nx.connected_component_subgraphs(g_after))
            for s in subgraphs:
                if set(station_ids).isdisjoint(set(s.nodes)) == False:
                    nlist.append(s)  
            for n in nlist: 
                if len(n.nodes) > 1:  #filter out single node graphs 
                    for station in station_ids:                         # to get count of stations serving customers
                        if list(n.nodes).count(station) > 0:
                            stationlist.append(list(n.nodes).count(station))
                    for e in n.edges():        
                        elist.append(int(n.edges[e]["edge_connections_count"]))
            qlist.append([ntop,len(subgraphs),len(nlist),sum(elist),len(stationlist)])      # list of topn , subgraphs, subgraphs w/stations, sum of connections
        print(qlist)
        for q in qlist: 
            x_list.append(q[0])
            y_list.append(q[3])   
        print(x_list)
        print(y_list)
        plt.clf()
        plt.plot(x_list,y_list, color="red")
        plt.tick_params(axis='both', which='major', labelsize=20)
        plt.tick_params(axis='both', which='minor', labelsize=20)
        plt.xlabel('removed top n by degree', fontsize=15)
        plt.ylabel('serviced customers', fontsize=15)
        plt.ylim((0,max(y_list)))
        plt.xlim(0,max(x_list))
        plt.title('Customers with access to a station', fontsize =19)     
        plt.subplots_adjust(bottom=0.2)
        plt.subplots_adjust(left=0.15)
        displayPlot(plt)
    elif mode == 'risk':
        riskedlist = []
        qlist = []
        x_list = []
        y_list = []
        for q in q_range: 
            riskedlist.append(int(len(floodrisk_ids)* q))
        for nrisk in riskedlist:
            nlist = [] # list of subgraphs with a station per top n attack 
            elist = [] # number of connections per node in n list of subgraphs with stations  
            stationlist = []
            g_before = network
            g_after = nx_spatialrisk(g_before,nrisk)
            subgraphs = list(nx.connected_component_subgraphs(g_after))
            for s in subgraphs:
                if set(station_ids).isdisjoint(set(s.nodes)) == False:
                    nlist.append(s)  
            for n in nlist: 
                if len(n.nodes) > 1:  #filter out single node graphs 
                    for station in station_ids:                         # to get count of stations serving customers
                        if list(n.nodes).count(station) > 0:
                            stationlist.append(list(n.nodes).count(station))
                    for e in n.edges():        
                        elist.append(int(n.edges[e]["edge_connections_count"]))
            qlist.append([nrisk,len(subgraphs),len(nlist),sum(elist),len(stationlist)])      # list of topn , subgraphs, subgraphs w/stations, sum of connections
        print(qlist)
        for q in qlist: 
            x_list.append(q[0])
            y_list.append(q[3])   
        print(x_list)
        print(y_list)
        plt.clf()
        plt.plot(x_list,y_list, color="red")
        plt.tick_params(axis='both', which='major', labelsize=20)
        plt.tick_params(axis='both', which='minor', labelsize=20)
        plt.xlabel('removed flood risk nodes', fontsize=15)
        plt.ylabel('serviced customers', fontsize=15)
        plt.ylim((0,max(y_list)))
        plt.xlim(0,max(x_list))
        plt.title('Customers with access to a station', fontsize =19)     
        plt.subplots_adjust(bottom=0.2)
        plt.subplots_adjust(left=0.15)
        displayPlot(plt)

    else: 
        print("no mode selected")


# # t = time.process_time()
plot_servicelevel_per_q(RG2,np.linspace(0,1,10),80,mode="risk")
# # elapsed_time_service_perq = time.process_time() - t
# # print("elapsed_time for service level", elapsed_time_service_perq)

###############################################################################

def plot_meangcc_per_q(network, q_range, samples=1, mode = "random"):
    if mode == "random":
        sgcc = []
        for q in q_range:     
            s = 0
            for i in range(samples):         
                g_before = network
                g_after = nx_remove_frac(g_before, q)
                s+= len((max(nx.connected_component_subgraphs(g_after),key=len)).nodes)/len((max(nx.connected_component_subgraphs(g_before),key=len))) # ratio size lgcc to disrupted network 
            sgcc.append(s/samples) #adding the mean GCC per q to the list sgcc 
        print(q_range)
        print(sgcc)
        plt.clf()
        plt.plot(q_range,sgcc, color="red")
        #plt.plot(q_range,[.25,.3,.45,.7,.99], color="blue")
        plt.tick_params(axis='both', which='major', labelsize=20)
        plt.tick_params(axis='both', which='minor', labelsize=20)
        plt.xlabel('$q$', fontsize=30)
        plt.ylabel('mean size of surviving gcc', fontsize=15)
        plt.xlabel('fraction of removal', fontsize=15)
        plt.title('Average size of GCC per fraction of removal', fontsize =19)
        plt.ylim((min(sgcc),max(sgcc)))
        plt.xlim((min(q_range),max(q_range)))
        plt.subplots_adjust(bottom=0.2)
        plt.subplots_adjust(left=0.15)
        displayPlot(plt)
    if mode =="betweenness":
        sgcc = []
        topnlist = []
        for q in q_range: 
            #topnlist.append(int(q*100))
            topnlist.append(int(len(network.nodes)* q))
        
        for topn in topnlist:
            s = 0
            g_before = network
            g_after = nx_remove_between(g_before, topn)
            s= len((max(nx.connected_component_subgraphs(g_after),key=len)).nodes)/len((max(nx.connected_component_subgraphs(g_before),key=len)))
            sgcc.append(s)  
        print(topnlist)
        print(sgcc)
        plt.clf()
        plt.plot(topnlist ,sgcc, color="red")
        plt.tick_params(axis='both', which='major', labelsize=20)
        plt.tick_params(axis='both', which='minor', labelsize=20)
        plt.xlabel('$q$', fontsize=30)
        plt.ylabel('size of surviving gcc', fontsize=15)
        plt.xlabel('removed top n by betweenness', fontsize=15)
        plt.title('Size of GCC per top n removed by betweenness', fontsize =18)
        plt.ylim((min(sgcc),max(sgcc)))
        plt.xlim(0,max(topnlist))
        plt.subplots_adjust(bottom=0.2)
        plt.subplots_adjust(left=0.15)
        displayPlot(plt)
    if mode =="closeness":
        sgcc = []
        topnlist = []
        for q in q_range: 
            #topnlist.append(int(q*100))
            topnlist.append((int(len(network.nodes)* q)))
        for topn in topnlist:
            s = 0
            g_before = network
            g_after = nx_remove_closeness(g_before, topn)
            s= len((max(nx.connected_component_subgraphs(g_after),key=len)).nodes)/len((max(nx.connected_component_subgraphs(g_before),key=len)))
            sgcc.append(s)        
        print(topnlist)
        print(sgcc)
        plt.clf()
        plt.plot(topnlist ,sgcc, color="red")
        plt.tick_params(axis='both', which='major', labelsize=20)
        plt.tick_params(axis='both', which='minor', labelsize=20)
        plt.xlabel('$q$', fontsize=30)
        plt.ylabel('size of surviving gcc', fontsize=15)
        plt.xlabel('removed top n by closeness', fontsize=15)
        plt.title('Size of GCC per top n removed by closeness', fontsize =18)
        plt.ylim(0,max(sgcc))
        plt.xlim((min(topnlist),max(topnlist)))
        plt.subplots_adjust(bottom=0.2)
        plt.subplots_adjust(left=0.15)
        displayPlot(plt)
    if mode =="degree":
        sgcc = []
        topnlist = []
        for q in q_range: 
            #topnlist.append(int(q*100))
            topnlist.append(int(len(network.nodes)* q))
        for topn in topnlist:
            s = 0
            g_before = network
            g_after = nx_remove_degree(g_before, topn)
            s= len((max(nx.connected_component_subgraphs(g_after),key=len)).nodes)/len((max(nx.connected_component_subgraphs(g_before),key=len)))
            sgcc.append(s) 
        print(topnlist)
        print(sgcc)
        plt.clf()
        plt.plot(topnlist ,sgcc, color="red")
        plt.tick_params(axis='both', which='major', labelsize=20)
        plt.tick_params(axis='both', which='minor', labelsize=20)
        plt.xlabel('$q$', fontsize=30)
        plt.ylabel('size of surviving gcc', fontsize=15)
        plt.xlabel('removed top n by degree', fontsize=15)
        plt.title('Size of GCC per top n removed by degree', fontsize =18)
        plt.ylim(0,max(sgcc))
        plt.xlim((min(topnlist),max(topnlist)))
        plt.subplots_adjust(bottom=0.2)
        plt.subplots_adjust(left=0.15)
        displayPlot(plt)
    if mode =="risk":
        sgcc = []
        riskedlist = []
        for q in q_range: 
            riskedlist.append(int(len(floodrisk_ids)* q))
        for nrisk in riskedlist:
            s = 0
            g_before = network
            g_after = nx_spatialrisk(g_before,nrisk)
            s= len((max(nx.connected_component_subgraphs(g_after),key=len)).nodes)/len((max(nx.connected_component_subgraphs(g_before),key=len)))
            sgcc.append(s) 
        print(riskedlist)
        print(sgcc)
        plt.clf()
        plt.plot(riskedlist ,sgcc, color="red")
        plt.tick_params(axis='both', which='major', labelsize=20)
        plt.tick_params(axis='both', which='minor', labelsize=20)
        plt.xlabel('$q$', fontsize=30)
        plt.ylabel('size of surviving gcc', fontsize=15)
        plt.xlabel('removed top flood risk', fontsize=15)
        plt.title('Size of GCC per flood risk nodes', fontsize =18)
        plt.ylim(0,max(sgcc))
        plt.xlim((min(riskedlist),max(riskedlist)))
        plt.subplots_adjust(bottom=0.2)
        plt.subplots_adjust(left=0.15)
        displayPlot(plt)    
        
        
# t = time.process_time()
#plot_meangcc_per_q(RG2,np.linspace(0,.95,10),80,mode="risk")
# elapsed_time_mean_perq = time.process_time() - t
# print("elapsed_time for mean gcc", elapsed_time_mean_perq)

################################################################################

#def plot_meangcc_per_samples(network,q,samples=1,mode = "random"):
#    gcc = []
#    sgcc = []  
#    slist =[]
#    meanlist = []
#    s = 0
#    for i in range(1,samples):         
#        g_before = network
#        if mode == "random":
#            g_after = nx_remove_frac(g_before, q)
##            else:
##                g_after = remove_top_frac(g_before, q)
#        s= len((max(nx.connected_component_subgraphs(g_after),key=len)).nodes)/len(g_after.nodes) # ratio size lgcc to disrupted network 
#        gcc.append(s)
#        sgcc.append([i,statistics.mean(gcc)]) #adding the mean GCC per sample to the list sgcc 
#    for i in sgcc: 
#        slist.append(i[0])
#        meanlist.append(i[1])
#    #print(slist)
#    #print(meanlist)
#    plt.clf()
#    plt.plot(slist,meanlist, color="red",label = q)
#    plt.tick_params(axis='both', which='major', labelsize=20)
#    plt.tick_params(axis='both', which='minor', labelsize=20)
#    plt.xlabel('$samples$', fontsize=30)
#    plt.ylabel('mean size of surviving gcc', fontsize=20)
#    plt.legend()
#    plt.title('Mean GCC per sample size')
#    plt.ylim((min(meanlist),max(meanlist)))
#    plt.xlim((min(slist),max(slist)))
#    plt.subplots_adjust(bottom=0.2)
#    plt.subplots_adjust(left=0.15)
#    displayPlot(plt)
#    
#t = time.process_time()
#plot_meangcc_per_samples(RG,.4,100,mode="random") #min 80, max 100 / varying qs 
#elapsed_time_mean_pers = time.process_time() - t
#print("elapsed_time for mean per sample size", elapsed_time_mean_pers)

################################################################################
#
#def plot_sdgcc_per_samples(network,q,samples=1,mode = "random"):
#    gcc = []
#    sgcc = []  
#    slist =[]
#    stdevlist = []
#    s = 0
#    for i in range(1,samples):   
#        g_before = network
#        if mode == "random":
#            g_after = nx_remove_frac(g_before, q)
##            else:
##                g_after = remove_top_frac(g_before, q)
#        s= len((max(nx.connected_component_subgraphs(g_after),key=len)).nodes)/len(g_after.nodes) # ratio size lgcc to disrupted network 
#        gcc.append(s)
#        if len(gcc) > 1: 
#            sgcc.append([i,statistics.stdev(gcc)]) #adding the std GCC per sample to the list sgcc 
#    for i in sgcc: 
#        slist.append(i[0])
#    for t in sgcc:
#        stdevlist.append(t[1])
#    #print(slist)
#    #print(stedvlist)
#    plt.clf()
#    plt.plot(slist,stdevlist, color="red",label = q)
#    plt.tick_params(axis='both', which='major', labelsize=20)
#    plt.tick_params(axis='both', which='minor', labelsize=20)
#    plt.xlabel('$samples$', fontsize=30)
#    plt.ylabel('stdev of surviving lcc', fontsize=20)
#    plt.legend()
#    plt.title('Stdev GCC per sample size')
#    plt.ylim((min(stdevlist),max(stdevlist)))
#    plt.xlim((min(slist),max(slist)))
#    plt.subplots_adjust(bottom=0.2)
#    plt.subplots_adjust(left=0.15)
#    displayPlot(plt)
#    
#t = time.process_time()
#plot_sdgcc_per_samples(RG,.5,100,mode="random")
#elapsed_time_sd_pers = time.process_time() - t
#print("elapsed_time for stdev per sample size", elapsed_time_sd_pers)
#







