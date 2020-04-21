# Results of the model

# Limits

We don't take into account the eventual false postive of nasal test. We consider here that there is none.

The variability of infectioussness seems to be really high: an infected that will develop symptoms is really contagious during the 4 days befor the symptoms 
and less for the 4 days after the symptoms.

The geographical heterogeneity of a nationnal territory is not taken into account, this is a simulation just for one isolated community


## Influence of the time for tests results

We use test parameters to model the current test abilities in France :
 * 5 day for test results
 * A 3 to 10 days validity window
 * 30% of false positive

Even with a great adhesion of the population (80%) the change in the epidemic spread isn't even visible because of the test delay.
Indeed the characteristic time is 2*5=10 days between the suspicion of the first infected and the quarantine of the person notified
and infected by the first. This is more than the incubation time (~5 days) and around the time of infectiousness of asymptomatics.
In fact, the decision of quarantine arrives after the symptoms of the newly infected person or even after he's cured.

Moreover the windows of validity for testing will really limit the effectiveness of testing. Even if we
succeed in having test results available in the day, because of the 3-10 days windows validity we will not be able to
identify isolated presymptomatic cases that just got infected. Example of curve comparison with and without the window validity :
* with the window validity:
  <img src="https://raw.githubusercontent.com/GuilhemN/covid-19-tracing-app-modelling/master/images/viz_80app_q_nowindow.png" alt="with window validity" style="width: 500px;"/>
* without it:
  <img src="https://raw.githubusercontent.com/GuilhemN/covid-19-tracing-app-modelling/master/images/viz_80app_q.png" alt="without window validity" style="width: 500px;"/>


Even with better screening (2 days of delay and 15% of false negative), we can see that the curve of the test requests appears earlier, but the
quarantine curve doesn't change much. This can explained by the fact that a close contact has a probability of only about 2% of chance of causing a
contamination (according to a WHO report in China). So this leads to high requesting of tests from persons that only have low chance of being
infected.

We may imagine a more nuanced system to determine if we need a test: the number of notifications received, the presumed infectiousness of the infected
at the time of the contact etc. This could enable a more precise tracking of the presumed risk of individuals.

## Quarantine after notification:

<img src="https://raw.githubusercontent.com/GuilhemN/covid-19-tracing-app-modelling/master/images/viz_80app_q.png" alt="quarantine after notification" style="width: 500px;"/>

It provides a more aggressive response against the epidemic and prove to be effective even with the current test abilities.
Its effectiveness is even better with better tests without causing more quarantine days.
This policy really uses the ability to get swift testing to get an earlier and more efficient quarantine.
However, it also comes with high social cost because it means a voluntary quarantine during the waiting time of results.
Because of the great number of contacts in a day, it means that almost all the users of the app quarantined after the first spread in the population.
This high social cost could lead to a lesser adoption of the app by the population.

Nonetheless if test results can be available quickly, both the effectiveness of this policy and the social cost are improved.


## Warning after symptoms

<img src="https://raw.githubusercontent.com/GuilhemN/covid-19-tracing-app-modelling/master/images/viz_80app_w.png" alt="warning after symptoms" style="width: 500px;"/>

The proportion of notifications sent because of symptoms unrelated to COVID is difficult to estimate.
However if we manage to keep it fairly low ( < 0.5% of chance of no covid symptoms per person per day)
this can provide an effective work around of test delays.

## Influence of the proportion of users

In the case of better tests and the application of "Quarantine after notification" policy, we plot the influence on the proportion of
user on several key values.

We see that the use of the app will not reduce by much the maximal pressure on healthcare system (max. symptomatic) but will
significantly curb the total spread of the app.
By doubling the average day in quarantine per person, it triples the final proportion of healthy persons.
