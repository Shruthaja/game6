import pyodbc as pyodbc
from flask import Flask, render_template, request

app = Flask(__name__)
server = 'assignmnet6.database.windows.net'
database = 'testDB'
username = 'shruthaja'
password = 'mattu4-12'
driver = '{ODBC Driver 17 for SQL Server}'

conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')
cursor = conn.cursor()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
pname1 = ''
pname2 = ''
pile1 = 0
pile2 = 0
min = 0
max = 0


def game(pname1, pname2, pile1, pile2, pick1, pick2):
    pile = [10, 10, 10]
    player1 = 0
    pileidx = int(pile1)
    player1 = pick1
    pile[pileidx] = pile[pileidx] - player1
    pileidx = int(pile2)
    player2 = pick2
    pile[pileidx] = pile[pileidx] - player2
    if player2 > player1:
        return [" Player " + pname1 + " has : " + str(player1), "Player " + pname2 + " wins with : " + str(player2)]
    else:
        return ["Player " + pname1 + " wins with : " + str(player1), "Player " + pname2 + " has : " + str(player2)]
    return


@app.route('/', methods=['GET', 'POST'])
def home():
    result = []
    global pname1, pname2, pile1, pile2, min, max
    query = "select min,max from admin where id=1"
    cursor.execute(query)
    r = cursor.fetchall()
    print(r)
    min = r[0][0]
    max = r[0][1]
    picked = 0
    if request.method == "POST":
        pname1 = request.form['player1']
        # pname2 = request.form['player2']
        pile1 = int(request.form['player1pile']) - 1
        picked = int(request.form['pick1'])
        # pile2 = int(request.form['player2pile']) - 1
        query = "insert into player values(?,?,?)"
        cursor.execute(query, pname1, pile1, picked)
        cursor.commit()
        return render_template('index.html', success="Entered details successfully", min=min, max=max)
    else:
        return render_template('index.html', result=result, min=min, max=max)


@app.route('/game', methods=['GET', 'POST'])
def game1():
    result = []
    query = "select count(*) from dbo.player"
    cursor.execute(query)
    count = cursor.fetchone()
    print(count[0])
    if (count[0] > 2 or count[0] < 2):
        return "Incorrect player count!!"
    query = "select player,pile,picked from dbo.player"
    cursor.execute(query)
    p = cursor.fetchall()
    print(p)
    result = game(p[0][0], p[1][0], p[0][1], p[1][1], int(p[0][2]), int(p[1][2]))
    query = "truncate table player"
    cursor.execute(query)
    cursor.commit()
    print(min, max)
    return render_template('game.html', pname1=p[0][0], pname2=p[1][0], result=result, min=min, max=max)


@app.route('/login', methods=['GET', 'POST'])
def login():
    global min, max
    if request.method == "POST":
        min = request.form['min']
        max = request.form['max']
        query = "update  admin set min=? , max=? where id=1"
        cursor.execute(query, min, max).commit()
        print(min, max)
        return render_template("index.html", min=min, max=max)
    return render_template("login.html")


if __name__ == '__main__':
    app.run(debug=True)
