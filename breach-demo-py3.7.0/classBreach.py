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

import pygame, math, random

class Title(pygame.sprite.Sprite):
    '''     PURPOSE   Defines the sprite for the Title, as a class.
            
        INHERITANCE   The Sprite class.
    '''
    def __init__(self, screen):
        '''     SYNTAX   object.Title(screen : obj)
        
               PURPOSE   The title is the main menu's primary component and plays
                         the role as the introducer of the player to the game.
                         
            PARAMETERS   The screen object.
        '''
        # Initialize: call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        # Initialize: instance variables
        self.__screen = screen
        self.__menuSection = 0
        self.__waveCounterFont = pygame.font.Font("fonts\\pixelated_arial_bold_11.ttf", 196)
        
        # Initialize: image and rect attributes of the Title object.
        self.__filePath = "images\\menu\\"
        
        self.image = pygame.Surface(screen.get_size())
        self.rect = self.image.get_rect()
        self.image.fill((0, 0, 0))

        imageBG = pygame.image.load(self.__filePath + "image_Menu_Background.png").convert()
        self.image.blit(imageBG, (0, 0))
        
        imageTitle = pygame.image.load(self.__filePath + "image_Menu_Title.png").convert_alpha()
        self.image.blit(imageTitle, (screen.get_width() / 2 - imageTitle.get_width() / 2, \
                                     screen.get_height() / 2 - imageTitle.get_height() / 2))
        
    def executeLoadingScreen(self, LOADING_LABEL_COLOR = (250, 250, 250)):
        '''   SYNTAX   object.executeLoadingScreen()
        
             PURPOSE   To execute the loading screen segment of the game.
        '''
        imageBG = pygame.image.load(self.__filePath + "image_Menu_Background.png").convert()
        self.image.blit(imageBG, (0, 0))
        
        loadingLabel = self.__waveCounterFont.render("LOADING ", 0, LOADING_LABEL_COLOR)   
        placeImageOnCoords = (self.__screen.get_width() / 2 - loadingLabel.get_width() / 2 + 25, \
                              self.__screen.get_height() / 2 - loadingLabel.get_height() / 2)
        self.image.blit(loadingLabel, placeImageOnCoords)
        
class Utility(pygame.sprite.Sprite):
    '''     PURPOSE   Defines the sprite for the Utility, as a class.
            
        INHERITANCE   The Sprite class.
    '''
    def __init__(self, initialCoords, direction, utilityName, \
                 INITIAL_THROW_SPEED = 50):
        '''     SYNTAX   object.Utility(initialCoords : tuple, direction : float,
                         utilityName : str)
        
               PURPOSE   The utility plays the role of the player supporter in
                         the game. It is a class of items that helps the player
                         outside of boosts and can be used more mechanically
                         than boosts.
                         
                         Initializes the initial coordinates, radian direction,
                         utility name, live time, and rotated angle.
    
            PARAMETERS   The initial coordinates as a (x, y) tuple of integer
                         coordinates, the direction as a float value in radians,
                         and the utility name.
        '''
        # Initialize: call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        # Initialize: instance variables
        self.__direction = direction
        self.__utilityName = utilityName
        self.__liveTime = 0
        self.__throwSpeed = INITIAL_THROW_SPEED
        self.__changedForm = False
        
        filePath = "images\\item\\"
        self.__imageUtility = pygame.image.load( \
            filePath + "image_" + self.__utilityName + ".png").convert()
        
        filePath = "images\\entity\\"
        self.__imageAOECircle = pygame.image.load( \
            filePath + "image_AOESignal.png").convert()
        
        self.__imageAOECircle.set_colorkey((255, 255, 255))
        
        # Initialize: the image and rect attributes of the Utility object
        self.updateImage(initialCoords)
        
    def getTimeToForm(self, FORMATION_TIME = 45):
        '''  SYNTAX   object.getTimeToForm()
        
            PURPOSE   To get the time for the utility to reach its form.
                      
             RETURN   The time as an integer in frames.
        '''
        return FORMATION_TIME
    
    def getDirection(self):
        '''  SYNTAX   object.getDirection()
    
            PURPOSE   Accessor Method: to get the object's direction in radians.
        
             RETURN   The object's rotation by radians as a float value.
        '''
        return self.__direction
        
    def updateLiveTime(self):
        '''  SYNTAX   object.updateLiveTime()
             
            PURPOSE   To update the time the object lives for on the screen.
        '''
        self.__liveTime += 1
        
    def getLiveTime(self):
        '''  SYNTAX   object.getLiveTime()
        
            PURPOSE   Accessor Method: to get the object's screen live time.
            
             RETURN   The object's screen live time as an integer.
        '''
        return self.__liveTime
    
    def getUtilityName(self):
        '''  SYNTAX   object.getUtilityName()
        
            PURPOSE   Accessor Method: to get the object's utility name.
            
             RETURN   The object's utility name as a string.
        '''
        return self.__utilityName
        
    def utilitySpin(self, image, initialCoords):
        '''     SYNTAX   object.utilitySpin(image : obj, initialCoords : iter)
             
               PURPOSE   To change the utility's spinning image to its direction.
            
            PARAMETERS   The image object and initial coordinates as an iterable.
        '''
        image = pygame.transform.rotate(image, self.getDirection())
        
        self.rect = image.get_rect(center = self.rect.center)
        image.get_rect(center = self.rect.center)
        
        
    def updateImage(self, initialCoords, AOE_DIAMETER = 1024, IMAGE_SIDE_LENGTH = 64):
        '''     SYNTAX   object.updateImage()
        
               PURPOSE   To update the image and rect attributes of the object.
               
            PARAMETERS   The initial coordinates of the object as a (x, y) tuple.
        '''        
        # Image Attributes: with utility item
        self.__diameter = AOE_DIAMETER
        self.image = pygame.Surface((AOE_DIAMETER, AOE_DIAMETER))
        self.image.set_colorkey((0, 0, 0))
        self.updateAOECircle()
        imageUtility = pygame.transform.scale(self.__imageUtility, \
                                              (IMAGE_SIDE_LENGTH, IMAGE_SIDE_LENGTH))
        imageUtility.set_colorkey((255, 255, 255))
        
        posOnImage = (self.image.get_width() / 2 - imageUtility.get_width() / 2, \
                      self.image.get_height() / 2 - imageUtility.get_height() / 2)
        
        # Rect attributes
        self.rect = self.image.get_rect()
        self.rect.center = initialCoords
        self.image.blit(imageUtility, posOnImage)
        
        # Set: initial image
        
        self.__initImage = self.image.copy()
        
    def updateAOECircle(self):
        '''  SYNTAX   object.updateAOECircle()
        
            PURPOSE   To update the AOE signal radius.
        '''
        # Image and Rect: Place AOE Signal Diameter
        diameterOfCirc = int(round(self.getLiveTime() / float( \
            self.__throwSpeed) * self.__diameter))
        if diameterOfCirc > self.__diameter:
            diameterOfCirc = self.__diameter
        scaledAOECircle = pygame.transform.scale( \
            self.__imageAOECircle, (diameterOfCirc, diameterOfCirc))
        
        posOnImage = (self.image.get_width() / 2 - scaledAOECircle.get_width() / 2, \
                      self.image.get_height() / 2 - scaledAOECircle.get_height() / 2)
        self.image.blit(scaledAOECircle, posOnImage)
        
    def setChangedForm(self, state):
        '''     SYNTAX   object.setChangedForm(state : bool)
            
               PURPOSE   Mutator Method: to set the object's changed form
                         attribute to a new state.
                         
            PARAMETERS   The updated state of the object's form as a boolean value.
        '''
        self.__changedForm = state
        
    def getChangedForm(self):
        '''  SYNTAX   object.getChangedForm()
    
            PURPOSE   Accessor Method: to get the object's changed form.
        
             RETURN   A boolean value expressing the changed form of the object.
        '''
        return self.__changedForm
        
    def update(self, RAD90_VALUE = math.pi / 2.0):
        '''  SYNTAX   object.update()
        
            PURPOSE   To update the live time of the object.
        '''
        self.updateImage((self.rect.centerx, self.rect.centery))
        self.updateLiveTime()
        
        if self.getLiveTime() < self.getTimeToForm():
            # Spin Form: pre-utility power
            self.rect.centerx += math.sin(self.__direction + RAD90_VALUE) * self.__throwSpeed / (self.getLiveTime())
            self.rect.centery += math.cos(self.__direction + RAD90_VALUE) * self.__throwSpeed / (self.getLiveTime())
            
        elif self.getLiveTime() == self.getTimeToForm():
            # Utility Form: has utility power
            self.setChangedForm(True)

class Bullet(pygame.sprite.Sprite):
    '''     PURPOSE   Defines the sprite for the Bullet, as a class.
        
        INHERITANCE   The Sprite class.
    '''
    def __init__(self, screen, initialCoords, isFromPlayer, damage, direction, \
                 velocity, accuracy):
        '''     SYNTAX   object.Bullet(screen : obj, initialCoords : tuple, 
                         isFromPlayer : bool, damage : int, direction : float, 
                         velocity : float, 0 <= accuracy : int <= 90)
        
               PURPOSE   The primary damage-dealer of the entire game, hosted
                         by guns. Instantiation is required in an orderly
                         conduct in the main game loop.
                         
                         Initializes the screen, Bullet's location, damage, direction, 
                         velocity, if it came from the player or not, file path, and
                         live time.
    
            PARAMETERS   The screen object; the initial coordinates of the bullet 
                         on the screen as a (x, y) tuple; the boolean value expressing 
                         if the bullet comes from the player; the bullet's damage as an
                         integer; bullet direction in radians; bullet velocity 
                         as a float value; and bullet accuracy in terms of degrees,
                         as an integer.
        '''
        # Initialize: call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        # Initialize: instance variables
        self.__screen = screen
        self.__isFromPlayer = isFromPlayer
        self.__bulletDamage = damage
        self.__bulletDirection = direction
        self.__bulletVelocity = velocity
        self.__accuracy = accuracy
        self.__filePath = "images\\entity\\"
        self.__liveTime = 0
        
        # Initialize: the image and rect attributes for the Bullet
        self.executeAccuracyDirectionOffset()
        self.initBulletImage(initialCoords[0], initialCoords[1])
    
    def initBulletImage(self, initialCoordX, initialCoordY):
        '''  SYNTAX   object.initBulletImage(initialCoordX : int, initialCoordY : int)
        
            PURPOSE   To initialize the image and rect attributes for the
                      bullet.
                      
            PARAMETERS   The initial coordinates X and Y on the screen for the
                         bullet to spawn.
        '''
        # Image attributes
        self.image = pygame.image.load(self.__filePath + "image_BulletExplode.png").convert()
        self.image.set_colorkey((255, 255, 255))
        
        # Rect attributes
        self.rect = self.image.get_rect()
        self.rect.centerx = initialCoordX
        self.rect.centery = initialCoordY
        
    def explodeOnScreen(self):
        '''  SYNTAX   object.explodeOnScreen()
        
            PURPOSE   For the object to explode while on screen before dying.
        '''
        self.__explodingOnScreenFrames = 1
        self.initBulletImage(self.rect.centerx, self.rect.centery)
        
    def executeAccuracyDirectionOffset(self, ANGLE_IN_RAD = math.pi / 180):
        '''  SYNTAX   object.executeAccuracyDirectionOffset()
        
            PURPOSE   To update the object's direction based on the given accuracy.
        '''
        self.__bulletDirection += random.uniform(-ANGLE_IN_RAD * (90 - self.__accuracy), \
                                                 ANGLE_IN_RAD * (90 - self.__accuracy))
    
    def changeBulletImage(self):
        '''   SYNTAX   object.changeBulletImage()
             
             PURPOSE   To change the bullet's image as of after its initial image.        
        '''
        retainedPosition = self.rect.center
        
        # Image attributes
        self.image = pygame.image.load(self.__filePath + "image_BulletBase.png").convert()
        self.image.set_colorkey((255, 255, 255))
        
        # Rect attributes
        self.rect = self.image.get_rect()
        self.rect.center = retainedPosition
        
        # Image and Rect: rotate bullet to face in its angle
        bulletAngle = math.degrees(self.__bulletDirection)
        self.image = pygame.transform.rotate(self.image, bulletAngle)
        self.rect = self.image.get_rect(center = self.rect.center)
        self.image.get_rect(center = self.rect.center)

    def updateLiveTime(self):
        '''  SYNTAX   object.updateLiveTime()
             
            PURPOSE   To update the time the object lives for on the screen.
        '''
        self.__liveTime += 1
        
    def getIsFromPlayer(self):
        '''  SYNTAX   object.getIsFromPlayer()
        
            PURPOSE   Accessor Method: to get if the object was "created" from
                      a Player.
            
             RETURN   A boolean value expressing if the object originated from
                      the Player.
        '''
        return self.__isFromPlayer
    
    def getDamage(self):
        '''  SYNTAX   object.getDamage()
        
            PURPOSE   Accessor Method: to get the object's damage.
            
             RETURN   The object's damage as an integer.
        '''
        return self.__bulletDamage

    def getLiveTime(self):
        '''  SYNTAX   object.getLiveTime()
        
            PURPOSE   Accessor Method: to get the object's screen live time.
            
             RETURN   The object's screen live time as an integer.
        '''
        return self.__liveTime        

    def update(self, FRAMES_AT_DEATH = 2, RAD90_VALUE = math.pi / 2.0):
        '''  SYNTAX   object.update()
        
            PURPOSE   To update the bullet so that it travels in its appropriate
                      direction and kills itself offscreen.
        '''
        # Update: live time, changes image
        self.updateLiveTime()
        if self.getLiveTime() == 2:
            self.changeBulletImage()
        
        # Update: bullet position
        updatedBulletDirection = self.__bulletDirection + RAD90_VALUE
        self.rect.centerx += math.sin(updatedBulletDirection) * self.__bulletVelocity
        self.rect.centery += math.cos(updatedBulletDirection) * self.__bulletVelocity
        
        if (self.rect.bottom < -self.__screen.get_height() * 0.5 or self.rect.top > self.__screen.get_height() * 1.5) or \
           (self.rect.right < -self.__screen.get_width() * 0.5 or self.rect.left > self.__screen.get_width() * 1.5):
            # Kill: bullet off-screen
            self.kill()
        
