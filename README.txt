First of all ,I created 2 robots and i have two global variables.
The scanning variable is for telling distance when the distance between Wall and robot is less then 0.75, otherwise it is 1. If the distance is less then 0.75 robot rotates,moves and rotates again.
Rotate count is to determine the rotation direction.
I am taking R1 and R2 from yaml file which are 3 and 2 robot keeps your robot running until it reaches the final point in while body.
After that,I am calling movetask.The parameters of this function are the distance between Wall and robot, rotate direction and R value.
I give the variable values. I set the distance to 0.4 because After moving the robot, when it's done, I check its distance from the Wall.
If the scan value is less bigger than 0.75 , it moves forward otherwise, it moved up to the Wall.
If the modulo of the rotate direction we give is 0, it turns right, then it moves as much as the R value, that is, 3 units, then turns right again. If the modulo of the rotate direction we give is 1, it turns left, then it moves 3 units, then turns left again.At the end of two if body, we set the scanning value is to .
Because the callback of laser scan When it approaches the wall, it makes the global scanning variable less than 0.75. Since I am sending this variable to movetask as a parameter, I need to set a value greater than 0.75 for it to work correctly.
After that, I repeat the same process to second robot and task2 is finished.
In my launch file, firstly i indroduce my yaml file.Then,To run World file, I define the path of the world file.
Finally, I write the required line to run the python file and I write the distance that the robot goes as horizontally in yaml file.