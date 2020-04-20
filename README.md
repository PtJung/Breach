# Breach
![](readme-demo/demo.gif)



## Program Description

Breach is my battle royale-inspired Pygame project, accompanied by custom graphics and object design. It was inspired by **surviv.io**, an online 2-D battle royal game.

**Python Libraries:**
* pygame
           
## Player's Goal
                      
This is a 2-D single-player game. The goal of the game is to survive and eliminate as many waves of bots as possible, with an increasing difficulty in every wave. There will be a maximum of twenty-five waves and the only way to win the game is to successfully beat all twenty-five waves, or else the game is lost.

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

