#include "phylib.h"

//PART I:
phylib_object *phylib_new_still_ball(unsigned char number, phylib_coord *pos) {

    //Allocate memory for the new still ball
    phylib_object * still_ball = (phylib_object*)malloc(sizeof(phylib_object));

    if(still_ball == NULL) {
        return NULL;
    }

    //Set its type, number, and position according to function parameters
    still_ball->type = PHYLIB_STILL_BALL;
    still_ball->obj.still_ball.number = number;
    still_ball->obj.still_ball.pos = *pos;

    return still_ball;
}

phylib_object *phylib_new_rolling_ball(unsigned char number, phylib_coord *pos, phylib_coord *vel, phylib_coord *acc) {

    //Allocate memory for a new rolling ball
    phylib_object * rolling_ball = (phylib_object*)malloc(sizeof(phylib_object));

    if(rolling_ball == NULL) {
        return NULL;
    }

    //Set its type, number, position, velocity, and acceleration
    rolling_ball->type = PHYLIB_ROLLING_BALL;
    rolling_ball->obj.rolling_ball.number = number;
    rolling_ball->obj.rolling_ball.pos = *pos;
    rolling_ball->obj.rolling_ball.vel = *vel;
    rolling_ball->obj.rolling_ball.acc = *acc;

    return rolling_ball;
}

phylib_object *phylib_new_hole(phylib_coord *pos) {

    //Allocate memory for a new hole
    phylib_object * new_hole = (phylib_object*)malloc(sizeof(phylib_object));

    if(new_hole == NULL) {
        return NULL;
    }

    //Set its type and position according to function parameters
    new_hole->type = PHYLIB_HOLE;
    new_hole->obj.hole.pos = *pos;

    return new_hole;
}

phylib_object *phylib_new_hcushion(double y) {

    //Allocate memory for a new horizontal cushion
    phylib_object * new_hcushion = (phylib_object*)malloc(sizeof(phylib_object));

    if(new_hcushion == NULL) {
        return NULL;
    }

    //Set its type and position according to function parameters
    new_hcushion->type = PHYLIB_HCUSHION;
    new_hcushion->obj.hcushion.y = y;

    return new_hcushion;
}

phylib_object *phylib_new_vcushion(double x) {

    //Allocate memory for a new vertical cushion
    phylib_object * new_vcushion = (phylib_object*)malloc(sizeof(phylib_object));

    if(new_vcushion == NULL) {
        return NULL;
    }

    //Set its type and position according to function parameters
    new_vcushion->type = PHYLIB_VCUSHION;
    new_vcushion->obj.vcushion.x = x;

    return new_vcushion;
}

phylib_table *phylib_new_table(void) {

    //Allocate memory for a new table
    phylib_table * new_table = (phylib_table*)malloc(sizeof(phylib_table));

    if(new_table == NULL) {
        return NULL;
    }

    //Set the start time to 0.0
    new_table->time = 0.0;

    //Set up the cushions of the table
    new_table->object[0] = phylib_new_hcushion(0.0);
    new_table->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH);
    new_table->object[2] = phylib_new_vcushion(0.0);
    new_table->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH);

    //Create a placeholder coordinate to use for hole creation
    phylib_coord * hole_coord = (phylib_coord*)malloc(sizeof(phylib_coord));

    if(hole_coord == NULL) {
        return NULL;
    }

    //Create hole at (0,0)
    hole_coord->x = 0.0;
    hole_coord->y = 0.0;
    new_table->object[4] = phylib_new_hole(hole_coord);

    //Create hole at (0, 1350)
    hole_coord->y = PHYLIB_TABLE_WIDTH;
    new_table->object[5] = phylib_new_hole(hole_coord);

    //Create hole at (0, 2700)
    hole_coord->y = PHYLIB_TABLE_LENGTH;
    new_table->object[6] = phylib_new_hole(hole_coord);

    //Create hole at (1350, 0)
    hole_coord->x = PHYLIB_TABLE_WIDTH;
    hole_coord->y = 0.0;
    new_table->object[7] = phylib_new_hole(hole_coord);

    //Create hole at (1350, 1350)
    hole_coord->y = PHYLIB_TABLE_WIDTH;
    new_table->object[8] = phylib_new_hole(hole_coord);

    //Create hole at (1350, 2700)
    hole_coord->y = PHYLIB_TABLE_LENGTH;
    new_table->object[9] = phylib_new_hole(hole_coord);

    //Free the placeholder coordinate
    free(hole_coord);

    //Set the remaining items in the table to NULL for later use
    for(int i = 10; i < PHYLIB_MAX_OBJECTS; i++) {
        new_table->object[i] = NULL;
    }

    return new_table;
}

