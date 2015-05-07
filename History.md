# Origin #

Stableorbit started out as two programs, a Genetic Algorithm and a 3D solar system visualiser (named 'GA' and 'planetarium' respectively). The Genetic Algorithm uses stochastic methods to find long lasting (stable) solar system configurations. Through repeated mutations and simulations GA pushes a population of solar systems, each containing one or more stars and multiple planets towards long-term stability. The planetary systems can then be displayed in 3D using our planetarium tool.

# Evolution #

GA and planetarium were excellent candidates for creating a distributed GA that doubled as a screen saver. By offloading the CPU-intensive fitness evaluation to the client (running planetarium as the screen saver) we were able to vastly increase the number of systems generated simultaneously simply by connecting more clients.

Although operational, further modifications were needed before we started to generate systems with both good stability ratings as well as elliptical orbits. More of this is described later.