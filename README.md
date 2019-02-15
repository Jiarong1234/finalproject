

## **My snake**

**Introduction：**

This is my EE 551 individual project| Author:Jiarong Xia

**Proposals：**

This project is to build a game named My snake. This puzzle game is very simple, through the keyboard user can control the direction of the snake to eat more eggs, then user can get higher scores. Provide a nice game experience and a good GUI.

 **Features:**
 
 * Welcome interface
 
 * Submit the username
 
 * Record the highest score
 
 * Graphic user interface
 
 * Keep running the game
 
 * Voice prompt
 
 
 **TODO:**
 
 * Create a login/username submit interface
 
 * Design the logical structure of the game:

   * Initial the length of the snake
   * Using the keyboard user can control the direction of the snake
   * When the snake touch the eggs, the length of the snake will extend.
   * When the length extend the score will increase
   
* Add feature: Voice prompt

* Add feature: Record the highest score
 
 **Logic:**
 
 * The resolution of the game interface is 640 * 480. The snake and the egg are made up of one or more square blocks of 20 * 20 pixels. There are total 32 * 24 points, which could use pygame.draw.rect to draw.
 * After initial the game, the length of the snake is 3 and egg is 1. The initial direction is right, we can use an array to represent the snake, every element in the array is the coordinate, the first element is the tail of the snake and the last element is the head.
 * When the game start, according to the current direction of the movement of the snake, Append the point in front of the direction of the snake to the end of the snake array, and then remove the snake tail. The snake's coordinate array is equivalent to moving one forward
 * When the snake eat the egg (the coordinate of the snake's head is equal to the egg), Then in the second point, the snake tail does not need to be removed, which has the effect of increasing the length of the snake; after the food is eaten, it is randomly placed in an empty position to generate another egg.
 * Change the direction of the snake through PyGame's event monitoring button
 * When the snake hits itself or the wall, then game over. When the snake head hits itself,  there is data in the snake coordinate array that repeats the coordinates of the snake head. When it hits the wall, the coordinates of the snake head exceed the boundary.
