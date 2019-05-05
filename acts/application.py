import json
import sqlite3
from werkzeug.exceptions import HTTPException
import atexit
from flask import Flask, request, Response, render_template, jsonify
APP = Flask(__name__)


##################################################################
#   START/END FUNCTIONS                                          #
#################################################################

def startup():
    """
        Function to present the index page
        """
    json = {}
    results =[]
    temp = {}
    temp[[0][0]] = {}
    temp[[0][0]]["title"] = "Welcome to Selfieless Acts"
    results.append(temp[[0][0]])
    json["index"] = results
    return results

def shutdown():
    """
    Function to ensure the database is closed during app exit
    """
    global conn

    #close database
    conn.commit()
    conn.close()

##################################################################
#   DATABASE FUNCTIONS                                          #
#################################################################
def user_create(user_name, password):
    """
    This function creates a user

    :param user_name: user name
    :type user_name: str
    :param password: user password
    :type password: str
    """

    try:
        with sqlite3.connect("/opt/db/selfieless.db") as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(
                """INSERT INTO users (usr_name, password)
                VALUES (?, ?)""",
                (user_name, password)
            )
            con.commit()
            msg = "Record successfully added"
            return True
    except Exception as err:
        return False


def category_create(category_name, acts):
    """
        This function creates a category

        :param category_name: category name
        :type category_name: str
        :param acts: no. of acts
        :type acts: int
        """
    global DBB_CONN
    global DBB_CUR

    try:
        with sqlite3.connect("/opt/db/selfieless.db") as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(
                """INSERT INTO categories (category_name, acts)
                VALUES (?, ?)""",
                (category_name, acts)
                           )
            con.commit()
            return True
    except:
        return False

