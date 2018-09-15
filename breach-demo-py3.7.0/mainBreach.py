'''    Name: Patrick Jung
       
       Date: 14 September, 2018

       Description: This program serves as the main file of my PyGame project,
                    "Breach". The idea of the game is explained below:
                    
                    BACKGROUND
                    
                    As a result of their unsuspected artificial intelligence, 
                    lab robots are on the run to eliminate humanity. However, 
                    hope is still left; you hold the tools that are able to 
                    destroy the runaway robots. The robots had already detected 
                    them, so they are hunting you first -- as you are deemed 
                    their biggest threat.
                    
                    PLAYER'S GOAL
                      
                    This is a single-player game. The goal of the game is to 
                    survive and eliminate as many waves of bionic entities as 
                    possible, with an increasing difficulty in every wave. There 
                    will be a maximum of twenty waves; the only possible way to 
                    win the game is to successfully manage all twenty-five waves, 
                    or else you lose the game.

                    CONTROL KEYS
                    
                    The control keys used are the following: 
                          - Player Movement: ([UP], [LEFT], [DOWN], [RIGHT]), 
                                             ([W], [A], [S], [D]); 
                          - Player Hotbar: ([1], [2], [3], [4]); 
                          - Item Interaction: [E]; and
                          - Quit Game: [ESCAPE]
'''

################################################################################
##                                                                            ##
##                                Functions                                   ##
##                                                                            ##
################################################################################
   
def interactPlayerItem(playerObject, hotbarObject, radiusToPlayerCenter, itemDropGroup):
   '''     SYNTAX   interactPlayerItem(playerObject : obj, hotbarObject : obj,
                    radiusToPlayerCenter : int, itemDropGroup : group)
   
          PURPOSE  This function deals with the interaction between the Player
                   object and the ItemDrop object.
                   
         DETAILS   Three cases involve this interaction:
                      I. if the player's Nth slot is empty and an item of the Nth 
                         category is present, pick up the item;
                     II. if the player's Nth slot is full and an item of the Nth 
                         category is not present, drop the player's Nth item; and
                    III. if the player's Nth slot is full and an item of the Nth 
                         category is present, switch the item on the ground with 
                         the one in the player's inventory.
          
       PARAMETERS   The player object; the hotbar object; the radius to the 
                    Player's center as an integer; the bottom and top layer 
                    sprite groups; and item drop group.
                    
           RETURN   The group of in-game sprites; and the new middle-layer object 
                    of precedence 0, the new item drop.
   '''
   spritesInGameGroupAppend, midLayerPrecedenceListAppend = [], [[], [], []]
   itemDrop = isPlayerNearItemDrop(playerObject, itemDropGroup, radiusToPlayerCenter)
   
   if itemDrop:
      
      # Memorize: the item drop's item
      dropHeldItem = itemDrop.getHeldItem()
      if "Gun_" in dropHeldItem:
         
         # Interaction Case 1: for the weapons [1, 2] slots
         # Identify: the dropped item is a Gun
         if not playerObject.getInventory()[0]:
            # Weapon 1 Slot: if empty, pick up the dropped item
            playerObject.setInventorySlotItem(0, dropHeldItem)
         elif not playerObject.getInventory()[1]:
            # Weapon 2 Slot: if empty, pick up the dropped item
            playerObject.setInventorySlotItem(1, dropHeldItem)
            
         # Interaction Case 3: for the weapons [1, 2] slots
         else:
            # Weapon [1, 2] Slot: if not empty, switch the dropped item with the
            # held item, placing the dropped item in one of the Weapon slots
            if playerObject.getSelectBarSlot() != 1:
               # Weapon 1 slot: if slot was selected (or by default)
               droppedPlayerItem = classBreach.ItemDrop( \
                  playerObject.getInventory()[0], playerObject.rect.center, True)
               spritesInGameGroupAppend, midLayerPrecedenceListAppend = \
                  insertMiddleSprite(0, [droppedPlayerItem])                  
               playerObject.setInventorySlotItem(0, dropHeldItem)
            else:
               # Weapon 2 slot: if slot was selected
               droppedPlayerItem = classBreach.ItemDrop( \
                  playerObject.getInventory()[1], playerObject.rect.center, True)
               spritesInGameGroupAppend, midLayerPrecedenceListAppend = \
                  insertMiddleSprite(0, [droppedPlayerItem])                  
               playerObject.setInventorySlotItem(1, dropHeldItem)
      elif ("Util_" in dropHeldItem) or ("Boost_" in dropHeldItem):
         
         # Interaction Case 1: for the utilities / boosts slot
         # Identify: the dropped item is a Utility or a Boost
         if not playerObject.getInventory()[2]:
            # Utility Slot: if empty, pick up the dropped item
            playerObject.setInventorySlotItem(2, dropHeldItem)
            hotbarObject.setInventory(playerObject.getInventory())
            
         # Interaction Case 3: for the utilities / boosts slot
         else:
            # Utility Slot: if not empty, switch the dropped item with the held item
            droppedPlayerItem = classBreach.ItemDrop( \
               playerObject.getInventory()[2], playerObject.rect.center, True)
            spritesInGameGroupAppend, midLayerPrecedenceListAppend = \
               insertMiddleSprite(0, [droppedPlayerItem])                  
            playerObject.setInventorySlotItem(2, dropHeldItem)
      
      # Kill: item drop (after taking)
      itemDrop.kill()
            
   else:
      # Interaction Case 2: player object drops its selected item, assuming its
      # not the "unarmed" slot (3)
      playerHeldItem = playerObject.getHeldItem()
      if playerObject.getSelectBarSlot() < 3 and playerHeldItem:
         playerObject.setInventorySlotItem(playerObject.getSelectBarSlot(), "")
         droppedPlayerItem = classBreach.ItemDrop(playerHeldItem, playerObject.rect.center, True)
         spritesInGameGroupAppend, midLayerPrecedenceListAppend = \
            insertMiddleSprite(0, [droppedPlayerItem])
         
   # Update: hotbar inventory and player model
   hotbarObject.setInventory(playerObject.getInventory())
   playerObject.updateImage()
      
   # Return: values
   return spritesInGameGroupAppend, midLayerPrecedenceListAppend[0]
   
def isPlayerNearItemDrop(playerObject, itemDropObjectList, radiusToPlayerCenter, 
                         RADIUS_TO_ITEM_DROP_CENTER = 54):
   '''     SYNTAX   isPlayerNearItemDrop(playerObject : obj, itemDropObjectList 
                    : list, radiusToPlayerCenter : int)
   
          PURPOSE   To test if the Player object is near an ItemDrop object.
          
       PARAMETERS   The player object; the item drop object list; and the radius
                    to the Player's center as an integer.
           
           RETURN   The item drop if the Player object is near an ItemDrop object.
                    Otherwise, False.
   '''
   itemDrops = yieldIterInRadius( \
      playerObject, itemDropObjectList, radiusToPlayerCenter + RADIUS_TO_ITEM_DROP_CENTER)
   if itemDrops:
      return itemDrops[0]
   else:
      return False

def getAIModes():
   '''  SYNTAX   getAIModes()
   
       PURPOSE   To list all of the AI modes.
          
       DETAILS   The AI modes include:
                    I. ranged 1; 
                   II. ranged 2; and
                  III. ranged 3.
                    
        RETURN   A tuple representing all AI modes.
   '''
   allAIModes = ("AImode_ranged1", "AImode_ranged2", "AImode_ranged3")
   
   # Return: values
   return allAIModes

def randomizeDamage(baseDamageValue):
   '''     SYNTAX   randomizeDamage(baseDamageValue : int)
   
          PURPOSE   To randomize damage values from their base damage value.
          
       PARAMETERS   The base damage value as an integer.
       
           RETURN   The new damage value as an integer.
   '''
   return random.randint(int(round(baseDamageValue * 0.80)), \
                         int(round(baseDamageValue  * 1.25)))

def getAllGunNames():
   '''  SYNTAX   getAllGunNames()
   
       PURPOSE   To list all of the in-game guns' names.
          
       DETAILS   The in-game guns include:
                    I. handgun;
                   II. machine gun;
                  III. shot gun;
                   IV. assault rifle;
                    V. sniper rifle; and
                   VI. rail gun.
                    
        RETURN   A tuple representing all the names of in-game guns as strings.
   '''
   allGuns = ("Gun_Hand", "Gun_Mach", "Gun_Shot", "Gun_Aslt", "Gun_Snip", "Gun_Rail")
   
   # Return: values
   return allGuns

