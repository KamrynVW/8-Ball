import phylib
import math
import sqlite3
import os

################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS    = phylib.PHYLIB_BALL_RADIUS;
BALL_DIAMETER  = phylib.PHYLIB_BALL_DIAMETER;
HOLE_RADIUS    = phylib.PHYLIB_HOLE_RADIUS;
TABLE_LENGTH   = phylib.PHYLIB_TABLE_LENGTH;
TABLE_WIDTH    = phylib.PHYLIB_TABLE_WIDTH;
SIM_RATE       = phylib.PHYLIB_SIM_RATE;
VEL_EPSILON    = phylib.PHYLIB_VEL_EPSILON;
DRAG           = phylib.PHYLIB_DRAG;
MAX_TIME       = phylib.PHYLIB_MAX_TIME;
MAX_OBJECTS    = phylib.PHYLIB_MAX_OBJECTS;
FRAME_INTERVAL = 0.01;

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE", # 0
    "YELLOW", # 1
    "BLUE", # 2
    "RED", # 3 
    "PURPLE", # 4 
    "ORANGE", # 5 
    "GREEN", # 6
    "BROWN", # 7
    "BLACK", # 8
    "LIGHTYELLOW", # 9
    "LIGHTBLUE", # 10
    "PINK",             # no LIGHTRED # 11
    "MEDIUMPURPLE",     # no LIGHTPURPLE # 12
    "LIGHTSALMON",      # no LIGHTORANGE # 13
    "LIGHTGREEN", # 14
    "SANDYBROWN",       # no LIGHTBROWN  # 15
    ];

################################################################################
# SVG constants
HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="700" height="1375" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />""";
FOOTER = """</svg>\n""";

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;

################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall;

    def svg(self):
        string = """ <circle id="ball%d" cx="%d" cy="%d" r="%d" fill="%s" />\n"""% ( self.obj.still_ball.number, self.obj.still_ball.pos.x, self.obj.still_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.still_ball.number])
        return string

################################################################################
class RollingBall( phylib.phylib_object ):
    """
    Python RollingBall class.
    """

    def __init__( self, number, pos, vel, acc ):
        """
        Constructor function. Requires ball number, position (x,y), velocity,
        and acceleration as arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_ROLLING_BALL, 
                                       number, 
                                       pos, vel, acc, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = RollingBall;

    # add an svg method here
    def svg(self):
        string = """ <circle id="ball%d" cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.rolling_ball.number, self.obj.rolling_ball.pos.x, self.obj.rolling_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.rolling_ball.number])
        return string

################################################################################
class Hole( phylib.phylib_object ):
    """
    Python Hole class.
    """

    def __init__( self, pos ):
        """
        Constructor function. Requires position (x,y), as arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HOLE, 
                                       0, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = Hole;

    def svg(self):
        string = """ <circle cx="%d" cy="%d" r="%d" fill="black" />\n""" % (self.obj.hole.pos.x, self.obj.hole.pos.y, HOLE_RADIUS)
        return string

################################################################################
class HCushion( phylib.phylib_object ):
    """
    Python HCushion class.
    """

    def __init__( self, y ):
        """
        Constructor function. Requires y-value as argument.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HCUSHION, 
                                       0, 
                                       None, None, None, 
                                       0.0, y );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = HCushion;

    def svg(self):
        if(self.obj.hcushion.y == 0):
            string = """ <rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" % (-25)
        else:
            string = """ <rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" % (2700)

        return string

################################################################################
class VCushion( phylib.phylib_object ):
    """
    Python VCushion class.
    """

    def __init__( self, x ):
        """
        Constructor function. Requires x-value as argument.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_VCUSHION, 
                                       0, 
                                       None, None, None, 
                                       x, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = VCushion;

    def svg(self):
        if(self.obj.vcushion.x == 0):
            string = """ <rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" % (-25)
        else:
            string = """ <rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" % (1350)

        return string