def act_create(act_id, username, timestamp, caption, category, image, upvotes):
    """
        This function creates an act.

        :param act_id: Act ID
        :type act_id: int
        :param username: User name
        :type user_name: str
        :param timestamp: Time and date of the act
        :type timestamp: str
        :param caption: Caption for the act
        :type caption: str
        :param category: Category of the act
        :type catgory: str
        :param image: Base64 string of the image binary
        :type catgory: str
        :param upvotes: Upvotes received on the act
        :type upvotes: int
        """

    try:
        with sqlite3.connect("/opt/db/selfieless.db") as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(
                """INSERT INTO acts (act_id, user_name, timestamp, caption, category, imgB64, upvotes)
                VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (act_id, username, timestamp, caption, category, image, upvotes)
                )
            con.commit()
            #Update the number of acts in the category table
            cur.execute(
                "UPDATE categories SET acts = acts + 1 WHERE category_name=?",
                (category,)
            )
            con.commit()
            return True
    except:
        return False

def act_exists(act_id):
    """
        This function checks if an act exists

        :param act_id: Act ID
        :type act_id: int
        """

    with sqlite3.connect("/opt/db/selfieless.db") as con:
        cur = con.cursor()
        cur.execute(
                "SELECT EXISTS (SELECT 1 FROM acts WHERE act_id=?);",
                (act_id,)
        )
        exists= cur.fetchone()[0]
        if exists == 1:
            return True
        else:
            return False

def act_upvote(act_id):
    """
        This function adds an upvote to the act

        :param act_id: Act ID
        :type user_id: int
        """

    try:
        with sqlite3.connect("/opt/db/selfieless.db") as con:
            cur = con.cursor()
            cur.execute(
                "UPDATE acts SET upvotes = upvotes + 1 WHERE act_id=?",
                (act_id,)
            )
            con.commit()
            return True
    except:
        return False


def user_remove(username):
    """
    This function removes a user.

    :param user_id: user ID
    :type user_id: int
    """

    try:
        with sqlite3.connect("/opt/db/selfieless.db") as con:
            cur = con.cursor()
            cur.execute(
                "DELETE FROM users WHERE usr_name=?",
                (username,)
            )
            con.commit()
            #check whether an user was removed
            if cur.rowcount > 0:
                return True
            return False
    except:
        return False

def category_remove(category_name):
    """
        This function removes a category

        :param category_name: category name
        :type category_name: str
        """

    try:
        with sqlite3.connect("/opt/db/selfieless.db") as con:
            cur = con.cursor()
            cur.execute(
                "DELETE FROM categories WHERE category_name=?",
                (category_name,)
            )
            con.commit()
            #check whether an user was removed
            if cur.rowcount > 0:
                return True
            return False
    except:
        return False

def act_remove(act_id):
    """
        This function removes an act

        :param act_id: Act ID
        :type act_id: int
        """
    try:
        with sqlite3.connect("/opt/db/selfieless.db") as con:
            cur = con.cursor()
            cur.execute(
                "DELETE FROM acts WHERE act_id=?",
                (act_id,)
            )
            con.commit()
            #check whether an user was removed
            if cur.rowcount > 0:
               return True
            return False
    except:
        return False

def category_get(category_name):
    """
        This function retrieves all properties of a category

        :param category_name: Category name
        :type category_name: str
        """
    with sqlite3.connect("/opt/db/selfieless.db") as con:
        cur = con.cursor()
        #execute database query
        if category_name:
            cur.execute(
                "SELECT * FROM categories WHERE category_name=?;",
                 (category_name,)
            )
        else:
            cur.execute("SELECT * FROM categories;")

        json = {}
        results =[]
        temp = {}

        for row in cur:
            results.append({
                row[0]: row[1]
            })
        return results

def acts_get(act_id):
    """
        This function retrieves all properties of an act

        :param act_id: Act ID
        :type act_id: int
        """

    with sqlite3.connect("/opt/db/selfieless.db") as con:
        cur = con.cursor()
        if act_id:
            cur.execute(
                "SELECT * FROM acts WHERE act_id=?;",
                (act_id,)
            )
        else:
            cur.execute("SELECT * FROM acts;")

        json = {}
        results =[]
        temp = {}
        for row in cur:
                temp[row[0]] = {}
                temp[row[0]]["act_id"] = row[0]
                temp[row[0]]["user_name"] = row[1]
                temp[row[0]]["timestamp"] = row[2]
                temp[row[0]]["caption"] = row[3]
                temp[row[0]]["category"] = row[4]
                temp[row[0]]["imgB64"] = row[5]
                temp[row[0]]["upvotes"] = row[6]
                results.append(temp[row[0]])
        json["results"] = results
        return results

def category_acts_count(category_name):
    """
        This function retrieves the number of acts in a category

        :param category_name: Category name
        :type category_name: str
        """

    try:
        with sqlite3.connect("/opt/db/selfieless.db") as con:
            cur = con.cursor()
            cur.execute(
                           "SELECT count(*) FROM acts WHERE category=?;",
                           (category_name,)
                           )
    except:
        return -1

    results =[]
    temp = {}
    for row in cursor:
        temp[row[0]] = row[0]
        results.append(temp[row[0]])
    return results

def category_exists(category_name):
    """
        This function checks if a category exists

        :param category_name: Category name
        :type category_name: str
        """
    with sqlite3.connect("/opt/db/selfieless.db") as con:
        cur = con.cursor()
        cur.execute(
                "SELECT EXISTS (SELECT 1 FROM categories WHERE category_name=?);",
                (category_name,)
        )
        exists= cur.fetchone()[0]
        if exists == 1:
            return True
        else:
            return False

def category_acts_get(category_name):
    """
        This function retrieves all the acts under a category

        :param category_name: Category name
        :type category_name: str
        """
    with sqlite3.connect("/opt/db/selfieless.db") as con:
        cur = con.cursor()
        cur.execute(
            "SELECT count(*) FROM acts WHERE category=?;",
            (category_name,)
        )
        count= cur.fetchone()[0]
        if (count > 100):
            return False
        else:
            cur.execute(
                "SELECT * FROM acts WHERE category=?;",
                (category_name,)
            )

        json = {}
        results =[]
        temp = {}
        for row in cur:
            temp[row[0]] = {}
            temp[row[0]]["act_id"] = row[0]
            temp[row[0]]["user_name"] = row[1]
            temp[row[0]]["timestamp"] = row[2]
            temp[row[0]]["caption"] = row[3]
            temp[row[0]]["category"] = row[4]
            temp[row[0]]["imgB64"] = row[5]
            temp[row[0]]["upvotes"] = row[6]
            results.append(temp[row[0]])
        json["results"] = results
        return results

def acts_get_count_range(category_name, startRange, endRange):
    """
        This function retrieves the acts under a category within a given range

        :param category_name: Category name
        :type category_name: str
        :param startRange: Starting range
        :type startRange: int
        :param endRange: Ending range
        :type endRange: int
        """
    try:
        with sqlite3.connect("/opt/db/selfieless.db") as con:
            cur = con.cursor()
            cur.execute(
                "SELECT * FROM acts WHERE category=? AND ROWID > ? AND ROWID <= ?;",
                (category_name, startRange, endRange,)
            )
    except:
        return -1

    json = {}
    results =[]
    temp = {}
    for row in cur:
        temp[row[0]] = {}
        temp[row[0]]["act_id"] = row[0]
        temp[row[0]]["user_name"] = row[1]
        temp[row[0]]["timestamp"] = row[2]
        temp[row[0]]["caption"] = row[3]
        temp[row[0]]["category"] = row[4]
        temp[row[0]]["imgB64"] = row[5]
        temp[row[0]]["upvotes"] = row[6]
        results.append(temp[row[0]])
    json["results"] = results
    return results


##################################################################
#   FLASK FUNCTIONS                                              #
#################################################################

@APP.route("/")
def index():
    """
    This function presents the main page.
    """
    return jsonify(startup())

@APP.route("/api/v1/users", methods=["POST"])
def api_create_user():
    """
    This function creates a user
    """

    try:
        myname = request.form["name"]
        mypwd = request.form["password"]
    except:
        #400 Bad Request
        return jsonify(error=400), 400
    user=""
    password=""

    user+=(str(myname))
    password+=(str(mypwd))

    if(len(password)!=40):
        return jsonify(error=400), 400

    for char in password:
        if ((((char>='0' and char<='9') or (char>='A' and char<='F') or (char>='a' and char<='f'))) != True):
            return jsonify(error=400), 400

    if user_create(
                    request.form["name"], request.form["password"]
                    ):
        #201 Created
        return jsonify(success=201), 201
    return jsonify(error=400), 400

@APP.route("/api/v1/users/<path:username>", methods=["DELETE"])
def api_delete_user(username):
    """
    This function deletes a particular user.

    :param username: user name
    :type username: str
    """
    result = user_remove(username)
    if result:
        return jsonify(success=200), 200
    else:
        return jsonify(error=400), 400

@APP.route("/api/v1/categories", methods=["GET"])
def api_list_categories():
    """
        This function lists all categories
        """
    categories = category_get(0)
    if len(categories) == 0:
        #We process a 200 error and display it as 204 since
        #204 is NOT an error and will not contain any body
        return jsonify(error=204), 200
    else:
        return jsonify(categories)

@APP.route("/api/v1/categories", methods=["POST"])
def api_create_category():
    """
        This function adds a category
        """
    if category_create(
                    request.form["categoryName"], 0
                    ):
        return jsonify(success=201), 201
    return jsonify(error=400), 400

@APP.route("/api/v1/categories/<path:category_name>", methods=["DELETE"])
def api_delete_category(category_name):
    """
        This function deletes a particular category.

        :param category_name: category name
        :type category_name: str
        """
    result = category_remove(category_name)
    if result:
        return jsonify(success=200), 200
    else:
        return jsonify(error=400), 400

@APP.route("/api/v1/categories/<path:category_name>/acts", methods=["GET"])
def api_list_acts_category(category_name):
    """
        This function lists all acts for a given category
        :param category_name: category name
        :type category_name: str
        """
    exists = category_exists(category_name)
    if not exists:
        return jsonify(error=400), 400
    else:
        acts = category_acts_get(category_name)
        if len(acts) == 0:
            #We process a 200 error and display it as 204 since
            #204 is NOT an error and will not contain any body
            return jsonify(error=204), 200
        else:
            return jsonify(acts)

@APP.route("/api/v1/categories/<path:category_name>/acts/size", methods=["GET"])
def api_category_acts_count(category_name):
    """
        This function lists the number of acts for a given category
        """
    exists = category_exists(category_name)
    if not exists:
        return jsonify(error=400), 400
    else:
        acts = category_acts_count(category_name)
        if len(acts) == 0:
            #We process a 200 error and display it as 204 since
            #204 is NOT an error and will not contain any body
            return jsonify(error=204), 200
        elif len(acts) < 0:
            return jsonify(error=400), 400
        else:
            return jsonify(acts)

#TODO - This API is not working
@APP.route("/api/v1/categories/<path:category_name>/acts", methods=["GET"])
def api_range_acts(category_name):
    """
        This function lists all acts for a given category in a given range
        """
    startRange = request.args.get('start', None)
    endRange = request.args.get('end', None)
    acts = acts_get_count_range(category_name, startRange, endRange)
    if len(acts) == 0:
        #We process a 200 error and display it as 204 since
        #204 is NOT an error and will not contain any body
        return jsonify(error=204), 200
    elif len(acts) < 0:
        return jsonify(error=400), 400
    else:
        return jsonify(acts)

@APP.route("/api/v1/acts/upvote", methods=["POST"])
def api_act_upvote():
    """
        This function upvotes a specific act
        """
    exists = act_exists(request.form["act_id"])
    if not exists:
        return jsonify(error=400), 400
    else:
        if act_upvote(
                    request.form["act_id"]
                    ):
            return jsonify(error=200), 200
        return jsonify(error=400), 400

@APP.route("/api/v1/acts/<int:act_id>", methods=["DELETE"])
def api_delete_act(act_id):
    """
        This function deletes a particular act.

        :param act_id: Act ID
        :type act_id: int
        """
    result = act_remove(act_id)
    if result:
        return jsonify(success=200), 200
    else:
        return jsonify(error=400), 400

@APP.route("/api/v1/acts", methods=["POST"])
def api_create_act():
    """
        This function creates an act
        """
    #At the time of act creation, the upvotes is 0
    upvotes = 0
    result = act_create(
                    request.form["actId"], request.form["username"],
                    request.form["timestamp"], request.form["caption"],
                    request.form["categoryName"], request.form["imgB64"],upvotes
                )
    if result:
        return jsonify(success=200), 200
    else:
        return jsonify(error=400), 400

@APP.errorhandler(HTTPException)
def handle_error(e):
    try:
        if e.code < 400:
            return flask.Response.force_type(e, flask.request.environ)
        elif e.code == 404:
            return jsonify(error=404), 404
        raise e
    except:
        return jsonify(error=405), 500

##################################################################
#   MAIN FUNCTION                                                #
#################################################################
def create_db():
    conn = sqlite3.connect("/opt/db/selfieless.db")
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys = ON')
    c.execute('''CREATE TABLE users(
        usr_name TEXT PRIMARY KEY NOT NULL,
        password TEXT NOT NULL);''')

    c.execute('''CREATE TABLE categories(
        category_name TEXT PRIMARY KEY NOT NULL,
        acts INTEGER );''')

    c.execute('''CREATE TABLE acts(
        act_id INTEGER PRIMARY KEY,
        user_name TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        caption TEXT NOT NULL,
        category TEXT NOT NULL,
        imgB64 TEXT NOT NULL,
        upvotes INTEGER,
        FOREIGN KEY (category) REFERENCES categories (category_name),
        FOREIGN KEY (user_name) REFERENCES users (usr_name));''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    global conn
    global cursor
    create_db()
    # 'At exit' calls functions when a program is closing down
    # Here, the shutdown function is called on program exit
    atexit.register(shutdown)
    #Start the database
    #check_same_thread is set to False to allow the connection to run on multiple threads
    conn = sqlite3.connect("/opt/db/selfieless.db", check_same_thread=False)
    cursor = conn.cursor()
    APP.run(debug=False)
