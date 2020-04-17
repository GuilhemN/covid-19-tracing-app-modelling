from IPython import get_ipython
# %%
####################
# GRAPH GENERATION #
####################

nbIndividuals = 1000 # number of people in the graph | nombre d'individus dans le graphe
initHealthy = 0.90 # percentage of healthy people at start | la proportion de personnes saines à l'intant initial (les autres sont porteurs asymptomatiques)
initCured = 0.05


# graph generation for exponential degrees distribution
#------------------------------------------------------
deg_avg = 100 # average number of connexions per person | le nombre moyen de connexions par personne
av_household_size = 6 # avergave size of household | la taille moyenne d'un foyer
household_proba = 1 # probability of meeting a person of the same household | la probabilité de contact par jour entre membres d'un même foyer
extern_contact_proba = 0.3 # probabilty of meeting a person of a different household | la probabilité de contact par jour entre personne de foyers différents

# average contact per day = 0.3*(100-6) + 6 = 34.2

# graph generation with organization in households
#-------------------------------------------------
household_size = (2,6) # min and max size of an household (uniform distribution) | extremums de la taille d'un foyer
household_link = 1 # probability of contact between members of a household | proba de contact entre membres d'un foyer

community_size = 500 # 2500 is good but a bit slow | number of households in the community | nombre de foyers dans une communauté
community_link = 0.3 # probability of contact across households | proba de contact entre foyers
av_deg_by_household = 400 # number of link from a household | nombre moyen de liens depuis un foyer

# average external degree of an individual : 400/4 (4 is the average size of an household)
# average contacts per day = (400/4)*0.3 + 4 = 34

##############
# APP PARAMS #
##############

daysNotif = 14 # number of days the app checks back for contact notification | nombre de jours vérifiés par l'appli pour notifier un contact
utilApp = 0.8 # percentage of people having the app | la proportion d'utilisateurs de l'application dans la population générale

pDetection = 0.9 # prob. that the app detects a contact | proba que l'appli détecte un contact
pReport = 0.9 # prob. that a user reports his symptoms | proba qu'un utilisateur alerte de ses symptômes
pQNotif = 0.8 # probablity of going into quarantine upon recieving a notification | proba de mise en confinement lors de la réception d'une notification

pSymptomsNotCovid = 0.001 # every day, everyone sends a notification with prob. pSymptomsNotCovid | chaque jour, tout le monde envoie une notif avec proba PSymptomsNotCovid

############
# POLICIES #
############


# people warn the app immediately after having symptoms | on prévient l'application directement après avoir développé les symptômes 
warningAfterSymptoms = False

# upon notification, an individual asks for a test (with some prob.)
# if true, user waits for test results in quarantine, else he goes in quarantine only upon reception of positive test results
# |
# à la reception d'une notif, l'utilisateur demande un test (avec une certaine proba)
# si vrai, is attend les résultats en quarantaine, sinon il ne se met en quarantaine qu'aux résultats d'un test positif
quarantineAfterNotification = True

###############
# TEST PARAMS #
###############


testWindow = (3, 10) # tests are only effective in a given window (time since infection) | les tests ne sont efficaces que dans une fenêtre de temps après infection
daysUntilResult = 2 # attente pour l'obtention des résultats
pFalseNegative = 0.3 # prob. of false negative | proba d'avoir un faux négatif


#################
# PROBABILITIES #
#################
# !! Probabilities are given for 1 step of the process, thus overall prob. follows a geometric law for which expected values have been calculated

#paramters estimated -> a limit of the model
pCloseContact = 0.02 # prob. that a contact is a close contact (those detected by the app) | proba qu'un contact soit rapproché (ceux détectés par l'appli)
pContaminationCloseContact = 0.25 # prob. of contamination after close contact with an infected person | proba de contamination après contact rapproché avec qqn d'infecté
pContaminationCloseContactAsymp = 0.05
#the contamination by asymptomatics seems to be really low according to [4] and "Temporal dynamics in viral shedding and transmissibility of COVID-19"[6]

