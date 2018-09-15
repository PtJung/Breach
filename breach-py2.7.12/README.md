# Breach
The game menu may refer this file as "README.txt". If you come for instructions, you found the right place.

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

3. Prioritize bots with specific guns over other bots, to decrease the chances of taking high damage-per-second.

4. Stay away from the map's edges, as bots can surprise you from the edges if you are too close to them.

5. Maximize your health gain from health boosts by finishing a fight before using the boost.

6. Gain and stack as many boosts you can find as possible for a maximum effect.

7. Utilities are risky to use. However, when used properly, they can really turn the game around.

8. Tend to exploit the fact that bots cannot shoot off-screen.

## Known Bugs
	
### Defect Severity Scale

A scale is used to measure the severity of the known bugs, and a measurement will be placed next to each bug.

	SYMBOL(S)  	SEVERITY

	*         	trivial
	**       	minor
	***     	major
	**** 		critical

### List of Bugs

1. The world border moves in the player's direction by some
units for each time the player enters the map's "edge 
area". **\***

2. Fast enough bullets can pass through fast enough entities.
An entity can include both player and bot. **\*\***

3. If more than one crate in the world is destroyed at the
same time, the crates will only yield one item drop. **\*\***

4. Bots will move in a rough-follow manner when approaching
the player from the edge of the screen. **\***

## Game Mechanic Details

* All base damage is randomized through (80 - 125) % to get actual damage.

### Player

* The player regenerates 1% of their maximum health (rounded) every 2.5 seconds.

### Bot

* The bot gets stronger with every wave — through health, damage, speed, and numbers.

### Boss Bot

* The boss has a lot of health and owns a powerful gun that none of its subordinates have.

### Terrain

* While a player or bot is slowed by a piece of terrain, they are unable to shoot.

		- Stump: slows upon contact, has 200 HP
		- Barrel: slows upon contact, has 500 HP
		- Crate: item drop upon breaking, has 80 HP
		- Bush: decoration purposes
		- Pebble: decoration purposes

### Items

* Item drops last 15 seconds before despawning from the world.

#### Guns

* Let 'B' represent bullet; 'DMG' represent damage; 'u' represent unit 
  distance; 'f' represent frame count; and 'S' represent shot.

		- Hand Gun: 
			- 80 DMG/B; 1.00 B/s; 65 u/f; 1 B/S
			- only obtainable through first wave
		- Machine Gun:		
			- 30 DMG/B; 8.00 B/s; 60 u/f; 1 B/S
		- Shot Gun:		
			- 50 DMG/B; 0.67 B/s; 50 u/f; 6 B/S
		- Assault Rifle:	
			- 60 DMG/B; 5.0 B/s; 60 u/f; 1 B/S
		- Sniper Rifle:		
			- 600 DMG/B; 0.50 B/s; 80 u/f; 1 B/S
					
#### Boosts

* All boosts are consumables; they will disappear upon usage.

		- Health Boost: 
			- permanently gains an additional 50 max health
			- heals for 50% of max health after the increment
		- Movement Speed Boost:
			- permanently gains an additional 10% of original movement speed
		- Attack Damage Boost:
			- permanently gains an additional 25% of original attack damage

#### Utilities

* All utilities are consumables; they will disappear upon usage.
* Each utility has a radius of effect of 256 units.

		- Barrier:
			- blocks all bullets from bots anywhere within range for up to 5 seconds
		- Stunner:
			- stuns all bots within range for 5 seconds
		- Bomb:
			- deals 750 damage to all bots within range
				