################################################################################
class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    def roll( self, t ):
        new = Table();
        for ball in self:
            if isinstance( ball, RollingBall ):
                # create4 a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number,
                                        Coordinate(0,0),
                                        Coordinate(0,0),
                                        Coordinate(0,0) );             
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t );
                # add ball to table
                new += new_ball;          
            if isinstance( ball, StillBall ):
                # create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number,
                Coordinate( ball.obj.still_ball.pos.x,
                ball.obj.still_ball.pos.y ) );
                # add ball to table
                new += new_ball;   
        # return table
        return new;

    def svg(self):
        """
        Calls all svg() functions from objects within the table to
        create a pool interface.
        """

        string = HEADER

        # For all non-None objects in the table, add the .svg contents
        for object in self:
            if(object != None):
                string += object.svg()

        string += FOOTER

        return string

    def createFullTable(self):
        # Add cue ball
        pos = Coordinate(TABLE_WIDTH/2.0, TABLE_LENGTH - TABLE_WIDTH/2.0 )
        sb  = StillBall( 0, pos )

        self += sb

        # Ball 1
        pos = Coordinate(TABLE_WIDTH / 2.0, TABLE_WIDTH / 2.0)

        sb = StillBall( 1, pos )
        self += sb

        # Ball 2
        pos = Coordinate(TABLE_WIDTH/2.0 - (BALL_DIAMETER+4.0)/2.0,
                         TABLE_WIDTH/2.0 - math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0))
        sb = StillBall( 2, pos )
        self += sb

        # Ball 3
        pos = Coordinate(TABLE_WIDTH/2.0 + (BALL_DIAMETER+4.0)/2.0,
                         TABLE_WIDTH/2.0 - math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0))
        sb = StillBall( 3, pos )
        self += sb

        # Ball 4
        pos = Coordinate(TABLE_WIDTH/2.0 - 2 * (BALL_DIAMETER+4.0)/2.0, TABLE_WIDTH/2.0 - 2 * (math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0)))
        sb = StillBall(4, pos)
        self += sb

        # Ball 5
        pos = Coordinate(TABLE_WIDTH/2.0, TABLE_WIDTH/2.0 - 2 * (math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0)))
        sb = StillBall(5, pos)
        self += sb

        # Ball 6
        pos = Coordinate(TABLE_WIDTH/2.0 + 2 * (BALL_DIAMETER+4.0)/2.0, TABLE_WIDTH/2.0 - 2 * (math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0)))
        sb = StillBall(6, pos)
        self += sb

        # Ball 7
        pos = Coordinate(TABLE_WIDTH/2.0 - 3 * (BALL_DIAMETER+4.0)/2.0,
                         TABLE_WIDTH/2.0 - 3 * (math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0)))
        sb = StillBall(7, pos)
        self += sb

        # Ball 8
        pos = Coordinate(TABLE_WIDTH/2.0 - (BALL_DIAMETER+4.0)/2.0,
                         TABLE_WIDTH/2.0 - 3 * (math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0)))
        sb = StillBall(8, pos)
        self += sb

        # Ball 9
        pos = Coordinate(TABLE_WIDTH/2.0 + 3 * (BALL_DIAMETER+4.0)/2.0,
                         TABLE_WIDTH/2.0 - 3 * (math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0)))
        sb = StillBall(9, pos)
        self += sb

        # Ball 10
        pos = Coordinate(TABLE_WIDTH/2.0 + (BALL_DIAMETER+4.0)/2.0,
                         TABLE_WIDTH/2.0 - 3 * (math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0)))
        sb = StillBall(10, pos)
        self += sb

        # Ball 11
        pos = Coordinate(TABLE_WIDTH/2.0 - 4 * (BALL_DIAMETER+4.0)/2.0, TABLE_WIDTH/2.0 - 4 * (math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0)))
        sb = StillBall(11, pos)
        self += sb

        # Ball 12
        pos = Coordinate(TABLE_WIDTH/2.0 - 2 * (BALL_DIAMETER+4.0)/2.0, TABLE_WIDTH/2.0 - 4 * (math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0)))
        sb = StillBall(12, pos)
        self += sb

        # Ball 13
        pos = Coordinate(TABLE_WIDTH/2.0, TABLE_WIDTH/2.0 - 4 * (math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0)))
        sb = StillBall(13, pos)
        self += sb

        # Ball 14
        pos = Coordinate(TABLE_WIDTH/2.0 + 2 * (BALL_DIAMETER+4.0)/2.0, TABLE_WIDTH/2.0 - 4 * (math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0)))
        sb = StillBall(14, pos)
        self += sb

        # Ball 15
        pos = Coordinate(TABLE_WIDTH/2.0 + 4 * (BALL_DIAMETER+4.0)/2.0, TABLE_WIDTH/2.0 - 4 * (math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0)))
        sb = StillBall(15, pos)
        self += sb

    def createDemoTable(self):
        # Add cue ball
        pos = Coordinate(HOLE_RADIUS + 100, TABLE_LENGTH - (HOLE_RADIUS + 100))
        sb  = StillBall( 0, pos )

        self += sb

        # Ball 1
        pos = Coordinate(HOLE_RADIUS + 5, HOLE_RADIUS + 5)
        sb = StillBall(1, pos)

        self += sb

        # Ball 2
        pos = Coordinate(HOLE_RADIUS + 5, TABLE_LENGTH - (HOLE_RADIUS + 5))
        sb = StillBall(2, pos)

        self += sb

        # Ball 8
        pos = Coordinate(TABLE_WIDTH - (HOLE_RADIUS + 5), TABLE_LENGTH - (HOLE_RADIUS + 5))
        sb = StillBall(8, pos)

        self += sb

        # Ball 14
        pos = Coordinate(TABLE_WIDTH - (HOLE_RADIUS + 30), TABLE_WIDTH)
        sb = StillBall(14, pos)

        self += sb

        # Ball 15
        pos = Coordinate(HOLE_RADIUS + 30, TABLE_WIDTH)
        sb = StillBall(15, pos)

        self += sb

    def addCueBall(self):
        # Add cue ball
        pos = Coordinate(TABLE_WIDTH/2.0, TABLE_LENGTH - TABLE_WIDTH/2.0 )
        sb  = StillBall( 0, pos )

        self += sb

