## Results of the model

## Limits

 * We don't take into account the eventual false postive of nasal test. We consider here that there is none.

 * The variability of infectioussness seems to be really high: an infected that will develop symptoms is really contagious during the 4 days before the symptoms and less for the 4 days after the symptoms according to [6].

 * The geographical heterogeneity of a nationnal territory is not taken into account, this is a simulation just for one isolated community

 * In the initial state a proportion of the population is contaminated at the same time. In reallity, after the end of the lockdown the person infected will have been infected at different instant, smoothing the pressure on healthcare systems.

 * Note: the evolution of Rt seems really chaotic after the 10 first days. This is due to the fact that after the 10 first days, there is not to much contamination that
take place. It means that the computation of the average of the number of contamination caused by an infected at time t will be done on little cases. This causes great random fluctuation to interpret carefully.

### Baseline case: without any app
<img src="https://raw.githubusercontent.com/GuilhemN/covid-19-tracing-app-modelling/master/images/0%25%2C-%2C-%2C[3%2C10]%2C5j%2C0.3.png" alt="current test in France" style="width: 500px;"/>

We see that the outbreak spread freely from the 5% initial infected until it contaminate almost all the population.
The initial Rt (R0) is a bit lower than 2 because the initial population has cured individual (10%) and because people who notice symptoms directly quarantine themselves.
This was not the case during the begining of the outbreak when R0 was evaluated around 2.

This graph is the reference of the future analysis.

### Influence of the time for tests results

We use these test parameters to model the current test abilities in France :
 * 5 day for test results
 * A 3 to 10 days validity window
 * 30% of false positive

Even with a great adhesion of the population (80%) the change in the epidemic spread on the graph below isn't even visible because of the test delay.
<img src="https://raw.githubusercontent.com/GuilhemN/covid-19-tracing-app-modelling/master/images/80%25%2C-%2C-%2C[3%2C10]%2C5j%2C0.3.png" alt="current test in France" style="width: 500px;"/>

In fact the crucial time length to keep in mind to curb the spread of the desease is the 5 days incubation period.
According to the last epidemiological satistics, it seems that asymptomatics are about 40% of the infected, yet they cause only 6% of the infection. [4]
The infectioussness of presymptomatics seems really high [4] [6], so much so that the majority of contamination are presymptomatic.
Moreover, when symptoms arise the person goes in quarantine. This means that symptomatic transmission is contained if this measure is well respected. This also means that presymptomatics contamination will be even more present.
To avoid them, there is a need to identify and quarantine infected in the begining of the incubation period. In fact, a 5-day delay is already to late.

* Note: The 5 days spaced spikes in test demand are due to the fact that an individual cannot request a test if he already had a demand waiting.

In the case of current France test abilities, the characteritic time is 2*5=10 days between the suspicion of the first infected and the quarantine 
of the person notified and infected by the first. The quarantine decision arrive far to late to be effective.

Furthermore the windows of validity for nasal testing is a key factor that limits the effectiveness of tests. Even if we
succeed in having almost perfect test (1% of false positive) and with results available with no delay, because of the 3-10 days window validity we will not be able to
identify and isolate presymptomatic cases that just got infected. Example of curve comparison with and without the window validity :

* with the window validity:
  <img src="https://raw.githubusercontent.com/GuilhemN/covid-19-tracing-app-modelling/master/images/80%25%2C-%2C-%2C[3%2C10]%2C0j%2C0.01.png" alt="with window validity" style="width: 500px;"/>
* without it:
  <img src="https://raw.githubusercontent.com/GuilhemN/covid-19-tracing-app-modelling/master/images/80%25%2C-%2C-%2C[-1%2C100]%2C0j%2C0.01.png" alt="without window validity" style="width: 500px;"/>

With the validity window, we can only identify infected 3 day after the infection, that's already a significant part of the incubation period.

* with better tests (2 days of delay and 15% of false negative) :
  <img src="https://raw.githubusercontent.com/GuilhemN/covid-19-tracing-app-modelling/master/images/80%25%2C-%2C-%2C[3%2C10]%2C2j%2C0.15.png" alt="with better tests" style="width: 500px;"/>