class WaveCounterGUI(pygame.sprite.Sprite):
    '''     PURPOSE   Defines the sprite for the WaveCounterGUI, as a class.
        
        INHERITANCE   The Sprite class.
    '''
    def __init__(self, screen, initialWaveTime, lastWave):
        '''     SYNTAX   object.WaveCounterGUI(screen : obj, initialWaveTime : 
                         int, lastWave : int)
        
               PURPOSE   To display the wave count to be kept track of
                         visually.
                         
                         Initializes the WaveCounterGUI's image and rect 
                         attributes, wave number, wave time, and screen.
    
            PARAMETERS   The screen object; the time per wave as an integer; and
                         the last wave as an integer.
        '''
        # Initialize: call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        # Initialize: the image and rect attributes for the empty WaveCounterGUI
        # and instance variables
        self.__screen = screen
        self.__waveFinishedInFrame = False
        self.__waveNumber = 5
        self.__endWaveNumber = lastWave + 1
        self.__endWaveTime = 0
        self.__maxWaveTime = initialWaveTime
        self.__waveTime = initialWaveTime
        self.__filePathGUI = "images\\gui\\"
        self.__waveCounterFont = pygame.font.Font("fonts\\pixelated_arial_bold_11.ttf", 96)
        
        self.updateImage()
        
    def resetImage(self):
        '''  SYNTAX   object.resetImage()
        
            PURPOSE   To reset the state of the original image.
        '''
        self.image = pygame.Surface((528, 124))
        self.image.set_colorkey((0, 0, 0))
        
        imageBase = pygame.image.load( \
            self.__filePathGUI + "image_WaveCounter.png").convert()
        imageBase.set_colorkey((255, 255, 255))
        self.image.blit(imageBase, (0, self.image.get_height() / 2 - \
                                    imageBase.get_height() / 2))
        
        self.rect = self.image.get_rect()
        self.rect.centerx = self.__screen.get_width() / 2
        self.rect.centery = self.image.get_height() / 2
                        
    def updateImage(self, BEAM_MAX_WIDTH = 516, BEAM_HEIGHT = 6, BAR_SIDE_LENGTH = 6, \
                    BAR_LEVERAGE = 3,  WAVE_COUNT_BEAM_COLOR = (254, 254, 254), \
                    WAVE_NUMBER_COLOR_1 = (100, 255, 100), \
                    WAVE_NUMBER_COLOR_2 = (245, 215, 55), \
                    WAVE_NUMBER_COLOR_3 = (255, 100, 100)):
        '''  SYNTAX   object.updateImage()
        
            PURPOSE   Updates the object's image to implement the wave count.
        '''
        # Implement: wave counter border
        self.resetImage()
        
        # Implement: wave bar
        
        # Wave Count Beam Width: correlate with player's current to max health
        waveTimeCorrelatedBeamWidth = int(round(self.getWaveTime() / float( \
            self.getMaxWaveTime()) * BEAM_MAX_WIDTH / 2))
                    
        # Wave Count Beam Final Draw
        pygame.draw.rect( \
            self.image, WAVE_COUNT_BEAM_COLOR, \
            (BEAM_MAX_WIDTH / 2 - waveTimeCorrelatedBeamWidth + BAR_SIDE_LENGTH, \
             self.image.get_height() / 2 - BAR_LEVERAGE, waveTimeCorrelatedBeamWidth * 2, BEAM_HEIGHT))
        
        # Implement: wave number
        if not self.getWaveNumber():
            waveNumberLabel = self.__waveCounterFont.render( \
                "%s" % "START", 0, WAVE_NUMBER_COLOR_1)
        elif self.getWaveNumber() < self.getEndWaveNumber() - 1:
            waveNumberLabel = self.__waveCounterFont.render( \
                "%d" % self.getWaveNumber(), 0, WAVE_NUMBER_COLOR_2)
        elif self.getWaveNumber() >= self.getEndWaveNumber() - 1:
            waveNumberLabel = self.__waveCounterFont.render( \
                "%s" % "BOSS", 0, WAVE_NUMBER_COLOR_3)
            
        # Final Implementation Blit
        placeImageOnCoords = (self.image.get_width() / 2 - waveNumberLabel.get_width() / 2, \
                              self.image.get_height() / 2 - waveNumberLabel.get_height() / 2)
        self.image.blit(waveNumberLabel, placeImageOnCoords)
        
    def getFinishedInFrame(self):
        '''  SYNTAX   object.getFinishedInFrame()
        
            PURPOSE   Accessor Method: to return the object's input on if a
                      wave just finished.
                      
             RETURN   A boolean value expressing if a wave just finished or not.
        '''
        return self.__waveFinishedInFrame
    
    def setFinishedInFrame(self, waveFinished):
        '''     SYNTAX   object.setFinishedInFrame(waveFinished : bool)
        
               PURPOSE   Mutator Method: to change the object's state on if a
                         wave had just finished.
                         
            PARAMETERS   A boolean value expressing the state of if a wave just 
                         finished or not.
        '''
        self.__waveFinishedInFrame = waveFinished
    
    def getMaxWaveTime(self):
        '''  SYNTAX   object.getMaxWaveTime()
        
            PURPOSE   Accessor Method: to return the object's max wave time.
                         
             RETURN   An integer expressing the object's max wave time.
        '''
        return self.__maxWaveTime    

    def getWaveTime(self):
        '''  SYNTAX   object.getWaveTime()
        
            PURPOSE   Accessor Method: to return the object's wave time.
                         
             RETURN   An integer expressing the object's wave time.
        '''
        return self.__waveTime
    
    def getEndWaveNumber(self):
        '''  SYNTAX   object.getEndWaveNumber()
        
            PURPOSE   Accessor Method: to return the object's end wave number.
                         
             RETURN   An integer expressing the object's end wave number.
        '''
        return self.__endWaveNumber    

    def getWaveNumber(self):
        '''  SYNTAX   object.getWaveNumber()
        
            PURPOSE   Accessor Method: to return the object's wave number.
                         
             RETURN   An integer expressing the object's wave number.
        '''
        return self.__waveNumber    
    
    def setMaxWaveTime(self, maxWaveTime):
            '''     SYNTAX   object.setMaxWaveTime(maxWaveTime : int)
            
                   PURPOSE   Mutator Method: to change the object's max wave time.
                             
                PARAMETERS   An integer expressing the new max wave time.
            '''
            self.__maxWaveTime = maxWaveTime  

    def setWaveTime(self, waveTime):
        '''     SYNTAX   object.setWaveTime(waveTime : int)
        
               PURPOSE   Mutator Method: to change the object's wave time.
                         
            PARAMETERS   An integer expressing the new wave time.
        '''
        self.__waveTime = waveTime
        
    def updateWaveTime(self):
        '''  SYNTAX   object.updateWaveTime()
             
            PURPOSE   To update the object's wave time.
        '''
        self.__waveTime -= 1
        
    def updateWaveNumber(self):
        '''  SYNTAX   object.updateWaveNumber()
             
            PURPOSE   To update the object's wave number.
        '''
        self.__waveNumber += 1
        
    def getTimeInEndWave(self):
        '''  SYNTAX   object.getTimeInEndWave()
        
            PURPOSE   Accessor Method: to get the time in the object's end wave.
            
             RETURN   The end wave time as an integer.
        '''
        return self.__endWaveTime
    
    def updateTimeInEndWave(self):
        '''  SYNTAX   object.updateTimeInEndWave()
        
            PURPOSE   To update the object's end wave time.
        '''
        self.__endWaveTime += 1 
        
    def update(self, STEP_FRAME_INCREMENT_PER_WAVE = 100):
        '''  SYNTAX   object.update()
        
            PURPOSE   Update the timer to decrease each frame, until the timer
                      reaches 0 frames, at which it will reset and add to the
                      wave counter, up to the number of waves it takes to end.
                      
                      self.getFinishedInFrame()
        '''
        if self.getWaveNumber() < self.getEndWaveNumber() - 1:
            # Wave: normal
            self.setFinishedInFrame(False)
            self.updateWaveTime()
            self.updateImage()
            if not self.getWaveTime():
                # Wave Counter: reset upon hitting 0 time for the specific wave
                self.setMaxWaveTime(self.getMaxWaveTime() + STEP_FRAME_INCREMENT_PER_WAVE)
                self.setWaveTime(self.getMaxWaveTime())
                self.setFinishedInFrame(True)
                self.updateWaveNumber()
        else:
            # Wave: boss
            self.setFinishedInFrame(False)
            self.setWaveTime(0)
            if not self.getTimeInEndWave():
                self.updateTimeInEndWave()
                self.updateImage()
        
