from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import gettempdir
import sys
from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = gettempdir()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():
    if request.method == "GET":
        return render_template("index.html", userid = session["username"])
    return apology("TODO")

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    if request.method == "GET":
        return render_template("buy.html")
    else:
        if request.form.get("symbol") == "" or request.form.get("shares") == "":
            return apology("Symbol or shares is empty.")
            
        if int(request.form.get("shares")) < 0:
            return apology("Shares must be a positive integer")
            
        quote = lookup(request.form.get("symbol"))
        if quote == None:
            return apology("Symbol not found")
        else:
            #gets the price of the symbol
            price = quote["price"]
            
            #query the current cash the user got
            cash = db.execute("SELECT cash FROM users WHERE id=:idd", idd=session["user_id"])
            
            #check if cash on hand is not enough to buy shares
            if cash[0]["cash"] < int(request.form.get("shares")) * price:
                return apology("Not enough cash")
            else:
                #update user database with the new balance
                balance = cash[0]["cash"] - int(request.form.get("shares")) * price
                db.execute("UPDATE users SET cash = :balance WHERE id = :idd", balance=balance, idd=session["user_id"])
                db.execute("INSERT INTO purchaseRecord (user_id, symbol, price_paid, qty, name) VALUES (:user_id, :symbol, :price_paid, :qty, :name)", user_id=session["user_id"], symbol=quote["symbol"], price_paid=int(request.form.get("shares")) * price,
                qty=request.form.get("shares"), name=quote["name"])
                flash("Share bought!")
                return render_template("index.html")

@app.route("/history")
@login_required
def history():
    """Show history of transactions."""
    return apology("TODO")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]
        
        shares = db.execute("SELECT purchaseRecord.id, user_id, symbol, price_paid, date_time, sum(qty) as qty, Name, username, hash FROM purchaseRecord join users on user_id = users.id where user_id = :idd group by symbol", idd=session["user_id"])
        # redirect user to home page
        #return redirect(url_for("index"))
        l = []
        if shares == None:
            shares = []
            q = 0
        else:
            for i in range(len(shares)):
                shares[i]["price_paid"] = usd(float(shares[i]["price_paid"]))
                q = lookup(shares[i]["symbol"])
                shares[i]["totalPrice"] = usd(q["price"] * shares[i]["qty"])
                shares[i]["price"] = usd(float(q["price"]))
                #q["price"] = usd(float(q["price"]))
        return render_template("index.html", userid=rows[0]["username"], shares=shares)

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")
    else:
        quote = lookup(request.form.get("quote"))
        if quote != None:
            quote["price"] = usd(float(quote["price"]))
            return render_template("quoted.html", quote=quote)
        else:
            return apology("LOOKUP RETURNED NONE") 
   

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    
    if request.method == "POST":
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
        
        #check if the username is empty or username exists
        if request.form.get("username") == "" or len(rows) != 0:
            return apology("Username is empty or already exists.")
        
        #check if both is not empty
        if request.form.get("password") == "" or request.form.get("confirmPassword") == "":
            return apology("Both password and confirm password must not be empty.")
        #check if both not the same    
        elif request.form.get("password") != request.form.get("cfmPassword"):
            return apology("Password and password confirmation do not match.")
        
        rows = db.execute("INSERT INTO users (username, hash) VALUES (:username, :password)", username=request.form.get("username"), password=pwd_context.encrypt(request.form.get("password")))
        flash("Registration successful! You may login now.")
        return render_template("login.html")
    else:
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""
    return apology("TODO")
 