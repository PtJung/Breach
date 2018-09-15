# Breach

## Program Description

"Breach" is the name of my ICS3U culminating assignment, inspired by **surviv.io**, an online 2-D battle royal game. 

**Python Libraries:**
* pygame

## Idea

The idea of the game is explained below:
                    
### Background
                    
As a result of their unsuspected artificial intelligence, lab robots are on the run to eliminate humanity. However, hope is still left; you hold the tools that are able to destroy the runaway robots. The robots had already detected them, so they are hunting you first -- as you are deemed their biggest threat.
                    
### Player's Goal
                      
This is a 2-D single-player game. The goal of the game is to survive and eliminate as many waves of bot entities as possible, with an increasing difficulty in every wave. There will be a maximum of twenty-five waves; the only possible way to win the game is to successfully manage all twenty-five waves, or else you lose the game.

## Control Keys
                    
The control keys used are the following:

* Player Movement: 
	* [UP], [LEFT], [DOWN], [RIGHT]
	* [W], [A], [S], [D]
* Player Hotbar: 
	* [1], [2], [3], [4] 
* Item Interaction:
	* [E]
* Quit Game: 
	* [ESCAPE]

## Tips

1. During a wave, keep on moving around to keep yourself from getting shot, especially from snipers.

2. Never get to close to a bot, or else dodging their close-up bullets will become difficult; in some cases, dodging will be impossible.

3. Prioritize bots with specific guns over other bots, to decrease the chances of taking incredible amounts of damage-per-second.

4. Stay away from the map's edges, as bots can surprise you from the edges if you are too close to them.

5. Maximize your health gain from health boosts by finishing a fight before using the boost.

6. Gain and stack as many boosts you can find as possible for a maximum effect.

7. Utilities are risky to use. However, when used properly, they can really turn the game around.

8. Tend to exploit the fact that bots cannot shoot off-screen.

## Changelog

(Sept. 14, 2018)
* Updated Breach from Python 2.7.12 to 3.7.0.
* Added item drop name and key labels.
* Improved end-of-game screen.
* Adjustments to nearly all items.
* Adjustments to bots and boss bot.
* Removed utility spin due to frame-drop issues.
* Fixed 2 bugs:
  1. More than one item drop can now appear in the world within the same frame.
  2. High-velocity bullets no longer pass through smaller structures.