pContaminationFar = 0.001 # prob. of contamination upon non close contact (environnemental or short contact) | proba de contamination par contact environnemental ou bref
pContaminationFarAsymp = 0.0005


# we took R0=2 estimate from [4] and : 34 contacts/day, an average time of infectiousness of 10 days (pre symptomatic + begining of symptoms period)
# So 10*34*(0.02*0.25 + 0.98*0.001) = 2.03 persons infected by an infected that will have symptoms
# this is plausible given the estimate of R0 and the fact that asymptomatics containation seems to be not really important
#[4] and [6]

#and 0.98*0.001/(0.98*0.0005 + 0.02*0.25) = 0.1638 -> the proportion of contamiation that are not close contact (environnemental/ remote contact) estimated according to environnemental contamination in [4]


#for Asymptomatics : 10*34*(0.02*0.05 + 0.98*0.0005) = 0.203 -> the number of person that will be infected by an asymptomatic infected

#So the proportion of assymptomatic contamination is : 0.4*0.203/(0.6*2.03 + 0.4*0.203) = 0.06 plausible according to [4]



pAsympt = 0.4 # probability of being asymptomatic when infected | proba qu'une personne infectée soit asymptomatique
# according to [4] and Diamond Princess estimates

# parameters for the lognormal law of the incubation period | paramètres pour la loi lognormale de la période d'incubation
incubMeanlog = 1.644 # -> ~5.5 days
incubSdlog = 0.363 # -> ~2.1 days
# according to [4]



pAtoG = 0.1 # probability of going from asymptomatic state to cured | proba de passer de asymptomatique à guéri
#according to "Clinical characteristics of 24 asymptomatic infections with COVID-19 screened among close contacts in Nanjing, China"[7]


pIStoC = 0.07 # probability of going from symptomatic state to cured | proba de passer de avec symptômes à gueri
pIStoD = 0.003 # probability of dying when symptomatic | proba de décès d'une personne présentant des symptômes

# average time with symptoms : 1/(0.07+0.003) = 13.7 days : plausible according to [4]
# death rate when symptoms : 0.003/0.07 = 4.3% : plausible in France according to estimate of 1.6M cases with symptoms
# and 6 000 deaths the 3 April 
# https://www.mgfrance.org/publication/communiquepresse/2525-enquete-mg-france-plus-d-un-million-et-demi-de-personnes-prises-en-charge-par-leur-medecin-generaliste-pour-le-covid-19-entre-le-17-mars-et-le-3-avril

pQSymptoms = 0.9 # probability of going into quarantine when one has symptoms | proba de confinement lors de détection des symptômes

quarantineFactor = 100 # reduction factor applied to the probabilities when one is in quarantine | réduction des probas de rencontre lors du confinement
daysQuarantine = 14 # duration of the quarantine | durée de la quarantaine



# # Libs and defs

# Librairies
import random
import numpy as np

# -> sliders
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets


HEALTHY = 0
ASYMP = 1
PRESYMP = 2
SYMP = 3
CURED = 4
DEAD = 5


class Graph:
    """ Object holding the representation of the graph and some metrics """
    
    def __init__(self):
        self.individuals = []
        self.adj = []

        self.encounters = [[[] for jour in range(daysNotif)] for individual in range(nbIndividuals)]

        self.nbHealthy = 0
        self.nbAS = 0
        self.nbPS = 0
        self.nbS = 0
        self.nbCured = 0
        self.nbDead = 0
        self.nbQuarantine = 0

        self.nbTest = 0

        # cumulative counters :
        self.nbQuarantineTotal = 0
        self.nbInfectedByASPS = 0
        self.nbQuarantineNonD = 0
        self.nbQuarantineNonI = 0

# Class to handle individuals, to use for later
class Individual:
    """ Object holding the representation of an individual """
    
    def __init__(self, state, daysQuarantine, app, sentNotification, daysIncubation, timeSinceInfection, timeLeftForTestResult):
        self.state = state
        self.daysQuarantine = daysQuarantine
        self.app = app
        self.sentNotification = sentNotification
        self.daysIncubation = daysIncubation
        self.timeSinceInfection = timeSinceInfection
        self.timeLeftForTestResult = timeLeftForTestResult

    def in_state(self, state):
        return self.state == state

    def is_infected(self):
        return self.state in [PRESYMP, ASYMP, SYMP]
    
    def has_no_covid(self):
        return self.state in [HEALTHY, CURED]

    def in_quarantine(self):
        return self.daysQuarantine > 0

    def go_quarantine(self):
        if self.daysQuarantine <= 0:
            self.daysQuarantine = daysQuarantine # goes into quarantine if isn't already

