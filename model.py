from IPython import get_ipython
# %%
####################
# GRAPH GENERATION #
####################

# TODO: remove duplicate of nbIndividuals in viz
nbIndividuals = 1000 # number of people in the graph | nombre d'individus dans le graphe
initHealthy = 0.85 # proportion of healthy people at start | la proportion de personnes saines à l'intant initial
initCured = 0.1 # proportion of cured people at start | proportion de personnes guéries à l'instant initial
# The other people are 60% presymptomatic and 40% asymptomatic at start | Les autres personnes sont 40% d'asymptomatiques et 60% de présymptomatiques au départ

# graph generation for exponential degrees distribution
#------------------------------------------------------
deg_avg = 100 # average number of connexions per person | le nombre moyen de connexions par personne
av_household_size = 6 # avergave size of household | la taille moyenne d'un foyer
household_proba = 1 # probability of meeting a person of the same household | la probabilité de contact par jour entre membres d'un même foyer
extern_contact_proba = 0.3 # probabilty of meeting a person of a different household | la probabilité de contact par jour entre personne de foyers différents

# average contacts per day = 0.3*(100-6) + 6 = 34.2

# graph generation with organization in households
#-------------------------------------------------
household_size = (3, 5) # min and max size of an household (uniform distribution) | extremums de la taille d'un foyer
household_link = 1 # probability of contact between members of a household | proba de contact entre membres d'un foyer

community_size = 1000 # 2500 is good but a bit slow | number of households in the community | nombre de foyers dans une communauté
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
pReadNotif = 0.8 # probablity of taking a notification into account (ask for a test, quarantine) | proba de prendre en compte une notification (demande de test, quarantaine)

pSymptomsNotCovid = 0.005 # every day, everyone sends a notification with prob. pSymptomsNotCovid | chaque jour, tout le monde envoie une notif avec proba PSymptomsNotCovid

############
# POLICIES #
############

# people warn the app immediately after having symptoms | on prévient l'application directement après avoir développé les symptômes
warningAfterSymptoms = False

# upon notification, an individual asks for a test (with some prob.)
# if true, user waits for test results in quarantine, else he goes in quarantine only upon reception of positive test results
# |
# à la reception d'une notif, l'utilisateur demande un test (avec une certaine proba)
# si vrai, il attend les résultats en quarantaine, sinon il ne se met en quarantaine qu'aux résultats d'un test positif
quarantineAfterNotification = False

###############
# TEST PARAMS #
###############

testWindow = (3, 10) # tests are only effective in a given window (time since infection) | les tests ne sont efficaces que dans une fenêtre de temps après infection

daysUntilResult = 2 # attente pour l'obtention des résultats
pFalseNegative = 0.15 # prob. of false negative | proba d'avoir un faux négatif
daysBetweenTests = 0


##############
# QUARANTINE #
##############

pQSymptoms = 0.9 # probability of going into quarantine when one has symptoms | proba de confinement lors de détection des symptômes
quarantineFactor = 100 # reduction factor applied to the probabilities when one is in quarantine | réduction des probas de rencontre lors du confinement
daysQuarantine = 14 # duration of the quarantine | durée de la quarantaine

#################
# PROBABILITIES #
#################
# !! Probabilities are given for 1 step of the process, thus overall prob. follows a geometric law for which expected values have been calculated

# paramters estimated -> a limit of the model
pCloseContact = 0.375 # prob. that a contact is a close contact (those detected by the app) | proba qu'un contact soit rapproché (ceux détectés par l'appli)
pContaminationCloseContact = 0.02 # prob. of contamination after close contact with an infected person | proba de contamination après contact rapproché avec qqn d'infecté
#according to https://www.who.int/docs/default-source/coronaviruse/who-china-joint-mission-on-covid-19-final-report.pdf -> around 1 to 5% of close contact lead to virus transmission
pContaminationCloseContactAsymp = 0.006
# infectiousness of asymptomatic people appears to be very low according to [4] and "Temporal dynamics in viral shedding and transmissibility of COVID-19" [6]

pContaminationFar = 0.001 # prob. of contamination upon non close contact (environmental or short contact) | proba de contamination par contact environnemental ou bref
pContaminationFarAsymp = 0.0003