def getAllGunStats(EXPECTED_FPS = 30):
   '''  SYNTAX   getAllGunStats()
   
       PURPOSE   To list all of the in-game guns' stats in an ordered manner.
       
       DETAILS   Every index in the tuple corresponds to its occuring gun name 
                 in the function getAllGunNames().
                 
                 For all Bot objects that use a gun, damage is expected to be
                 impaired by some factor applicable to the Player's health.
                 
                 Every tuple contains the following (for that gun, in order):
                    I. damage per gun bullet;
                   II. cooldown per gun shot (FPS / shots per second);
                  III. number of bullets per gun shot;
                   IV. bullet velocity (per frame);
                    V. accuracy (by degrees; 0 <= A <= 90); and
                   VI. length of gun.
                    
        RETURN   A tuple representing the stats of each in-game gun as a tuple
                 of attack damage integer, attack speed float value, number of 
                 bullets per shot as an integer, bullet velocity as a float value, 
                 accuracy as an integer, and length of the gun as an integer.
   '''
   stats_Gun_Hand = (80, int(EXPECTED_FPS), 1, 65, 88, 41)
   stats_Gun_Mach = (40, int(EXPECTED_FPS / 8.0), 1, 60, 86, 101)
   stats_Gun_Shot = (65, int(EXPECTED_FPS * 1.5), 6, 50, 83, 86)
   stats_Gun_Aslt = (65, int(EXPECTED_FPS / 5.0), 1, 60, 86, 101)
   stats_Gun_Snip = (150, int(EXPECTED_FPS * 2.0), 1, 75, 90, 129)
   stats_Gun_Rail = (100, int(EXPECTED_FPS * 1.5), 20, 75, 80, 111)
   
   allGunStats = (stats_Gun_Hand, stats_Gun_Mach, stats_Gun_Shot, stats_Gun_Aslt, \
                  stats_Gun_Snip, stats_Gun_Rail)
   
   # Return : values
   return allGunStats

def getAllBoostNames():
   '''  SYNTAX   getAllBoostNames()
   
       PURPOSE   To list all of the in-game boosts' names.
          
       DETAILS   The in-game boosts include:
                    I. attack damage boost permanent;
                   II. movement speed boost permanent; and
                  III. health recovery boost.
                    
        RETURN   A tuple representing all the in-game boosts for each string
                 it contains.
   '''
   allBoosts = ("Boost_AttackDamage", "Boost_MovementSpeed", "Boost_Health")
   
   # Return: values
   return allBoosts

def getAllBoostEffects():
   '''  SYNTAX   getAllBoostEffects()
   
       PURPOSE   To list all of the effects of the in-game boosts.
       
       DETAILS   Each different boost has a different effect:
                    I. attack damage, a multiplier value;
                   II. movement speed, a raw value; and
                  III. health bonus, a raw value and a multiplier value.
                  
        RETURN   Each index in this returned tuple corresponds to its respective
                 item in getAllBoostNames().
   '''
   addAttackDamage = 0.25
   addMovementSpeed = 3
   addHealth = (20, 0.75)
   
   allBoostEffects = (addAttackDamage, addMovementSpeed, addHealth)
   
   # Return: values
   return allBoostEffects

def getAllUtilityNames():
   '''  SYNTAX   getAllUtilityNames()
   
       PURPOSE   To list all of the in-game utilities' names.
          
       DETAILS   The in-game utilities include:
                    I. throwable stunner;
                   II. throwable barrier;
                  III. throwable bomb.
                    
        RETURN   A tuple representing all the in-game utilities' names as strings.
   '''
   allUtilities = ("Util_Stunner", "Util_Bomb", "Util_Barrier")
   
   # Return: values
   return allUtilities

def getAllUtilityEffects():
   '''  SYNTAX   getAllUtilityEffects()
   
       PURPOSE   To list all of the effects of the in-game boosts.
       
       DETAILS   Each different utility has a different effect:
                    I. throwable stunner -- stun enemies in radius for a duration;
                   II. throwable barrier -- blocks Bot bullets within a range; and
                  III. throwable bomb -- deals massive damage to all but the Player
                       object in a radius.
                  
        RETURN   Each index in this returned tuple corresponds to its respective
                 item in getAllUtilityNames().
   '''
   stunnerTime = 300
   barrierDuration = 90
   bombDamage = 1000
   
   allUtilityEffects = (stunnerTime, barrierDuration, bombDamage)
   
   # Return: values
   return allUtilityEffects

def executeEntityShoot(isFromPlayer, entityObject, screenObject, \
                       spritesSolidGroup, RANDOM_BOT_SHOOT_INTERVAL = 5, \
                       IMPAIR_BOT_VELOCITY_FACTOR = 2.0, IMPAIR_BOT_DAMAGE_FACTOR = \
                       7.5, ACCEPTABLE_RADIUS_TO_TERRAIN_CENTER = 48):
   '''     SYNTAX   executeEntityShoot(isFromPlayer : bool, entityObject : obj, 
                    screenObject : obj, spritesSolidGroup : group)
   
          PURPOSE   To instantiate and produce from the Bullet class, relative
                    to the entity's position and gun.
                     
       PARAMETERS   A boolean value expressing if the bullets were to be shot
                    are from the player or not; the entity object; the 
                    screen object; and the group of all solid sprites.
       
           RETURN   The sprites needed to be appended to the groups of in-game
                    sprites and all of precedence 1 from the middle layer 
                    precedence list.
   '''
   if (not checkCircCollideAdaptable(entityObject, spritesSolidGroup)) and \
      (not entityObject.getIsKilled()):
      # Player: execute each frame; Bot: execute every RANDOM_BOT_SHOOT_INTERVAL frames
      if isFromPlayer:
         usageChance = 0
      else:
         usageChance = RANDOM_BOT_SHOOT_INTERVAL - 1
        
      # Entity: create shot bullet
      if entityObject.canUseGun() and not random.randint(0, usageChance):
         # Yield: the Entity object's held gun's stats
         heldGunStats = getAllGunStats()[getAllGunNames().index(entityObject.getHeldItem())]
         entityObject.setGunCooldown(heldGunStats[1])
         
         # Initialize: location and count of created bullet(s)
         bulletsInstantiated = []
         for bulletNumber in range(heldGunStats[2]):
            if isFromPlayer:
               bulletDamage = heldGunStats[0]
               bulletVelocity = heldGunStats[3]
               bulletDirection = entityObject.getDirectionRad()
               bulletDamage *= entityObject.getADMultiplier()
               coordsFacedInInstant = entityObject.generateFrontPoint(True, heldGunStats[5])
            else:
               # Bot: unique bullets for self
               bulletDamage = heldGunStats[0] / IMPAIR_BOT_DAMAGE_FACTOR * entityObject.getADMultiplier()
               bulletVelocity = heldGunStats[3] / IMPAIR_BOT_VELOCITY_FACTOR
               bulletDirection = -entityObject.getDirectionRad()
               coordsFacedInInstant = entityObject.generateFrontPoint(False, heldGunStats[5])
            
            # Instantiate: bullets of the held gun   
            currentBullet = classBreach.Bullet( \
               screenObject, coordsFacedInInstant, isFromPlayer, bulletDamage, \
               bulletDirection, bulletVelocity, heldGunStats[4])
            bulletsInstantiated.append(currentBullet)
         
         # Return: values (case 1)
         spritesInGameGroupAppend, midLayerPrecedenceListAppend = insertMiddleSprite(1, bulletsInstantiated)
         return spritesInGameGroupAppend, midLayerPrecedenceListAppend[1]
   
   # Return: values (case 2)
   return [], []

def genCrateItem():
   '''  SYNTAX   genCrateItem()
   
       PURPOSE   To pick an item from the list of all boosts to be used in
                 crates. This may also include no item at all.
                 
       DETAILS   An integer roll is used to determine which item drops.
       
        RETURN   A string representing the picked item for the crate. If the
                 string is empty, it represents no item.
   '''
   # Generate: picked item (by % chance)
   pickedItemSection = random.randint(1, 100)
   
   if 1 <= pickedItemSection <= 80:
      # Picked Item: boost
      crateItem = getAllBoostNames()[random.randrange(0, len(getAllBoostNames()))] 
   elif 81 <= pickedItemSection <= 100:
      # Picked Item: utility
      crateItem = getAllUtilityNames()[random.randrange(0, len(getAllUtilityNames()) - 1)]
      
   # Return: values
   return crateItem
   
def interactPlayerPunch(radiusToPlayerCenter, playerObject, cameraObject, \
                        killableObjectsList, STARTING_FRAME = 0):
   '''     SYNTAX   interactPlayerPunch(radiusToPlayerCenter : int, playerObject 
                    : obj, cameraObject : obj, killableObjectList : list)
   
          PURPOSE   A function to execute all interactions with the Player's
                    punch, that is in the list of killable objects.
                    
       PARAMETERS   The radius to the player's center as an integer; the player
                    object; the camera object; and the list of all killable 
                    sprites.
   '''
   # Handling: Player: Punch
   if playerObject.getUsedPunch():
      if STARTING_FRAME < playerObject.getTimeInPunchCycle() < playerObject.getTotalPunchCycle():
         # During Punch: throw and retract arm for TOTAL_PUNCH_CYCLE frames
         playerObject.simulatePunch()
         playerObject.updateTimeInPunchCycle()
      
         if playerObject.isAtPunchPoint():
            # Between throw / retract of arm; one trial of punch collision
            if pygame.sprite.spritecollide(playerObject, killableObjectsList, False):
               objectPunched = checkCircCollide( \
                  (playerObject.getPunchHitPoint()[0], playerObject.getPunchHitPoint()[1]), \
                  playerObject, killableObjectsList, radiusToPlayerCenter)
      
               if objectPunched:
                  # Assume the punched object is a bot, which has an inventory
                  objectPunched.takeDamage(randomizeDamage( \
                     playerObject.getPunchDamage()))
                  cameraObject.resetScrollSpeed()
      
      elif not playerObject.getTimeInPunchCycle():
         # Start of Punch: choose which arm to punch with and start the cycle
         playerObject.setLArmForPunch(random.choice([True, False]))
         playerObject.updateTimeInPunchCycle()
      
      else:
         # End of Punch: reset all punch values
         playerObject.resetPunch()
   
