# Factorio Quality Calculator

Markov chain simulations of production quality in the video game Factorio. [The web app can be accessed here](https://factorio-quality.streamlit.app/).

## Project Overview

The project is a single page web application consisting of: 
1. a backend coded in Python including a FastAPI API.
2. a Python frontend using the Streamlit framework.

Streamlit is used for building simple frontends for data-intensive applications. The entire project is built using Docker.

Unfortunately having an API made it harder to host the finished project online for free. To get around this, this project has 2 branches: ```main``` and ```streamlit```. The ```main``` branch contains the finished app, ready to be run locally through Docker. The ```streamlit``` contains an uglier, API-less version of the code which is solely used to deploy the web app [here](https://factorio-quality.streamlit.app/). The finished project on the two branches is identical, the ```main``` branch just has more readable and maintainable code as well as more up-to-date documentation.

## Running the project

To run the Streamlit app, run ```docker-compose up --build``` from the base directory on the ```main``` branch. This will install Python and its dependencies, run the unit tests and then start the project. After that the project can be found at ```localhost:8501/```.

## About the simulations in the project

In the video game Factorio, the goal is to build a factory. As the player progresses the game, they gain the ability to construct machines of higher quality, which are better.

Players will usually pursue this strategy late-game to mass-produce items of high quality:

1. Build an item in an assembly machine, which has a small chance to produce an item of higher quality than the quality of the ingredients used.

2. If the item produced does not have the desired quality, put it in a recycler. This returns a fraction of the ingredients which were used to construct the item in step 1, possibly upgrading their quality in process.

These two steps are repeated indefinitely. The fraction of initial ingredients that end up as quality items depends on several factors including research and what chips are inserted into the assembly machines.

The purpose of this app is to allow a user to experiment with how these various factors impact the number of ingredients needed to produce high quality items.

The situation outlined here is a stochastic process which shares many similarities with [Markov chains](https://en.wikipedia.org/wiki/Markov_chain). As a result, an algorithm heavily inspired by Markov chain theory was developed and implemented in the backend as part of this project.