//PART II:
void phylib_add_object(phylib_table *table, phylib_object *object) {
    
    //Iterate through the table and find a NULL object pointer
    for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        if(table->object[i] == NULL) {
            //Set the NULL pointer to the object and leave the loop
            table->object[i] = object;
            break;
        }
    }
}

void phylib_free_table(phylib_table *table) {
    
    //Iterate through the table and free all non-NULL pointers
    for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
            if(table->object[i] != NULL) {
                free(table->object[i]);
            }
    }

    //After freeing all contents, free the table
    free(table);
}

phylib_coord phylib_sub(phylib_coord c1, phylib_coord c2) {

    //Placeholder coordinate for result
    phylib_coord sub_coord;

    //Subtract the x and y values and place them into the placeholder
    sub_coord.x = c1.x - c2.x;
    sub_coord.y = c1.y - c2.y;

    return sub_coord;
}

double phylib_dot_product(phylib_coord a, phylib_coord b) { 

    double dot_product;

    //Multiply the x and y values of each coordinate, then add the products
    dot_product = (a.x * b.x) + (a.y * b.y);

    return dot_product;
}

phylib_table *phylib_copy_table(phylib_table *table) {

    //Allocate memory for a new table
    phylib_table * new_table = (phylib_table*)malloc(sizeof(phylib_table));

    if(new_table == NULL) {
        return NULL;
    }

    //Copy over the time of the table
    new_table->time = table->time;

    //Iterate through the old table, if an object exists, copy it; otherwise, set the pointer to NULL
    for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        if(table->object[i] != NULL) {
            phylib_copy_object(&new_table->object[i], &table->object[i]);
        } else {
            new_table->object[i] = NULL;
        }
    }

    return new_table;
}

double phylib_length(phylib_coord c) { 

    //Square both the x and y values
    double x_square = c.x * c.x;
    double y_square = c.y * c.y;

    //Return the square root of the sum of both squares (Pythagorean theorem)
    return sqrt(x_square + y_square);
}

void phylib_copy_object(phylib_object **dest, phylib_object **src) {

    //If the source pointer is set to NULL, do the same for the destination
    if(src == NULL) {
        *dest = NULL;
    } else {
        //Otherwise, allocate memory for the new object and deep copy the memory over
        *dest = (phylib_object*)malloc(sizeof(phylib_object));

        memcpy(*dest, *src, sizeof(phylib_object));
    }
}

