# Discussion around the proposed model

### Context of creation

This model was created during the COVID19 Hackaton between the 10th and the 12th of April and organized by HEC and l'Ecole Polytechnique.
It was created to model the impact of the adoption of a social tracing app like STOP COVID in France on the spread of the pandemic.
Its primary goal is to show the influence of parameters such as the proportion of users using the app in the global population or the account of the applicaiton notification: after a suspected transmission notified by the app, will the citizen choose to directly quarantine themselves ?


### Motivation

We are students at ENS de Lyon in computer science, so we aren't expert in the field of epidemiology. This model isn't supposed to give predictions for the future of the pandemic.
However, we developped this simple but clear model in 2 days (!) to get a rapid sense of what we could expect from a social tracing app !
It gives a good intuition of the impact of a social tracing app on the epidemic depending of the adoption of the app. 
Change the parameters yourself to convince yourself that precise quarantining of suspected cases can lead to a great limitation of the spread if it is well adopted by the population.
Play with them !

### Bibliography

Contact network epidemiology is a paradigm to modelize an epidemic, it has been widely studied and it can account for discrepency of transmission between individuals.
It has been discussed that this approach is suited to model epidemic as SARS Cov 1 in [1].
That's why we chose this approach.
Moreover, the structure of the graph chosen has a great impact of the final size of the outbreat, as discussed in [2].
We chose two models for the graph : a model using an exponential law for the degrees distribution. This seems suited for a desease such as SARS and urban areas [3]. 
For the second graph structure, we used a method from [3] and we built the network by stages : first we build households, next the connection between them.

As for the epidemiological parameters of the desease, we adapted parameters from [4] to be suited for our model.
Also, other models for the impact of a social tracing app have been proposed such as in [5] and [4].

### The model

Each vertex of the graph is an individual that can be : Healthy, Infected with symptoms, Infected without symptoms, Dead or Recovered.
At each step we go trough all the edges and with the probability given by these edges, there is a contact between the individuals.
If one of them is infected and the other healthy, it gives the infection to the other. With a propability of detection, the app notices this contact.

After that, if an individual infected get symtoms, the app warns with a certain probability all the persons he met in the past 14 days. 
All the warned individual quarantine themselves for 14 days themselves with a certain propability.


### Limits of the model

The stronger limit of the model is the duration of infected period. As we use a Markov chain like modelisation at the scale of the individual, the expected time in the 
state "Infected" follows a geometric law as opposed to a law closer to log-normal according to [4].
Moreover, the parameters of the initial graph were determined to get an average number of contact of around 30 / days without much support nor information found about this.

With this fixed average contact per day, the average time infectious and R0 estimated by [4], we computed the propability of transmistion during a contact.

### Pseudocode of the model


* [1] Contact network epidemiology: Bond percolation applied to infectious disease prediction and control, Lauren Ancel Meyers 
* [2] Contact Network Epidemiology: MathematicalMethods of Modeling a Mutating Pathogen ona Two-type NetworkRobert by L. Seilheimer
* [3] Network theory and SARS: predicting outbreak diversity by Lauren Ancel Meyers &al.
* [4] Quantifying SARS-CoV-2 transmission suggests epidemic control with digital contact tracing.  - PubMed - NCBI
* [5] The Impact of Contact Tracing in Clustered Populations by Thomas House & Matt J Keeling