# # Graph generation

def init_graph_exp(graph):
    """ Graph initialisation based on exponential ditribution of degrees """
    
    # creation of individuals
    for i in range(nbIndividuals):
        app = False
        if random.uniform(0,1) < utilApp:
            app = True
        s = PRESYMP
        r = random.random()
        if r < initHealthy:
            s = HEALTHY
            graph.nbHealthy += 1
        elif r> initHealthy and r< initHealthy + initCured:
            s = CURED
            graph.nbCured += 1
        else:
            graph.nbPS += 1
        
        # state, quarantine, app, notif, incubation, timeSinceInfection, timeLeftForTestResult
        graph.individuals.append(Individual(s,  0, app, False, 0, -1, -1))

    # affecting degrees to vertices
    degrees = np.around(np.random.exponential(deg_avg, nbIndividuals))

    # to get an even number of total degrees
    S = sum(degrees)
    if S%2 == 1:
        degrees[0] += 1
        S += 1

    graph.adj = [[] for i in range(nbIndividuals)]
    while S > 0:
        #creating an edge
        [p1, p2] = np.random.choice(len(degrees), 2, replace=False, p=degrees/S)
        if degrees[p1] <= av_household_size or degrees[p2] <= av_household_size:
            graph.adj[p1].append({"node" : p2, "proba" : household_proba})
            graph.adj[p2].append({"node" : p1, "proba" : household_proba})
        else:
            graph.adj[p1].append({"node" : p2, "proba" : extern_contact_proba})
            graph.adj[p2].append({"node" : p1, "proba" : extern_contact_proba})
        degrees[p1] -= 1
        degrees[p2] -= 1
        S -= 2


def init_graph_household(graph):
    """ Graph generation based on households organisation """
    
    global nbIndividuals   

    #creation of the households
    graph.adj = []

    for i in range(community_size):
        size = random.randint(household_size[0], household_size[1])
        nb = len(graph.adj)
        for i in range(nb, nb+size):
            vois = []
            for j in range(nb, nb+size):
                if (i != j):
                    vois.append({"node": j, "proba": household_link})
            graph.adj.append(vois)

    #linkage of the households
    for i in range(av_deg_by_household*community_size):
        x1 = random.randint(0, len(graph.adj)-1)
        x2 = random.randint(0, len(graph.adj)-1)

        graph.adj[x1].append({"node": x2, "proba": community_link})
        graph.adj[x2].append({"node": x1, "proba": community_link})

    nbIndividuals = len(graph.adj)
    
    # creation of individuals
    for i in range(nbIndividuals):
        app = False
        if random.uniform(0,1) < utilApp:
            app = True
        s = PRESYMP
        r = random.random()
        if r < initHealthy:
            s = HEALTHY
            graph.nbHealthy += 1
        elif r> initHealthy and r< initHealthy + initCured:
            s = CURED
            graph.nbCured += 1
        else:
            graph.nbPS += 1

        # state, quarantine, app, notif, incubation, timeSinceInfection, timeLeftForTestResult
        graph.individuals.append(Individual(s,  0, app, False, 0, -1, -1))
        
    graph.encounters = [[[] for jour in range(daysNotif)] for individual in range(nbIndividuals)]

# # Updating the graph