double phylib_distance(phylib_object *obj1, phylib_object *obj2) {

    //If the initial object isn't a rolling ball, return -1.0
    if(obj1->type != PHYLIB_ROLLING_BALL) {
        return -1.0;
    }

    double distance;
    double origin_distance;
    phylib_coord distance_coord;

    //Otherwise, check the type of the other object
    switch(obj2->type) {
        case (PHYLIB_STILL_BALL):
            //In the case of a still_ball, use the length less the radii of the balls
            distance_coord = phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.still_ball.pos);            
            distance = phylib_length(distance_coord) - (PHYLIB_BALL_RADIUS * 2);
            break;
        case (PHYLIB_ROLLING_BALL):
            //In the case of a rolling_ball, use the length less the radii of the balls
            distance_coord = phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.rolling_ball.pos);
            distance = phylib_length(distance_coord) - (PHYLIB_BALL_RADIUS * 2);
            break;
        case (PHYLIB_HOLE):
            //In the case of a hole, use the length less the radius of the hole
            distance_coord = phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.hole.pos);
            distance = phylib_length(distance_coord) - PHYLIB_HOLE_RADIUS;
            break;
        case (PHYLIB_HCUSHION):
            //In the case of a hcushion, use the absolute value of the proper coordinate, less the ball radius
            origin_distance = fabs(obj1->obj.rolling_ball.pos.y - obj2->obj.hcushion.y);
            distance = origin_distance - PHYLIB_BALL_RADIUS;
            break;
        case (PHYLIB_VCUSHION):
            //In the case of a vcushion, use the absolute value of the proper coordinate, less the ball radius
            origin_distance = fabs(obj1->obj.rolling_ball.pos.x - obj2->obj.vcushion.x);
            distance = origin_distance - PHYLIB_BALL_RADIUS;
            break;
        default:
            distance = -1.0;
    }

    return distance;
}

//PART III:
unsigned char phylib_stopped(phylib_object *object) {

    double x_value;
    double y_value;
    unsigned char number;

    //If the ball's speed is less than the epsilon, copy data and make it a still ball
    if(phylib_length(object->obj.rolling_ball.vel) < PHYLIB_VEL_EPSILON) {
        x_value = object->obj.rolling_ball.pos.x;
        y_value = object->obj.rolling_ball.pos.y;
        number = object->obj.rolling_ball.number;
        object->type = PHYLIB_STILL_BALL;
        object->obj.still_ball.number = number;
        object->obj.still_ball.pos.x = x_value;
        object->obj.still_ball.pos.y = y_value;
        return 1;
    } else {
        //Otherwise do nothing
        return 0;
    }
}

unsigned char phylib_rolling(phylib_table *t) {

    unsigned char count = 0;

    //Iterate through the table and increment count for all rolling_ball's
    for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        if(t->object[i] != NULL && t->object[i]->type == PHYLIB_ROLLING_BALL) {
            count++;
        }
    }

    return count;
}

double physics(double p, double v, double a, double t) {
    //Helper function to complete position update equation
    return p + (v * t) + (0.5 * a * (t * t));
}

int signCheck(double x) {
    //Helper function to check whether a number is positive or negative
    if(x <= 0) {
        return 0;
    } else {
        return 1;
    }
}

void phylib_roll(phylib_object *new, phylib_object *old, double time) {
    
    //Confirm both old and new are rolling balls, do nothing otherwise
    if(new->type == PHYLIB_ROLLING_BALL && old->type == PHYLIB_ROLLING_BALL) {

        //Copy position, velocity, and acceleration for simpler equations
        double p_x = old->obj.rolling_ball.pos.x;
        double p_y = old->obj.rolling_ball.pos.y;
        double v_x = old->obj.rolling_ball.vel.x;
        double v_y = old->obj.rolling_ball.vel.y;
        double a_x = old->obj.rolling_ball.acc.x;
        double a_y = old->obj.rolling_ball.acc.y;
        
        //Run the physics helper equation and simple velocity equation to update values
        new->obj.rolling_ball.pos.x = physics(p_x, v_x, a_x, time);
        new->obj.rolling_ball.pos.y = physics(p_y, v_y, a_y, time);
        new->obj.rolling_ball.vel.x = v_x + (a_x * time);
        new->obj.rolling_ball.vel.y = v_y + (a_y * time);

        //If the x velocity changed signs, set both the velocity and acceleration to 0.0
        if(signCheck(new->obj.rolling_ball.vel.x) != signCheck(v_x)) {
            new->obj.rolling_ball.vel.x = 0.0;
            new->obj.rolling_ball.acc.x = 0.0;
        }

        //If the y velocity changed signs, set both the velocity and acceleration to 0.0
        if(signCheck(new->obj.rolling_ball.vel.y) != signCheck(v_y)) {
            new->obj.rolling_ball.vel.y = 0.0;
            new->obj.rolling_ball.acc.y = 0.0;
        }
    }
}

