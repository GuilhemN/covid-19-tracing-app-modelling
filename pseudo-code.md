# Pseudo-code : modelisation de l'impact de d'adoption d'application de traçage social

### Initialisation 

* Graphe social pondéré par des poids P(u,v) dans [0,1]
    * Organisation en communauté avec 3 niveau de proximité : foyer, communauté, éloigné
* Proportion initiale de Guéri (G), Sain (S), Infecté avec symptomes (IS), Infectés assymptomatiques (A)
* Proportion d'utilisateurs de l'appli (Uapp)

### Itération

```
Pour tout (u,v) ds E 
    Avec proba P(u,v):
        Il y a contact entre u et v.
        Si exactement un des deux est infecté, l'autre le devient avec une proba P[trans]
        
        Si Appli[u] et Appli[v], avec proba P[detect appli]:
            ajouter le contact à l'historique H
    Sinon:
        Avec porba P[faux positif appli]:
            ajouter le contact à H
            
Pour tout u dans V:
    Si u est dans A:
        Avec proba P[A->G]:
            u va dans G
        Avec proba P[A->IS]:
            u va dans IS
            Si u a l'appli:
                Avec proba P[signalement symptomes]:
                    Je préviens les contacts de H que j'ai eu dans les J derniers jours
                    Les prévenus passent en quarantaine avec proba P[Q|notif]
            Je passe en quarantaien avec proba P[Q|symptome]
            
    Si u est dans IS:
        avec proba P[IS->G]:
            je passe dans G
        avec proba P[IS->M]:
            je passe dans M (les morts)

POur tout u dans E:
    Si u vient de passer en quarantaine:
        CptQ[u] <- D[Q]
        diviser tous les P(u,v), avec v dans V par RedQ
    Si CptQ[u] >0:
        CptQ[u] -= 1
        Si CptQ[u] == 0:
            multiplier tous les P[u,v], v dans V par RedQ
```
            
### Paramètres:
    * Topologie du graphe
    * Proportion initiale G, A, IS
    * Uapp : utilisation de l'appli
    * P[A->G]
    * P[A->IS]
    * P[Q|notif]
    * P[Q|symptome]
    * P[IS->M]
    * P[IS->G]
    * P[trans]
    * D[Q]
    * RedQ
    * J =~ 14 jours
    * P[detect appli] /!\ prendre en compte qu'il existe des transmissions de surfaces etc : out ce qui n'est pas par contact social /!\
    * P[faux positif appli]
            
### Hypothèses:
    * La plus grosse hypothèse est l'espérance du temps resté infecté, ici cela suite une loi géométrique alors que dans la vraie vie cela semble etre plus binomiale/ loi normale ...
    * Imunité après la guérison
        
            
            
            
            
            
            
            
            
        