# we took R0=2 estimate from [4] and : 34 contacts/day, an average time of infectiousness of 10 days (pre symptomatic + begining of symptoms period)

#average number of infected by symptomatic : (0.375*0.02+0.625*0.001)*34*10 = 2.76
#average number of infected by asymptomatic : (0.375*0.006+0.625*0.0003)*34*10 = 0.83

# this gives 0.6*2.76 + 0.4*0.83 = 1.99 persons infected in average by an infected
# this is plausible given the estimate of R0 and the fact that asymptomatic contamination appears to be minor
# [4] and [6]

# and (0.6*0.625*0.001 + 0.4*0.625*0.0003)*34*10 / R0 = 0.0765 -> the proportion of contaminations which are not due to close contact (environmental / short contact) (contaminations by asymptomatic people are neglected) estimated according to environmental contamination estimate in [4]
# thus most infections (92%) are susceptible to be noticed by the app

# -> the proportion of contaminations by asympt. people is : 0.4*0.83/(0.6*2.76 + 0.4*0.0.83) = 0.17 plausible according to the presumed low infectiosity shown in [4], but this is a conservative estimate (not the 0.06 given by this paper) given the high uncertainty around the results


pAsympt = 0.4 # probability of being asymptomatic when infected | proba qu'une personne infectée soit asymptomatique
# according to [4] and Diamond Princess estimates

# parameters for the lognormal law of the incubation period | paramètres pour la loi lognormale de la période d'incubation
incubMeanlog = 1.644 # -> ~5.5 days
incubSdlog = 0.363 # -> ~2.1 days
# according to [4]

pAtoG = 0.1 # probability of going from asymptomatic state to cured | proba de passer de asymptomatique à guéri
# according to "Clinical characteristics of 24 asymptomatic infections with COVID-19 screened among close contacts in Nanjing, China" [7]

pIStoC = 0.07 # probability of going from symptomatic state to cured | proba de passer de avec symptômes à gueri
pIStoD = 0.003 # probability of dying when symptomatic | proba de décès d'une personne présentant des symptômes

# average time with symptoms : 1/(0.07+0.003) = 13.7 days : plausible according to [4]
# death rate when symptoms : 0.003/0.07 = 4.3% : plausible in France according to estimate of 1.6M cases with symptoms and 6 000 deaths the 3 April
# https://www.mgfrance.org/publication/communiquepresse/2525-enquete-mg-france-plus-d-un-million-et-demi-de-personnes-prises-en-charge-par-leur-medecin-generaliste-pour-le-covid-19-entre-le-17-mars-et-le-3-avril


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

        self.nbTest = 0

        # cumulative counters :
        self.nbQuarantineTotal = 0
        self.nbInfectedByASPS = 0
        self.nbQuarantineI = 0
        self.nbQuarantineNonI = 0
        
        #to cumpute Rt
        self.stepNb = 0
        self.contaminations = []
        self.infectedByTTimeInfected = []

class Individual:
    """ Object holding the representation of an individual """

    def __init__(self, state, daysQuarantine, app, sentNotification, daysIncubation, timeSinceInfection, timeLeftForTestResult):
        self.state = state
        self.daysQuarantine = daysQuarantine
        self.app = app
        self.sentNotification = sentNotification
        self.daysIncubation = daysIncubation
        self.timeSinceInfection = timeSinceInfection
        self.timeSinceLastTest = np.inf # we don't want to test people too often
        self.timeLeftForTestResult = timeLeftForTestResult
        self.nbInfected = 0

    def in_state(self, state):
        return self.state == state

    def is_infected(self):
        return self.state in [PRESYMP, ASYMP, SYMP]

    def has_no_covid(self):
        return self.state in [HEALTHY, CURED]

    def in_quarantine(self):
        return self.daysQuarantine > 0

    def go_quarantine(self): # TODO: use throughout the code
        if self.daysQuarantine <= 0:
            self.daysQuarantine = daysQuarantine # goes into quarantine if isn't already

# # Graph generation