void phylib_bounce(phylib_object **a, phylib_object **b) {

    unsigned char number;
    phylib_coord r_ab;

    //Assume (*a) is a rolling_ball, check the type of (*b)
    switch((*b)->type) {
        case (PHYLIB_HCUSHION):
            //If it hits a hcushion, flip the y-velocity and y-acceleration
            (*a)->obj.rolling_ball.vel.y = (*a)->obj.rolling_ball.vel.y * -1;
            (*a)->obj.rolling_ball.acc.y = (*a)->obj.rolling_ball.acc.y * -1;
            break;
        case (PHYLIB_VCUSHION):
            //If it hits a vcushion, flip the x-velocity and x-acceleration
            (*a)->obj.rolling_ball.vel.x = (*a)->obj.rolling_ball.vel.x * -1;
            (*a)->obj.rolling_ball.acc.x = (*a)->obj.rolling_ball.acc.x * -1;
            break;
        case (PHYLIB_HOLE):
            //If it hits a hole, free the ball and set it to NULL (ball's gone)
            free(*a);
            *a = NULL;
            break;
        case (PHYLIB_STILL_BALL):
            //If it hits a still_ball, update still_ball to rolling_ball and proceed to next case
            number = (*b)->obj.still_ball.number;
            double x = (*b)->obj.still_ball.pos.x;
            double y = (*b)->obj.still_ball.pos.y;
            phylib_coord not_moving_coord;
            not_moving_coord.x = 0.0;
            not_moving_coord.y = 0.0;
            (*b)->type = PHYLIB_ROLLING_BALL;
            (*b)->obj.rolling_ball.pos.x = x;
            (*b)->obj.rolling_ball.pos.y = y;
            (*b)->obj.rolling_ball.number = number;
            (*b)->obj.rolling_ball.acc = not_moving_coord;
            (*b)->obj.rolling_ball.vel = not_moving_coord;
            //Proceeding to next case with new rolling ball!
        case (PHYLIB_ROLLING_BALL):
            //If it hits a rolling_ball, run a lot of complicated physics to find new acceleration and velocity
            r_ab = phylib_sub((*a)->obj.rolling_ball.pos, (*b)->obj.rolling_ball.pos);
            phylib_coord v_rel = phylib_sub((*a)->obj.rolling_ball.vel, (*b)->obj.rolling_ball.vel);
            phylib_coord n;
            n.x = r_ab.x / phylib_length(r_ab);
            n.y = r_ab.y / phylib_length(r_ab);
            double v_rel_n = phylib_dot_product(v_rel, n);

            (*a)->obj.rolling_ball.vel.x -= v_rel_n * n.x;
            (*a)->obj.rolling_ball.vel.y -= v_rel_n * n.y;
            (*b)->obj.rolling_ball.vel.x += v_rel_n * n.x;
            (*b)->obj.rolling_ball.vel.y += v_rel_n * n.y;

            double a_speed = phylib_length((*a)->obj.rolling_ball.vel);
            double b_speed = phylib_length((*b)->obj.rolling_ball.vel);

            //If the speed is less than the epsilon, modify it
            if(a_speed > PHYLIB_VEL_EPSILON) {
                (*a)->obj.rolling_ball.acc.x = ((0.0 - (*a)->obj.rolling_ball.vel.x)/a_speed) * PHYLIB_DRAG;
                (*a)->obj.rolling_ball.acc.y = ((0.0 - (*a)->obj.rolling_ball.vel.y)/a_speed) * PHYLIB_DRAG;
            } else {
                (*a)->obj.rolling_ball.acc.x = a_speed;
                (*a)->obj.rolling_ball.acc.y = a_speed;
            }

            //If the speed is less than the epsilon, modify it
            if(b_speed > PHYLIB_VEL_EPSILON) {
                (*b)->obj.rolling_ball.acc.x = ((0.0 - (*b)->obj.rolling_ball.vel.x)/b_speed) * PHYLIB_DRAG;
                (*b)->obj.rolling_ball.acc.y = ((0.0 - (*b)->obj.rolling_ball.vel.y)/b_speed) * PHYLIB_DRAG;

            } else {
                (*b)->obj.rolling_ball.acc.x = b_speed;
                (*b)->obj.rolling_ball.acc.y = b_speed;
            }

            break;
    }
}

