import Physics
import sys
import cgi
import os
import glob
import random
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

SHOOT_HEADER = """
                <html>
                    <head>
                        <title>8-Ball: Shooting</title>
                        <script src="https://cdn.tailwindcss.com"></script>
                        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
                    </head>

                    <body class="overflow-hidden h-32 bg-gradient-to-b from-blue-500 via-purple-500 to-blue-500">

                        <form method="post" action="Rolling.html" id="shotForm">
                            <input type="hidden" id="xVel" name="xVel"/>
                            <input type="hidden" id="yVel" name="yVel"/>
                        </form>

                        <div class="flex justify-between">
                            <div class="border-6 border-black p-6 h-screen" style="background-color: navy">"""

SHOOT_MIDDLE = """
                            </svg>
                            </div>

                            <div id="container" class="bg-transparent w-full h-screen flex flex-col items-center justify-center absolute z-10"></div>

                                <svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" class="w-full h-screen absolute pointer-events-none z-20">
                                    <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                                        <stop offset="0%" style="stop-color:rgb(218,165,32);stop-opacity:1" /> <!-- Light brown -->
                                        <stop offset="100%" style="stop-color:rgb(139,69,19);stop-opacity:1" /> <!-- Dark brown -->
                                    </linearGradient>

                                    <line id="vector" x1="0" y1="0" x2="0" y2="0" stroke-width="6" stroke="url(#gradient)" class="hidden"/>
                                </svg>

                            <div class="border-6 border-black p-6 h-screen" style="background-color: navy">"""

SHOOT_FOOTER = """
                            </svg>
                            </div>

                        </div>

                        <script>

                            //Find the length of a vector
                            const length = (x, y) => {
                                return Math.sqrt((x * x) + (y * y))
                            }

                            const makeMaxVector = (x1, y1, x2, y2) => {
                                // Get length
                                const len = length(x2-x1, y2-y1)

                                if (len == 0) return [0, 0]

                                // If within allotted range, return unchanged offset
                                if (len < 1000){
                                    return [x2-x1, y2-y1]
                                }

                                // Otherwise shorten magnitude while maintaining angle (unit vector) 
                                return [1000 * (x2 - x1) / len, 1000 * (y2 - y1) / len]
                            }

                            //Load the table and subsequent SVG objects
                            function reloadAJAX() {
                                $.ajax ({
                                    url: '/baseTable.svg',
                                    dataType: 'xml',
                                    success: (svg) => {
                                        content = $(svg.documentElement)

                                        const tableContainer = $('#container')
                                        tableContainer.empty()
                                        tableContainer.append(content)

                                        const cueBall = tableContainer.find("#ball0")

                                        if (cueBall.length === 0) {
                                            fetch('/reloadCueBall').then()(reloadAJAX())
                                        }

                                        const vector = $("#vector")

                                        function makeVector(x1, y1, x2, y2) {
                                            vector.removeClass("hidden")
                                            vector.attr("x1", x1)
                                            vector.attr("y1", y1)
                                            vector.attr("x2", x2)
                                            vector.attr("y2", y2)
                                        }

                                        let dragging = false
                                        let X, Y

                                        cueBall.on('mousedown', function(event) {
                                            dragging = true

                                            X = event.clientX
                                            Y = event.clientY
                                        })

                                        $(document).on('mousemove', function(event) {
                                            if(dragging) {
                                                const [dX, dY] = makeMaxVector(X, Y, event.clientX, event.clientY)
                                                makeVector(X, Y, X + dX, Y + dY)
                                            }
                                        })

                                        $(document).on('mouseup', function(event) {
                                            if(dragging) {
                                                vector.addClass("hidden");
                                                dragging = false;

                                                var [vX, vY] = makeMaxVector(X, Y, event.clientX, event.clientY);
                                                vX = vX * -10
                                                vY = vY * -10
                                                $('#xVel').val(vX)
                                                $('#yVel').val(vY)

                                                form = $('#shotForm').submit()

                                            }
                                        })
                                    }
                                })
                            }

                            reloadAJAX()
                        </script>
                    </body>
                </html>"""

WINNER_HEADER = """
                <html>
                    <head>
                        <title>8-Ball: Shooting</title>
                        <script src="https://cdn.tailwindcss.com"></script>
                        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
                    </head>

                    <body class="overflow-hidden h-32 bg-gradient-to-b from-blue-500 via-purple-500 to-blue-500">"""

WINNER_FOOTER = """
                        <br><br><br>
                        <form class="text-center" action="MainMenu.html" method="post">
                            <button class ="text-center p-5 text-bold text-4xl border-8 border-black bg-gradient-to-r from-blue-500 via-purple-500 to-blue-500 "type="submit">Play Again?</button>
                        </form>
                    </body>
                </html>"""