def create_individuals(graph):
    graph.contaminations.append(0)
    for i in range(nbIndividuals):
        app = False
        if random.uniform(0,1) < utilApp:
            app = True
        s = PRESYMP
        time_since_infection = -1
        incub = 0
        r = random.random()
        if r < initHealthy:
            s = HEALTHY
            graph.nbHealthy += 1
        elif r < initHealthy + initCured:
            s = CURED
            graph.nbCured += 1
        else:
            graph.contaminations[0] +=1 #we start as if a proportion of the population just has been infected
            time_since_infection = 0
            if random.random() < pAsympt:
                graph.nbAS+=1
                s = ASYMP
                
            else:
                s = PRESYMP
                incub = round(np.random.lognormal(incubMeanlog, incubSdlog))
                graph.nbPS += 1

        # state, quarantine, app, notif, incubation, timeSinceInfection, timeLeftForTestResult
        graph.individuals.append(Individual(s,  0, app, False, incub, time_since_infection, -1))


def init_graph_exp(graph):
    """ Graph initialisation based on exponential ditribution of degrees """
    
    create_individuals(graph)

    # affecting degrees to vertices
    degrees = np.around(np.random.exponential(deg_avg, nbIndividuals))

    # to get an even number of total degrees
    S = sum(degrees)
    if S%2 == 1:
        degrees[0] += 1
        S += 1

    graph.adj = [[] for i in range(nbIndividuals)]
    while S > 0:
        # creating an edge
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

    # creation of the households
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

    # linkage of the households
    for i in range(av_deg_by_household*community_size):
        x1 = random.randint(0, len(graph.adj)-1)
        x2 = random.randint(0, len(graph.adj)-1)

        graph.adj[x1].append({"node": x2, "proba": community_link})
        graph.adj[x2].append({"node": x1, "proba": community_link})

    nbIndividuals = len(graph.adj)

    create_individuals(graph)

    graph.encounters = [[[] for jour in range(daysNotif)] for individual in range(nbIndividuals)]

# # Updating the graph

def contamination(graph, i, j, closeContact):
    """ Individuals i and j have come into contact, leading to a possible contamination | Les individus i et j sont entrés en contact, une contamination est possible """

    if graph.individuals[i].state == graph.individuals[j].state:
        return

    if graph.individuals[i].in_state(HEALTHY):
        contamination(graph, j, i, closeContact)
        return

    # i is the infected individual
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
                # j becomes infected
                
                #for Rt compuation
                graph.contaminations[graph.stepNb] +=1
                #print(len(graph.infectedByTTimeInfected), graph.stepNb - graph.individuals[i].timeSinceInfection)
                graph.infectedByTTimeInfected[graph.stepNb - graph.individuals[i].timeSinceInfection] +=1
                
                if graph.individuals[i].in_state(ASYMP) or graph.individuals[i].in_state(PRESYMP):
                    graph.nbInfectedByASPS += 1
                graph.individuals[j].timeSinceInfection = 0
                graph.individuals[i].nbInfected += 1 # i has infected one more person
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

    # the person was tested not long ago
    if individual.timeSinceLastTest < daysBetweenTests:
        return

    # the person is tested
    individual.timeSinceLastTest = 0
    graph.nbTest += 1
    individual.timeLeftForTestResult = daysUntilResult

    if individual.has_no_covid():
        individual.lastTestResult = False # we assume that there are no false positives
        return

    if individual.timeSinceInfection < testWindow[0] or individual.timeSinceInfection > testWindow[1]:
        individual.lastTestResult = False # not in the detection window, the test fails
        return

    # otherwise the person is ill
    # the test result depends whether we have a false negative or not
    individual.lastTestResult = not (random.random() < pFalseNegative)


nbNotif = 0
nbPersNotif = 0
def send_notification(graph, i):
    """ Send notification to people who have been in touch with i | Envoi d'une notif aux personnes ayant été en contact avec i """

    global nbNotif
    global nbPersNotif

    if graph.individuals[i].sentNotification:
        return # notifications already sent

    nbNotif += 1

    graph.individuals[i].sentNotification = True
    for daysEncounter in graph.encounters[i]:
        # note: graph.encounter[i] is empty if i does not have the app so there is no need to have an additional condition
        for contact in daysEncounter:
            if random.random() < pReadNotif: # if the person takes the notification into account
                # the person is always tested (TODO: change this ?)
                test_individual(graph.individuals[contact], graph) # asks for a test
                if quarantineAfterNotification: # in this case, the person waits for test results in quarantine
                    graph.individuals[contact].go_quarantine()
                nbPersNotif += 1