Even with better screening, we can see that the curve of the test requests appears earlier, but the
quarantine curve doesn't change much. This can be explained by the fact that a close contact has a probability of only about 2% of chance of causing a
contamination (according to a WHO report in China [9]). So this leads to a high test demand from persons that only have low chance of being
infected. And yet, in the better case, the decision of quarantining is taken 4 days after the infection, also to late.

In these simulations the test request is unrealistically high because we don't add any constraint on test capacity.
We may imagine a more nuanced system to determine if we need a test: the number of notifications received, the presumed infectiousness of the infected
at the time of the contact, the comorbidity factors etc. This could enable a more precise tracking of the presumed risk of individuals.

### Quarantine after notification:

* application of "quarantine after notification" and with current tests
  <img src="https://raw.githubusercontent.com/GuilhemN/covid-19-tracing-app-modelling/master/images/80%25%2CN%2C-%2C[3%2C10]%2C5j%2C0.3.png" alt="quarantine after notification with current tests" style="width: 500px;"/>

It provides a more aggressive response against the epidemic and prove to be effective even with the current test abilities. 
However a great part of its effectiveness is likely to be caused by the imposed quarantine of 80% of the population.
We can aslo see oscillations in the number of person in quarantine: when the pandemic first spread, a great part of the population 
quarantine itself according to the notification they received. After testing, a lot of them end the quarantine, causing the epidemic to spread again.

* application of "quarantine after notification" and with better tests (2 days of delay and 15% of false negative):
  <img src="https://raw.githubusercontent.com/GuilhemN/covid-19-tracing-app-modelling/master/images/80%25%2CN%2C-%2C[3%2C10]%2C2j%2C0.15.png" alt="quarantine after notification with better tests" style="width: 500px;"/>

The effectiveness of this policy is greater with better tests without causing more quarantine days because quarantine arrives before the 
great part of the incubation period. 
This is illustrated by the rapid collapse of Rt during the first days (red curve). 
This policy uses swift testing to get earlier and more efficient quarantines.
However, it also comes with high social cost because it means a voluntary quarantine during the waiting time of results.
Because of the great number of contacts in a day (34 on average), it means that almost all the users of the app quarantined after the first spread in the population.
This high social cost could lead to a lesser adoption of the app by the population.

Nonetheless if test results can be available quickly, both the effectiveness of this policy and the social cost are improved.


### Warning after symptoms

* application of "quarantine after notification", "warning after symptoms" and with better tests (2 days of delay and 15% of false negative):
  <img src="https://raw.githubusercontent.com/GuilhemN/covid-19-tracing-app-modelling/master/images/80%25%2CN%2CW%2C[3%2C10]%2C2j%2C0.15.png" alt="warning after symptoms with better tests" style="width: 500px;"/>

The proportion of notifications sent because of symptoms unrelated to COVID is difficult to estimate.
However if we manage to keep it fairly low ( < 0.5% of chance of no covid symptoms per person per day)
this can provide an effective work around of test delays if applied with "quarantine after notification".

### Influence of the proportion of users

In the case of better tests (2 days of delay and 15% of false negative) and the application of "Quarantine after notification" policy, 
we plot the influence on the proportion of users on several key values.

<img src="https://raw.githubusercontent.com/GuilhemN/covid-19-tracing-app-modelling/master/images/day_in_quarantine.png" alt="days in quarantine" style="width: 500px;"/>
<img src="https://raw.githubusercontent.com/GuilhemN/covid-19-tracing-app-modelling/master/images/max_assymp.png" alt="maximum number of assymptomatic cases" style="width: 500px;"/>
<img src="https://raw.githubusercontent.com/GuilhemN/covid-19-tracing-app-modelling/master/images/proportion_of_healthy.png" alt="Proportion of healthy persons after 60 days" style="width: 500px;"/>

We see that the use of the app will not reduce by much the maximal pressure on healthcare system (max. symptomatic) but will
significantly curb the total spread of the app.
By doubling the average day in quarantine per person, it triples the final proportion of healthy persons.