class HealthBarGUI(pygame.sprite.Sprite):
    '''     PURPOSE   Defines the sprite for the HealthBarGUI, as a class.
    
        INHERITANCE   The Sprite class.
    '''
    def __init__(self, screen, maxPlayerHealth, heightOfHotBar):
        '''     SYNTAX   object.HealthBarGUI(screen : obj, maxPlayerHealth
                         : int, heightOfHotBar : int)
        
               PURPOSE   To display the Player's health to be kept track of
                         visually.
                         
                         Initializes the HealthBarGUI's image and rect attributes,
                         screen, and the tracked player's health and height of
                         the hotbar (for relative placement purposes), the font 
                         object, and file paths as strings.
    
            PARAMETERS   The screen object; the Player's health as an integer;
                         and the height of the hotbar GUI image as an integer.
        '''
        # Initialize: call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        # Initialize: the image and rect attributes for the empty HealthBarGUI,
        # also screen, tracked player's health and hotbar height, font, and file paths
        self.__maxPlayerHealth = maxPlayerHealth
        self.__currentPlayerHealth = maxPlayerHealth
        self.__heightOfHotBar = heightOfHotBar
        self.__screen = screen
        self.__filePathGUI = "images\\gui\\"
        self.__healthBarFont = pygame.font.Font("fonts\\pixelated_arial_bold_11.ttf", 31)
        
        self.updateImage()
        
    def setHealth(self, playerHealth):
        '''     SYNTAX   object.setHealth(playerHealth : tuple)
            
               PURPOSE   Mutator Method: to set the object's currentPlayerHealth and
                         maxPlayerHealth attribute to a new state. Since the tracked 
                         player health has been changed, the object's image must adapt 
                         to the new set value.
                         
            PARAMETERS   A (max, curr) tuple of numbers representing the max
                         and current health of the Player object, respectfully.
        '''
        self.__maxPlayerHealth = playerHealth[0]
        self.__currentPlayerHealth = playerHealth[1]
        self.updateImage()
        
    def updateHealth(self, changeInHealth):
        '''  SYNTAX   object.updateHealth(changeInHealth : int)
            
            PURPOSE   Mutator Method: to update the object's currentPlayerHealth
                      attribute by a value. Since the tracked player health
                      has been changed, the object's image must adapt to the new
                      set value.
        '''
        self.__currentPlayerHealth += changeInHealth
        self.updateImage()    
        
    def resetImage(self):
        '''  SYNTAX   object.resetImage()
        
            PURPOSE   To reset the state of the original image.
        '''
        self.image = pygame.image.load( \
            self.__filePathGUI + "image_HealthBar.png").convert()
        self.image.set_colorkey((255, 255, 255))
        
        self.rect = self.image.get_rect()
        self.rect.centerx = self.__screen.get_width() / 2
        self.rect.centery = self.__screen.get_height() - self.image.get_height() \
            / 2 - self.__heightOfHotBar - 10
                
    def updateImage(self, BAR_SIDE_LENGTH = 9, BEAM_MAX_WIDTH = 603, \
                    BEAM_HEIGHT = 31, MAX_RGB = 255, MAXIMUM_COLOR_CHANGE = 510):
        '''  SYNTAX   object.updateImage()
        
            PURPOSE   Updates the object's image to implement the Player's health.
        '''
        # Implement: player's health bar
        self.resetImage()
        
        if self.__currentPlayerHealth > 0:
            # Health Bar Ratios: the player's current health to max health and health change
            healthBarRatioToMax = self.__currentPlayerHealth / float(self.__maxPlayerHealth)
            healthBarRatioChange = (self.__maxPlayerHealth - self.__currentPlayerHealth) \
                / float(self.__maxPlayerHealth)
            
            # Health Bar Color: correlate with player's current to max health
            # where (green = 100%; yellow = 50%; and red = 0%).
            healthBarColorChange = int(round(healthBarRatioChange * MAXIMUM_COLOR_CHANGE))
            
            if healthBarColorChange < MAX_RGB:
                # Health: 100% => 50%
                healthBarColorRed = healthBarColorChange
                healthBarColorGreen = MAX_RGB
            else:
                # Health: 50% => 0%
                healthBarColorRed = MAX_RGB
                healthBarColorGreen = MAX_RGB * 2 - healthBarColorChange
            healthBarColor = (healthBarColorRed, healthBarColorGreen, 0)
            
            # Health Bar Width: correlate with player's current to max health
            healthCorrelatedBeamWidth = int(round(healthBarRatioToMax * BEAM_MAX_WIDTH))
            
            # Health Bar Final Draw
            pygame.draw.rect(self.image, healthBarColor, (BAR_SIDE_LENGTH, BAR_SIDE_LENGTH, healthCorrelatedBeamWidth, BEAM_HEIGHT))
                
            # Health Bar Label
            filePath = "fonts\\"
            healthBarLabel = self.__healthBarFont.render( \
                "%d | %d" % (int(math.ceil(self.__currentPlayerHealth)), \
                             self.__maxPlayerHealth), 0, (25, 37, 51))
            placeImageOnCoords = (self.image.get_width() / 2 - healthBarLabel.get_width() / 2, \
                                  self.image.get_height() / 2 - healthBarLabel.get_height() / 2)
            self.image.blit(healthBarLabel, placeImageOnCoords)
            
    #def update(self):
        #'''   SYNTAX   object.update()
        
             #PURPOSE   Display a decay at the Player's health. This is a feature
                       #used precisely for testing purposes, whereas the real
                       #features involve using setHealth().
        #'''
        #self.updateHealth(-0.005)

class HotBarGUI(pygame.sprite.Sprite):
    '''     PURPOSE   Defines the sprite for the HotBarGUI, as a class.
    
        INHERITANCE   The Sprite class.
    '''
    def __init__(self, screen, playerInventory, selectBarSlot):
        '''     SYNTAX   object.HotBarGUI(screen : obj, playerInventory : list,
                         selectBarSlot : int)
        
               PURPOSE   To display the Player's hotbar to be kept track of
                         visually.
                         
                         Initializes the HotBarGUI's image and rect attributes,
                         screen, and the tracked player's inventory.
    
            PARAMETERS   The screen object; the Player's inventory as a list.
        '''
        # Initialize: call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        # Initialize: the image and rect attributes for the empty HotBarGUI
        # object, inventory, selected bar slot, and screen
        self.__playerInventory = playerInventory
        self.__selectBarSlot = selectBarSlot
        self.__screen = screen
        
        filePath = "images\\gui\\"
        self.__selectBarSlotBorder = pygame.image.load( \
            filePath + "image_SelectBarSlot.png").convert()
        self.__selectBarSlotBorder.set_colorkey((255, 255, 255))
        
        self.updateImage()
        
    def setSelectBarSlot(self, slot):
        '''  SYNTAX   object.setSelectBarSlot(slot : int)
            
            PURPOSE   Mutator Method: to set the object's selectBarSlot
                      attribute to a new state.
        '''
        self.__selectBarSlot = slot    

    def setInventory(self, playerInventory):
        '''  SYNTAX   object.setInventory(playerInventory : list)
                    
            PURPOSE   Mutator Method: to set the HotBarGUI's inventory to a new
                      inventory.
                      
                      Also, since the inventory is updated, the hotbar's image
                      must update with the inventory.
        '''
        self.__playerInventory = playerInventory
        self.updateImage()
    
    def resetImage(self):
        '''  SYNTAX   object.resetImage()
        
            PURPOSE   To reset the state of the original image.
        '''
        filePath = "images\\gui\\"
        
        self.image = pygame.image.load(filePath + "image_HotBar.png").convert()
        self.image.set_colorkey((255, 255, 255))
        
        self.rect = self.image.get_rect()
        self.rect.centerx = self.__screen.get_width() / 2
        self.rect.centery = self.__screen.get_height() - self.image.get_height() / 2 - 5        
        
    def updateImage(self, BAR_SIDE_LENGTH = 9, SLOT_SIDE_LENGTH = 144):
        '''  SYNTAX   object.updateImage()
        
            PURPOSE   Updates the object's image to implement all items of the
                      Player's inventory.
        '''
        # Implement: inventory items by slot
        filePath = "images\\item\\image_"
        self.resetImage()
        for imageSlot in range(len(self.__playerInventory)):
            
            # Iterate: through each inventory slot. If there exists an item in
            # the slot, add it to the entire image.
            if self.__playerInventory[imageSlot]:
                
                # Location: set relative to hotbar GUI image
                placeImageOnCoords = ( \
                    BAR_SIDE_LENGTH + (SLOT_SIDE_LENGTH + BAR_SIDE_LENGTH) * \
                    imageSlot, BAR_SIDE_LENGTH)
                
                # Load, Scale, Colorkey, Blit: current slot image
                imageTempSlot = pygame.image.load( \
                    filePath + self.__playerInventory[imageSlot] + ".png").convert()
                imageTempSlot = pygame.transform.scale( \
                    imageTempSlot, (SLOT_SIDE_LENGTH, SLOT_SIDE_LENGTH))
                imageTempSlot.set_colorkey((255, 255, 255))
                self.image.blit(imageTempSlot, placeImageOnCoords)
                
        # Implement: selected bar slot border
        placeImageOnCoords = ( \
            BAR_SIDE_LENGTH + (SLOT_SIDE_LENGTH + BAR_SIDE_LENGTH) * \
            self.__selectBarSlot, BAR_SIDE_LENGTH)
        self.image.blit(self.__selectBarSlotBorder, placeImageOnCoords)
            