################################################################################
class Database ():

    def __init__(self, reset=False):
        if reset is True:
            if os.path.exists('phylib.db'):
                os.remove('phylib.db')

        self.conn = sqlite3.connect('phylib.db')

    def createDB(self):
        cursor = self.conn.cursor()
        # Ball table creation
        cursor.execute("""  CREATE TABLE IF NOT EXISTS Ball (
                            BALLID      INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            BALLNO      INTEGER NOT NULL,
                            XPOS        FLOAT NOT NULL,
                            YPOS        FLOAT NOT NULL,
                            XVEL        FLOAT,
                            YVEL        FLOAT); """)

        # TTable table creation
        cursor.execute("""  CREATE TABLE IF NOT EXISTS TTable (
                            TABLEID     INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            TIME        FLOAT NOT NULL); """)

        # BallTable table creation
        cursor.execute("""  CREATE TABLE IF NOT EXISTS BallTable (
                            BALLID      INTEGER,
                            TABLEID     INTEGER,
                            FOREIGN KEY (BALLID) REFERENCES Ball(BALLID),
                            FOREIGN KEY (TABLEID) REFERENCES TTable(TABLEID)); """)

        # Game table creation
        cursor.execute("""  CREATE TABLE IF NOT EXISTS Game (
                            GAMEID      INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            GAMENAME    VARCHAR(64) NOT NULL); """)

        # Player table creation
        cursor.execute("""  CREATE TABLE IF NOT EXISTS Player (
                            PLAYERID    INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            GAMEID      INTEGER NOT NULL,
                            PLAYERNAME  VARCHAR(64) NOT NULL,
                            FOREIGN KEY (GAMEID) REFERENCES Game(GAMEID)); """)

        # Shot table creation
        cursor.execute("""  CREATE TABLE IF NOT EXISTS Shot (
                            SHOTID      INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            PLAYERID    INTEGER NOT NULL,
                            GAMEID      INTEGER NOT NULL,
                            FOREIGN KEY (GAMEID) REFERENCES Game(GAMEID),
                            FOREIGN KEY (PLAYERID) REFERENCES Player(PLAYERID)); """)

        # TableShot table creation
        cursor.execute("""  CREATE TABLE IF NOT EXISTS TableShot (
                            TABLEID     INTEGER NOT NULL,
                            SHOTID      INTEGER NOT NULL,
                            FOREIGN KEY (TABLEID) REFERENCES TTable(TABLEID),
                            FOREIGN KEY (SHOTID) REFERENCES Shot(SHOTID)); """)
        
        # self.conn.commit()
        cursor.close()

    def readTable(self, tableID):
        tableID += 1
        cursor = self.conn.cursor()

        table = Table()

        cursor.execute("SELECT * FROM BallTable WHERE TABLEID = ?", (tableID,))
        row = cursor.fetchone()

        if row:
            cursor.execute("SELECT TIME FROM TTable WHERE TABLEID = ?", (tableID,))
            table.time = cursor.fetchone()[0]
            

            cursor.execute("""SELECT Ball.BALLNO, Ball.XPOS, Ball.YPOS, Ball.XVEL, Ball.YVEL
                           FROM Ball
                           JOIN BallTable ON Ball.BALLID = BallTable.BALLID
                           WHERE BallTable.TABLEID = ? """, (tableID,))

            balls = cursor.fetchall()

            for ball in balls:
                if ball[3] == None or ball[4] == None:
                    still_ball_coord = Coordinate(ball[1], ball[2])
                    still_ball = StillBall(ball[0], still_ball_coord)
                    table += still_ball
                else:
                    rolling_ball_pos = Coordinate(ball[1], ball[2])
                    rolling_ball_vel = Coordinate(ball[3], ball[4])

                    acc = math.sqrt((ball[3] * ball[3]) + (ball[4] * ball[4]))

                    if acc > VEL_EPSILON:
                        acc_x = ((0.0 - ball[3])/acc) * DRAG
                        acc_y = ((0.0 - ball[4])/acc) * DRAG
                    else:
                        acc_x = 0.0
                        acc_y = 0.0

                    rolling_ball_acc = Coordinate(acc_x, acc_y)

                    rolling_ball = RollingBall(ball[0], rolling_ball_pos, rolling_ball_vel, rolling_ball_acc)
                    table += rolling_ball
            
        else:
            table = None

        cursor.close()

        return table

    def writeTable(self, table):
        cursor = self.conn.cursor()

        # Insert the table time
        cursor.execute("INSERT INTO TTable (TIME) VALUES (?)", (table.time,))
        table_id = cursor.lastrowid

        # Prepare the insert statements outside the loop
        insert_rolling_ball = "INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL) VALUES (?, ?, ?, ?, ?)"
        insert_still_ball = "INSERT INTO Ball (BALLNO, XPOS, YPOS) VALUES (?, ?, ?)"
        insert_ball_table = "INSERT INTO BallTable (BALLID, TABLEID) VALUES (?, ?)"

        for obj in table:
            if obj is not None:
                add_row = False

                if obj.type == phylib.PHYLIB_ROLLING_BALL:
                    add_row = True
                    ball_data = (obj.obj.rolling_ball.number, obj.obj.rolling_ball.pos.x,
                                obj.obj.rolling_ball.pos.y, obj.obj.rolling_ball.vel.x,
                                obj.obj.rolling_ball.vel.y)
                    cursor.execute(insert_rolling_ball, ball_data)
                    ball_id = cursor.lastrowid

                elif obj.type == phylib.PHYLIB_STILL_BALL:
                    add_row = True
                    ball_data = (obj.obj.still_ball.number, obj.obj.still_ball.pos.x,
                                obj.obj.still_ball.pos.y)
                    cursor.execute(insert_still_ball, ball_data)
                    ball_id = cursor.lastrowid

                if add_row:
                    cursor.execute(insert_ball_table, (ball_id, table_id))

        cursor.close()

        return table_id - 1

    def close(self):
        self.conn.commit()
        self.conn.close()

    def setGame(self, gameName, playerOneName, playerTwoName):
        cursor = self.conn.cursor()

        cursor.execute("INSERT INTO Game (GAMENAME) VALUES (?)", (gameName,))
        game_id = cursor.lastrowid

        cursor.execute("INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (?, ?)", (game_id, playerOneName))
        cursor.execute("INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (?, ?)", (game_id, playerTwoName))

        self.conn.commit()
        cursor.close()

    def getGame(self, gameID):
        cursor = self.conn.cursor()

        cursor.execute("""SELECT G.GAMENAME, P1.PLAYERNAME, P2.PLAYERNAME
                          FROM Game G
                          JOIN Player P1 ON G.GAMEID = P1.GAMEID
                          JOIN Player P2 ON G.GAMEID = P2.GAMEID
                          WHERE G.GAMEID = ?
                          ORDER BY P1.PLAYERID
                          LIMIT 1""", (gameID))

        row_of_values = cursor.fetchone()

        self.conn.commit()
        cursor.close()

        return row_of_values

    def newShot(self, player_name, game_name):
        cursor = self.conn.cursor()

        cursor.execute("""SELECT PLAYERID
                          FROM Player
                          WHERE PLAYERNAME = ?""", (player_name,))
        
        player_id = cursor.fetchone()[0]

        cursor.execute("""SELECT GAMEID
                          FROM Game
                          WHERE GAMENAME = ?""", (game_name,))
        
        game_id = cursor.fetchone()[0]

        cursor.execute("INSERT INTO Shot (PLAYERID, GAMEID) VALUES (?, ?)", (player_id, game_id))

        shot_id = cursor.lastrowid

        self.conn.commit()
        cursor.close()

        return shot_id
    
    def addTableShot(self, shotID, tableID):
        cursor = self.conn.cursor()

        insert_into_tableshot = "INSERT INTO TableShot (TABLEID, SHOTID) VALUES (?, ?)"
        tableshot_data = (tableID + 1, shotID)

        cursor.execute(insert_into_tableshot, tableshot_data)

        cursor.close()

    def getTablesOfShot(self, shotID):
        cursor = self.conn.cursor()

        cursor.execute("SELECT TABLEID FROM TableShot WHERE SHOTID = ?", (shotID,))
        rows = cursor.fetchall()

        tables = [row[0] for row in rows]

        cursor.close()

        return tables