ROLLING_HEADER = """
            <html>
                <head>
                    <title>8-Ball: Rolling</title>
                    <script src="https://cdn.tailwindcss.com"></script>
                    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
                </head>

                <body class="overflow-hidden h-32 bg-gradient-to-b from-blue-500 via-purple-500 to-blue-500">

                    <form id="form" action="Shooting.html" method="post">
                        <input type="hidden" id="sunk_balls" name="sunk_balls"/>
                        <input type="hidden" id="playing" name="playing" value="1"/>
                    </form>

                    <div class="relative">

                    <div id="container" class="bg-transparent w-full h-screen flex flex-col items-center justify-center absolute z-10"></div>

                    </div>

                    <script>
                    """

ROLLING_FOOTER = """
                        var index = 0
                        var beginningBalls = []
                        var endingBalls = []


                        url = '/table-' + index + '.svg'

                        $.ajax ({
                            url: url,
                            dataType: 'xml',
                            success: (svg) => {
                                content = $(svg.documentElement)

                                const tableContainer = $('#container')
                                tableContainer.empty()
                                tableContainer.append(content)

                                for(var i = 0; i <= 15; i++) {
                                    const ball = $('#ball' + i)
                                    if(ball.length) {
                                        beginningBalls.push(i)
                                    }
                                }
                            }
                        });

                        function displayFrames() {
                            if(index < frames){
                        
                                url = '/table-' + index + '.svg'

                                ajaxPromise = $.ajax ({
                                    url: url,
                                    dataType: 'xml',
                                    success: (svg) => {
                                        content = $(svg.documentElement)

                                        const tableContainer = $('#container')
                                        tableContainer.empty()
                                        tableContainer.append(content)
                                    }
                                })
                                
                                if(index === frames - 1) {
                                    ajaxPromise.then(() => {
                                        index++
                                        setTimeout(displayFrames, 10)
                                    })
                                } else {
                                    index++
                                    setTimeout(displayFrames, 10)
                                }

                            } else {
                                for(var i = 0; i <= 15; i++) {
                                    const ball = $('#ball' + i)
                                    if(ball.length) {
                                        endingBalls.push(i)
                                    }
                                }

                                let combinedBalls = beginningBalls.concat(endingBalls)

                                let uniqueBalls = combinedBalls.filter((value, index, self) => {
                                    return self.indexOf(value) === index
                                })

                                var sunkBalls = uniqueBalls.filter(value => !endingBalls.includes(value))

                                var sunkBallsStr = sunkBalls.join(',')

                                $('#sunk_balls').val(sunkBallsStr)

                                $('#form').submit()
                                
                            }
                        }

                        displayFrames()
                    </script>
                </body>
            </html>
            """

# ssh -L 57047:localhost:57047 vanwyckk@linux.socs.uoguelph.ca