def getBrokenCrates(cratesObjectGroup):
   '''     SYNTAX   getBrokenCrates(cratesObjectGroup : group)
   
          PURPOSE   Yield all broken crates in the world.
                    
       PARAMETERS   A group of all crate objects.
       
           RETURN   All existing destroyed crates in a list.
   '''
   destroyedCrates = []
   for crate in cratesObjectGroup:
      if crate.getDestroyed():
         destroyedCrates.append(crate)
   return destroyedCrates

def checkForKilledBot(botsObjectGroup):
   '''     SYNTAX   checkForKilledBot(botsObjectGroup : group)
   
          PURPOSE   Check for a killed bot that exists in the world.
          
       PARAMETERS   A list of all Bot objects.
       
           RETURN   True if a bot was recently killed, and False otherwise.
   '''
   for bot in botsObjectGroup:
      if bot.getIsKilled():
         return True
   return False
   
def executeUtilityForm(utilityObject, midLayerPrecedenceList, botsObjectGroup, \
                       killableObjectsGroup, EFFECT_RADIUS = 512):
   '''     SYNTAX   executeUtilityForm(utilityObject : obj, midLayerPrecedenceList 
                    : group, botsObjectGroup : group, killableObjectsGroup : group)
   
          PURPOSE   To handle any new utility form.
          
       PARAMETERS   The utility object that has changed form; the middle-layer 
                    list of objects by precedence; the group of all Bot objects;
                    and the group of all killable objects.
   '''
   if "Util_" in utilityObject.getUtilityName():
      if "Stunner" in utilityObject.getUtilityName():
         # Utility: stunner (consumption upon activation)
         for botObject in yieldIterInRadius(utilityObject, botsObjectGroup, EFFECT_RADIUS):
            botObject.setStunTime(getAllUtilityEffects()[0])
         utilityObject.kill()
         
      elif "Barrier" in utilityObject.getUtilityName():
         # Utility: barrier (duration upon activation)
         if utilityObject.getTimeToForm() <= utilityObject.getLiveTime() <= \
            getAllUtilityEffects()[1] + utilityObject.getTimeToForm():
            for bulletObject in yieldIterInRadius(utilityObject, midLayerPrecedenceList[1], EFFECT_RADIUS):
               if not bulletObject.getIsFromPlayer():
                  bulletObject.kill()
         else:
            utilityObject.kill()
            
      elif "Bomb" in utilityObject.getUtilityName():
         # Utility: bomb (consumption upon activation)
         for killableObject in yieldIterInRadius(utilityObject, killableObjectsGroup, EFFECT_RADIUS):
            killableObject.takeDamage(randomizeDamage(getAllUtilityEffects()[2]))
         utilityObject.kill()
   
def genInitBotCoords(screenObject, MINIMUM_DISTANCE_FROM_SCREEN = 150, \
                     MAXIMUM_DISTANCE_FROM_SCREEN = 2500):
   '''     SYNTAX   genInitBotCoords(screenObject : obj)
   
          PURPOSE   To generate the initial coordinates for the Bot object's
                    spawn upon wave number increment.
                    
          DETAILS   The initial coordinates will be outside the screen, from within
                    MINIMUM_DISTANCE_FROM_SCREEN and MAXIMUM_DISTANCE_FROM_SCREEN
                    units.
                    
       PARAMETERS   The screen object.
       
           RETURN   The (x, y) tuple of coordinates of where the Bot object
                    will spawn screen-wise.
   '''
   # Generate: initial coordinate X
   if random.randint(0, 1):
      initialCoordX = random.randint( \
         -MAXIMUM_DISTANCE_FROM_SCREEN - MINIMUM_DISTANCE_FROM_SCREEN, \
         -MINIMUM_DISTANCE_FROM_SCREEN)
   else:
      initialCoordX = random.randint(\
         screenObject.get_width() + MINIMUM_DISTANCE_FROM_SCREEN, \
         screenObject.get_width() + MAXIMUM_DISTANCE_FROM_SCREEN + MINIMUM_DISTANCE_FROM_SCREEN)
      
   # Generate: initial coordinate Y
   if random.randint(0, 1):
      initialCoordY = random.randint( \
         -MAXIMUM_DISTANCE_FROM_SCREEN - MINIMUM_DISTANCE_FROM_SCREEN, \
         -MINIMUM_DISTANCE_FROM_SCREEN)
   else:
      initialCoordY = random.randint(\
         screenObject.get_height() + MINIMUM_DISTANCE_FROM_SCREEN, \
         screenObject.get_height() + MAXIMUM_DISTANCE_FROM_SCREEN + MINIMUM_DISTANCE_FROM_SCREEN)   
      
   # Return: values
   return (initialCoordX, initialCoordY)

def spawnBotsByWave(radiusToPlayerCenter, screenObject, wavecounterObject, \
                    BOT_SELECTED_HOTBAR_SLOT = 3):
   '''     SYNTAX   spawnBotsByWave(radiusToPlayerCenter : int,
                    screenObject : obj, wavecounterObject : obj)
   
          PURPOSE   Given the game's wave number, a group of Bot objects are
                    to be created across the map.
                    
          DETAILS   Only one execution of this function is needed to supply
                    enough difficulty for the following wave.
         
       PARAMETERS   The radius to the player's center; the screen object; and
                    the wave counter object.
       
           RETURN   A list of created Bot objects that are required to be appended
                    to the following groups: spritesBots, spritesKillable, 
                    spritesInGame, and spritesAll (for spritesAll, use spritesBots).
   '''
   botsCreated = []
   
   # Wave Number: normal enemy wave
   if wavecounterObject.getWaveNumber() < wavecounterObject.getEndWaveNumber() - 1:
      # Bot Stats 1: differ per wave; all alike
      botWaveHealth = 75
      botWaveSpeed = 10
      botCount = 10 + wavecounterObject.getWaveNumber() ** 2
      botADMultiplier = 0.50
      
      # Instantiate: botCount number of bots
      for botObject in range(botCount):
         
         # Bot Stats 2: unique to bot
         initialCoords = genInitBotCoords(screenObject)
         botGun = getAllGunNames()[random.randrange(0, len(getAllGunNames()) - 1)]
         botInventory = ["", "", "", botGun]
         botAImode = random.choice(getAIModes()[:-1])
         
         # Bot: append to list
         botsCreated.append(classBreach.Bot( \
            screenObject, botInventory, initialCoords, BOT_SELECTED_HOTBAR_SLOT, \
            botWaveHealth, botWaveSpeed, botAImode, radiusToPlayerCenter, \
            botADMultiplier))
         
   # Wave Number: boss wave
   else:
      botWaveHealth = 5000 + 1000 * wavecounterObject.getWaveNumber()
      botWaveSpeed = 5 + 0.20 * wavecounterObject.getWaveNumber()
      botADMultiplier = 0.50
      
      # Bot Stats 2: unique to bot
      initialCoords = genInitBotCoords(screenObject)
      botGun = getAllGunNames()[-1]
      botInventory = ["", "", "", botGun]
      botAImode = random.choice(getAIModes()[:-1])
               
      # Bot: append to list
      botsCreated.append(classBreach.Bot( \
         screenObject, botInventory, initialCoords, BOT_SELECTED_HOTBAR_SLOT, \
         botWaveHealth, botWaveSpeed, botAImode, radiusToPlayerCenter, botADMultiplier))
   
   # Return: values
   return botsCreated
   
def getItemDisplayName(itemDropName, ITEM_DROP_NAMES = [ \
   ["Attack Damage Bonus", "Health Bonus", "Movement Speed Bonus"], \
   ["Assault Rifle", "Handgun", "Machine Gun", "Shotgun", "Sniper Rifle"], \
   ["Barrier Utility", "Bomb Utility", "Stun Utility"]]):
   ''' '''
   if "Boost" in itemDropName:
      category = 0
      if "AttackDamage" in itemDropName:
         index = 0
      elif "Health" in itemDropName:
         index = 1
      elif "MovementSpeed" in itemDropName:
         index = 2
   elif "Gun" in itemDropName:
      category = 1
      if "Aslt" in itemDropName:
         index = 0
      elif "Hand" in itemDropName:
         index = 1
      elif "Mach" in itemDropName:
         index = 2
      elif "Shot" in itemDropName:
         index = 3
      elif "Snip" in itemDropName:
         index = 4
   elif "Util" in itemDropName:
      category = 2
      if "Barrier" in itemDropName:
         index = 0
      elif "Bomb" in itemDropName:
         index = 1
      elif "Stunner" in itemDropName:
         index = 2
   return ITEM_DROP_NAMES[category][index]
   