def make_encounters(graph, i):
    """ Assess all encounters made by i in one day | Détermine toutes les rencontres faites par i en un jour """

    for edge in graph.adj[i]:
        j = edge['node']
        if j < i:
            continue # only check one way of the edge | on ne regarde qu'un sens de chaque arête

        # if i and/or j are in quarantine, reduce the probability that they meet | si i et/ou j sont confinés, réduction de leur proba de rencontre
        factor = 1
        if graph.individuals[i].in_quarantine():
            factor *= quarantineFactor
        if graph.individuals[j].in_quarantine():
            factor *= quarantineFactor

        if random.random() < edge['proba'] / factor:
            if random.random() < pCloseContact: # if this is a close contact
                # if i and j have the app, we save their encounter | si i et j ont l'appli, on note la rencontre
                if graph.individuals[i].app and graph.individuals[j].app and random.random() < pDetection:
                    graph.encounters[i][-1].append(j)
                    graph.encounters[j][-1].append(i)
                contamination(graph, i, j, True)
            else:
                contamination(graph, i, j, False)

def step(graph):
    """ Step from a day to the next day | Passage au jour suivant du graphe """

    graph.nbTest = 0
    for encounter in graph.encounters:
        encounter.append([]) # will contain every encounter of the day | contiendra les nouvelles rencontres du jour

    graph.contaminations.append(0)
    graph.infectedByTTimeInfected.append(0)
    

    ## go through each possible encounter | on constate toutes les rencontres entre individus
    for i in range(nbIndividuals):
        make_encounters(graph, i)

    ## update the states | on met à jour les états des individus
    for i, individual in enumerate(graph.individuals):

        # TODO: test management should be done *after* test attribution (currently daysUntilResult is 1 more than expected)
        # TODO (?): separate function
        # reception of test results | réception des résultats de test
        if individual.timeLeftForTestResult == 0:
            if individual.in_quarantine() and individual.lastTestResult == False: # is in quarantine and gets a negative test
                individual.daysQuarantine = 0 # end of quarantine

            if individual.lastTestResult == True:
                individual.go_quarantine()
                individual.timeLeftForTestResult = np.inf # people tested positive are not tested again

                if random.random() < pReport: # not everyone reports a positive test to the app
                    send_notification(graph, i)

                individual.app = False # unsubscribe from the app in order to not consider new notifications
        individual.timeLeftForTestResult -= 1

        if individual.in_state(ASYMP):
            if random.random() < pAtoG:
                graph.nbAS -= 1
                graph.nbCured += 1
                individual.state = CURED

        elif individual.in_state(PRESYMP):
            if individual.daysIncubation == 0: # the person develops symptoms
                graph.nbPS -= 1
                graph.nbS += 1
                individual.state = SYMP

                # send the notifications (encounters[i] is empty if i doesn't have the app) | envoi des notifs (encounters[i] vide si i n'a pas l'appli)
                if random.random() < pReport and warningAfterSymptoms:
                    send_notification(graph, i)
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

        # if warningAfterSymptoms is True, each individual has a probability of sending a false notification due to symptoms that are misinterpreted as from COVID-19
        # | si warningAfterSymptoms est vrai, chaque individu a une probabilité d'envoyer une notification en raison de symptômes faussement perçus comme relevant du COVID-19
        if warningAfterSymptoms and random.random() < pSymptomsNotCovid:
            send_notification(graph, i)

    ## handle new day | on passe au jour suivant
    graph.nbQuarantineNonI = 0
    graph.nbQuarantineI = 0

    for individual in graph.individuals:
        if individual.in_state(DEAD):
            continue

        individual.daysQuarantine -= 1
        individual.daysIncubation -= 1
        individual.timeSinceLastTest += 1

        # if there are still symptoms we don't end the quarantine
        if (not individual.in_quarantine()) and individual.in_state(SYMP):
            individual.daysQuarantine = 1

        if individual.in_quarantine():
            graph.nbQuarantineTotal += 1/nbIndividuals
            if not individual.is_infected():
                graph.nbQuarantineNonI += 1
            else:
                graph.nbQuarantineI += 1

        if individual.timeSinceInfection >= 0:
            individual.timeSinceInfection += 1

    ## deleting oldest recorded day | suppression du plus vieux jour de l'historique
    for encounter in graph.encounters:
        encounter.pop(0)
    graph.stepNb +=1

