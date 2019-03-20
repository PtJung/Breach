# Breach
<p align="center">
  <img width="750" height="562" src="https://i.imgur.com/pExtEUC.png">
</p>



## Program Description

"Breach" is the name of my ICS3U culminating assignment, inspired by **surviv.io**, an online 2-D battle royal game. 

**Python Libraries:**
* pygame
           
## Player's Goal
                      
This is a 2-D single-player game. The goal of the game is to survive and eliminate as many waves of bots as possible, with an increasing difficulty in every wave. There will be a maximum of twenty-five waves and the only possible way to win the game is to successfully manage all twenty-five waves, or else you lose the game.

## Control Keys
                    
The control keys used are the following:

* Player Movement: 
	* <tt>UP</tt>, <tt>LEFT</tt>, <tt>DOWN</tt>, <tt>RIGHT</tt>
	* <tt>W</tt>, <tt>A</tt>, <tt>S</tt>, <tt>D</tt>
* Player Hotbar: 
	* <tt>1</tt>, <tt>2</tt>, <tt>3</tt>, <tt>4</tt>
* Item Interaction:
	* <tt>E</tt>
* Quit Game: 
	* <tt>ESCAPE</tt>

## Tips

1. During a wave, keep on moving around to keep yourself from getting shot, especially from snipers.

2. Never get to close to a bot, or else dodging their close-up bullets will become difficult. In some cases, dodging will be impossible.

3. Prioritize bots with specific guns over other bots, to decrease the chances of taking incredible amounts of damage over time.

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
* Breach Demo 3.7.0 now available.
	* This mode is for extremely quick plays.
	* Further adjustments to nearly all items.
	* Further adjustments to bots and boss bot.
	* Guns and the Barrier Utility are disabled from dropping from crates.
* Fixed 2 bugs:
  	1. More than one item drop can now appear in the world within the same frame.
  	2. High-velocity bullets no longer pass through smaller structures.