def handlingMiscInteractEvents(radiusToPlayerCenter, screenObject, wavecounterObject, \
                               healthbarObject, playerObject, cameraObject, labelText, \
                               midLayerPrecedenceList, botsObjectGroup, cratesObjectGroup, \
                               killableObjectsGroup, killableTerrainObjectsGroup, \
                               spritesSolidGroup):
   '''     SYNTAX   handlingMiscInteractEvents(radiusToPlayerCenter : int, screenObject 
                    : obj, wavecounterObject : obj, healthbarObject : obj, playerObject 
                    : obj, cameraObject : obj, midLayerPrecedenceList : list, 
                    botsObjectGroup : group, cratesObjectGroup : group, 
                    killableObjectsGroup : group, killableTerrainObjectsGroup : 
                    group, spritesSolidGroup : group)
   
          PURPOSE   Handle all important miscellaneous events held by 
                    interactions.
                    
       PARAMETERS   The radius of the Player's base; the screen object; the wave 
                    counter GUI object; the health bar GUI object; the player 
                    object; the camera object; the middle layer precedence list; 
                    the group of all Bot objects; the group of all Crate objects; 
                    the group of all killable objects; the group of all killable
                    terrain objects; and the group of all solid sprites.
       
           RETURN   The group of in-game sprites; the new item drop object by 
                    player-item interaction; and the new bullets created by the 
                    bots.
   '''
   spritesBotsGroupAppend, spritesInGameGroupAppend, spritesKillableGroupAppend, \
      midLayerPrecedenceListAppend = [], [], [], [[], [], []]

   # Event: show label for pick up
   itemDrop = isPlayerNearItemDrop(playerObject, midLayerPrecedenceList[0], radiusToPlayerCenter)
   if itemDrop:
      labelText[0].updateText(getItemDisplayName(itemDrop.getHeldItem()))
      labelText[1].updateColor((250, 250, 250))
      labelText[1].updateText("[E]")
      for textIndex in range(2):
         labelText[textIndex].showText()
   else:
      for textIndex in range(2):
         labelText[textIndex].hideText()
   
   # Event: execute existing utility form
   if midLayerPrecedenceList[2]:
      for utilityObject in midLayerPrecedenceList[2]:
         if utilityObject.getChangedForm():
            executeUtilityForm( \
               utilityObject, midLayerPrecedenceList, botsObjectGroup, killableObjectsGroup)
      
   # Event: punch mechanism
   interactPlayerPunch(radiusToPlayerCenter, playerObject, cameraObject, killableObjectsGroup)

   # Event: bots track player
   botsTrackPlayer(playerObject, botsObjectGroup)
   
   # Event: spawn bots each wave
   if wavecounterObject.getFinishedInFrame() and \
      wavecounterObject.getWaveNumber() < wavecounterObject.getEndWaveNumber():
      spritesBotsAppend = spawnBotsByWave(radiusToPlayerCenter, screenObject, wavecounterObject)
      
      for botObject in spritesBotsAppend:
            spritesBotsGroupAppend.append(botObject)
            spritesInGameGroupAppend.append(botObject)
            spritesKillableGroupAppend.append(botObject)

   # Event: bots shoot bullets
   for botObject in botsObjectGroup:
      if botObject.isOnScreen():
         spritesInGameGroupAppend1, newBulletAppend = \
            executeEntityShoot(False, botObject, screenObject, spritesSolidGroup)
         for newIndividualBulletAppend in newBulletAppend:
            midLayerPrecedenceListAppend[1].append(newIndividualBulletAppend) 
            spritesInGameGroupAppend.append(newIndividualBulletAppend)   
   
   # Event: bullet collision
   interactTerrainBullet(midLayerPrecedenceList[1], killableTerrainObjectsGroup)
   interactBotBullet(midLayerPrecedenceList[1], botsObjectGroup)
   interactPlayerBullet(midLayerPrecedenceList[1], healthbarObject, playerObject)
   
   # Event: health bar must match player regeneration
   if not playerObject.getRegenTimer():
      healthbarObject.setHealth(playerObject.getHealth())
   
   # Event: destroyed crate drop (check for any broken crates existing in the world)
   destroyedCrates = getBrokenCrates(cratesObjectGroup)
   for destroyedCrate in destroyedCrates:
      # Instantiate: item drop at location
      droppedCrateItem = classBreach.ItemDrop(genCrateItem(), destroyedCrate.rect.center, True)
      spritesInGameGroupAppend2, midLayerPrecedenceListAppendForItem = \
         insertMiddleSprite(0, [droppedCrateItem])
      
      # Sprite Groups: append created item drop to existing
      for newItemDropAppend in midLayerPrecedenceListAppendForItem[0]:
         midLayerPrecedenceListAppend[0].append(newItemDropAppend)
         spritesInGameGroupAppend.append(newItemDropAppend)
   
   # Return: values
   return spritesBotsGroupAppend, spritesInGameGroupAppend, spritesKillableGroupAppend, \
          midLayerPrecedenceListAppend[0], midLayerPrecedenceListAppend[1]

def interactTerrainBullet(bulletGroup, killableTerrainObjectsGroup, \
                          BULLET_RADIUS = 5):
   '''  SYNTAX   interactTerrainBullet(bulletGroup : group, 
                 killableTerrainObjectsGroup : group)
       
       PURPOSE   This function coordinates the collisions between all Bullet
                 objects with Terrain objects.
   '''
   # Quick Test 1: the Bullet group has at least one bullet in it and there are
   # existing Terrain objects in the world
   if bulletGroup and killableTerrainObjectsGroup:
      for terrainObject in killableTerrainObjectsGroup:
         
         # Quick Test 2: the Terrain objects that can only be affected by bullets
         # must be on the screen (or at least near, check Terrain.isOnScreen())
         if terrainObject.isOnScreen():
            collidedBullets = pygame.sprite.spritecollide(terrainObject, bulletGroup, False)
            
            # Quick Test 3: the Terrain object collided with collidedBullets number of bullets  
            for bullet in collidedBullets:
               
               # Test: the specified Bullet object collides perfectly with the Terrain object
               if checkCircCollide( \
                  (bullet.rect.centerx, bullet.rect.centery), \
                  bullet, [terrainObject], BULLET_RADIUS + terrainObject.image.get_width() / 2):
                  terrainObject.takeDamage(randomizeDamage(bullet.getDamage()))
                  bullet.kill()  
   
def interactPlayerBullet(bulletGroup, healthbarObject, playerObject, \
                         ACCEPTABLE_HIT_RADIUS = 41):
   '''     SYNTAX   interactPlayerBullet(bulletGroup : group, healthbarObject : obj,
                    playerObject : obj)
    
          PURPOSE   This function coordinates the collisions between Bot-made
                    Bullet objects with the Player objects.
                 
       PARAMETERS   The group of all bullets; the health bar GUI object; and the
                    player object.
   '''
   # Quick Test 1: the Bullet group has at least one bullet created by the Bot(s)
   if bulletGroup:
      existingBulletFromBot = False
      for bullet in bulletGroup:
         if not bullet.getIsFromPlayer():
            existingBulletFromBot = True
            break
      if existingBulletFromBot:
         collidedBullets = pygame.sprite.spritecollide(playerObject, bulletGroup, False)
         
         # Quick Test 2: the Player object collided with collidedBullets number of bullets         
         for bullet in collidedBullets:
            
            # Test: the specified Bullet object collides perfectly with the Player object
            if checkCircCollide( \
               (bullet.rect.centerx, bullet.rect.centery), \
                  bullet, [playerObject], ACCEPTABLE_HIT_RADIUS):
               
               # Player: take damage from the bullet; Bullet: kill self
               playerObject.takeDamage(randomizeDamage( \
                  bullet.getDamage()))
               healthbarObject.setHealth(playerObject.getHealth())
               bullet.kill()

def interactBotBullet(bulletGroup, botsObjectGroup, ACCEPTABLE_HIT_RADIUS = 41):
   '''  SYNTAX   interactBotBullet(bulletGroup : group, botsObjectGroup : group)
    
       PURPOSE   This function coordinates the collisions between Player-made
                 Bullet objects with Bot objects.
   '''
   # Quick Test 1: the Bullet group has at least one bullet created by the Player
   if bulletGroup:
      existingBulletFromPlayer = False
      for bullet in bulletGroup:
         if bullet.getIsFromPlayer():
            existingBulletFromPlayer = True
            break
         
      # Quick Test 2: Bot objects exist somewhere in the world
      if existingBulletFromPlayer and botsObjectGroup:
         for botObject in botsObjectGroup:
            
            # Quick Test 3: check if the specified Bot is already dead
            if not botObject.getIsKilled():
               collidedBullets = pygame.sprite.spritecollide(botObject, bulletGroup, False)
               
               # Quick Test 3: the sprites of each Bot in the group has collided with
               # collidedBullets number of bullets
               for bullet in collidedBullets:
                  
                  # Test: the specified bullet in the list is from the player and
                  # collides perfectly with one of the Bot objects
                  if bullet.getIsFromPlayer() and checkCircCollide( \
                     (bullet.rect.centerx, bullet.rect.centery), \
                     bullet, [botObject], ACCEPTABLE_HIT_RADIUS):
                     
                     # Bot: take damage from the bullet; Bullet: kill self
                     botObject.takeDamage(randomizeDamage(bullet.getDamage()))
                     bullet.kill()
   
def insertMiddleSprite(precedence, middleObjectList):
   '''     SYNTAX   insertMiddleSprite(0 <= precedence : int <= 2, middleObjectList : list)
   
          PURPOSE   Creates the middle layer sprite in a list that replicates
                    the format of the middle layer sprite list, ordered by
                    precedence.
                      
       PARAMETERS   The precedence number as an integer and the object to be 
                    inserted into the middle layer.
                    
           RETURN   The list of in-game sprite objects needed to be appended and 
                    the list of middle-layer sprite objects needed to be appended.
   '''
   spritesInGameGroupAppend, midLayerPrecedenceListAppend = [], [[], [], []]
   for middleObject in middleObjectList:
      midLayerPrecedenceListAppend[precedence].append(middleObject)
      spritesInGameGroupAppend.append(middleObject)
   
   # Return: values
   return spritesInGameGroupAppend, midLayerPrecedenceListAppend