class MyServer(HTTPServer):
    def __init__(self, address, handler):
        self.gameName = None
        self.game = None
        self.playerOne = None
        self.playerOneHighLow = None # 1 = Low, 2 = High
        self.playerOneCanWin = None
        self.playerTwo = None
        self.playerTwoHighLow = None # 1 = Low, 2 = High
        self.playerTwoCanWin = None
        self.currentPlayer = None
        self.winner = 0
        self.balls = None
        self.table = None
        super().__init__(address, handler)

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed = urlparse(self.path)

        if self.path == '/baseTable.svg':
            self.send_response(200)
            self.send_header('Content-type', 'image/svg+xml')
            self.end_headers()

            fp = open('.'+self.path)
            content = fp.read()
            self.wfile.write(bytes(content, "utf-8"))
            fp.close()

        elif parsed.path.startswith('/table-') and parsed.path.endswith('.svg'):
            table_number = self.path[7:-4]
            file_path = f'table-{table_number}.svg'

            if os.path.exists(file_path):
                fp = open('.'+self.path)
                content = fp.read()

                self.send_response(200)
                self.send_header('Content-type', 'image/svg+xml')
                self.end_headers()

                self.wfile.write(bytes(content, "utf-8"))
                fp.close()
            else:
                self.send_response( 404 )
                self.end_headers()
                self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) )

        elif self.path == '/reloadCueBall':
            self.send_response(200)
            self.end_headers()
            self.server.table.addCueBall()

            with open('baseTable.svg', 'w') as f:
                f.write(self.server.table.svg())

        elif self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            with open('Main_Menu.html', 'rb') as f:
                self.wfile.write(f.read())

    def do_POST(self):
        if self.path in ['/MainMenu.html']:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            with open('Main_Menu.html', 'rb') as f:
                self.wfile.write(f.read())

        elif self.path in ['/Shooting.html']:
            # Get the values from the form of main menu
            form = cgi.FieldStorage( fp=self.rfile,
                                     headers=self.headers,
                                     environ = { 'REQUEST_METHOD': 'POST',
                                                 'CONTENT_TYPE': 
                                                   self.headers['Content-Type'],
                                               } 
                                   )

            # Figure out if this is a concurrent game or a new one
            current_game = int(form.getvalue('playing'))
            game_type = form.getvalue('gameType')

            if game_type is not None:
                game_type = int(game_type)

            if(current_game == 0):
                # Make the new game and log the values
                self.server.gameName = form.getvalue('gameName')
                self.server.playerOne = form.getvalue('player1Name')
                self.server.playerTwo = form.getvalue('player2Name')

                # Generate random first turn
                turn = random.choice([1,2])
        
                if(turn == 1):
                    self.server.currentPlayer = self.server.playerOne
                else:
                    self.server.currentPlayer = self.server.playerTwo
                
                # Create the game database and table
                self.server.game = Physics.Game(gameName=self.server.gameName, player1Name=self.server.playerOne, player2Name=self.server.playerTwo)

                if game_type == 1:
                    self.server.table = Physics.Table()
                    self.server.table.createFullTable()
                    self.server.balls = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
                elif game_type == 2:
                    self.server.table = Physics.Table()
                    self.server.table.createDemoTable()
                    self.server.balls = [1,2,8,14,15]

                self.server.winner = 0

            else:
                # If the game is going, this came from a shot; thus, check for sunken balls
                sunk_balls_str = form.getvalue('sunk_balls')

                gameOver = 0

                # If balls were sunk, log them as int's
                if sunk_balls_str is not None:
                    sunk_balls = [int(x) for x in sunk_balls_str.split(',')]
                else:
                    sunk_balls = []

                # If any balls were sunk
                if len(sunk_balls) != 0:

                    # Initial high-low assignment assuming that a ball was sunk
                    if self.server.playerOneHighLow is None or self.server.playerTwoHighLow is None:
                        lowBalls = 0
                        highBalls = 0

                        for x in sunk_balls:
                            if x != 0:
                                if x > 8:
                                    highBalls += 1
                                elif x < 8:
                                    lowBalls += 1

                        # Depending on the majority ranking of sunken balls, assign HIGH and LOW ball sets
                        if lowBalls > highBalls:
                            if self.server.currentPlayer == self.server.playerOne:
                                self.server.playerOneHighLow = 1
                                self.server.playerTwoHighLow = 2
                            else:
                                self.server.playerTwoHighLow = 1
                                self.server.playerOneHighLow = 2
                        elif highBalls > lowBalls:
                            if self.server.currentPlayer == self.server.playerOne:
                                self.server.playerOneHighLow = 2
                                self.server.playerTwoHighLow = 1
                            else:
                                self.server.playerTwoHighLow = 2
                                self.server.playerOneHighLow = 1

                        elif highBalls == lowBalls and highBalls != 0:
                            if self.server.currentPlayer == self.server.playerOne:
                                self.server.playerOneHighLow = 2
                                self.server.playerTwoHighLow = 1
                            else:
                                self.server.playerTwoHighLow = 2
                                self.server.playerOneHighLow = 1

                    
                    for x in sunk_balls:
                        if(x != 0):
                            self.server.balls.remove(x)
                        if(x == 8):
                            gameOver = 1

                    if(gameOver):
                        if self.server.currentPlayer == self.server.playerOne:
                            # If player one sunk the 8 ball, they either win or lose
                            if self.server.playerOneCanWin:
                                self.server.winner = 1
                            else:
                                self.server.winner = 2
                        else:
                            # If player two sunk the 8 ball, they either win or lose
                            if self.server.playerTwoCanWin:
                                self.server.winner = 2
                            else:
                                self.server.winner = 1

                else:
                    # Swap turns only if no balls were sunk
                    if self.server.currentPlayer == self.server.playerOne:
                        self.server.currentPlayer = self.server.playerTwo
                    else:
                        self.server.currentPlayer = self.server.playerOne
                
            if self.server.winner == 0:
                # Create the base table (either the first ever table, or the last table from the shot)
                with open('baseTable.svg', 'w') as f:
                    f.write(self.server.table.svg())

                highRemainingBalls = 0
                lowRemainingBalls = 0

                html = SHOOT_HEADER

                if self.server.currentPlayer is self.server.playerOne:
                    html += f"      <h1 class='text-green-500 text-4xl font-bold text-center'>{self.server.playerOne}</h1>"
                else:
                    html += f"      <h1 class='text-4xl font-bold text-center'>{self.server.playerOne}</h1>"

                if self.server.playerOneHighLow == 1:
                    html += """     <h2 class='text-2xl text-red-500 font-bold text-center'>LOW</h2>
                                    <h1 class='text-1xl font-bold text-center'>Balls to Sink:</h1><br>"""
                    
                    for i in range(1,8):
                        if i in self.server.balls:
                            html += f"<h1 style='color: {Physics.BALL_COLOURS[i]};' class='text-2xl font-bold text-center' id='{i}'>{i}</h1>"
                            lowRemainingBalls += 1

                    if lowRemainingBalls == 0:
                        html += "<h1 class='font-bold text-center'>All balls sunk! Go for 8!</h1>"
                        self.server.playerOneCanWin = 1

                elif self.server.playerOneHighLow == 2:
                    html += """     <h2 class='text-red-500 text-2xl font-bold text-center'>HIGH</h2>
                                    <h1 class='text-1xl font-bold text-center'>Balls to Sink:</h1><br>"""
                    
                    for i in range(9,16):
                        if i in self.server.balls:
                            html += f"<h1 style='color: {Physics.BALL_COLOURS[i]};' class='text-2xl font-bold text-center' id='{i}'>{i}</h1>"
                            highRemainingBalls += 1

                    if highRemainingBalls == 0:
                        html += "<h1 class='font-bold text-center'>All balls sunk! Go for 8!</h1>"
                        self.server.playerOneCanWin = 1

                html += SHOOT_MIDDLE
                
                if self.server.currentPlayer is self.server.playerTwo:
                    html += f"      <h1 class='text-green-500 text-4xl font-bold text-center'>{self.server.playerTwo}</h1>"
                else:
                    html += f"      <h1 class='text-4xl font-bold text-center'>{self.server.playerTwo}</h1>"

                if self.server.playerTwoHighLow == 1:
                    html += """     <h2 class='text-2xl text-red-500 font-bold text-center'>LOW</h2>
                                    <h1 class='text-1xl font-bold text-center'>Balls to Sink:</h1><br>"""
                    for i in range(1,8):
                        if i in self.server.balls:
                            html += f"<h1 style='color: {Physics.BALL_COLOURS[i]};' class='text-2xl font-bold text-center' id='{i}'>{i}</h1>"
                            lowRemainingBalls += 1

                    if lowRemainingBalls == 0:
                        html += "<h1 class='font-bold text-center'>All balls sunk! Go for 8!</h1>"
                        self.server.playerTwoCanWin = 1

                elif self.server.playerTwoHighLow == 2:
                    html += """     <h2 class='text-red-500 text-2xl font-bold text-center'>HIGH</h2>
                                    <h1 class='text-1xl font-bold text-center'>Balls to Sink:</h1><br>"""
                    
                    for i in range(9,16):
                        if i in self.server.balls:
                            html += f"<h1 style='color: {Physics.BALL_COLOURS[i]};' class='text-2xl font-bold text-center' id='{i}'>{i}</h1>"
                            highRemainingBalls += 1

                    if highRemainingBalls == 0:
                        html += "<h1 class='font-bold text-center'>All balls sunk! Go for 8!</h1>"
                        self.server.playerTwoCanWin = 1

                html += SHOOT_FOOTER

            else:
                # If someone has won, send the winner page rather than the shoot page and insert the winner
                html = WINNER_HEADER

                html += "<h1 class='font-bold text-center text-6xl'>"
                
                if self.server.winner == 1:
                    html += f"{self.server.playerOne} WINS!!!</h1>"
                else:
                    html += f"{self.server.playerTwo} WINS!!!</h1>"

                html += WINNER_FOOTER

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(bytes(html, "utf-8"))

        elif self.path in ['/Rolling.html']:
            form = cgi.FieldStorage( fp=self.rfile,
                                     headers=self.headers,
                                     environ = { 'REQUEST_METHOD': 'POST',
                                                 'CONTENT_TYPE': 
                                                   self.headers['Content-Type'],
                                               } 
                                   )

            # Get the shot velocities
            x_vel = int(form.getvalue('xVel'))
            y_vel = int(form.getvalue('yVel'))

            # Delete all currently existing table files
            print("Deleting current .svg files...")
            files_to_delete = glob.glob('*.svg')
            for file in files_to_delete:
                os.remove(file)

            # Create the shot in the database and log the shot ID
            shot_id = self.server.game.shoot(self.server.gameName, self.server.currentPlayer, self.server.table, x_vel, y_vel)
            
            # Get all of the tables, and create sequential files for each to represent frames
            tables = self.server.game.getTablesFromShot(shot_id)
            index = 0

            for tableNum in tables:
                frameTable = self.server.game.constructTable(tableNum)

                with open(f'table-{index}.svg', 'w') as f:
                    f.write(frameTable.svg())

                index += 1

            # Set the base table to the last table of the shot for repeat shots
            self.server.table = frameTable

            html = ROLLING_HEADER
            
            html += f"  var frames = {len(tables)}"

            html += ROLLING_FOOTER

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(bytes(html, "utf-8"))

if __name__ == "__main__":
    httpd = MyServer(('localhost', int(sys.argv[1])), Handler)
    httpd.serve_forever()