class Background(pygame.sprite.Sprite):
    '''     PURPOSE   Defines the sprite for the Background, as a class.
        
        INHERITANCE   The Sprite class.
    '''
    def __init__(self, screen):
        '''     SYNTAX   object.Background(screen : obj)
               
               PURPOSE   To display a background sprite so the screen is
                         constantly updating.
            
                         Initializes the Background's image and rect attributes.
                      
            PARAMETERS   The screen object.
        '''        
        # Initialize: call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        # Initialize: the image and rect attributes of the Background object
        self.image = pygame.Surface(screen.get_size())
        self.image.fill((125, 175, 85))
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        
class Entity(pygame.sprite.Sprite):
    '''     PURPOSE   Defines the sprite for the Entity, as a class.
        
        INHERITANCE   The Sprite class.
    '''
    def __init__(self, isPlayer, initialCoord, inventory, \
                 selectBarSlot, health, attackDamageMultiplier, \
                 PLAYER_COLOR = (252, 200, 117), BOT_COLOR = (190, 200, 210)):
        '''     SYNTAX   object.Entity(isPlayer : bool, initialCoord : iter, 
                         inventory : list, selectBarSlot : int, health : int, 
                         attackDamageMultiplier : float)
               
               PURPOSE   To give general functions to both the Player object and
                         the Bot object.
            
                         Initializes the Entity's color; initial coordinates;
                         health; selected bar slot; killed state; gun cooldown;
                         inventory; direction; attack damage multiplier; skin 
                         color; and image and rect attributes.
                                 
            PARAMETERS   A boolean value representing if the object is a player; 
                         the initial coordinates as a two-index tuple of integers;
                         the inventory as a four-index list of strings; and
                         the starting health as an integer.
        '''        
        # Initialize: call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        # Initialize: instance variables
        self.__isPlayer = isPlayer
        self.__maxHealth = health
        self.__currentHealth = health
        self.__selectBarSlot = selectBarSlot
        self.__isKilled = False
        self.__framesInKilled = 0
        self.__gunCooldown = 0
        self.__inventory = [inventory[0], inventory[1], inventory[2], inventory[3]]
        self.__directionRad = 0
        self.__attackDamageMultiplier = attackDamageMultiplier
        self.__defaultSkinColor = (200, 200, 200)
        
        if self.__isPlayer:
            self.__entityColor = PLAYER_COLOR
        else:
            self.__entityColor = BOT_COLOR
            
        # Initialize: the object's actual dimensions
        self.resetDimensions()
        self.createImageComponents()
        
        # Initialize: relative held positions
        self.__gunPos = (self.__actualHitbox[0] / 2 + 36, self.__actualHitbox[1] / 2 - 5)
        self.__utilPos = (self.__actualHitbox[0] / 2 + 48, self.__actualHitbox[1] / 2 + 4)
        self.__boostPos = (self.__actualHitbox[0] / 2 + 48, self.__actualHitbox[1] / 2 - 14)
        
        # Initialize: the image and rect attributes for the empty Entity object
        # (original hitbox)
        if self.__isPlayer:
            self.updateImage()
            
            self.rect = self.image.get_rect()
            self.rect.centerx = initialCoord[0]
            self.rect.centery = initialCoord[1]
        else:
            self.rect = self.image.get_rect()
            self.rect.centerx = initialCoord[0]
            self.rect.centery = initialCoord[1]
            
            self.updateImage()
            
    def resetDimensions(self, HITBOX_SIDE_LENGTH = 288):
        '''  SYNTAX   object.resetDimensions()
           
            PURPOSE   To reset the object's image component dimensions and
                      start its image anew.
        '''
        self.__actualHitbox = (HITBOX_SIDE_LENGTH, HITBOX_SIDE_LENGTH)
        self.image = pygame.Surface(self.__actualHitbox).convert()
        self.image.set_colorkey((0, 0, 0))
        
        # Initialize: relative arm positions
        self.__relativeStartBaseX = self.__actualHitbox[0] / 2 - 41
        self.__relativeStartBaseY = self.__actualHitbox[1] / 2 - 41
        
        self.__relativeStartLArmX = self.__actualHitbox[0] / 2 + 13
        self.__relativeStartLArmY = self.__actualHitbox[1] / 2 - 41
        
        self.__relativeStartRArmX = self.__actualHitbox[0] / 2 + 13
        self.__relativeStartRArmY = self.__actualHitbox[1] / 2 + 15
        
    def genComponentExplodeVectors(self):
        '''  SYNTAX   object.genComponentExplodeVectors()
        
            PURPOSE   Used for animating the object's death by moving its
                      components in a deathly fashion. This function handles
                      with creating the deathly fashion.
        '''
        self.__vectorHeld = random.uniform(-math.pi, math.pi)
        self.__vectorBase = random.uniform(-math.pi, math.pi)
        self.__vectorLArm = random.uniform(-math.pi, math.pi)
        self.__vectorRArm = random.uniform(-math.pi, math.pi)
        
    def animateDeath(self, framesInDeath, FRAMES_UNTIL_STOP = 30, \
                     MAXIMUM_FRAME_DISPLACEMENT = 12):
        '''  SYNTAX   object.animateDeath()
        
            PURPOSE   Used for animating the object's death by moving its
                      components in a deathly fashion. This function handles
                      with visually updating the deathly fashion.
        '''
        # Change: in left arm position (tuple)
        changeInLArm = (math.sin(self.__vectorLArm) * ( \
            FRAMES_UNTIL_STOP - framesInDeath) / MAXIMUM_FRAME_DISPLACEMENT, math.cos( \
                self.__vectorLArm) * (FRAMES_UNTIL_STOP - framesInDeath) / \
                        MAXIMUM_FRAME_DISPLACEMENT)
        
        # Change: in right arm position (tuple)
        changeInRArm = (math.sin(self.__vectorRArm) * ( \
            FRAMES_UNTIL_STOP - framesInDeath) / MAXIMUM_FRAME_DISPLACEMENT, math.cos( \
                self.__vectorRArm) * (FRAMES_UNTIL_STOP - framesInDeath) / \
                        MAXIMUM_FRAME_DISPLACEMENT)
        
        # Change: in base position (tuple)
        changeInBase = (math.sin(self.__vectorBase) * ( \
            FRAMES_UNTIL_STOP - framesInDeath) / MAXIMUM_FRAME_DISPLACEMENT, math.cos( \
                self.__vectorBase) * (FRAMES_UNTIL_STOP - framesInDeath) / \
                        MAXIMUM_FRAME_DISPLACEMENT)        
        
        # Change: in held item position (tuple)
        changeInHeld = (math.sin(self.__vectorHeld) * ( \
            FRAMES_UNTIL_STOP - framesInDeath) / MAXIMUM_FRAME_DISPLACEMENT, math.cos( \
                self.__vectorHeld) * (FRAMES_UNTIL_STOP - framesInDeath) / \
                        MAXIMUM_FRAME_DISPLACEMENT)             

        # Restrict Frames in Death
        if framesInDeath > FRAMES_UNTIL_STOP:
            changeInLArm, changeInRArm, changeInBase, changeInHeld = \
                (0, 0), (0, 0), (0, 0), (0, 0)
        
        # Update Arm, Base, and Held Locations
        self.updateInitImage()
        self.updateBaseLoc(changeInBase)
        self.updateHeldLoc(changeInHeld)
        self.updateArmLoc(False, changeInLArm[0], changeInLArm[1], changeInRArm[0], \
                          changeInRArm[1])
        self.equipHeldItemVisual()
        
        # Retain Faced Angle
        self.image = pygame.transform.rotate(self.getInitImage(), math.degrees(self.getDirectionRad()))
        self.rect = self.image.get_rect(center = self.rect.center)
        self.image.get_rect(center = self.rect.center)       
        
    def generateFrontPoint(self, isPlayer, distanceInFront, RAD90_VALUE = math.pi / 2.0):
        '''     SYNTAX   object.generateFrontPoint(isPlayer : bool, distanceInFront 
                         : float)
        
               PURPOSE   To generate the coordinates of a point distanceInFront
                         units in front of the object.
                        
            PARAMETERS   A boolean value expressing if it comes from the player
                         or not; a float value representing the distance in front of
                         the object.
                         
                RETURN   An (x, y) tuple of integers representing the coordinates 
                         of the point distanceInFront units in front of the object.
        '''
        if isPlayer:
            point = (int(round(self.rect.centerx + math.sin( \
                self.getDirectionRad() + RAD90_VALUE) * distanceInFront)), \
                     int(round(self.rect.centery + math.cos( \
                         self.getDirectionRad() + RAD90_VALUE) * \
                               distanceInFront)))
        else:
            point = (int(round(self.rect.centerx + math.cos( \
                self.getDirectionRad()) * distanceInFront)), \
                     int(round(self.rect.centery + math.sin( \
                         self.getDirectionRad()) * \
                               distanceInFront)))
            
        # Return: values
        return point
    
    def getFramesInKilled(self):
        '''  SYNTAX   object.getFramesInKilled()
        
            PURPOSE   Accessor Method: to get the object's frames in its killed
                      state.
        '''
        return self.__framesInKilled
    
    def setFramesInKilled(self, newFramesInKilled):
        '''     SYNTAX   object.setFramesInKilled(newFramesInKilled : int)
        
               PURPOSE   Mutator Method: to set the object's new frames in its
                         killed state.
              
            PARAMETERS   An integer representing the new frames in the object's
                         killed state.
        '''
        self.__framesInKilled = newFramesInKilled
        
    def updateFramesInKilled(self):
        '''  SYNTAX   object.updateFramesInKilled()
        
            PURPOSE   To update the frame count in the object's kill state.
        '''
        self.__framesInKilled += 1
        
    def getDirectionRad(self): 
        '''  SYNTAX   object.getDirectionRad()
        
            PURPOSE   Accessor Method: to get the object's faced direction
                      in radians.
        '''
        return self.__directionRad
    
    def setDirectionRad(self, newDirectionRad):
        '''     SYNTAX   object.getDirectionRad(newDirectionRad : float)
        
               PURPOSE   Mutator Method: to set the object's faced direction
                         in radians.
              
            PARAMETERS   The float value of the new faced direction of the object.
        '''
        self.__directionRad = newDirectionRad
        
    def createImageComponents(self):
        '''  SYNTAX   object.createImageComponents()
        
            PURPOSE   To initialize the images of the entity's components
                      including its base and arms.
        '''
        filePath = "images\\entity\\"
        
        # Create: image of entity base
        self.__imageBase = pygame.image.load(filePath + "image_EntityBase.png").convert()
        self.__imageBase.set_colorkey((255, 255, 255))
        pygame.PixelArray(self.__imageBase).replace(self.__defaultSkinColor, self.__entityColor)
        
        # Create: image of entity arms
        imageArm = pygame.image.load(filePath + "image_EntityArm.png").convert()
        imageArm.set_colorkey((255, 255, 255))
        pygame.PixelArray(imageArm).replace(self.__defaultSkinColor, self.__entityColor)
        
        self.__imageLArm = imageArm
        self.__imageRArm = imageArm
        
    def updateImage(self):
        '''  SYNTAX   object.updateImage()
        
            PURPOSE   To update the image so that it resets fully and
                      positioned so that items are automatically (visually)
                      equipped upon this unpdate function. This is not
                      the function to be used constantly, but rather
                      on occasion.
        '''
        self.resetDimensions()
        
        relativeStartBaseX = self.__relativeStartBaseX
        relativeStartBaseY = self.__relativeStartBaseY
        relativeStartLArmX = self.__relativeStartLArmX
        relativeStartLArmY = self.__relativeStartLArmY
        relativeStartRArmX = self.__relativeStartRArmX
        relativeStartRArmY = self.__relativeStartRArmY         
        
        # Set: the image attributes and relative body location for the object's base
        self.__relativeStartBase = (relativeStartBaseX, relativeStartBaseY)
        self.image.blit(self.__imageBase, self.__relativeStartBase)
        
        # Set: the image attributes and relative body location for the object's arms
        self.__relativeStartLArm = (relativeStartLArmX, relativeStartLArmY)
        self.image.blit(self.__imageLArm, self.__relativeStartLArm)
        
        self.__relativeStartRArm = (relativeStartRArmX, relativeStartRArmY)
        self.image.blit(self.__imageRArm, self.__relativeStartRArm)
        
        # Set: move the object's arms to the item its holding
        self.posArmsToItem()
        
        # Set: equip the item currently held
        self.equipHeldItemVisual()
        
        # Initialize: a copy of the initial image to refer to for effecient rotation purposes
        self.updateInitImage()

    def posArmsToItem(self):
        '''  SYNTAX   object.posArmsToImage()
        
            PURPOSE   To position the arms to match the object's held item.
        '''
        if self.getHeldItem() not in ["Unarmed", ""]:
            if "Gun_" in self.getHeldItem():
                if "Hand" in self.getHeldItem():
                    self.updateArmLoc(True, 12, 29, 25, -27)
                elif "Mach" in self.getHeldItem():
                    self.updateArmLoc(True, 12, 29, 37, -27)
                elif "Shot" in self.getHeldItem():
                    self.updateArmLoc(True, 12, 29, 39, -27)
                elif "Aslt" in self.getHeldItem():
                    self.updateArmLoc(True, 12, 29, 41, -27)
                elif "Snip" in self.getHeldItem():
                    self.updateArmLoc(True, 12, 29, 63, -27)
                elif "Rail" in self.getHeldItem():
                    self.updateArmLoc(True, 32, 15, 32, -15)                
            elif ("Util_" in self.getHeldItem()):
                self.updateArmLoc(True, 0, 0, 17, -8)
            elif ("Boost_" in self.getHeldItem()):
                self.updateArmLoc(True, 15, 9, 15, -9)
                
    def equipHeldItemVisual(self):
        '''  SYNTAX   object.equipHeldItemVisual()
        
            PURPOSE   To add an image of the item to the object's model, as
                      the object holds it.
        '''
        if self.getHeldItem() not in ["Unarmed", ""]:
            if "Gun_" in self.getHeldItem():
                # Held: gun
                filePath = "images\\entity\\"
                self.__imageHeldGun = pygame.image.load( \
                    filePath + "image_Held_" + self.getHeldItem() + ".png").convert()
                self.__imageHeldGun.set_colorkey((255, 255, 255))
                self.image.blit(self.__imageHeldGun, self.__gunPos)
                
            elif "Util_" in self.getHeldItem():
                # Held: utility
                filePath = "images\\entity\\"
                self.__imageHeldUtil = pygame.image.load( \
                    filePath + "image_HeldUtil.png").convert()
                self.__imageHeldUtil.set_colorkey((255, 255, 255))
                self.image.blit(self.__imageHeldUtil, self.__utilPos)
            
            elif "Boost_" in self.getHeldItem():
                # Held: boost
                filePath = "images\\item\\"
                self.__imageHeldBoost = pygame.image.load( \
                    filePath + "image_" + self.getHeldItem() + ".png").convert()
                self.__imageHeldBoost = pygame.transform.scale(self.__imageHeldBoost, (25, 25))
                self.__imageHeldBoost.set_colorkey((255, 255, 255))                 
                self.image.blit(self.__imageHeldBoost, self.__boostPos)
        
    def getHealth(self):
        '''  SYNTAX   object.getHealth()
                    
            PURPOSE   Accessor Method: to return the object's maximum health and
                      current health.
                  
             RETURN   The object's maximum health and current health, respectively
                      in a tuple.
        '''
        return (self.__maxHealth, self.__currentHealth)
        
    def getGunCooldown(self):
        '''  SYNTAX   object.getGunCooldown()
                    
            PURPOSE   Accessor Method: to return the object's gun cooldown.
                  
             RETURN   The object's gun cooldown as an integer.
        '''
        return self.__gunCooldown
    
    def canUseGun(self):
        '''  SYNTAX   object.canUseGun()
                    
            PURPOSE   Check if the object can use their gun.
                  
             RETURN   A boolean value expressing if the object can use their gun
                      or not based off of the gun's cooldown.
        '''
        return self.__gunCooldown == 0

    def getIsKilled(self):
        '''  SYNTAX   object.getIsKilled()
                    
            PURPOSE   Accessor Method: to return the object's killed state.
                  
             RETURN   The object's killed state as a boolean value.
        '''
        return self.__isKilled
    
    def setIsKilled(self, isKilled):
        '''     SYNTAX   object.setIsKilled(isKilled : bool)
        
               PURPOSE   Mutator Method: to set the object's killed state to a
                         new value.
                         
            PARAMETERS   The new killed state as a boolean value.
        '''
        self.__isKilled = isKilled 
    
    def takeDamage(self, damageValue):
        '''  SYNTAX   object.takeDamage(damageValue : int)
                            
            PURPOSE   Mutator Method: to negate a value, as damage, from the
                      current health. Also checks if the object is meant to be
                      killed.
        '''
        self.__currentHealth -= damageValue
        self.isKilled()
        
    def setMaxHealth(self, newMaxHealth):
        '''     SYNTAX   object.setMaxHealth(newMaxHealth : int)
        
               PURPOSE   Mutator Method: to set the object's max health to a new
                         value.
                         
            PARAMETERS   The new max health as an integer.
        '''
        self.__maxHealth = newMaxHealth
        
    def recoverHealth(self, healthValue):
        '''  SYNTAX   object.recoverHealth(healthValue : int)
                                    
            PURPOSE   Mutator Method: to recover a value, as health, from the
                      current health. This cannot exceed the object's max health.
         '''
        self.__currentHealth += healthValue
        if self.__currentHealth > self.__maxHealth:
            self.__currentHealth = self.__maxHealth
        
    def getInitImage(self):
        '''  SYNTAX   object.getInitImage()
            
            PURPOSE   Accessor Method: to return the object's current
                      initImage value.
                      
             RETURN   The object representing the sprite's initial image.
        '''
        return self.__initImage
    
    def getSelectBarSlot(self):
        '''  SYNTAX   object.getSelectBarSlot()
            
            PURPOSE   Accessor Method: to return the object's current
                      selectBarSlot value.
                      
             RETURN   An integer representing the sprite's currently selected 
                      slot. 
        '''
        return self.__selectBarSlot
    
    def getInventory(self):
        '''  SYNTAX   object.getInventory()
            
            PURPOSE   Accessor Method: to return the object's current
                      inventory list.
                      
             RETURN   A four-index tuple representing inventory slots, respectively.
        '''
        return self.__inventory       
    
    def getHeldItem(self):
        '''  SYNTAX   object.getHeldItem()
        
            PURPOSE   Accessor Method: to return the object's currently held item.
            
             RETURN   The name of the object's held item as a string.
        '''
        return self.__inventory[self.__selectBarSlot]
    
    def setGunCooldown(self, newGunCooldown):
        '''  SYNTAX   object.setGunCooldown(newGunCooldown : int)
            
            PURPOSE   Mutator Method: to set the object's gunCooldown
                      attribute to a new state with an integer number of frames.
                      The minimum value for this method is 1.
        '''
        if newGunCooldown < 1:
            newGunCooldown = 1
            
        self.__gunCooldown = newGunCooldown
        
    def updateGunCooldown(self):
        '''  SYNTAX   object.updateGunCooldown()
        
            PURPOSE   This function is expected to occur each frame. It updates
                      the cooldown in which the gun loads to.
        '''
        self.__gunCooldown -= 1
        
    def updateInitImage(self):
        '''  SYNTAX   object.updateInitImage()
            
            PURPOSE   Mutator Method: to set the object's initial image
                      attribute to its image.
        '''
        self.__initImage = self.image.copy()

    def setSelectBarSlot(self, slot):
        '''  SYNTAX   object.setSelectBarSlot(slot : int)
            
            PURPOSE   Mutator Method: to set the object's selectBarSlot
                      attribute to a new state.
        '''
        self.__selectBarSlot = slot
        
    def setInventorySlotItem(self, slot, itemName):
        '''  SYNTAX   object.setInventorySlotItem(slot : int, itemName : str)
            
            PURPOSE   Mutator Method: to set a slot in the object's 
                      inventory to have a specified item.
        '''
        self.__inventory[slot] = itemName
        
    def updateHeldLoc(self, changeBase):
        '''     SYNTAX   object.updateHeldLoc(changeBase : iter)
        
               PURPOSE   To change the starting location of the object's held
                         components. This function will affect all held components.
              
            PARAMETERS   The integer change in the base's X and Y coordinates, in 
                         two-index tuple.
        '''
        newGunX = self.__gunPos[0] + changeBase[0]
        newGunY = self.__gunPos[1] + changeBase[1]
        
        newUtilX = self.__utilPos[0] + changeBase[0]
        newUtilY = self.__utilPos[1] + changeBase[1]
        
        newBoostX = self.__boostPos[0] + changeBase[0]
        newBoostY = self.__boostPos[1] + changeBase[1]
        
        self.__gunPos = (newGunX, newGunY)
        self.__utilPos = (newUtilX, newUtilY)
        self.__boostPos = (newBoostX, newBoostY)
        
    def updateBaseLoc(self, changeBase):
        '''     SYNTAX   object.updateBaseLoc(changeBase : iter)
        
               PURPOSE   To change the starting location of the object's base 
                         component.
              
            PARAMETERS   The integer change in the base's X and Y coordinates, in 
                         two-index tuple.
        '''
        newBaseX = self.__relativeStartBase[0] + changeBase[0]
        newBaseY = self.__relativeStartBase[1] + changeBase[1]
        
        self.__relativeStartBase = (newBaseX, newBaseY)
        
    def updateArmLoc(self, relativeToOrigin, changeLArmX, changeLArmY, \
                     changeRArmX, changeRArmY):
        '''   SYNTAX   object.updateArmLoc(relativeToOrigin : bool, 
                       (changeLArmX : float, changeLArmY : float) : tuple, 
                       (changeRArmX : float, changeRArmY : float) : tuple)
        
             PURPOSE   Update the location of the Entity object's arms, to move 
                       relative to its displacement or original point. 
        '''
        # Initialize: the image and rect attributes for Player's surface
        retainedPosition = (self.rect.centerx, self.rect.centery)
        
        self.image = pygame.Surface(self.__actualHitbox)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        
        self.rect.center = retainedPosition        
        
        # Initialize: the image and rect attributes for Player's base
        self.image.blit(self.__imageBase, self.__relativeStartBase)
        
        # Initialize: the image and rect attributes for Player's arms
        if relativeToOrigin:
            self.__relativeStartLArm = (self.__relativeStartLArmX + changeLArmX, \
                                        self.__relativeStartLArmY + changeLArmY)
            self.__relativeStartRArm = (self.__relativeStartRArmX + changeRArmX, \
                                        self.__relativeStartRArmY + changeRArmY)
        else:
            self.__relativeStartLArm = (self.__relativeStartLArm[0] + changeLArmX, \
                                        self.__relativeStartLArm[1] + changeLArmY)
            self.__relativeStartRArm = (self.__relativeStartRArm[0] + changeRArmX, \
                                        self.__relativeStartRArm[1] + changeRArmY)            
        
        self.image.blit(self.__imageLArm, self.__relativeStartLArm)
        self.image.blit(self.__imageRArm, self.__relativeStartRArm)
        
        # Initial Image: as a copy
        self.updateInitImage()
        
    def getADMultiplier(self):
        '''  SYNTAX   object.getADMultiplier()
        
            PURPOSE   Accessor Method: to return the object's attack damage
                      multiplier.
                      
             RETURN   The object's attack damage multiplier as a float value.
        '''
        return self.__attackDamageMultiplier  
    
    def setADMultiplier(self, newADMultiplier):
        '''     SYNTAX   object.setADMultiplier(newADMultiplier : float)
        
               PURPOSE   Mutator Method: to set the object's attack damage
                         multiplier to a new value.
               
            PARAMETERS   An integer representing the new attack damage multiplier
                         of the object.
        '''
        self.__attackDamageMultiplier = newADMultiplier    
        
    def isKilled(self):
        '''  SYNTAX   object.isKilled()
        
            PURPOSE   Properly kill itself as a "killable" object, if it has
                      a current health of equal to or less than 0.
        '''
        if self.getHealth()[1] <= 0:
            self.setIsKilled(True)
            self.update()
    
