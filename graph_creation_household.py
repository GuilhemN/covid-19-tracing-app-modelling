##creationde graphe par foyer
household_size = (2,6)
household_link = 0.9

communauty_size = 300 #number of households in the communauty
communauty_link = 0.3
av_deg_by_household = 200

def init_graphe_household():
    global adj
    global individus

    adj = []

    for i in range(communauty_size):
        size = random.randint(household_size[0], household_size[1])
        nb = len(adj)
        for i in range(nb,nb+size):
            vois = []
            for j in range(nb,nb+size):

                if (i!=j):
                    vois.append({"noeud":j, "proba": household_link})
            adj.append(vois)


    for i in range(av_deg_by_household*communauty_size):
        x1 = random.randint(0, len(adj)-1)
        x2 = random.randint(0, len(adj)-1)

        adj[x1].append({"noeud":x2, "proba": communauty_link})
        adj[x2].append({"noeud":x1, "proba": communauty_link})

    #init individus
    individus = []

    for i in range(nbIndividus):
        app = False
        if random.uniform(0, 1) < UtilAppli:
            app =True

        s = MALADEASYMP
        if random.uniform(0, 1) < InitSain:
            s = SAIN
            nbSain +=1
        else:
            nbMaladeAS +=1

        individus.append({"state": s, "resteConfinement": 0, "appli": app})
