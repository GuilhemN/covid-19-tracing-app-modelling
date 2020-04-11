
import math as m
import random as rd

def get_matching(u, distrib):
    a =0
    b = len(distrib)-1
    if (u> distrib[b]):
        return b
    else:

        while (b-a > 1):
            m = (a+b)//2

            if distrib[m] > u:
                b= m
            else:
                a=m
        m = (a+b)//2

        if distrib[m] > u:
            return a +1
        else:
            return b+1

def somme(l):
    s = 0
    for x in l:
        s +=x
    return s

def not_empty(l):
    for x in l:
        if x> 0:
            return True
    return False


def get_ind(x, degrees):
    s = 0
    for i in range(len(degrees)):
        s += degrees[i]
        if x <=s:
            return i



def rd_pair(S, degrees):
    x1 = rd.randint(1,S)
    x2 = rd.randint(1,S)

    ind1 = get_ind(x1, degrees)
    ind2 = get_ind(x2, degrees)
    return ind1, ind2

#params

N = 1000
moy = 6
household_size = 3
household_proba = 0.9
extern_contact_proba = 0.1

distrib = [1- m.exp(-1/moy)] #for k = 0


degrees = []

for k in range(1,100):
    p = (1- m.exp(-1/moy))* m.exp(-k/moy)
    distrib.append(distrib[k-1]+p)

for i in range(N):
    u = rd.uniform(0,1)
    deg = get_matching(u, distrib)
    degrees.append(deg)

#to get an even number of total degrees
save_deg = degrees[:]

S = somme(degrees)
if S%2 == 1:
    degrees[0] +=1

adj = []

for i in range(N):
    adj.append([])


while S>0:
    p1, p2 = rd_pair(S, degrees)
    if degrees[p1] <= household_size or degrees[p2] <= household_size:
        adj[p1].append({"noeud" : p2, "proba" : household_proba})
        adj[p2].append({"noeud" : p1, "proba" : household_proba})
    else:
        adj[p1].append({"noeud" : p2, "proba" : extern_contact_proba})
        adj[p2].append({"noeud" : p1, "proba" : extern_contact_proba})
    degrees[p1] -= 1
    degrees[p2] -= 1
    S -= 2