class Player(Entity):
    '''     PURPOSE   Defines the sprite for the Player, as a class.
        
        INHERITANCE   The Entity class.
    '''
    def __init__(self, screen, inventory, selectBarSlot, health, attackDamageMultiplier, \
                 INITIAL_TOTAL_PUNCH_TIME = 3, INITIAL_WALK_SPEED = 12):
        '''     SYNTAX   object.Player(screen : obj, inventory : list, 
                         selectBarSlot : int, health : int, attackDamageMultiplier
                         : float)
                       
               PURPOSE   The main-character, the Player object, is meant to be
                         controlled by the player.
                             
                         Initializes the Player's feature usage and screen.
                                                  
            PARAMETERS   The screen object; the inventory list; the selected
                         bar slot; the starting health; and the attack damage
                         multiplier.
        '''               
        # Initialize: call the parent __init__() method
        Entity.__init__(self, True, (screen.get_width() / 2, screen.get_height() / 2), \
                        inventory, selectBarSlot, health, attackDamageMultiplier)
 
        # Initialize: instance variables to keep track of the Player object's
        # feature usage and screen
        self.__usedPunch = False
        self.__regenTime = 0
        self.__walkSpeed = INITIAL_WALK_SPEED
        self.__screen = screen
        
        # Initialize: extra punch attributes
        self.__damagePunch = 50
        self.__useLArmForPunch = True
        self.__timeInPunchCycle = 0
        self.setTotalPunchTime(INITIAL_TOTAL_PUNCH_TIME)
        
    def getWalkSpeed(self):
        '''  SYNTAX   object.getWalkSpeed()
        
            PURPOSE   Accessor Method: to return the object's walk speed.
                      
             RETURN   The object's walk speed as an integer.
        '''
        return self.__walkSpeed
    
    def getImpairedWalkSpeed(self):
        '''  SYNTAX   object.getImpairedWalkSpeed()
        
            PURPOSE   Accessor Method: to return the object's impaired walk speed.
                      
             RETURN   The object's impaired walk speed as an integer.
        '''
        return self.__walkSpeed / 5 + 1
        
    def setWalkSpeed(self, newWalkSpeed):
        '''     SYNTAX   object.setWalkSpeed(newWalkSpeed : int)
        
               PURPOSE   Mutator Method: to set the object's walk speed to a new
                         value.
               
            PARAMETERS   An integer representing the new walk speed value.
        '''
        self.__walkSpeed = newWalkSpeed
    
    def getRegenTimer(self):
        '''  SYNTAX   object.getRegenTimer()
        
            PURPOSE   Accessor Method: to return the object's regeneration timer.
                      
             RETURN   The object's regeneration timer as frames as an integer.
        '''
        return self.__regenTime
        
    def setRegenTimer(self, newRegenTime):
        '''     SYNTAX   object.setRegenTimer(newRegenTime : int)
        
               PURPOSE   Mutator Method: to set the object's regeneration timer 
                         to a new value.
               
            PARAMETERS   An integer representing the new regeneration time of
                         the object.
        '''
        self.__regenTime = newRegenTime
        
    def updateRegenTimer(self):
        '''  SYNTAX   object.updateRegenTimer()
        
            PURPOSE   To update the timer on the object's regeneration.
        '''
        self.__regenTime += 1
    
    def getPunchHitPoint(self):
        '''  SYNTAX   object.getPunchHitPoint()
            
            PURPOSE   Accessor Method: to return the object's current
                      punchHitPoint value.
                      
             RETURN   A two-index tuple of the coordinates representing the
                      (x, y) coordinates of the Player object's punch at its
                      highest point.
        '''
        return self.__punchHitPoint              
                
    def getUsedPunch(self):
        '''  SYNTAX   object.getUsedPunch()
            
            PURPOSE   Accessor Method: to return the object's current
                      usedPunch value.
                      
             RETURN   True if the user used their punch. Otherwise, False.
        '''
        return self.__usedPunch
    
    def setUsedPunch(self, state):
        '''  SYNTAX   object.setUsedPunch(state : bool)
            
            PURPOSE   Mutator Method: to set the object's usedPunch
                      attribute to a new state.
        '''
        self.__usedPunch = state 
        
    def isAtPunchPoint(self):
        '''  SYNTAX   object.isAtPunchPoint()
        
            PURPOSE   Used to check if the object's time in the punch cycle
                      matches the total punch time it takes to fully displace
                      the object's arm.
                      
            DETAILS   Usage is expected to happen when using the object's punch
                      hit point.
        '''
        state = self.getTimeInPunchCycle() == self.getTotalPunchTime()
        if state:
            self.setPunchHitPoint(self.getDirectionRad())
        return state
            
    def updateTimeInPunchCycle(self, FRAMES_PER_UPDATE = 1):
        '''  SYNTAX   object.updateTimeInPunchCycle()
        
            PURPOSE   To add '1' frame to the object's time in its current
                      punch cycle.
        '''
        self.__timeInPunchCycle += FRAMES_PER_UPDATE
        
    def setTimeInPunchCycle(self, timeInPunchCycle):
        '''     SYNTAX   object.setTimeInPunchCycle(timeInPunchCycle : int)
        
               PURPOSE   Mutator Method: to change the current setTimeInPunchCycle
                         attribute to a new value.
                        
            PARAMETERS   An integer representing the new time in the object's 
                         current punch cycle as frames.
        '''
        self.__timeInPunchCycle = timeInPunchCycle
        
    def setTotalPunchTime(self, totalPunchTime):
        '''     SYNTAX   object.setTotalPunchTime(totalPunchTime : int)
        
               PURPOSE   Mutator Method: to change the current totalPunchTime
                         attribute to a new value. Since totalPunchCycle is
                         a dependant variable of totalPunchTime, it must be
                         updated as well.
                        
            PARAMETERS   An integer representing the total time it takes for
                         the object's punch to occur.
        '''
        self.__totalPunchTime = totalPunchTime
        self.__totalPunchCycle = totalPunchTime * 2 - 1
    
    def setLArmForPunch(self, useLArmForPunch):
        '''     SYNTAX   object.setLArmForPunch(useLArmForPunch : bool)
        
               PURPOSE   Mutator Method: to change the current useLArmForPunch
                         attribute to a new value.
                        
            PARAMETERS   The new boolean value for if the object should use
                         their left arm or not for their punch.
        '''
        self.__useLArmForPunch = useLArmForPunch
        
    def setPunchHitPoint(self, radMatchScreen, RAD90_VALUE = math.pi / 2.0, \
                      RADIUS_TO_STRETCHED_PUNCH = 65):
        '''     SYNTAX   object.setPunchHitPoint(radMatchScreen : float)
        
               PURPOSE   Mutator Method: to change the current punchHitPoint
                         attribute to a new value.
                        
            PARAMETERS   A float value representing the radian value of the
                         player's facing direction on the screen.
        '''
        self.__punchHitPoint = (int(round(self.rect.centerx + math.sin( \
            radMatchScreen + RAD90_VALUE) * RADIUS_TO_STRETCHED_PUNCH)), \
                                int(round(self.rect.centery + math.cos( \
                                    radMatchScreen + RAD90_VALUE) * \
                                          RADIUS_TO_STRETCHED_PUNCH)))   
        
    def getLArmForPunch(self):
        '''  SYNTAX   object.getLArmForPunch()
        
            PURPOSE   Accessor Method: to return the object's current
                      useLArmForPunch attribute.
                      
             RETURN   A boolean value expressing if the object should use
                      their left arm for the following punch, or the right arm.
        '''
        return self.__useLArmForPunch
    
    def getPunchDamage(self):
        '''  SYNTAX   object.getPunchDamage()
        
            PURPOSE   Accessor Method: to return the object's current
                      damagePunch attribute.
                      
             RETURN   An integer representing the damage the object deals
                      when the object's punch has occurred.
        '''
        return int(round(self.__damagePunch * self.getADMultiplier()))
        
    def getTimeInPunchCycle(self):
        '''  SYNTAX   object.getTimeInPunchCycle()
        
            PURPOSE   Accessor Method: to return the object's current
                      timeInPunchCycle attribute.
                      
             RETURN   An integer representing the number of frames in that
                      the object has been punching for since its start.
        '''
        return self.__timeInPunchCycle
    
    def getPunchVectorPerFrame(self, MAX_PUNCHX_DISPLACEMENT = 35, \
                               MAX_PUNCHY_DISPLACEMENT = 25):
        '''  SYNTAX   object.getPunchVectorPerFrame()
        
            PURPOSE   Accessor Method: to return the object's current
                      punch vector, for both x and y, cut by the totalPunchTime
                      attribute.
                      
             RETURN   A tuple of floats, where each float value is the x and y
                      displacement, respectively, for each occuring punch frame.
                      It is expected that the maximum reach occurs at
                      totalPunchTime frames.
        '''
        return (float(MAX_PUNCHX_DISPLACEMENT) / self.__totalPunchTime, \
                float(MAX_PUNCHY_DISPLACEMENT) / self.__totalPunchTime)
    
    def getTotalPunchCycle(self):
        '''  SYNTAX   object.getTotalPunchCycle()
        
            PURPOSE   Accessor Method: to return the object's current
                      totalPunchCycle attribute.
                      
             RETURN   An integer representing the number of frames it takes
                      for a punch to fully occur, thus 1 cycle.
        '''
        return self.__totalPunchCycle
    
    def getTotalPunchTime(self):
        '''  SYNTAX   object.getTotalPunchTime()
        
            PURPOSE   Accessor Method: to return the object's current
                      totalPunchTime attribute.
                      
             RETURN   An integer representing the number of frames it takes
                      for an arm to be displaced for a "punch hit" to occur.
        '''
        return self.__totalPunchTime
        
    def resetPunch(self):
        '''  SYNTAX   object.resetPunch()
        
            PURPOSE   To reset all punch values if the object is currently
                      using a punch. This will reset the frames in the punch,
                      its boolean value, and the arm displacement.
        '''
        if self.getUsedPunch():
            self.setTimeInPunchCycle(0)
            self.setUsedPunch(False)
            self.updateArmLoc(True, 0, 0, 0, 0)
        
    def isHoldingGun(self):
        '''     SYNTAX   object.isHoldingGun()
        
               PURPOSE   To test if the Player object used their gun.
               
               DETAILS   This function is accompanied by the handling of mouse click-
                         hold.
            
                RETURN   The boolean value answering if the Player is currently
                         wielding a gun. When paired with the handling of mouse
                         click-hold, it answers if the Player used its gun in
                         the last frame.
        '''
        return "Gun_" in self.getHeldItem() 

    def faceCursor(self):
        '''   SYNTAX   object.faceCursor()
        
             PURPOSE   Rotate toward mouse cursor. 
        '''
        # Processing 1: find angle of the Player object to the cursor
        mouseX, mouseY = pygame.mouse.get_pos()
        vector = (float(mouseX - self.rect.centerx), \
                  float(mouseY - self.rect.centery))
        self.setDirectionRad(-math.atan2(vector[1], vector[0]))
        angleToCursor = math.degrees(self.getDirectionRad())
        
        # Processing 2: update the Player object to face cursor and manage the 
        # rect to stay in the center
        self.image = pygame.transform.rotate(self.getInitImage(), angleToCursor)
        self.rect = self.image.get_rect(center = self.rect.center)
        self.image.get_rect(center = self.rect.center)
            
    def restrictToBorder(self, playerHitboxRadius):
        '''  SYNTAX   object.restrictToBorder(playerHitboxRadius : int)
        
            PURPOSE   Restrict the player from leaving the border when possible.
            
             RETURN   Two boolean values representing True if restrictions were
                      made upon the respective axis, and False otherwise.
        '''
        restrictionsWereMadeX = False
        restrictionsWereMadeY = False
        
        # Player: Restrict: Y-position
        if self.rect.centery < playerHitboxRadius: 
            self.rect.centery = playerHitboxRadius
            restrictionsWereMadeX = True
        elif self.rect.centery > self.__screen.get_height() - playerHitboxRadius:
            self.rect.centery = self.__screen.get_height() - playerHitboxRadius
            restrictionsWereMadeX = True
        
        # Player: Restrict: X-position
        if self.rect.centerx < playerHitboxRadius: 
            self.rect.centerx = playerHitboxRadius
            restrictionsWereMadeY = True
        elif self.rect.centerx > self.__screen.get_width() - playerHitboxRadius:
            self.rect.centerx = self.__screen.get_width() - playerHitboxRadius
            restrictionsWereMadeY = True
            
        # Return: values
        return restrictionsWereMadeX, restrictionsWereMadeY
        
    def simulatePunch(self):
        '''   SYNTAX   object.simulatePunch()
        
             PURPOSE   Simulate the Player object's punch event for each given
                       frame.
        '''
        if self.getLArmForPunch():
           # Simulate Punch: in the left arm (LArm)
            if self.getTimeInPunchCycle() < self.getTotalPunchTime():
                self.updateArmLoc(False, self.getPunchVectorPerFrame()[0], \
                                          self.getPunchVectorPerFrame()[1], 0, 0)
            else:
                self.updateArmLoc(False, -self.getPunchVectorPerFrame()[0], \
                                          -self.getPunchVectorPerFrame()[1], 0, 0)
        else:
           # Simulate Punch: in the right arm (RArm)
            if self.getTimeInPunchCycle() < self.getTotalPunchTime():
                self.updateArmLoc(False, 0, 0, self.getPunchVectorPerFrame()[0], \
                                                  -self.getPunchVectorPerFrame()[1])
            else:
                self.updateArmLoc(False, 0, 0, -self.getPunchVectorPerFrame()[0], \
                                                  self.getPunchVectorPerFrame()[1]) 
    
    def update(self, REGENERATION_FRAME = 75):
        '''    SYNTAX   object.update()
        
              PURPOSE   Regenerate the object's health overtime and to update 
                        the killed state of the object and the angle its facing 
                        and to reduce the object's gun cooldown each frame upon usage.      
        '''
        if 0 < self.getHealth()[1] < self.getHealth()[0]:
            self.updateRegenTimer()
            if self.getRegenTimer() == REGENERATION_FRAME:
                self.recoverHealth(int(round(self.getHealth()[0] * 0.01)))
                self.setRegenTimer(0)
        self.faceCursor()
        if self.getGunCooldown():
            self.updateGunCooldown()
        if self.getIsKilled():
            if not self.getFramesInKilled():
                self.genComponentExplodeVectors()
            self.updateFramesInKilled()
            self.animateDeath(self.getFramesInKilled())
        