phylib_table *phylib_segment(phylib_table *table) {
    
    //If there are no rolling balls on the table, return NULL and free the copy
    if(phylib_rolling(table) == 0){
        return NULL;
    }

    int break_loop = 0;
    double time = PHYLIB_SIM_RATE;

    phylib_table * new_table = phylib_copy_table(table);

    while(time < PHYLIB_MAX_TIME) {

        //Iterate through the table and roll all rolling balls
        for(int x = 0; x < PHYLIB_MAX_OBJECTS; x++) {
            if(new_table->object[x] != NULL && new_table->object[x]->type == PHYLIB_ROLLING_BALL) {

                phylib_roll(new_table->object[x], table->object[x], time);

            }
        }

        //Check for loop end conditions after all rolls
        for(int y = 0; y < PHYLIB_MAX_OBJECTS; y++) {

            //If the object is a rolling ball, check for collisions or it being still
            if(new_table->object[y] != NULL && new_table->object[y]->type == PHYLIB_ROLLING_BALL) {

                for(int z = 0; z < PHYLIB_MAX_OBJECTS; z++) {

                    //Double check that object is not NULL due to balls falling off the table
                    if(new_table->object[y] != NULL) {
                        if(new_table->object[z] != NULL && y != z && phylib_distance(new_table->object[y], new_table->object[z]) <= 0.0) {

                            //If the distance between the ball and an object is less than 0.0, make a collision and break the time loop
                            //printf("%lf\n", phylib_distance(new_table->object[y], new_table->object[z]));
                            //printf("%d,%d\n", y, z);
                            phylib_bounce(&new_table->object[y], &new_table->object[z]);
                            break_loop = 1;
                            break;

                        }              
                    }
                }

                if(new_table->object[y] != NULL && phylib_stopped(new_table->object[y]) == 1) {

                    //If the ball has stopped, break the time loop
                    //printf("stopped break");
                    break_loop = 1;

                }
            }

            if(break_loop == 1){
                break;
            }
        }

        //Leave the loop if conditions are met
        if(break_loop == 1) {
            break;
        }

        time += PHYLIB_SIM_RATE;

    }

    new_table->time += time;

    return new_table;
}

char *phylib_object_string( phylib_object *object )
{
    static char string[80];
    if (object==NULL)
    {
        snprintf( string, 80, "NULL;" );
        return string;
    }
    
    switch (object->type)
        {
        case PHYLIB_STILL_BALL:
            snprintf( string, 80,
            "STILL_BALL (%d,%6.1lf,%6.1lf)",
            object->obj.still_ball.number,
            object->obj.still_ball.pos.x,
            object->obj.still_ball.pos.y );
            break;
        case PHYLIB_ROLLING_BALL:
            snprintf( string, 80,
            "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
            object->obj.rolling_ball.number,
            object->obj.rolling_ball.pos.x,
            object->obj.rolling_ball.pos.y,
            object->obj.rolling_ball.vel.x,
            object->obj.rolling_ball.vel.y,
            object->obj.rolling_ball.acc.x,
            object->obj.rolling_ball.acc.y );
            break;
        case PHYLIB_HOLE:
            snprintf( string, 80,
            "HOLE (%6.1lf,%6.1lf)",
            object->obj.hole.pos.x,
            object->obj.hole.pos.y );
            break;
        case PHYLIB_HCUSHION:
            snprintf( string, 80,
            "HCUSHION (%6.1lf)",
            object->obj.hcushion.y );
            break;
        case PHYLIB_VCUSHION:
            snprintf( string, 80,
            "VCUSHION (%6.1lf)",
            object->obj.vcushion.x );
            break;
        }

    return string;
}