def contamination(graph, i, j, closeContact):
    if graph.individuals[i].state == graph.individuals[j].state:
        return

    if graph.individuals[i].in_state(HEALTHY):
        contamination(graph, j, i, closeContact)
        return

    #i is the infected
    if graph.individuals[i].is_infected():
        if graph.individuals[j].in_state(HEALTHY):
            
            if closeContact:
                pContamination = pContaminationCloseContact
                pContaminationAsymp = pContaminationCloseContactAsymp
            else:
                pContamination = pContaminationFar
                pContaminationAsymp = pContaminationFarAsymp
            
            if (random.random() < pContamination and (not graph.individuals[i].in_state(ASYMP))) or \
                (random.random() < pContaminationAsymp and graph.individuals[i].in_state(ASYMP)):
                if graph.individuals[i].in_state(ASYMP) or graph.individuals[i].in_state(PRESYMP):
                    graph.nbInfectedByASPS += 1
                graph.individuals[j].timeSinceInfection = 0
                graph.nbHealthy -= 1
                if random.random() < pAsympt:
                    graph.individuals[j].state = ASYMP
                    graph.nbAS += 1
                else:
                    graph.individuals[j].state = PRESYMP
                    graph.individuals[j].daysIncubation = round(np.random.lognormal(incubMeanlog, incubSdlog))
                    graph.nbPS += 1
            

def test_individual(individual, graph):
    # if there is a test incoming, the person is not tested again
    if individual.timeLeftForTestResult >= 0 or individual.in_state(DEAD):
        return
        
    graph.nbTest +=1
    individual.timeLeftForTestResult = daysUntilResult
    if individual.has_no_covid():
        individual.lastTestResult = False # We assert there are no false positives
        return

    if individual.timeSinceInfection < testWindow[0] or individual.timeSinceInfection > testWindow[1]:
        individual.lastTestResult = False # Not in the detection window, the test fails
        return
    
    # Otherwise the person is ill
    # The test result depends whether we have a false negative
    individual.lastTestResult = not (random.random() < pFalseNegative)


def send_notification(graph, i):
    """ Send notification to people who have been in touch with i | Envoi d'une notif aux personnes ayant été en contact avec i """
    # Note: graphe.encounter[i] is empty if i does not have the app so there is no need to have an additional test
    
    if graph.individuals[i].sentNotification:
        return # notifications already sent
  
    graph.individuals[i].sentNotification = True
    for daysEncounter in graph.encounters[i]:
        for contact in daysEncounter:
            # !!! TO UPDATE : pQNotif used wrong !!! >
            if random.random() < pQNotif: # if the person takes the notification into account
                # the person is always tested (CHANGE ??)
                test_individual(graph.individuals[contact], graph) # asks for a test
                if quarantineAfterNotification: # in this case, the person waits for test results in quarantine
                    graph.individuals[contact].go_quarantine()






