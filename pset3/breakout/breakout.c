//
// breakout.c
//
// Computer Science 50
// Problem Set 3
//

// standard libraries
#define _XOPEN_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

// Stanford Portable Library
#include <spl/gevents.h>
#include <spl/gobjects.h>
#include <spl/gwindow.h>

// height and width of game's window in pixels
#define HEIGHT 600
#define WIDTH 400

// number of rows of bricks
#define ROWS 5

// number of columns of bricks
#define COLS 10

// radius of ball in pixels
#define RADIUS 10

// lives
#define LIVES 3

//width and height of the paddle
#define PADDLE_HEIGHT 10
#define PADDLE_WIDTH  80

// prototypes
void initBricks(GWindow window);
GOval initBall(GWindow window);
GRect initPaddle(GWindow window);
GLabel initScoreboard(GWindow window);
void updateScoreboard(GWindow window, GLabel label, int points);
GObject detectCollision(GWindow window, GOval ball);

int main(void)
{
    // seed pseudorandom number generator
    srand48(time(NULL));

    // instantiate window
    GWindow window = newGWindow(WIDTH, HEIGHT);

    // instantiate bricks
    initBricks(window);

    // instantiate ball, centered in middle of window
    GOval ball = initBall(window);

    // instantiate paddle, centered at bottom of window
    GRect paddle = initPaddle(window);

    // instantiate scoreboard, centered in middle of window, just above ball
    GLabel label = initScoreboard(window);

    // number of bricks initially
    int bricks = COLS * ROWS;

    // number of lives initially
    int lives = LIVES;

    // number of points initially
    int points = 0;
    
    //initial velocity
    double  drand48(void);
    double velocity = 2 * drand48() + 1;
    double y_velocity = 3.0;
    // keep playing until game over
    while (lives > 0 && bricks > 0)
    {
        // TODO
        
        move(ball, velocity, y_velocity);
        if(getY(ball) + getWidth(ball) >= getHeight(window))
        {
            y_velocity = -y_velocity;
        }
        else if(getY(ball) <= 0)
        {
            y_velocity = -y_velocity;
        }
        
        if(getX(ball) + getWidth(ball) >= getWidth(window))
        {
            velocity = -velocity;
        }
        else if (getX(ball) <= 0)
        {
            velocity = -velocity;
        }
        pause(10);
        
        GObject object = detectCollision(window, ball);
        if (object == paddle)
        {
            y_velocity = -y_velocity;
            
        }
        if (object != NULL)
        {
          if (strcmp(getType(object), "GRect") == 0 && object != paddle)
          { 
            removeGWindow(window, object);
            y_velocity = -y_velocity;
            if(points <= 0)
                points = 0;
            points++;
            updateScoreboard(window, label, points);
          }
          else if (strcmp(getType(object), "GLabel") == 0)
          {
            continue;
          }  
        }
        GEvent event = getNextEvent(MOUSE_EVENT);
  
        if (event != NULL)
        {
            if (getEventType(event) == MOUSE_MOVED)
            {
                double x = getX(event) - (PADDLE_WIDTH / 2);
                setLocation(paddle, x, HEIGHT / 1.2);
            }
        }
        if (getY(ball) + getWidth(ball)  > getY(paddle) + PADDLE_HEIGHT)
        {
            lives--;
            setLocation(ball, WIDTH/2, HEIGHT/2); 
            move(ball, velocity, y_velocity);   
        }
        
     }


    // wait for click before exiting
    waitForClick();

    // game over
    closeGWindow(window);
    return 0;
}

/**
 * Initializes window with a grid of bricks.
 */
void initBricks(GWindow window)
{
    // TODO
    int x = 2;
    int y = 10;
    string color[5];
    color[0]="Red";
    color[1]="Blue";
    color[2]="Green";
    color[3]="Cyan";
    color[4]="Yellow";
    
    for (int rows = 0; rows < ROWS; rows++)
    {
        for(int cols =0; cols < COLS; cols++, x+=40)
        {
           GRect brick = newGRect(x, y, WIDTH/11, 10);
           setFilled(brick, true);
           setColor(brick, color[rows]);
           add(window, brick);
        }
        x = 2;
        y += 15;
    }
 
}

/**
 * Instantiates ball in center of window.  Returns ball.
 */
GOval initBall(GWindow window)
{
    // TODO
    int ball_diameter = 20;
    int ball_x = ((WIDTH / 2) - (ball_diameter / 2));
    int ball_y = ((HEIGHT / 2) - (ball_diameter / 2));
    GOval ball = newGOval(ball_x, ball_y, ball_diameter, ball_diameter);
    setFilled(ball, true);
    setColor(ball, "Yellow");
    add(window, ball);
    return ball;
}

/**
 * Instantiates paddle in bottom-middle of window.
 */
GRect initPaddle(GWindow window)
{
    // TODO
    double x = (getWidth(window) -  PADDLE_WIDTH)/2;
    double y = (getHeight(window)/1.2) - (PADDLE_HEIGHT/2);
   
    GRect paddle = newGRect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT);
    setColor(paddle, "Blue");
    setFilled(paddle, true);
    add(window, paddle);
    return paddle; 
}

/**
 * Instantiates, configures, and returns label for scoreboard.
 */
GLabel initScoreboard(GWindow window)
{
    // TODO
    GLabel label = newGLabel(" 0 ");
    setFont(label, "Times New Roman-20");
    double x = (getWidth(window) - getWidth(label)) / 2;
    double y = (getHeight(window) - getHeight(label)) / 2;
    setLocation(label, x, y);
    add(window, label);
    
    return label;
}

/**
 * Updates scoreboard's label, keeping it centered in window.
 */
void updateScoreboard(GWindow window, GLabel label, int points)
{
    // update label
    char s[12];
    sprintf(s, "%i", points);
    setLabel(label, s);

    // center label in window
    double x = (getWidth(window) - getWidth(label)) / 2;
    double y = (getHeight(window) - getHeight(label)) / 2;
    setLocation(label, x, y);
}

/**
 * Detects whether ball has collided with some object in window
 * by checking the four corners of its bounding box (which are
 * outside the ball's GOval, and so the ball can't collide with
 * itself).  Returns object if so, else NULL.
 */
GObject detectCollision(GWindow window, GOval ball)
{
    // ball's location
    double x = getX(ball);
    double y = getY(ball);

    // for checking for collisions
    GObject object;

    // check for collision at ball's top-left corner
    object = getGObjectAt(window, x, y);
    if (object != NULL)
    {
        return object;
    }

    // check for collision at ball's top-right corner
    object = getGObjectAt(window, x + 2 * RADIUS, y);
    if (object != NULL)
    {
        return object;
    }

    // check for collision at ball's bottom-left corner
    object = getGObjectAt(window, x, y + 2 * RADIUS);
    if (object != NULL)
    {
        return object;
    }

    // check for collision at ball's bottom-right corner
    object = getGObjectAt(window, x + 2 * RADIUS, y + 2 * RADIUS);
    if (object != NULL)
    {
        return object;
    }

    // no collision
    return NULL;
}