# # Display
# Interactive model below (it takes about 10-15 sec to appear and to run a simulation)

# ! uncomment for the notebook version :
# %matplotlib notebook
import matplotlib.pyplot as plt

fig, ((ax, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=[15,10])
axRt = ax3.twinx()

xs = []
y_D = []
y_MS = []
y_MPS = []
y_MAS = []
y_S = []
y_G = []
y_Q = []
y_InfectByASPS = []
y_QuarantineNonI = []
y_QuarantineI = []
y_QuarantineNonITotal = []
y_Test = []
y_TestTotal = []
y_Rt = []

ax.set_ylim([0, nbIndividuals])

def update_viz(graph):
    if y_QuarantineNonITotal != []:
        y_QuarantineNonITotal.append((graph.nbQuarantineNonI + nbIndividuals*y_QuarantineNonITotal[-1])/nbIndividuals)
        y_TestTotal.append((graph.nbTest + nbIndividuals*y_TestTotal[-1])/nbIndividuals)
    else:
        y_QuarantineNonITotal.append(graph.nbQuarantineNonI/nbIndividuals)
        y_TestTotal.append(graph.nbTest/nbIndividuals)



    xs.append(len(xs))                                                  # TODO: put all these comments at variable def (in Graph class)
    y_D.append(graph.nbDead/nbIndividuals*100)                          # number of deceased people
    y_MS.append(graph.nbS/nbIndividuals*100)                            # number of symptomatic people
    y_MPS.append(graph.nbPS/nbIndividuals*100)                          # number of premptomatic people
    y_MAS.append(graph.nbAS/nbIndividuals*100)                          # number of asymptomatic people
    y_S.append(graph.nbHealthy/nbIndividuals*100)                       # number of healthy people
    y_G.append(graph.nbCured/nbIndividuals*100)                         # number of cured persons
    y_Q.append(graph.nbQuarantineTotal)                                 # number of people in quarantine
    y_InfectByASPS.append(graph.nbInfectedByASPS)                       # number of people infected by asymp. + presymp. people
    y_QuarantineNonI.append(graph.nbQuarantineNonI/nbIndividuals*100)
    y_QuarantineI.append(graph.nbQuarantineI/nbIndividuals*100)
    y_Test.append(graph.nbTest)
    


def draw_viz(graph):
    ax.clear()
    ax2.clear()
    ax3.clear()
    ax4.clear()
    axRt.clear()
    
    ax.set_xlabel("Days")
    ax2.set_xlabel("Days")
    ax3.set_xlabel("Days")
    ax4.set_xlabel("Days")
    
    
    for i in range(graph.stepNb):
        if graph.contaminations[i] !=0 and graph.contaminations[i] > 5: #we just take into account days where there was more than 5 contaminations to avoid great fluctuation caused by randomness during days with less than 5 contaminations.
            y_Rt.append(graph.infectedByTTimeInfected[i]/graph.contaminations[i])
        else:
            y_Rt.append(0)
            
    for i in range(1,graph.stepNb-1): #beacause of the great variability of Rt when there is little contamination, we smooth its values to get a more coherent evolution
        if y_Rt[i] == 0:
            y_Rt[i] = (y_Rt[i-1] + y_Rt[i+1])/2
    

    labels = [ "Symptomatic", "Deceased", "Asymptomatic","Presymptomatic", "Cured", "Healthy"]
    ax.stackplot(xs, y_MS, y_D, y_MAS,y_MPS, y_G, y_S, labels=labels, edgecolor="black", colors=["red", "darkred", "orange","yellow", "dodgerblue", "mediumseagreen"])
    ax.set_ylabel("Proportion of the population")

    labels2 = ["In quarantine and non infected (percentage)", "In quarantine and infected (percentage)"]
    ax2.stackplot(xs, y_QuarantineNonI, y_QuarantineI, labels=labels2)
    ax2.set_ylabel("Proportion of the population")
    #line, = ax3.plot(xs, y_InfectByASPS)
    #line.set_label("Total infections by asympt.")

    ax3.set_ylabel("Quarantine days / Tests")
    line, = ax3.plot(xs, y_Q)
    line.set_label("Cumulative quarantine days per person")
    line, = ax3.plot(xs, y_QuarantineNonITotal)
    line.set_label("Cumulative quarantine days of healthy people per person")
    line, = ax3.plot(xs, y_TestTotal)
    line.set_label("Cumulative number of tests per person")
    axRt.set_ylabel("Rt", color = 'red')
    line, = axRt.plot(xs, y_Rt, color = 'red')
    line.set_label("Rt (average number of infections caused by one infected)")

    line, = ax4.plot(xs, y_Test)
    line.set_label("Number of tests")
    ax4.set_ylabel("Tests")

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), shadow=True, ncol=3)
    ax2.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), shadow=True, ncol=1)
    #ax3.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), shadow=True, ncol=1)
    ax3.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), shadow=True, ncol=2)
    #axRt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), shadow=True, ncol=1) #to avoid legend on top of the other
    ax4.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), shadow=True, ncol=2)
    plt.tight_layout()