def botsTrackPlayer(playerObject, botsObjectGroup):
   '''     SYNTAX   botsTrackPlayer(playerObject : obj, botsObjectGroup : group)
   
          PURPOSE   A function for the bots to track the Player object by noting 
                    their relative position and will face the Player object.
                      
       PARAMETERS   The Player object and the list of all Bot objects.
   '''
   for trackingObject in botsObjectGroup:
      if not trackingObject.getIsKilled():
         trackingObject.facePlayer((playerObject.rect.centerx, playerObject.rect.centery))
      
def playerThrowUtil(playerObject, INITIAL_DISTANCE_FROM_PLAYER = 70):
   '''     SYNTAX   object.playerGainBoost(playerObject : obj, healthbarObject :
                    obj)
   
          PURPOSE   A function to deal with a consumed utility by the player
                    in a corresponding manner.
                   
       PARAMETERS   The player object.
       
           RETURN   The list of in-game sprite objects needed to be appended and 
                    the list of middle-layer sprite objects needed to be appended
                    at precedence 2.
   '''
   if "Util_" in playerObject.getHeldItem():
      initialUtilCoords = playerObject.generateFrontPoint(True, INITIAL_DISTANCE_FROM_PLAYER)
      utilityInstantiated = classBreach.Utility(initialUtilCoords, playerObject.getDirectionRad(), \
                                                playerObject.getHeldItem())
      spritesInGameGroupAppend, midLayerPrecedenceListAppend = insertMiddleSprite(2, [utilityInstantiated])
      
   # Return: values
   return spritesInGameGroupAppend, midLayerPrecedenceListAppend[2]

def playerGainBoost(playerObject, healthbarObject):
   '''     SYNTAX   object.playerGainBoost(playerObject : obj, healthbarObject :
                    obj)
   
          PURPOSE   A function to deal with a consumed boost by the player
                    in a corresponding manner.
                   
       PARAMETERS   The player object and the health bar object.
   '''
   if "Boost_" in playerObject.getHeldItem():
      if "AttackDamage" in playerObject.getHeldItem():
         playerObject.setADMultiplier(playerObject.getADMultiplier() + getAllBoostEffects()[0])
      elif "MovementSpeed" in playerObject.getHeldItem():
         playerObject.setWalkSpeed(playerObject.getWalkSpeed() + getAllBoostEffects()[1])
      elif "Health" in playerObject.getHeldItem():
         playerObject.setMaxHealth(playerObject.getHealth()[0] + getAllBoostEffects()[2][0])
         playerObject.recoverHealth(playerObject.getHealth()[0] * getAllBoostEffects()[2][1])
         healthbarObject.setHealth(playerObject.getHealth())

def interactPlayerCamera(screenObject, worldSizeBorder, radiusToPlayerCenter, \
                         playerObject, cameraObject, spritesInGameGroup):
   '''     SYNTAX   interactPlayerCamera(screenObject : obj, worldSizeBorder : tuple, 
                    radiusToPlayerCenter : int, playerObject : obj, cameraObject
                    : obj, spritesInGameGroup : group)
   
          PURPOSE   A function to execute all interactions between the Player
                    object and the Camera object.
                     
       PARAMETERS   The world border as a tuple; the radius to the player center
                    as an integer; the player object; the camera object; and
                    the in-game sprites group.
   '''
   invertWalk, displacement = cameraObject.moveInDirection()
            
   # Player Movement: along horizontal axis
   if worldSizeBorder[0][0] < displacement[0] < worldSizeBorder[0][1]:
      playerObject.rect.centerx = screenObject.get_width() / 2
      for movableObject in spritesInGameGroup:
         movableObject.rect.centerx += invertWalk[0]
   else:
      playerObject.rect.centerx -= invertWalk[0]
      
   # Player Movement: along vertical axis
   if worldSizeBorder[1][0] < displacement[1] < worldSizeBorder[1][1]:
      playerObject.rect.centery = screenObject.get_height() / 2
      for movableObject in spritesInGameGroup:
         movableObject.rect.centery += invertWalk[1]
   else:
      playerObject.rect.centery -= invertWalk[1]
      
   # Player Movement: restrict to border
   # Camera: displacement update at border
   restrictX, restrictY = playerObject.restrictToBorder(radiusToPlayerCenter)
   
   if not restrictX:
      cameraObject.updateDisplaceVector((0, invertWalk[1]))
   if not restrictY:
      cameraObject.updateDisplaceVector((invertWalk[0], 0))   

def interactPlayerSolid(radiusToPlayerCenter, playerObject, cameraObject, spritesSolidGroup):
   '''     SYNTAX   interactPlayerSolid(radiusToPlayerCenter : int, playerObject 
                    : obj, cameraObject : obj, spritesSolidGroup : group)
                    
          PURPOSE   A function to execute all interactions between the Player
                    object and a solid sprite.
                    
       PARAMETERS   The camera object; and the sprites solid group.
   '''
   collidedSolids = pygame.sprite.spritecollide(playerObject, spritesSolidGroup, False)
   if collidedSolids:
      for collidedSolid in collidedSolids:
         # Collision Detection: Impairment of player movement when possible
         if checkCircCollide((playerObject.rect.centerx, playerObject.rect.centery), \
                             playerObject, spritesSolidGroup, collidedSolid.image.get_width() \
                             / 2 + radiusToPlayerCenter):
            cameraObject.setScrollSpeed(playerObject.getImpairedWalkSpeed())
         else:
            cameraObject.setScrollSpeed(playerObject.getWalkSpeed())
   else:
      cameraObject.setScrollSpeed(playerObject.getWalkSpeed())

def handlingKeyHold(screenObject, worldSizeBorder, radiusToPlayerCenter, \
                    playerObject, cameraObject, spritesSolidGroup, spritesInGameGroup):
   '''    SYNTAX   handlingKeyHold(screenObject : obj, worldSizeBorder : tuple, 
                   radiusToPlayerCenter : int, playerObject : obj, cameraObject 
                   : obj, spritesSolidGroup : group, spritesInGameGroup : group)
   
         PURPOSE   Event handling of key-press holding.
       
      PARAMETERS   The screen object; world size border as a tuple of tuples of 
                   integers; the radius to the player center; the player's walk 
                   speed; the camera object; the group of solid sprites; and the 
                   group of in-game sprites.
   '''
   if 1 in pygame.key.get_pressed():
      # Handling: Player-Solid Interaction: Slowness
      interactPlayerSolid(radiusToPlayerCenter, playerObject, cameraObject, \
                          spritesSolidGroup)
      
      # Handling: Player-Camera Interaction: Global Object Movement
      interactPlayerCamera(screenObject, worldSizeBorder, radiusToPlayerCenter, 
                           playerObject, cameraObject, spritesInGameGroup)
   
def handlingMouseHold(playerObject, screenObject, hotbarObject, healthbarObject, \
                      spritesSolidGroup):
   '''     SYNTAX   handlingMouseHold(playerObject : obj, screenObject : obj, 
                    hotbarObject : obj, healthbarObject : obj, spritesSolidGroup
                    : group)
   
          PURPOSE   Event handling of mouse (left/right)-click holding.
       
       PARAMETERS   The main player object controlled by the user; the hotbar 
                    GUI object; the health bar GUI object; and the screen object.
       
           RETURN   The sprites needed to be appended to the groups of in-game 
                    sprites, with the new bullets list of objects, and with the
                    new utilities list of objects.
   '''
   spritesInGameGroupAppend, newBulletAppend, newUtilityAppend = [], [], []
   
   if pygame.mouse.get_pressed()[0]:
      # On mouse hold: Weapons 1-2: slots [0, 1]
      if playerObject.getSelectBarSlot() <= 1:
         if playerObject.isHoldingGun():
            spritesInGameGroupAppend, newBulletAppend = \
               executeEntityShoot(True, playerObject, screenObject, spritesSolidGroup)
         
      # On mouse click: Utility / Boost: slot [2]   
      elif playerObject.getSelectBarSlot() == 2:
         if playerObject.getHeldItem():
            if "Util_" in playerObject.getHeldItem():
               spritesInGameGroupAppend, newUtilityAppend = \
                  playerThrowUtil(playerObject)
            elif "Boost_" in playerObject.getHeldItem():
               playerGainBoost(playerObject, healthbarObject)
            
            # Consume Upon Use: Utility / Boost
            playerObject.setInventorySlotItem(2, "")
            hotbarObject.setInventory(playerObject.getInventory())
            playerObject.updateImage()
         
      # On mouse click: Punch: slot [3]   
      elif playerObject.getSelectBarSlot() == 3:
         playerObject.setUsedPunch(True)
         
   # Return: values
   return spritesInGameGroupAppend, newBulletAppend, newUtilityAppend
         
def handlingMenuKeyPress(continueLoop, cooldown, cooldownTimer):
   '''     SYNTAX   handlingMenuKeyPress(continueLoop : bool)

          PURPOSE   Event handling of key pressing, for the menu. Any key input
                    is enough to cancel the main menu.
                 
       PARAMETERS   A boolean value expressing if the menu loop should continue
                    or not.
                    
           RETURN   A boolean value expressing if the menu loop should continue
                    or not.
   '''
   for event in pygame.event.get():
         if event.type == pygame.KEYDOWN:
            if cooldown >= cooldownTimer:
               continueLoop = False
         elif event.type == pygame.QUIT:
            os._exit(1)
               
   # Return: values
   return continueLoop

