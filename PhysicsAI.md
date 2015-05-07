# Concepts #
Stableorbit didn't always produce pretty elliptical orbits. The searching algorithm required a great deal of tuning before the desired results were achieved.

# Physics & AI Concepts #

"Stableorbit utilizes an O(N^2) Leapfrog Euler Algorithm for numerical integration.  Using the leapfrog method we may make our time step larger while conserving the total energy of the system.  The derivation of the leapfrog method can be found here:

http://stableorbit.googlecode.com/files/SO-Physics.pdf

- Ryan Haynes (co-developer)

A solar system's stability (or fitness) is determined inside 'orbitSystem.py' using the Virial Theorem. The Virial Theorem provides us with a numerical representation of the ratio between potential and kinetic energy. A value between 0.3 and 1 indicates a potentially stable system. Because elliptical orbits cause planets to speed up and slow down (yielding different Virial ratios) the VT scores must be averaged over time.

The GA initially focused on trying to create multi-planet and multi-star systems. We had a difficult time creating anything that resembled an orbit. Even after evaluating systems over  extremely large time period (searching for VT averages of about 0.5) we couldn't find any orbits. Later on I determined the root of the problem.  Our systems were being generated with multiple stars and about fifteen planets, the masses of the additional star or stars were throwing off the Viral Theorem and causing the planets to become insignificant in terms of the VT. This left us with stable binary systems of two or more stars orbiting each other and numerous planets flying out into space.  Restricting the starting conditions to one star and one planet enabled orbits to be found using a simple random search without the need for a Genetic Algorithm.

More info on the Virial Theorem can be found here:

> http://en.wikipedia.org/wiki/Virial_theorem