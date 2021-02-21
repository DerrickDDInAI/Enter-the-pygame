# Enter-the-pygame
This is a work in progress.


## Table of Contents

- [Introduction](#introduction)

- [Installation](#installation)

- [Instructions](#instructions)

- [Architecture](#architecture)

- [Next steps](#next-steps)

---

## Introduction
### Description

**_Describe the game_**

### Objectives
The game purpose is to demonstrate how:
- to **code a game** with python and pygame;
- to implement an **AI model** to solve the game by using neat module.

### Visuals
add images or gif
Tools: ttygif or Asciinema


## Installation
To run the python game, you need the following libraries:
- **pygame**
- **neat-python**

Follow these instructions to install the required libraries: on terminal
1. open your terminal
2. cd to the directory where the file *requirements.txt* is located
3. activate your virtual environment.
4. run: 
```pip3 install -r requirements.txt```

You can even install the libraries and run the game directly after the installation by running the following command line:

4. run:
```pip3 install -r requirements.txt && python3 run_game.py```

## Instructions
### How to run the game
- Run *run_game.py* to start the game.
Or
- On your terminal:
```python3 run_game.py```

### Usage example
Show example of the game; its output

## Architecture
The project is structured as follows:

```
Enter-the-pygame
│   README.md               :explains the project
│   run_game.py             :script to run in order to start the game.
│   requirements.txt        :packages to install to run the game
│   LICENSE.txt             :license information
│   .gitignore              :specifies which files to ignore when pushing to the repository
│
└───gamecore                :directory contains the game logic and the entities (classes such as Player, AI, Monsters, Obstacles,...)
│   │   __init__.py
│   │   main.py             :execute the game logic with pygame module
│   │
│   └───assets              :contains the media used in the game
│       ├───fonts
│       ├───images
│       └───sounds
│   
└───data                    :contains player profiles, saved game session, Best AI performer, AI performance statistics
```

### Contributing
Open to contributions.
Requirements to be defined.
Instructions to contribute will be described in this section.

### Change log
- Project creation on the `21th of February 2021`

### Author(s) and acknowledgment
This project is carried out by **Van Frausum Derrick** from Theano 2.27 promotion at BeCode.

### License
Enter-the-pygame is available under the "To be determined" license. See *LICENSE.txt* for more information.

## Next steps