class Bot(Entity):
    '''     PURPOSE   Defines the sprite for the Bot, as a class.
        
        INHERITANCE   The Entity class.
    '''
    def __init__(self, screen, inventory, initialCoords, selectBarSlot, health, \
                 movementSpeed, AImode, radiusToPlayerCenter, attackDamageMultiplier):
        '''     SYNTAX   object.Bot(screen : obj, inventory : list, initialCoords 
                         : tuple, selectBarSlot : int, health : int, movementSpeed
                         : num, AImode : str, radiusToPlayerCenter : int,
                         attackDamageMultiplier : float)
                               
               PURPOSE   The Bot objects are meant to be the entities that
                         are AI-powered enemies made to defeat the Player.
                                     
                         Initializes the Bot's initial coordinates; health;
                         movement speed; stun timer; radius to Player center; 
                         AI mode; selected bar slot; and the attack damage
                         multiplier. Also, initializes special AI mode instance 
                         variables.
                                                          
            PARAMETERS   The screen object; the inventory list; the initial
                         coordinates as a tuple; the starting health as an integer; 
                         the starting movement speed as a number; the mode of AI 
                         as a string; the tracking of the Player's radius to 
                         its center; and the attack damage multiplier as a float
                         value.
        '''                       
        # Initialize: call the parent __init__() method
        Entity.__init__(self, False, (initialCoords[0], initialCoords[1]), \
                        inventory, selectBarSlot, health, attackDamageMultiplier)
        
        # Initialize: miscellaneous instance variables
        self.__screen = screen
        self.__movementSpeed = movementSpeed
        
        # Initialize: AI mode and radius to player.
        self.__radiusToPlayerCenter = radiusToPlayerCenter
        self.__AImode = AImode
        
        # Initiliaze: AI mode instance variables for unique movement
        self.__requiredRadius = random.uniform(5.5, 7.5)
        self.__uniqueModeTimer = random.randint(15, 75)
        self.__timerToNextMove = 0
        self.__framesInUniqueDirection = 0
        self.__stunTime = 0
        self.__vectorToPlayer = (0, 0)
        self.__newDirectionVector = (0, 0)
        self.__switchFactor = random.randint(1, 8)
        
    def moveWithAI(self):
        '''  SYNTAX   object.moveWithAI()
            
            PURPOSE   Based off the AI mode, the walking motion of the Bot
                      object will differ.
        '''
        if not (self.getStunTime() or self.getIsKilled()):
            # Bot objects: ranged type 1
            if "ranged1" in self.__AImode:
                if self.__framesInUniqueDirection:
                    # Ranged T1: unique movement to all other Bot objects
                    self.rect.centerx += int(round(math.cos(self.__temporaryVector[0]) * self.getMovementSpeed()))
                    self.rect.centery += int(round(math.sin(self.__temporaryVector[1]) * self.getMovementSpeed()))                   
                    self.__framesInUniqueDirection -= 1
                elif self.outsidePlayerRadius(self.__requiredRadius):
                    # Ranged T1: normal movement toward Player object
                    self.rect.centerx += int(round(math.cos(self.getDirectionRad()) * self.getMovementSpeed()))
                    self.rect.centery += int(round(math.sin(self.getDirectionRad()) * self.getMovementSpeed()))
                else:
                    # Ranged T1: when within the required range radius, set up for unique movement
                    self.__framesInUniqueDirection = self.__uniqueModeTimer * 3
                    
                    # Direction: to player
                    self.__temporaryVector = self.__vectorToPlayer
                    
            # Bot objects: ranged type 2
            if "ranged2" in self.__AImode: 
                if self.__framesInUniqueDirection:
                    # Ranged T2: unique movement to all other Bot objects
                    self.rect.centerx += int(round(math.cos(self.__randomDirectionRadians) * self.getMovementSpeed()))
                    self.rect.centery += int(round(math.sin(self.__randomDirectionRadians) * self.getMovementSpeed()))                   
                    self.__framesInUniqueDirection -= 1
                elif self.outsidePlayerRadius(self.__requiredRadius):
                    # Ranged T2: normal movement toward Player object
                    self.rect.centerx += int(round(math.cos(self.getDirectionRad()) * self.getMovementSpeed()))
                    self.rect.centery += int(round(math.sin(self.getDirectionRad()) * self.getMovementSpeed()))
                    self.__timerToNextMove = 0
                else:
                    # Ranged T2: when within the required range radius, set up for unique movement
                    self.__timerToNextMove += 1
                    if self.__timerToNextMove >= self.__uniqueModeTimer / self.__switchFactor:
                        self.__framesInUniqueDirection = self.__uniqueModeTimer
                        self.__timerToNextMove = 0
                        
                        # Direction: random
                        self.__randomDirectionRadians = random.uniform(-math.pi, math.pi)
                        
            # Bot objects: ranged type 3
            if "ranged3" in self.__AImode: 
                if self.__framesInUniqueDirection:
                    # Ranged T3: unique movement to all other Bot objects
                    self.rect.centerx += int(round(math.cos(self.__newDirectionVectorX) * self.getMovementSpeed()))
                    self.rect.centery += int(round(math.sin(self.__newDirectionVectorY) * self.getMovementSpeed()))                   
                    self.__framesInUniqueDirection -= 1
                elif self.outsidePlayerRadius(self.__requiredRadius):
                    # Ranged T3: normal movement toward Player object
                    self.rect.centerx += int(round(math.cos(self.getDirectionRad()) * self.getMovementSpeed()))
                    self.rect.centery += int(round(math.sin(self.getDirectionRad()) * self.getMovementSpeed()))
                    self.__timerToNextMove = 0
                else:
                    # Ranged T3: when within the required range radius, set up for unique movement
                    self.__timerToNextMove += 1
                    if self.__timerToNextMove >= self.__uniqueModeTimer / self.__switchFactor:
                        self.__framesInUniqueDirection = self.__uniqueModeTimer / 2
                        self.__timerToNextMove = 0
                        
                        # Direction: perpendicular
                        self.__newDirectionVectorX = self.__vectorToPlayer[1]
                        self.__newDirectionVectorY = self.__vectorToPlayer[0]
                        if random.randint(0, 1):
                            self.__newDirectionVectorX *= -1
                        else:
                            self.__newDirectionVectorY *= -1
            
    def outsidePlayerRadius(self, playerDiameterCount):
        '''     SYNTAX   object.outsidePlayerRadius(playerDiameterCount : int)
            
               PURPOSE   Check to see if the Bot object (self) is outside the
                         tracked range by the Player object's diameter count
                
            PARAMETERS   An integer representing the Bot's distance to the Player
                         in terms of the Player's base diameter.
                      
                RETURN   True if said condition is met. Otherwise, False.
        '''
        return (self.__vectorToPlayer[0] ** 2 + self.__vectorToPlayer[1] ** 2) ** 0.5 > \
               (2 * self.__radiusToPlayerCenter * playerDiameterCount)
    
    def getAIMode(self):
        '''  SYNTAX   object.getAIMode()
                
            PURPOSE   Accessor Method: to return the object's AI mode.
              
             RETURN   The object's AI mode as a string.
        '''
        return self.__AImode
    
    def getMovementSpeed(self):
        '''  SYNTAX   object.getMovementSpeed()
                
            PURPOSE   Accessor Method: to return the object's movement speed.
              
             RETURN   The object's movement speed as an integer.
        '''
        return self.__movementSpeed

    def setVectorToPlayer(self, vectorToPlayer):
        '''     SYNTAX   object.setVectorToPlayer(vectorToPlayer : tuple)
                       
               PURPOSE   Mutator Method: for the Bot object to keep track of the 
                         Player object's position.
                       
            PARAMETERS   The new vector to the Player object as an (x, y) tuple.
        '''
        self.__vectorToPlayer = vectorToPlayer
        
    def getStunTime(self):
        '''  SYNTAX   object.getStunTime()
                
            PURPOSE   Accessor Method: to return the object's stun time.
              
             RETURN   The object's stun time as an integer.
        '''
        return self.__stunTime
        
    def setStunTime(self, stunTime):
        '''     SYNTAX   object.setStunTime(stunTime : int)
                       
               PURPOSE   Mutator Method: to change the existing stun time on
                         the object to a new value.
                       
            PARAMETERS   The new stun time as an integer.
        '''
        self.__stunTime = stunTime
        
    def updateStunTime(self):
        '''  SYNTAX   object.updateStunTime()
                               
            PURPOSE   To update the object's stun time.
        '''
        self.__stunTime -= 1   
        
    def facePlayer(self, playerCurrent):
        '''   SYNTAX   object.facePlayer((playerCurrentX : int, playerCurrentY 
              : int) : tuple)
        
             PURPOSE   Rotate toward the player and to keep track of their
                       position. '''
        # Processing 1: find angle to and keep track of the Player object
        vector = (float(playerCurrent[0] - self.rect.centerx), \
                  float(playerCurrent[1] - self.rect.centery))
        self.setVectorToPlayer(vector)
        self.setDirectionRad(math.atan2(vector[1], vector[0]))
        angleToPlayer = -math.degrees(self.getDirectionRad())
        
        # Processing 2: turn Player to face cursor and manage rect to stay in the center
        self.image = pygame.transform.rotate(self.getInitImage(), angleToPlayer)
        self.rect = self.image.get_rect(center = self.rect.center)
        self.image.get_rect(center = self.rect.center)
        
    def isOnScreen(self):
        '''  SYNTAX   object.isOnScreen()
        
            PURPOSE   Check if this object can be seen on the screen.
        '''
        return ((self.rect.top < self.__screen.get_height() and self.rect.bottom > 0) \
                and (self.rect.left < self.__screen.get_width() and self.rect.right > 0))     
        
    def update(self, FRAMES_UNTIL_KILLED = 75):
        '''    SYNTAX   object.update()
        
              PURPOSE   To update the killed state of the object.        
        '''
        self.moveWithAI()
        if self.getGunCooldown():
            self.updateGunCooldown() 
        if self.getStunTime():
            self.updateStunTime()
        if self.getIsKilled():
            if not self.getFramesInKilled():
                self.genComponentExplodeVectors()
            self.updateFramesInKilled()
            self.animateDeath(self.getFramesInKilled())
            if self.getFramesInKilled() >= FRAMES_UNTIL_KILLED:
                self.kill()
        