def step(graph):
    """ Step from a day to the next day | Passage au jour suivant du graphe """


    graph.nbTest = 0
    for encounter in graph.encounters:
        encounter.append([]) # will contain every encounter of the day | contiendra les nouvelles rencontres du jour

    # for each possible encounter | on constate toutes les rencontres entre individus
    for i in range(nbIndividuals):

        graph.individuals[i].daysIncubation -= 1
        
        for edge in graph.adj[i]:
            j = edge['node']
            if j < i:
                continue # only check one way of the edge | on ne regarde qu'un sens de chaque arête
            
            factor = 1
            if graph.individuals[i].in_quarantine():
                factor *= quarantineFactor
            if graph.individuals[j].in_quarantine():
                factor *= quarantineFactor
            
            # if i or j are in quarantine, reduce the probability that they meet | Si i et/ou j sont confinés, réduction de leur proba de rencontre
            if random.random() > edge['proba'] / factor:
                continue # no encounter | pas de rencontre
            
            if random.random() < pCloseContact: #if this is a close contact
                # if i and j have the app, we save their encounter | Si i et j ont l'appli, on note la rencontre
                if graph.individuals[i].app and graph.individuals[j].app and random.random() < pDetection: 
                    graph.encounters[i][-1].append(j)
                    graph.encounters[j][-1].append(i)
            
                contamination(graph, i, j, True)
            else:
                contamination(graph, i, j, False)
    
    # handle new day | on passe au jour suivant
    graph.nbQuarantine = 0
    graph.nbQuarantineNonI = 0
    graph.nbQuarantineNonD = 0
    
    for i in range(nbIndividuals):
        graph.individuals[i].daysQuarantine -= 1
        
        if (not graph.individuals[i].in_quarantine()) and graph.individuals[i].in_state(SYMP): #if there is still symptoms we don't end quarantine
            graph.individuals[i].daysQuarantine =1
            
        
        if graph.individuals[i].in_quarantine():
            graph.nbQuarantineTotal += 1/nbIndividuals
            if not graph.individuals[i].in_state(DEAD):
                graph.nbQuarantineNonD += 1
            # update if pre-symp is added
            if not graph.individuals[i].is_infected():
                graph.nbQuarantineNonI += 1

        if graph.individuals[i].timeSinceInfection >= 0:
            graph.individuals[i].timeSinceInfection += 1

    # update the states | on met à jour les états des individus
    for i, individual in enumerate(graph.individuals):
        
        # TODO (?) : separate function
        ## TESTS MANAGEMENT
        if individual.timeLeftForTestResult == 0:
  
            if individual.in_quarantine() and individual.lastTestResult == False: # is in quarantine and gets a negative test
                individual.daysQuarantine = 0 # end of quarantine
                
            if individual.lastTestResult == True:
                individual.go_quarantine()
                   
                if random.random() < pReport: # not everyone reports a positive test to the app

                    send_notification(graph, i)
                    
                individual.app = False # unsubscribe from the app in order to not consider new notifications
            
        individual.timeLeftForTestResult -= 1
        

        if individual.in_state(ASYMP):
            if random.random() < pAtoG:
                graph.nbAS -= 1
                graph.nbCured += 1
                individual.state = CURED
        if individual.in_state(PRESYMP):
            if individual.daysIncubation == 0: # The person develops symptoms
                graph.nbPS -= 1
                graph.nbS += 1
                individual.state = SYMP

                # send the notifications (encounters[i] is empty if i doesn't have the app) | envoi des notifs (encounters[i] vide si i n'a pas l'appli)
                if random.random() < pReport and warningAfterSymptoms: # faire avec présymptomatique (TODO (?) : explicit comment)
                    send_notification(graph,i)
                if random.random() < pQSymptoms: # go into quarantine if symptoms appear | mise en confinement à la détection des symptômes
                    individual.daysQuarantine = daysQuarantine
                    
                test_individual(individual, graph)
                
        elif individual.in_state(SYMP):
            action = random.random()
            if action < pIStoC:
                graph.nbS -= 1
                graph.nbCured += 1
                individual.state = CURED
            elif action > 1 - pIStoD:
                graph.nbS -= 1
                graph.nbDead += 1
                individual.state = DEAD
                
        
        # some people send notif even though they are not actually infected by covid | certaines personnes envoient une notif alors qu'elles n'ont pas le covid
        # if warningAfterSymptoms is True, each individual has a probability of sending a false notification due to symptoms that are misinterpreted as from COVID19
        if warningAfterSymptoms and random.random() < pSymptomsNotCovid:
            send_notification(graph, i)
    
    # deleting oldest recorded day | suppression du plus vieux jour de l'historique
    for encounter in graph.encounters:
        encounter.pop(0)
        
    #updateCounters(graph)

# # Display
# Interactive model below (it takes about 10-15 sec to appear and to run a simulation)

import matplotlib.pyplot as plt

