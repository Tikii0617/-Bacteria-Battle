# Game Development Guide: Catch Euglena

## Overview
"Catch Euglena" is an interactive biotech game where players use a joystick to control LED lights, influencing the movement of Euglena displayed on a computer screen. The game aims to teach basic principles of biotechnology and the effects of light on microbial behavior in a fun and engaging way.

## Objectives
- **Educational**: Introduce players to the concept of phototaxis in Euglena.
- **Interactive**: Use physical controls to influence digital simulations.
- **Competitive**: Challenge players to move more Euglena to their side of the screen within a set time frame.

## Game Setup

### Hardware Integration:
- Connect the joystick to the Arduino.
- Setup LEDs around the display area, connected to the Arduino.
- Position the camera to capture the entire display area where Euglena movements will be shown.

### Software Setup:
- Use [OpenCV](https://github.com/Tikii0617/-Bacteria-Battle/blob/main/Game.py.py) on the computer to process the images captured by the camera, identifying and counting the Euglena.
- Write [Arduino scripts](https://github.com/Tikii0617/-Bacteria-Battle/blob/main/Game.py.py) to read joystick movements and control LED behavior accordingly.

## Game Mechanics

### Starting the Game:
- Players calibrate the joystick and ensure the LEDs are functioning.
- The game begins with Euglena evenly distributed across the display.

### During the Game:
- Players manipulate the LEDs using the joystick, trying to attract Euglena to their side of the display.
- The game captures and processes images in real-time, displaying the current count and distribution of Euglena.

### Ending the Game:
- When the timer ends, the software calculates which side has more Euglena.
- Points are awarded based on the difference in Euglena count between the two sides.

## Scoring System
- Points are awarded for the number of Euglena moved to the player’s side.
- Additional bonuses can be given for maintaining a lead for consecutive rounds.

## Conclusion
This biotech game not only serves as an educational tool but also provides a platform for fun and competitive gameplay. By following this guide, you can create a similar game, adapting and expanding upon the design to suit different themes or more advanced biotechnological concepts.

## Video
[Catch Euglena](https://github.com/Tikii0617/-Bacteria-Battle/blob/main/VIDEO.mp4)


## Something Extra Has Been Tried (Physical or Coding)

### Additional Effort 1:
In our initial setup, we tried integrating both smartphone and computer cameras to capture the dynamic movement of Euglena from multiple angles. Despite these efforts, the rapid motion of the Euglena led to unclear images. After various trials, we discovered that a microcamera, with its superior frame rate and resolution, was most effective in clearly capturing the fast-moving Euglena, thus greatly enhancing our visual accuracy.

### Additional Effort 2:
Initially, we observed that Euglena did not respond significantly to the additional LED lighting under the strong illumination of the microscope. To address this, we covered the main light source. Furthermore, the LED light was diffused and not focused, which was ineffective for guiding the Euglena in a specific direction. Therefore, we experimented with different materials, including black foam and tape, to wrap around parts of the LED. This modification allowed the light to be more focused and directed, enhancing its effectiveness in guiding Euglena movement.

### Additional Effort 3:
When our code and equipment were functioning correctly, we noticed that the samples were not as active as in the morning experiments. The lack of activity in our samples made it difficult to capture meaningful data. To address this issue, we experimented with different samples, including various sample reagents, slides, and different types of slide covers.

### Team

Sanil Pandhare，Viacheslav，Rachel (Yaqing) Huo，Rui Mao，Dekyi