def handlingKeyPress(playerObject, hotbarObject, midLayerPrecedenceList, \
                     radiusToPlayerCenter, continueLoop = True):
   '''     SYNTAX   handlingKeyPress(playerObject : obj, hotbarObject : obj,
                    midLayerPrecedenceList : list, radiusToPlayerCenter : int)
   
          PURPOSE   Event handling of key pressing.
       
          DETAILS   See header docstring for more control key details.
       
       PARAMETERS   The player object; the hotbar object; the middle layer of 
                    sprites by their list precedence; and the radius to the 
                    Player's center as an integer.
                    
           RETURN   A boolean value expressing if the main game loop should 
                    continue or not. Also, the group of in-game sprites and the
                    new item drop object made in the player-item interaction.
   '''
   spritesInGameGroupAppend, newItemDropAppend = [], []
   
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         os._exit(1)
      elif event.type == pygame.KEYDOWN:
         
         # Handling: Toolbar Slots
         toolbar = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]
         if event.key in toolbar:
            for key in range(len(toolbar)):
               # Switch Inventory Slot: according to pressed keys from 1 to 4
               if event.key == toolbar[key] and \
                  playerObject.getInventory()[key]:
                  if key != 3:
                     # Reset: Arm Displacement (Punches)
                     playerObject.resetPunch()
                     
                  # Update: player, object images
                  playerObject.setSelectBarSlot(key)
                  playerObject.updateImage()
                  
                  hotbarObject.setSelectBarSlot(key)
                  hotbarObject.updateImage()
                  
                  break
            
         # Handling: Control Keys
         elif event.key == pygame.K_e:
            spritesInGameGroupAppend, newItemDropAppend = \
               interactPlayerItem(playerObject, hotbarObject, radiusToPlayerCenter, \
                                  midLayerPrecedenceList[0])
            
         elif event.key == pygame.K_ESCAPE:
            continueLoop = False
            
   # Return: values
   return continueLoop, spritesInGameGroupAppend, newItemDropAppend
            
def genInitCoords(screenObject, worldSizeBorder, entityCoordsList, \
                  PERSONAL_RADIUS = 150, SCREEN_FRACTION_TO_EDGE = 8.0):
   '''     SYNTAX   getInitCoords(screenObject : obj, worldSizeBorder : tuple, 
                    entityCoordsList : list)
    
          PURPOSE   Generate coordinates for an object in the world. These
                    coordinates are designed to be at least PERSONAL_RADIUS 
                    units away from all other objects, so distribution of 
                    terrain is encouraged.
                    
       PARAMETERS   The world size border as a tuple of tuples of integers; the
                    list of all entity coordinates; and the screen object.
                    
           RETURN   The coordinates as a tuple of object integer coordinates.
   '''
   # Initialize: the initial coordinates of the Terrain object
   finalCoordsAcceptable = False
   
   while not finalCoordsAcceptable:
      initialCoordX = random.randint( \
         worldSizeBorder[0][0] + screenObject.get_width() * (1.0 / SCREEN_FRACTION_TO_EDGE), \
         worldSizeBorder[0][1] + screenObject.get_width() * ( \
            (SCREEN_FRACTION_TO_EDGE - 1.0) / SCREEN_FRACTION_TO_EDGE))
      initialCoordY = random.randint( \
         worldSizeBorder[1][0] + screenObject.get_height() * (1.0 / SCREEN_FRACTION_TO_EDGE), \
         worldSizeBorder[1][1] + screenObject.get_height() * ( \
            (SCREEN_FRACTION_TO_EDGE - 1.0) / SCREEN_FRACTION_TO_EDGE))
      
      initialCoordsAcceptable = True
      for coordinatePair in entityCoordsList:
         if ((coordinatePair[1] - initialCoordY) ** 2 + \
             (coordinatePair[0] - initialCoordX) ** 2) ** 0.5 < PERSONAL_RADIUS:
            initialCoordsAcceptable = False
      if initialCoordsAcceptable:
         finalCoordsAcceptable = True
            
   # Return: values
   return (initialCoordX, initialCoordY)
   
def mainGameObjects(backgroundObject, worldSizeBorder, radiusToPlayerCenter, \
                    screenObject, PLAYER_HEALTH = 100, BOT_HEALTH = 250, \
                    INITIAL_WAVE_TIME = 350, INITIAL_PLAYER_HOTBAR_SLOT = 3, \
                    LAST_WAVE_NUMBER = 5, INITIAL_PLAYER_AD_MULTIPLIER = 1.00):
   '''     SYNTAX   mainBackground(backgroundObject : obj, worldSizeBorder : tuple, 
                    radiusToPlayerCenter : int, screenObject : obj)
                
          PURPOSE   Execute the entites: background section of the game. 
      
       PARAMETERS   The world size border as a tuple of tuples of integers,
                    see the documentation for mainWorldBorder(); the radius to 
                    the Player's center as an integer; and the screen object.
                    
           RETURN   The list of all sprites, with each specific sprite group
                    and list created in this function for each type of sprite.
   '''

   # Create: Background Sprite
   background = classBreach.Background(screenObject)

   # Create: Player / Camera
   playerInventory = ["", "", "", "Unarmed"]
   player = classBreach.Player(screenObject, playerInventory, INITIAL_PLAYER_HOTBAR_SLOT, \
                               PLAYER_HEALTH, INITIAL_PLAYER_AD_MULTIPLIER)
   camera = classBreach.Camera(screenObject, worldSizeBorder, player.getWalkSpeed())
   
   # Ensure unique coordinates for all creations -- such as (0, 0) for player
   entityCoordsList = [(screenObject.get_width() / 2, screenObject.get_height() / 2)]
   
   # Create: Default Item Drop
   defaultItemDrop = classBreach.ItemDrop(getAllGunNames()[1], player.rect.center, True)
   
   # Create: Terrain
   barrels = []
   for barrelCount in range(8 ** 2):
      initialCoords = genInitCoords(screenObject, worldSizeBorder, entityCoordsList)
      entityCoordsList.append(initialCoords)      
      barrels.append(classBreach.Barrel(screenObject, initialCoords))
   crates = []
   for crateCount in range(14 ** 2):
      initialCoords = genInitCoords(screenObject, worldSizeBorder, entityCoordsList)
      entityCoordsList.append(initialCoords)      
      crates.append(classBreach.Crate(screenObject, initialCoords))
   bushes = []
   for bushCount in range(16 ** 2):
      initialCoords = genInitCoords(screenObject, worldSizeBorder, entityCoordsList)
      entityCoordsList.append(initialCoords)
      bushes.append(classBreach.Bush(screenObject, initialCoords)) 
   stumps = []
   for stumpCount in range(16 ** 2):
      initialCoords = genInitCoords(screenObject, worldSizeBorder, entityCoordsList)
      entityCoordsList.append(initialCoords)      
      stumps.append(classBreach.Stump(screenObject, initialCoords))
   pebbles = []
   for pebbleCount in range(24 ** 2):
      initialCoords = genInitCoords(screenObject, worldSizeBorder, entityCoordsList)
      entityCoordsList.append(initialCoords)      
      pebbles.append(classBreach.Pebble(screenObject, initialCoords))   
   
   # Create: GUI
   hotbar = classBreach.HotBarGUI(screenObject, playerInventory, INITIAL_PLAYER_HOTBAR_SLOT)
   healthbar = classBreach.HealthBarGUI(screenObject, PLAYER_HEALTH, hotbar.image.get_height())
   wavecounter = classBreach.WaveCounterGUI(screenObject, INITIAL_WAVE_TIME, LAST_WAVE_NUMBER)
   
   # Create: item drop and ending text
   itemDropNameText = classBreach.Label(screenObject, 36, -80)
   itemDropKeyText = classBreach.Label(screenObject, 24, -50)
   labelText = [itemDropNameText, itemDropKeyText]
   
   endingText = classBreach.Label(screenObject, 169, -150)
   
   # Create: sprite groups
   spritesBots = pygame.sprite.Group()
   spritesGUI = pygame.sprite.Group(hotbar, healthbar, wavecounter)
   spritesCrates = pygame.sprite.Group(crates)
   spritesKillable = pygame.sprite.Group(spritesBots, stumps, barrels, crates)
   spritesKillableTerrain = pygame.sprite.Group(stumps, barrels, crates)
   spritesSolid = pygame.sprite.Group(stumps, barrels)
   spritesInGame = pygame.sprite.Group(bushes, stumps, spritesBots, pebbles, barrels, \
                                       crates, defaultItemDrop)
   
   # Middle Sprite Group: in order of precedence from bottom-to-top:
   # (0) item drops; (1) utilities; (2) projectiles (bullets)
   midLayerPrecedenceList = [pygame.sprite.Group(defaultItemDrop), pygame.sprite.Group(), pygame.sprite.Group()]
   spritesAllMiddle = pygame.sprite.LayeredUpdates( \
      midLayerPrecedenceList[0], midLayerPrecedenceList[1], midLayerPrecedenceList[2], spritesBots)
   
   spritesAllBottom = pygame.sprite.LayeredUpdates(background, pebbles, stumps, barrels, crates)
   spritesAllTop = pygame.sprite.LayeredUpdates(player, bushes, spritesGUI, labelText, endingText)
   
   spritesAll = pygame.sprite.LayeredUpdates( \
      spritesAllBottom, spritesAllMiddle, spritesAllTop)
   
   # Return: values
   allSpritesList = [player, camera, hotbar, healthbar, wavecounter, bushes, stumps, 
                     pebbles, barrels, crates, spritesBots, midLayerPrecedenceList, 
                     spritesCrates, spritesKillable, spritesKillableTerrain, 
                     spritesSolid, spritesInGame, spritesAllBottom, 
                     spritesAllMiddle, spritesAllTop, spritesAll, endingText, 
                     labelText]
   return allSpritesList
   