fig, ((ax, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=[15,10])
xs = []
y_D = []
y_MS = []
y_MPS = []
y_MAS = []
y_S = []
y_G = []
y_Q = []
y_InfectByAS = []
y_QuarantineNonI = []
y_QuarantineNonD = []
y_QuarantineNonITotal = []
y_Test = []
y_TestTotal = []

ax.set_ylim([0, nbIndividuals])

def update_viz(graph):
    xs.append(len(xs))
    y_D.append(graph.nbDead)                        # number of deceased people
    y_MS.append(graph.nbS)                          # number of symptomatic people 
    y_MPS.append(graph.nbPS)                        # number of premptomatic people 
    y_MAS.append(graph.nbAS)                        # number of asymptomatic people
    y_S.append(graph.nbHealthy)                     # number of healthy people
    y_G.append(graph.nbCured)                       # number of cured persons
    y_Q.append(graph.nbQuarantineTotal)             # number of people in quarantine
    y_InfectByAS.append(graph.nbInfectedByASPS)     # number of people infected by asymp. people
    y_QuarantineNonI.append(graph.nbQuarantineNonI)
    y_QuarantineNonD.append(graph.nbQuarantineNonD)
    y_Test.append(graph.nbTest)
    if y_QuarantineNonITotal != []:
        y_QuarantineNonITotal.append((graph.nbQuarantineNonI + nbIndividuals*y_QuarantineNonITotal[-1])/nbIndividuals)
        y_TestTotal.append((graph.nbTest + nbIndividuals*y_TestTotal[-1])/nbIndividuals)
    else:
        y_QuarantineNonITotal.append(graph.nbQuarantineNonI/nbIndividuals)
        y_TestTotal.append(graph.nbTest/nbIndividuals)
    
def draw_viz():
    ax.cla()
    labels = ["Deceased", "Asymptomatic","Presymptomatic", "Symptomatic", "Cured", "Healthy"]
    ax.stackplot(xs, y_D, y_MAS,y_MPS, y_MS, y_G, y_S , labels=labels, edgecolor="black", colors=["darkred", "orange","yellow", "red", "dodgerblue", "mediumseagreen"])
    
    labels2 = ["In quarantine and non infected", "In quarantine"]
    ax2.stackplot(xs, y_QuarantineNonI, y_QuarantineNonD, labels=labels2)

    #line, = ax3.plot(xs, y_InfectByAS)
    #line.set_label("Total infections by asympt.")
    
    line, = ax3.plot(xs, y_Q)
    line.set_label("Cumulative quarantine days per person")
    line, = ax3.plot(xs, y_QuarantineNonITotal)
    line.set_label("Cumulative quarantine days of healthy people per person")
    line, = ax3.plot(xs, y_TestTotal)
    line.set_label("Cumulative number of tests per person")
    
    line, = ax4.plot(xs, y_Test)
    line.set_label("Number of tests")
    
    
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),shadow=True, ncol=3)
    ax2.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),shadow=True, ncol=2)
    #ax3.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),shadow=True, ncol=1)
    ax3.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),shadow=True, ncol=2)
    ax4.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),shadow=True, ncol=2)
    plt.tight_layout()

def update_prob(app_utilisation, report_to_app, quarantine_when_notif):
    global nbIndividuals
    global utilApp
    global pReport
    global pQNotif
    
    utilApp = app_utilisation
    pReport = report_to_app
    pQNotif = quarantine_when_notif
    nbSteps = 60
    
    nbIndividuals = 100 # you may change the number of individuals for the exponential distribution graph here

    graph = Graph()
    init_graph_household(graph) # default graph generation using households structure, as shown in the Results section
    # uncomment this to get a graph with degrees following an exponential distribution
    #init_graph_exp(graph)
    xs.clear()
    y_D.clear()
    y_MS.clear()
    y_MAS.clear()
    y_S.clear()
    y_G.clear()
    y_Q.clear()
    y_InfectByAS.clear()
    y_QuarantineNonI.clear()
    y_QuarantineNonITotal.clear()
    y_QuarantineNonD.clear()
    y_Test.clear()
    y_TestTotal.clear()
    
    maxSymp = 0
    for step_ind in range(nbSteps):
        # update matplotlib
        update_viz(graph)
        # update simulation
        step(graph)
        maxSymp = max(maxSymp, graph.nbS)

    print("Number of deceased:", graph.nbDead)
    print("Max. nb of sympomatic people:", maxSymp)
    draw_viz()
    plt.show()

update_prob(utilApp, pReport, pQNotif)

interact_manual(update_prob, \
                app_utilisation = widgets.FloatSlider(min=0.0, max=1.0, step=0.01, value = utilApp), \
                report_to_app = widgets.FloatSlider(min=0.0, max=1.0, step=0.01, value = pReport), \
                quarantine_when_notif = widgets.FloatSlider(min=0.0, max=1.0, step=0.01, value = pQNotif))