def update_prob(app_use_rate, report_to_app, read_notif, warning_after_symptoms, quarantine_after_notification):
    global nbIndividuals
    global utilApp
    global pReport
    global pReadNotif
    global quarantineAfterNotification
    global warningAfterSymptoms
    global xs, y_D, y_MS, y_MPS, y_MAS, y_S, y_G, y_Q, y_InfectByASPS, y_Rt
    global y_QuarantineNonI, y_QuarantineNonITotal, y_QuarantineI, y_Test, y_TestTotal

    # TODO: clarify/simplify ?
    utilApp = app_use_rate
    pReport = report_to_app
    pReadNotif = read_notif
    warningAfterSymptoms = warning_after_symptoms
    quarantineAfterNotification = quarantine_after_notification
    nbSteps = 60

    nbIndividuals = 4000 # you may change the number of individuals for the exponential distribution graph here

    graph = Graph()
    init_graph_household(graph) # default graph generation using households structure, as shown in the Results section
    # uncomment this to get a graph with degrees following an exponential distribution
    #init_graph_exp(graph)
    xs.clear()
    y_D.clear()
    y_MS.clear()
    y_MPS.clear()
    y_MAS.clear()
    y_S.clear()
    y_G.clear()
    y_Q.clear()
    y_InfectByASPS.clear()
    y_QuarantineNonI.clear()
    y_QuarantineNonITotal.clear()
    y_QuarantineI.clear()
    y_Test.clear()
    y_TestTotal.clear()
    y_Rt.clear()

    maxSymp = 0
    for step_ind in range(nbSteps):
        # update matplotlib
        update_viz(graph)
        # update simulation
        step(graph)
        maxSymp = max(maxSymp, graph.nbS)

    # print("Total individuals:", nbIndividuals)
    # print("Number of deceased:", graph.nbDead)
    # print("Max. nb of symptomatic people:", maxSymp)
    # print("Test per people:", y_TestTotal[-1])
    # print("Final healthy:", y_S[-1])
    print(maxSymp/nbIndividuals,",", y_S[-1],",", y_Q[-1], ",", y_TestTotal[-1])
    draw_viz(graph)
    plt.show()



update_prob(utilApp, pReport, pReadNotif, warningAfterSymptoms, quarantineAfterNotification)


# interact_manual(update_prob, \
#                 app_use_rate = widgets.FloatSlider(min=0.0, max=1.0, step=0.01, value=utilApp), \
#                 report_to_app = widgets.FloatSlider(min=0.0, max=1.0, step=0.01, value=pReport), \
#                 read_notif = widgets.FloatSlider(min=0.0, max=1.0, step=0.01, value=pReadNotif), \
#                 warning_after_symptoms = widgets.Checkbox(value=warningAfterSymptoms), \
#                 quarantine_after_notification = widgets.Checkbox(value=quarantineAfterNotification))
