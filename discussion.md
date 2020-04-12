# Discussion around the proposed model

### Context of creation

This model was created during the COVID19 Hackaton between the 10th and the 12th of April and organized by HEC et l'Ecole Polytechnique.
It was created to model the impact of the adoption of social tracing app as STOP COVID in France on the spread of the pandemic.
Its primary goal is to shwo the influence of parameters such as the proportion of user of the app in the global population or the account of the applicaiton notification: after a 
suspected transmission notified by the app, will the citizen chose to directly quarantine themself ?


### Motivation

We are student as ENS de Lyon in computer science, so we aren't expert in the field of epidemiology. This model isn't supposed to give prediction for the future of the pandemic.
However, it give a good intuition of the impact of social tracing app on the epidemic. Change the parameters yourself to convince you that this precise quarantining of suspected case can lead to great limitation of the spread.
Play with them !

### Bibliography

Contact network epidemiology is a paradigm to modelize an epidemic, it has been widely studied and it can account for discrepency of transmission beteween individuals.
It has been discussed that this approach is suited to model epidemic as SARS Cov 1 in [1].
That's why we chose this approach.
Moreover, the structure of the graph chosen has a great impact of the final size of the outbreat, as discussed in [2].
We chose two model for the graph : a model using an exponential law for the degrees distribution. This seems suited for desease as SARS and urban areas [3]. 
For the second graph structure, we used a method from [3] and we build the network by stages : first we build households, next the connection between them.

As for the epidemiological parameters of the desease, we adpated parameters from [4] to be suited for our model.
Also, other models for the impact of social tracing app have been proposed such as in [5] and [4].


### Limits of the model

The stronger limit of the model is the duration of infected period. As we use Markov chain like modelisation at the scale of the individual, the espected time in the 
state "Infected" follows a geometric law as opposed to a law closer to lognormal according to [4].
Moreover, the parameters of the initial graph were detecrmined to get an average number of contact of around 30 / days without much support nor information found about this.

With this fixed average contact per day,the average time infectious and R0 estimated by [4],  we computed the propability of transmistion during a contact.

### Pseudocode of the model


* [1] Contact network epidemiology: Bond percolation applied to infectious disease prediction and control, Lauren Ancel Meyers 
* [2] Contact Network Epidemiology: MathematicalMethods of Modeling a Mutating Pathogen ona Two-type NetworkRobert by L. Seilheimer
* [3] Network theory and SARS: predicting outbreak diversity by Lauren Ancel Meyers &al.
* [4] Quantifying SARS-CoV-2 transmission suggests epidemic control with digital contact tracing.  - PubMed - NCBI
* [5] The Impact of Contact Tracing in Clustered Populations by Thomas House & Matt J Keeling