def mainWorldBorder(WORLD_SIZE_BORDER_X = (-5000, 5000), WORLD_SIZE_BORDER_Y = (-5000, 5000)):
   '''  SYNTAX   mainWorldBorder()
             
       PURPOSE   Execute the entites: world border section of the game. 
       
        RETURN   A tuple (x, y) of tuples of integers (n1, n2) representing the 
                 world borders of the game.
   '''
   return (WORLD_SIZE_BORDER_X, WORLD_SIZE_BORDER_Y)
   
def mainBackground(screenObject):
   '''     SYNTAX   mainBackground(screenObject : obj)
             
          PURPOSE   Execute the entites: background section of the game. 
       
       PARAMETERS   The screen object.
       
           RETURN   The background object.
   '''
   background = pygame.Surface(screenObject.get_size())
   background.fill((0, 0, 0))
   screenObject.blit(background, (0, 0))
   
   # Return: values
   return background
   
def mainEntities(radiusToPlayerCenter, screenObject):
   '''     SYNTAX   mainEntities(radiusToPlayerCenter : int, screenObject : obj)
          
          PURPOSE   Execute the entites section of the game.
       
          DETAILS   Includes:
                       I. background;
                      II. world border; and
                     III. game objects, restricted by the world border.
                     
       PARAMETERS   The radius to the Player's center as an integer and the 
                    screen object.
       
           RETURN   The world border size as a tuple of tuples of integers; and
                    all instance objects, lists of instances, and sprite groups.
   '''
   return mainBackground(screenObject), mainWorldBorder(), mainGameObjects( \
      mainBackground(screenObject), mainWorldBorder(), radiusToPlayerCenter, \
      screenObject)

def mainDisplay():
   '''  SYNTAX   mainDisplay()
       
       PURPOSE   Execute the display section of the game. 
       
        RETURN   The screen object.
   '''
   screenObject = pygame.display.set_mode((1280, 960))
   pygame.display.set_caption("Breach")
   pygame.display.set_icon(pygame.image.load("images/misc/image_Icon.png").convert_alpha()) 
   
   return screenObject

def yieldIterInRadius(mainObject, collidingObjectIterable, requiredRadiusToObject):
   '''     SYNTAX   yieldIterInRadius(mainObject : obj, collidingObjectIterable 
                    : iter, requiredRadiusToObject : num)
                    
          PURPOSE   To yield which of the objects in the iterable is in a required
                    radius from the object.
                    
       PARAMETERS   The main object whose coordinates will be compared with each
                    colliding object; the iterable of all colliding objects; and
                    the required radius to the main object as a float value.
                    
          DETAILS   This function is different from checkCircCollide(), as this
                    function is for quick use of seeing if an object is at least
                    a distance away from the other objects.
                 
           RETURN   All of the colliding objects that are within the required
                    radius to the main object, in a list.
   '''
   collidingObjects = []
   
   # Test: the colliding object is within the required radius of the main object
   for collidingObject in collidingObjectIterable:
      if math.sqrt( \
         (mainObject.rect.centerx - collidingObject.rect.centerx) ** 2 + \
         (mainObject.rect.centery - collidingObject.rect.centery) ** 2) <= requiredRadiusToObject:
         collidingObjects.append(collidingObject)
   
   # Return: values
   return collidingObjects
   
def checkCircCollide(collidedPoint, collidedObject, collidedCircGroup, groupCircRadius):
   '''  SYNTAX   checkCircCollide(collidePoint : iter, collidedObject, collidedCircGroup 
                 : Group, groupCircRadius : float)
   
       PURPOSE   Check if the apparent collidedObject's coordinates collide
                 appropriately within the circular body of any object in 
                 collidedCircGroup, given the radius is groupCircRadius.
                 
       DETAILS   This function is different from yieldIterInRadius(), as this
                 function compares to see if sprite rects are colliding, before
                 proceeding. This process is recommended for larger groups.
                  
        RETURN   Return the specified entity that collided with the object. 
                 Otherwise, return False. 
   '''
   # Quick Test 1: see if the specified object and group collide and are close enough
   for collidedEntity in pygame.sprite.spritecollide(collidedObject, collidedCircGroup, False):
      # Test: if the player's arm is within the entity's body radius
         if math.sqrt((collidedPoint[0] - collidedEntity.rect.centerx) ** 2 + \
                      (collidedPoint[1] - collidedEntity.rect.centery) ** 2) <= groupCircRadius:
            # Return: values (case 1)
            return collidedEntity
   # Return: values (case 2)
   return False

def checkCircCollideAdaptable(collidedObject, collidedCircGroup):
   '''  SYNTAX   checkCircCollideAdaptable(collidedObject : obj, 
                 collidedCircGroup : group)
   
       PURPOSE   Check if the apparent collidedObject's coordinates collide
                 appropriately within the circular body of any object in 
                 collidedCircGroup, given the collidedCircGroup's object's
                 own radius from its rect (and assuming its width = height).
                  
        RETURN   Return the specified entity that collided with the object. 
                 Otherwise, return False. 
   '''
   # Quick Test 1: see if the specified object and group collide and are close enough
   for collidedEntity in pygame.sprite.spritecollide(collidedObject, collidedCircGroup, False):
      # Test: if the player's arm is within the entity's body radius
      if math.sqrt((collidedEntity.rect.centerx - collidedObject.rect.centerx) ** 2 + \
                   (collidedEntity.rect.centery - collidedObject.rect.centery) ** 2) <= \
         collidedEntity.image.get_width():
            # Return: values (case 1)
            return collidedEntity
   # Return: values (case 2)
   return False

def handlingInput(keepGoing, screenObject, playerObject, labelText, endingText, worldSizeBorder, \
                  radiusToPlayerCenter, wavecounterObject, healthbarObject, \
                  hotbarObject, cameraObject, botsObjectGroup, cratesObjectGroup, \
                  spritesKillableGroup, spritesKillableTerrainGroup, spritesSolidGroup, \
                  spritesInGameGroup, spritesAllBottom, midLayerPrecedenceList, \
                  spritesAllTop, spritesAll, endingTimeCounter, END_TIME_FRAMES = 150):
      '''     SYNTAX   handlingInput(keepGoing : bool, screenObject : obj, playerObject
                       : obj, worldSizeBorder : tuple, radiusToPlayerCenter : int,
                       wavecounterObject : obj, healthbarObject : obj, hotbarObject : obj,
                       cameraObject : obj, botsObjectGroup : group, cratesObjectGroup 
                       : group, spritesKillableGroup : group, spritesKillableTerrainGroup 
                       : group, spritesSolidGroup : group, spritesInGameGroup : group, 
                       spritesAllBottom : group, midLayerPrecedenceList : list, 
                       spritesAllTop : group, spritesAll : group)
                       
             PURPOSE   This function is used to handle and deal with all inputs 
                       created by the user.
             
             DETAILS   This is the main function of the game loop.
             
          PARAMETERS   A boolean value expressing if the game should continue or not;
                       the screen object; the player object; the world border as a 
                       tuple of tuples of integers; the actual radius to the Player 
                       sprite's center as an integer; the wave counter GUI object; the 
                       health bar GUI object; the hotbar GUI object; the camera object; 
                       the group of all Bot objects; the group of all Crate objects; 
                       the group of killable (all and terrain) sprites; the group 
                       of solid sprites; the group of all in-game sprites; the 
                       groups of the bottom and top layer sprites; the list of 
                       all middle-layer sprite objects; and the all-sprites group.
          
              RETURN   The new boolean value for if the game loop should continue
                       looping; the group of all in-game sprites; the group of all
                       middle-layer sprites; and the group of all sprites.
      '''
      
      # Input Intake: as player stays alive or not all bots are killed on the last wave
      if not playerObject.getIsKilled():
         # Handling Input 1: mouse-hold
         newInGameBullets1, newBulletAppend1, newUtilityAppend1 = \
            handlingMouseHold(playerObject, screenObject, hotbarObject, \
                              healthbarObject, spritesSolidGroup)
         
         # Handling Input 2: key-hold
         handlingKeyHold(screenObject, worldSizeBorder, radiusToPlayerCenter, \
                         playerObject, cameraObject, spritesSolidGroup, spritesInGameGroup)
         
         # Handling Input 3: key-press
         keepGoing, newInGameItemDrop1, newItemDropAppend1 = \
            handlingKeyPress(playerObject, hotbarObject, midLayerPrecedenceList, \
                             radiusToPlayerCenter)
         
         # Handling Input 4: deals with resulting miscellaneous interaction events
         newBotsAppend1, newInGameItemDrop2, \
            newKillableAppend1, newItemDropAppend2, newBulletAppend2 = \
            handlingMiscInteractEvents(radiusToPlayerCenter, screenObject, wavecounterObject, \
                                       healthbarObject, playerObject, cameraObject, \
                                       labelText, midLayerPrecedenceList, botsObjectGroup, \
                                       cratesObjectGroup, spritesKillableGroup, \
                                       spritesKillableTerrainGroup, spritesSolidGroup)
         
         # Update: in-game sprites group; middle-layer sprites group; and all sprites group
         spritesInGameGroupAppendList = [newInGameBullets1, newInGameItemDrop1, newInGameItemDrop2]
         newItemDropAppendList = [newItemDropAppend1, newItemDropAppend2]
         newBulletAppendList = [newBulletAppend1, newBulletAppend2]
         newUtilityAppendList = [newUtilityAppend1]
         newBotAppendList = [newBotsAppend1]
         newKillableAppendList = [newKillableAppend1]
         
         if (spritesInGameGroupAppendList != [[], [], []]) and \
            ((newItemDropAppendList != [[], []]) or (newBulletAppendList != [[], []]) or \
             (newUtilityAppendList != [[]]) or (newBotAppendList != [[]]) or (newKillableAppendList != [[]])):
            # Update: only if there is some group to update with a new sprite, otherwise stay the same
            spritesInGameGroup, midLayerPrecedenceList, spritesKillableGroup, spritesAll = \
               appendCreatedToSpritesGroups( \
                  spritesInGameGroupAppendList, newItemDropAppendList, newBulletAppendList, \
                  newUtilityAppendList, newBotAppendList, newKillableAppendList, \
                  botsObjectGroup, spritesInGameGroup, spritesKillableGroup, \
                  midLayerPrecedenceList, spritesAllBottom, spritesAllTop)
            
         # Alternative End Condition
         if wavecounterObject.getWaveNumber() == wavecounterObject.getEndWaveNumber() - 1 \
            and wavecounterObject.getTimeInEndWave() and not botsObjectGroup:
            endingTimeCounter += 1
            endingText.updateColor((215, 255, 215))
            endingText.updateText("VICTORY")
            endingText.showText()
            if endingTimeCounter >= END_TIME_FRAMES:
               keepGoing = False
         
      # Input Intake: none; player is dead      
      else:
         endingTimeCounter += 1
         endingText.updateColor((255, 215, 215))
         endingText.updateText("DEFEAT")
         endingText.showText()
         if endingTimeCounter >= END_TIME_FRAMES:
            keepGoing = False
         
      # Return: values
      return keepGoing, spritesInGameGroup, midLayerPrecedenceList, spritesAll, endingTimeCounter
   