################################################################################
class Game ():

    def __init__(self, gameID=None, gameName=None, player1Name=None, player2Name=None):

        # Connect to the database
        self.db = Database()

        # Constructor 1: Has a GAMEID to retrieve data from
        if gameID is not None and gameName is None and player1Name is None and player2Name is None:
            gameID += 1

            row_of_values = self.db.getGame(gameID)

            self.gameName = row_of_values[0]
            self.playerOneName = row_of_values[1]
            self.playerTwoName = row_of_values[2]

        # Constructor 2: No GAMEID, so we create one with name, player one, and player two
        elif gameID is None and gameName is not None and player1Name is not None and player2Name is not None:
            self.db.createDB()
            self.gameName = gameName
            self.playerOneName = player1Name
            self.playerTwoName = player2Name

            self.db.setGame(gameName, player1Name, player2Name)
            
        # Raise a TypeError if the constructors are not followed
        else:
            raise TypeError()

    def getTablesFromShot(self, shotID):
        return self.db.getTablesOfShot(shotID)

    def constructTable(self, tableID):
        return self.db.readTable(tableID - 1)

    def shoot(self, gameName, playerName, table, xvel, yvel):

        shot_id = self.db.newShot(playerName, gameName)

        for object in table:
            if object is not None:
                if object.type == phylib.PHYLIB_STILL_BALL and object.obj.still_ball.number == 0:
                    xpos = object.obj.still_ball.pos.x
                    ypos = object.obj.still_ball.pos.y

                    object.type = phylib.PHYLIB_ROLLING_BALL
                    object.obj.rolling_ball.number = 0
                    object.obj.rolling_ball.pos.x = xpos
                    object.obj.rolling_ball.pos.y = ypos
                    object.obj.rolling_ball.vel.x = xvel
                    object.obj.rolling_ball.vel.y = yvel

                    acc = math.sqrt((xvel * xvel) + (yvel * yvel))

                    if acc > VEL_EPSILON:
                        xacc = ((0.0 - xvel)/acc) * DRAG
                        yacc = ((0.0 - yvel)/acc) * DRAG
                    else:
                        xacc = 0.0
                        yacc = 0.0
                    
                    object.obj.rolling_ball.acc.x = xacc
                    object.obj.rolling_ball.acc.y = yacc

        while table:

            beginning_table_id = self.db.writeTable(table)
            self.db.addTableShot(shot_id, beginning_table_id)
    
            beginning_time = table.time
            print("Beginning time = ")
            print(beginning_time)

            segment_table = table.segment()

            if segment_table is not None:
                end_time = segment_table.time
                print("End time = ")
                print(end_time)

                frames = round((end_time - beginning_time) / FRAME_INTERVAL)
                print("Total frames = ")
                print(frames)

                for i in range(0, frames + 1):
                    frame_table = table.roll(i * FRAME_INTERVAL)
                    frame_table.time = beginning_time + (i * FRAME_INTERVAL)

                    table_id = self.db.writeTable(frame_table)
                    self.db.addTableShot(shot_id, table_id)

            table = segment_table

        self.db.conn.commit()
        return shot_id
        