class ItemDrop(pygame.sprite.Sprite):
    '''     PURPOSE   Defines the Item class.
            
        INHERITANCE   The Sprite class.
    '''
    def __init__(self, itemName, initialCoords, spawnedIn):
        '''     SYNTAX   object.Camera(itemName : str, initialCoords : tuple,
                         spawnedIn : bool)
                
               PURPOSE   The ItemDrop object is an interactive Player object
                         that holds an item.
                         
                         Initialize the object's held item, explode state and
                         vector and time, and the expiration timer.
                         
            PARAMETERS   The string name of the item; its initial coordinates
                         as a two-index tuple of integers (x, y); and a boolean
                         value expressing if it was spawned in or not.
        '''
        # Initialize: Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
                
        # Initialize: the image and rect attributes for the ItemDrop object
        filePath = "images\\item\\"
        
        self.image = pygame.image.load(filePath + "image_ItemDropBase.png").convert()
        self.image.set_colorkey((255, 255, 255))
        
        self.__imageItem = pygame.image.load(filePath + "image_" + itemName + ".png").convert()
        self.__imageItem.set_colorkey((255, 255, 255))
        self.__relativeStartBase = (self.image.get_width() / 2 - self.__imageItem.get_width() / 2, \
                                    self.image.get_height() / 2 - self.__imageItem.get_height() / 2)
        self.image.blit(self.__imageItem, self.__relativeStartBase)
        
        self.rect = self.image.get_rect()
        self.rect.centerx = initialCoords[0]
        self.rect.centery = initialCoords[1]
        
        # Initialize: the held item's name, explode status, explode vector, time
        # in explosion of the ItemDrop object, expiration timer
        self.__heldItem = itemName
        self.__hasExploded = False
        self.__explodeVector = (0, 0)
        self.__timeInExplosion = 0
        self.__expirationTimer = 1800
        
        # Explode: upon spawn
        if spawnedIn:
            self.castExplodeEffect()
        
    def getHeldItem(self):
        '''  SYNTAX   object.getHeldItem()
                        
            PURPOSE   Accessor Method: to return the object's held item.
                      
             RETURN   The object's held item as a string.
        '''
        return self.__heldItem     
        
    def getExploded(self):
        '''  SYNTAX   object.getExploded()
                
            PURPOSE   Accessor Method: to return the object's explode state.
              
             RETURN   The object's explode state.
        '''
        return self.__hasExploded      
        
    def castExplodeEffect(self, EXPLODE_SPEED = 5):
        '''    SYNTAX   object.explode()
                
              PURPOSE   Make the object cast an "explode" effect, in a direction. 
                        This is used as an aesthetic effect for item drops.
        '''        
        self.__hasExploded = True
        
        radian = random.uniform(-math.pi, math.pi)
        self.__explodeVector = (math.cos(radian) * EXPLODE_SPEED, math.sin(radian) * EXPLODE_SPEED)
        
    def update(self, EXPLODE_TIME = 50):
        '''    SYNTAX   object.update()
        
              PURPOSE   To update the object's location if the item were to
                        explode.
        '''
        # Explode Event
        if self.getExploded() and self.__timeInExplosion < EXPLODE_TIME:
            # Update: location based off a random radian (direction vector)
            self.rect.centerx += self.__explodeVector[0] * \
                ((EXPLODE_TIME - self.__timeInExplosion) / float(EXPLODE_TIME))
            self.rect.centery += self.__explodeVector[1] * \
                ((EXPLODE_TIME - self.__timeInExplosion) / float(EXPLODE_TIME))
            self.__timeInExplosion += 1
            
        elif self.__timeInExplosion >= self.__timeInExplosion:
            # Reset: explosion variables
            self.__hasExploded = False
            self.__timeInExplosion = 0
            
        # Expiration: after <self.__expirationTimer> frames
        if self.__expirationTimer:
            self.__expirationTimer -= 1
        else:
            self.kill()
    
