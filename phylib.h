//Constants
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

#define PHYLIB_BALL_RADIUS      (28.5) //mm
#define PHYLIB_BALL_DIAMETER    (2*PHYLIB_BALL_RADIUS)

#define PHYLIB_HOLE_RADIUS      (2*PHYLIB_BALL_DIAMETER)
#define PHYLIB_TABLE_LENGTH     (2700.0) //mm
#define PHYLIB_TABLE_WIDTH      (PHYLIB_TABLE_LENGTH/2.0) //mm

#define PHYLIB_SIM_RATE         (0.0001) //s
#define PHYLIB_VEL_EPSILON      (0.01) //mm/s^2

#define PHYLIB_DRAG             (150.0) //mm/s
#define PHYLIB_MAX_TIME         (600) //s

#define PHYLIB_MAX_OBJECTS      (26)

//Polymorphic object types
typedef enum {
    PHYLIB_STILL_BALL = 0,
    PHYLIB_ROLLING_BALL = 1,
    PHYLIB_HOLE = 2,
    PHYLIB_HCUSHION = 3,
    PHYLIB_VCUSHION = 4,
} phylib_obj;

//Class representing 2-dimension vector
typedef struct {
    double x;
    double y;
} phylib_coord;

//Child class representing table objects
typedef struct {
    unsigned char number;
    phylib_coord pos;
} phylib_still_ball;

typedef struct {
    unsigned char number;
    phylib_coord pos;
    phylib_coord vel;
    phylib_coord acc;
} phylib_rolling_ball;

typedef struct {
    phylib_coord pos;
} phylib_hole;

typedef struct {
    double y;
} phylib_hcushion;

typedef struct {
    double x;
} phylib_vcushion;

//Polymorphic parent class of table objects
typedef union {
    phylib_still_ball still_ball;
    phylib_rolling_ball rolling_ball;
    phylib_hole hole;
    phylib_hcushion hcushion;
    phylib_vcushion vcushion;
} phylib_untyped;

typedef struct {
    phylib_obj type;
    phylib_untyped obj;
} phylib_object;

//Table
typedef struct {
    double time;
    phylib_object * object[PHYLIB_MAX_OBJECTS];
} phylib_table;

/*
*
*   Allocates memory for a new phylib_object,
*   set its type to PHYLIB_STILL_BALL, and
*   transfer parameter data. Returns a pointer
*   to the phylib_object.
*
*/
phylib_object *phylib_new_still_ball(unsigned char number, phylib_coord *pos);

/*
*
*   Does the same as the previous function, but
*   with a rolling ball.
*
*/
phylib_object *phylib_new_rolling_ball( unsigned char number,
                                        phylib_coord *pos,
                                        phylib_coord *vel,
                                        phylib_coord *acc);

/*
*
*   Does the same as the previous function, but
*   with a hole.
*
*/
phylib_object *phylib_new_hole(phylib_coord *pos);

/*
*
*   Does the same as the previous function, but
*   with a new horizontal cushion.
*
*/
phylib_object *phylib_new_hcushion(double y);

/*
*
*   Does the same as the previous function, but
*   with a new vertical cushion.
*
*/
phylib_object *phylib_new_vcushion(double x);

/*
*
*   This function allocates memory for a new table
*   structure, sets the time to 0.0, and assigns the
*   values of its array elements to pointers to new objects.
*   The order of adding is: HCUSHION, HCUSHION, VCUSHION,
*   VCUSHION, 6 holes, and the remaining will be set to NULL.
*
*/
phylib_table *phylib_new_table(void);

/*
 * This function should allocate new memory for a phylib_object. Save the address of that
 * object at the location pointed to by dest, and copy over the contents of the object from the
 * location pointed to by src. Hint, you can use memcpy to make this a one-step operation that
 * works for any type of phylib_object. If src points to a location containing a NULL pointer,
 * then the location pointed to by dest should be assigned the value of NULL.
 */
void phylib_copy_object(phylib_object **dest, phylib_object **src);

/*
 * This function should allocate memory for a new phylib_table, returning NULL if the malloc
 * fails. Then the contents pointed to by table should be copied to the new memory location and
 * the address returned.
 */
phylib_table *phylib_copy_table(phylib_table *table);

/*
 * This function should iterate over the object array in the table until it finds a NULL pointer. It
 * should then assign that pointer to be equal to the address of object. If there are no NULL
 * pointers in the array, the function should do nothing.
 */
void phylib_add_object(phylib_table *table, phylib_object *object);

/*
 * This function should free every non- NULL pointer in the object array of table. It should then
 * also free table as well.
 */
void phylib_free_table(phylib_table *table);

/*
 * This function should return the difference between c1 and c2. That is the result’s x value
 * should be c1.x-c2.x and similarly for y.
 */
phylib_coord phylib_sub(phylib_coord c1, phylib_coord c2);

/*
 * This function should return the length of the vector/coordinate c. You can calculate this length
 * by using Pythagorean theorem. Important, you must not use the exp function from the math
 * library. That function is designed for raising values to a real power and is extremely inefficient
 * for something as simple as squaring a value.
 */
double phylib_length(phylib_coord c);

/*
 * This function should compute the dot-product between two vectors. Hint: the dot product is
 * equal to the sum of: the product of the x-values and the product of the y-values.
 */
double phylib_dot_product(phylib_coord a, phylib_coord b);

/*
 * Assignment provides detailed outline unable to be typed here.
 */
double phylib_distance(phylib_object *obj1, phylib_object *obj2);

/*
 * This function updates a new phylib_object that represents the old phylib_object after it
 * has rolled for a period of time. If new and old are not PHYLIB_ROLLING_BALLs, then the
 * function should do nothing. Otherwise, it should update the values in new.
 */
void phylib_roll(phylib_object *new, phylib_object *old, double time);

/*
 * This function will check whether a ROLLING_BALL has stopped, and if it has, will convert it to a
 * STILL_BALL.
 */
unsigned char phylib_stopped(phylib_object *object);

/*
 * This function simulates the ball bouncing off several different phylib_object's.
 */
void phylib_bounce(phylib_object **a, phylib_object **b);

/*
 * This function should return the number of ROLLING_BALLS on the table.
 */
unsigned char phylib_rolling(phylib_table *t);

/*
 * This function should return a segment of a pool shot.
 */
phylib_table *phylib_segment(phylib_table *table);

/* 
 * Helper function for physics math.
 */
double physics(double p, double v, double a, double t);

/*
 * Helper function to check if signs match.
 */
int signCheck(double x);

/*
 * This function takes an object and turns it into a printable string.
 */
char *phylib_object_string(phylib_object *object);