def appendCreatedToSpritesGroups(newInGameAppendList, newItemDropAppendList, \
                                 newBulletAppendList, newUtilityAppendList, newBotAppendList, \
                                 newKillableAppendList, botsObjectGroup, spritesInGameGroup, \
                                 spritesKillableGroup, midLayerPrecedenceList, \
                                 spritesAllBottom, spritesAllTop):
   '''     SYNTAX   appendCreatedToSpritesGroups(...)
     
          PURPOSE   To append all sprites created within the last frame to the
                    existing sprite groups for future reference.
        
       PARAMETERS   The list of new in-game sprites; the list of new item drop
                    sprites; the list of new bullet sprites; the list of new
                    utility sprites; the list of new Bot sprites; the list of
                    new killable sprites; the group of all Bot objects; the
                    group of all in-game sprites; the group of all killable
                    sprites; the list of groups of middle-layer sprites in
                    order of precedence; the group of all bottom-layer sprites;
                    and the group of all top-layer sprites.
         
           RETURN   The new in-game sprite group; the new middle-layer sprite
                    group by list precedence; the new killable sprite group;
                    and the new group of all sprites.
   '''
   # Section 1: all in-game sprite objects
   for spritesInGameGroupAppend in newInGameAppendList:
      spritesInGameGroup.add(spritesInGameGroupAppend)
      
   # Section 2: all killable sprite objects
   for killableObjectAppend in newKillableAppendList:
      spritesKillableGroup.add(killableObjectAppend)
      
   # Section 3a: all middle-layer sprite objects, by layer 1
   for newItemDropAppend in newItemDropAppendList:
      midLayerPrecedenceList[0].add(newItemDropAppend)
      
   # Section 3b: all middle-layer sprite objects, by layer 2
   for newBulletAppend in newBulletAppendList:
      midLayerPrecedenceList[1].add(newBulletAppend)
      
   # Section 3c: all middle-layer sprite objects, by layer 3
   for newUtilityAppend in newUtilityAppendList:
      midLayerPrecedenceList[2].add(newUtilityAppend)
      
   # Section 3d: all middle-layer sprite objects, unique layer 4; new wave bots
   for botObjectAppend in newBotAppendList:
      botsObjectGroup.add(botObjectAppend)

   # Section 3z: all middle-layer sprite objects, bound together   
   spritesAllMiddle = pygame.sprite.LayeredUpdates( \
      midLayerPrecedenceList[0], midLayerPrecedenceList[1], \
      midLayerPrecedenceList[2], botsObjectGroup)
      
   # Section 4: all sprite objects, bound together
   spritesAll = pygame.sprite.LayeredUpdates( \
      spritesAllBottom, spritesAllMiddle, spritesAllTop)
   
   return spritesInGameGroup, midLayerPrecedenceList, spritesKillableGroup, spritesAll
   
def executeMenu(screen, FRAMES_PER_SECOND = 30, COOLDOWN_TIMER = 45):
   '''     SYNTAX   executeMenu(screen : obj)
   
          PURPOSE   To execute the functions of the menu and display it, on loop.
          
       PARAMETERS   The screen object.
   '''
   # E: ENTITIES
   background = pygame.Surface(screen.get_size())
   background.fill((255, 255, 255))
   screen.blit(background, (0, 0))
   
   title = classBreach.Title(screen)
   spritesAll = pygame.sprite.Group(title)
   
   ### A: ASSIGN: Miscellaneous Variables ###
      
   # Variable(s): World
   keepGoing = True
   clock = pygame.time.Clock()
   cooldown = 0

   # L: LOOP
   while keepGoing:
        
      print(cooldown)
      # T: TIME
      clock.tick(FRAMES_PER_SECOND)
     
      # E: EVENT HANDLING
      keepGoing = handlingMenuKeyPress(keepGoing, cooldown, COOLDOWN_TIMER)
      if cooldown < COOLDOWN_TIMER:
         cooldown += 1
      
      if not keepGoing:
         title.executeLoadingScreen()
         
      # R: Refresh screen
      spritesAll.clear(screen, background)
      spritesAll.update()
      spritesAll.draw(screen)
      pygame.display.flip()
   
def executeGameLoop(screen):
   '''     SYNTAX   executeGameLoop(screen : obj)
   
          PURPOSE   To execute the functions of the entire game, on loop.
          
       PARAMETERS   The screen object.
   '''
   ### A: ASSIGN: Needed Constants & Variables for Entity Spawning ###
      
   # Constant: Player: Custom Hitbox Radius
   RADIUS_TO_PLAYER_CENTER = 36
   
   # E: ENTITIES
   background, WORLD_SIZE_BORDER, [player, camera, hotbar, healthbar, wavecounter, bushes, 
   stumps, pebbles, barrels, crates, bots, midLayerPrecedenceList, spritesCrates, 
   spritesKillable, spritesKillableTerrain, spritesSolid, spritesInGame, spritesAllBottom, 
   spritesAllMiddle, spritesAllTop, spritesAll, endingText, labelText] = \
      mainEntities(RADIUS_TO_PLAYER_CENTER, screen)
   
   ### A: ASSIGN: Miscellaneous Constants ###
   
   # Constant(s): Frames Per Second
   FRAMES_PER_SECOND = 30
   
   ### A: ASSIGN: Miscellaneous Variables ###
   
   # Variable(s): World
   keepGoing = True
   clock = pygame.time.Clock()
   endingTimeCounter = 0
   
   # L: LOOP
   while keepGoing:
     
      # T: TIME
      clock.tick(FRAMES_PER_SECOND)
     
      # E: EVENT HANDLING
      keepGoing, spritesInGame, midLayerPrecedenceList, spritesAll, endingTimeCounter = \
         handlingInput(keepGoing, screen, player, labelText, endingText, WORLD_SIZE_BORDER, \
                       RADIUS_TO_PLAYER_CENTER, wavecounter, healthbar, hotbar, camera, \
                       bots, spritesCrates, spritesKillable, spritesKillableTerrain, \
                       spritesSolid, spritesInGame, spritesAllBottom, \
                       midLayerPrecedenceList, spritesAllTop, spritesAll, endingTimeCounter)
      
      # R: Refresh screen
      spritesAll.clear(screen, background)
      spritesAll.update()
      spritesAll.draw(screen)
      pygame.display.flip()
   
################################################################################
##                                                                            ##
##                                   Main                                     ##
##                                                                            ##
################################################################################

# I: IMPORT AND INITIALIZE
import pygame, classBreach, math, random, os
pygame.init()
   
def main():
   '''   PURPOSE   This function defines the 'mainline logic' for the game. '''
    
   # D: DISPLAY
   screen = mainDisplay()
   
   # A: ACTION (DEMO, THEREFORE ON INFINITE LOOP)
   while True:
      executeMenu(screen)
      executeGameLoop(screen)
       
# Call the main function
main()