class Camera(object):
    '''     PURPOSE   Defines the Camera class.
        
        INHERITANCE   The Object class.
    '''
    def __init__(self, screen, border, initialScrollSpeed):
        '''     SYNTAX   object.Camera(screen : obj, border : tuple, 
                         initialScrollSpeed : int)
        
               PURPOSE   The Camera object is meant to create the scrolling
                         effect of the game accompanied by the main loop. This
                         will follow the Player all around the map.
                             
                         Initializes the Camera's instance variables, such as its
                         screen object, border tuple, and initial scroll speed as an
                         integer.
                         
               DETAILS   It will only scroll and follow the Player object if the
                         Player is within the border coordinate fields. If the
                         screen reaches the border coordinate fields, the Camera
                         object will stop scrolling.
                         
                         This class is mainly accompanied by the main loop since
                         all objects move with the Camera object.
                         
                         A displacement vector will be used to keep track of
                         where the Camera is, relatively above the Player.
                                                  
            PARAMETERS   The screen object; the world border as a tuple of
                         integers; and the initial scrolling speed as an integer.
        '''
        # Initialize: instance variables
        self.__screen = screen
        self.__border = border
        self.__initialScrollSpeed = initialScrollSpeed
        self.__scrollSpeed = initialScrollSpeed
        self.__displacementVectorX = 0
        self.__displacementVectorY = 0
        
    def moveInDirection(self, newDirectionX = 0, newDirectionY = 0):
        '''   SYNTAX   moveInDirection()
        
             PURPOSE   To provide a top-down camera view of the game screen.
                       
             DETAILS   The returned vectors are expected to apply to all 
                       directly in-game objects, and are inverted. This provides
                       the illusion of a "scrolling camera" feature.
                       
              RETURN   Returns a tuple featuring movement float vectors in the 
                       inverted direction of player-controllable walking
                       and a tuple representing the net displacement vector.
        '''
        # Input: Keys pressed
        keyInput = pygame.key.get_pressed()
        
        # Handling: Inverted X, Y directions for movement keys pressed
        if keyInput[pygame.K_LEFT] or keyInput[pygame.K_a]:
            newDirectionX = self.__scrollSpeed
        elif keyInput[pygame.K_RIGHT] or keyInput[pygame.K_d]:
            newDirectionX = -self.__scrollSpeed
            
        if keyInput[pygame.K_UP] or keyInput[pygame.K_w]:
            newDirectionY = self.__scrollSpeed
        elif keyInput[pygame.K_DOWN] or keyInput[pygame.K_s]:
            newDirectionY = -self.__scrollSpeed
        
        # Handling: reduce the scrolling speed for diagonal directions
        if newDirectionX != 0 and newDirectionY != 0:
            newDirectionX = int(newDirectionX * 0.7)
            newDirectionY = int(newDirectionY * 0.7)
        
        # Return: values
        return (newDirectionX, newDirectionY), \
               (self.__displacementVectorX, self.__displacementVectorY)
    
    
    def updateDisplaceVector(self, newDirection):
        '''  SYNTAX   object.updateDisplaceVector(newDirection : tuple)
                    
            PURPOSE   Mutator Method: to update the Camera object's displacement
                      by its current, with the given newDirection tuple (x, y).
        '''
        self.__displacementVectorX += newDirection[0]
        self.__displacementVectorY += newDirection[1]       
        
    def setScrollSpeed(self, scrollSpeed):
        '''  SYNTAX   object.setScrollSpeed(scrollSpeed : float)
            
            PURPOSE   Mutator Method: to set the Camera object's scrollSpeed to
                      a new numeric value.
        '''
        self.__scrollSpeed = scrollSpeed
        
    def resetScrollSpeed(self):
        '''  SYNTAX   object.resetScrollSpeed()
            
            PURPOSE   To set the Camera object's scrollSpeed to the initial value.
        '''
        self.__scrollSpeed = self.__initialScrollSpeed 
    
class Terrain(pygame.sprite.Sprite):
    '''     PURPOSE   Defines the sprite for the Terrain, as a class.
        
        INHERITANCE   The Sprite class.
    '''
    def __init__(self, screen, terrainImageFile, health, initialCoords):
        '''     SYNTAX   object.Terrain(screen : obj, terrainImageFile : string, 
                         health : int, initialCoords : tuple)
                         
               PURPOSE   The Bot objects are meant to be the entities that
                         are AI-powered enemies made to defeat the Player.
                         
                         Initializes the Terrain's screen object, initial 
                         coordinates, image and rect attributes, and its health.
                         
            PARAMETERS   The screen object; image file of the type of terrain as 
                         a string; the health as an integer; and the initial 
                         coordinates as a tuple.
        '''               
        # Initialize: Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        # Initialize: the image and rect attributes for the Terrain object
        self.image = pygame.image.load("images\\terrain\\" + terrainImageFile)
        self.image.set_colorkey((255, 255, 255))
        
        self.rect = self.image.get_rect()
        self.rect.centerx = initialCoords[0]
        self.rect.centery = initialCoords[1]
        
        # Initialize: instance variables
        self.__maxHealth = health
        self.__currentHealth = health
        self.__isDestroyed = False
        self.__screen = screen
        
    def getHealth(self):
        '''  SYNTAX   object.getHealth()
                    
            PURPOSE   Accessor Method: to return the object's maximum health and 
                      current health.
                  
             RETURN   The object's maximum health and current health, respectively
                      in a tuple.
        '''
        return (self.__maxHealth, self.__currentHealth)
    
    def takeDamage(self, damageValue):
        '''  SYNTAX   object.takeDamage(damageValue : int)
                            
            PURPOSE   Mutator Method: to negate a value, as damage, from the
                      current health. Also checks if the object is meant to be
                      destroyed.
                          
             RETURN   The object's damage taken as an integer.
        '''
        self.__currentHealth -= damageValue
        self.isDestroyed()
        
    def getDestroyed(self):
        '''  SYNTAX   object.getDestroyed()
                    
            PURPOSE   Accessor Method: to return the object's destroyed state.
                  
             RETURN   The object's destroyed state as a boolean value.
        '''
        return self.__isDestroyed
        
    def isDestroyed(self):
        '''   SYNTAX   object.isDestroyed()
        
             PURPOSE   Properly kill itself as a "breakable" object, if it has
                       a current health of less than 0.
                       
             DETAILS   0.1 is a sentinel value for unbreakable Terrain objects.
        '''
        if self.__currentHealth < 0.1:
            self.__isDestroyed = True
            
    def isOnScreen(self):
        '''  SYNTAX   object.isOnScreen()
        
            PURPOSE   Check if this object can be seen on the screen.
        '''
        return ((self.rect.top < self.__screen.get_height() * 1.5 and self.rect.bottom > -self.__screen.get_width() * 0.5) \
                and (self.rect.left < self.__screen.get_width() * 1.5 and self.rect.right > -self.__screen.get_width() * 0.5))
    
class Stump(Terrain):
    '''     PURPOSE   Defines the sprite for the Stump, as a class.
        
        INHERITANCE   The Terrain class.
    '''
    def __init__(self, screen, initialCoords):
        '''     SYNTAX   object.Stump(screen : obj, initialCoords : tuple)
                                 
               PURPOSE   The Stump is a piece of terrain that slows the
                         Player if the Player ever walks over it.
                                 
                         This class is accompanied by the main loop.
                                 
                         Initializes the Stump's initial coordinates; 
                         image and rect attributes; and its health.
                                 
            PARAMETERS   The screen object and the initial coordinates as a tuple.
        '''                       
        # Initialize: call the parent __init__() method
        Terrain.__init__(self, screen, "image_TerrainStump.png", 200, initialCoords)
        
        # Initialize: the Crate object's frames before death
        self.__framesBeforeDeath = 1       

    def update(self):
        '''    SYNTAX   object.update()
        
              PURPOSE   To update the destroyed state of the object.        
        '''
        if self.getDestroyed():
            self.__framesBeforeDeath -= 1
            if self.__framesBeforeDeath <= 0:
                self.kill()
        
class Bush(Terrain):
    '''     PURPOSE   Defines the sprite for the Bush, as a class.
            
        INHERITANCE   The Terrain class.
    '''
    def __init__(self, screen, initialCoords):
        '''     SYNTAX   object.Stump(screen : obj, initialCoords : tuple)
                                 
               PURPOSE   The Bush is a piece of terrain that overlaps the Entity
                         objects in terms of layering. This is mainly used for
                         decoration purposes, though.
                                 
                         This class is accompanied by the main loop.
                                 
                         Initializes the Bush's initial coordinates; 
                         image and rect attributes; and its health.
                                 
            PARAMETERS   The screen object and the initial coordinates as a tuple.
        '''         
        # Initialize: call the parent __init__() method
        Terrain.__init__(self, screen, "image_TerrainBush.png", -0.1, initialCoords)
        
class Pebble(Terrain):
    '''     PURPOSE   Defines the sprite for the Pebble, as a class.
            
        INHERITANCE   The Terrain class.
    '''    
    def __init__(self, screen, initialCoords):
        '''     SYNTAX   object.Pebble(screen : obj, initialCoords : tuple)
                                 
               PURPOSE   The Pebble is a piece of terrain that is mainly used
                         for decoration purposes.
                                 
                         This class is accompanied by the main loop.
                                 
                         Initializes the Pebble's initial coordinates; 
                         image and rect attributes; and its health.
                                 
            PARAMETERS   The screen object and the initial coordinates as a tuple.
        '''         
        # Initialize: call the parent __init__() method
        Terrain.__init__(self, screen, "image_TerrainPebble.png", -0.1, initialCoords)
        
class Barrel(Terrain):
    '''     PURPOSE   Defines the sprite for the Barrel, as a class.
            
        INHERITANCE   The Terrain class.
    '''    
    def __init__(self, screen, initialCoords):
        '''     SYNTAX   object.Barrel(screen : obj, initialCoords : tuple)
                                 
               PURPOSE   The Barrel is a piece of terrain that can either explode
                         or deflect bullets.
                                 
                         This class is accompanied by the main loop.
                                 
                         Initializes the Barrel's initial coordinates; 
                         image and rect attributes; and its health.
                                 
            PARAMETERS   The screen object and the initial coordinates as a tuple.
        '''         
        # Initialize: call the parent __init__() method
        Terrain.__init__(self, screen, "image_TerrainBarrel.png", 500, initialCoords)
        
        # Initialize: the Crate object's frames before death
        self.__framesBeforeDeath = 1
        
    def update(self):
        '''    SYNTAX   object.update()
        
              PURPOSE   To update the destroyed state of the object.        
        '''
        if self.getDestroyed():
            self.__framesBeforeDeath -= 1
            if self.__framesBeforeDeath <= 0:
                self.kill() 
        
class Crate(Terrain):
    '''     PURPOSE   Defines the sprite for the Crate, as a class.
            
        INHERITANCE   The Terrain class.
    '''    
    def __init__(self, screen, initialCoords):
        '''     SYNTAX   object.Crate(screen : obj, initialCoords : tuple)
                                 
               PURPOSE   The Crate is a piece of terrain that drops items upon 
                         being broken.
                                 
                         This class is accompanied by the main loop.
                                     
                         Initializes the Crate's initial coordinates; 
                         image and rect attributes; its health.
                                 
            PARAMETERS   The screen object and the initial coordinates as a tuple.
        '''         
        # Initialize: call the parent __init__() method
        Terrain.__init__(self, screen, "image_TerrainCrate.png", 80, initialCoords)

        # Initialize: the Crate object's frames before death
        self.__framesBeforeDeath = 1
    
    def update(self):
        '''    SYNTAX   object.update()
        
              PURPOSE   To update the destroyed state of the object.        
        '''
        if self.getDestroyed():
            self.__framesBeforeDeath -= 1
            if self.__framesBeforeDeath <= 0:
                self.kill()
                
class Label(pygame.sprite.Sprite):
    '''     PURPOSE   Defines the sprite for the Label, as a class.
            
        INHERITANCE   The Sprite class.
    '''
    def __init__(self, screen, labelFontSize, relativeCoordY):
        '''     SYNTAX   object.Label(screen : obj, labelFontSize : int, 
                         relativeCoordY : int)
                                 
               PURPOSE   The Label is an ingame label to inform the player on
                         screen in present time.
                                 
                         This class is accompanied by the main loop.
                                 
            PARAMETERS   The screen object, the label font size as an integer,
                         and the relative Y integer coordinate.
        '''         
        # Initialize: call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)

        # Initialize: the label text
        self.__relativeCoordY = relativeCoordY
        self.__screen = screen
        self.__labelFont = pygame.font.Font( \
            "fonts\\pixelated_arial_bold_11.ttf", labelFontSize)
        self.__labelTextColor = (255, 255, 250)
        self.__text = ""
        self.__isShown = False
        self.image = self.__labelFont.render(self.__text, 0, self.__labelTextColor)
        self.rect = self.image.get_rect()  
        
    def showText(self):
        self.__isShown = True
        
    def hideText(self):
        self.__isShown = False
        
    def updateText(self, text):
        self.__text = text
        
    def updateColor(self, colors):
        self.__labelTextColor = (colors[0], colors[1], colors[2])
        
    def update(self):
        if self.__isShown:
            self.image = self.__labelFont.render(self.__text, 0, self.__labelTextColor)
        else:
            self.image = self.__labelFont.render("", 0, self.__labelTextColor)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.__screen.get_width() / 2
        self.rect.centery = self.__screen.get_height() / 2 - self.image.get_height() / 2 + \
            self.__relativeCoordY