from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import gettempdir
import sys
from helpers import *
from flask_mail import Mail, Message

# configure application
app = Flask(__name__)
#setup flask mail
app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'drakewei123@gmail.com',
    MAIL_PASSWORD = 'tingwei3931@',
))
mail = Mail(app)


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
    if "user_id" not in session:
        return redirect(url_for("login"))
    if request.method == "GET":
        #populate table in index with data in stockRecord
        sharesOnHand = db.execute("SELECT * FROM stockRecord WHERE user_id=:uid", uid=session["user_id"])
        # redirect user to home page
        #return redirect(url_for("index"))
        total = 0
        if sharesOnHand == None:
            sharesOnHand = []
            q = 0
        else:
            for i in range(len(sharesOnHand)):
                q = lookup(sharesOnHand[i]["symbol"])
                sharesOnHand[i]["totalPrice"] = usd(q["price"] * sharesOnHand[i]["qtyOnHand"])
                total += q["price"] * sharesOnHand[i]["qtyOnHand"]
                sharesOnHand[i]["price"] = usd(float(q["price"]))
            b = db.execute("SELECT cash FROM users WHERE id = :idd", idd=session["user_id"])
            total += b[0]["cash"]
        return render_template("index.html", userid=session["username"], shares=sharesOnHand, cash_in_hand=usd(float(b[0]["cash"])), total=usd(total))
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
                db.execute("UPDATE users SET cash=:balance WHERE id=:idd", balance=balance, idd=session["user_id"])
                #insert new purchase record
                db.execute("INSERT INTO purchaseRecord (user_id, symbol, price_paid, qty, name) VALUES (:user_id, :symbol, :price_paid, :qty, :name)", user_id=session["user_id"], symbol=quote["symbol"], price_paid=int(request.form.get("shares")) * price,
                qty = request.form.get("shares"), name=quote["name"])
                #check if the stock is bought before by the user
                r = db.execute("SELECT * FROM stockRecord WHERE user_id=:uid and symbol=:symbol", uid=session["user_id"], symbol=quote["symbol"])
                if len(r) == 0: #if the stock is new stock
                    db.execute("INSERT INTO stockRecord (user_id, symbol, qtyOnHand, name) VALUES(:uid, :symbol, :qtyOnHand, :name)", uid=session["user_id"], symbol=quote["symbol"], qtyOnHand=request.form.get("shares"), name=quote["name"])
                else: #if the stock exists in user's portfolio
                    curr_qty = db.execute("SELECT qtyOnHand FROM stockRecord WHERE user_id = :uid and symbol=:symbol", uid = session["user_id"], symbol=quote["symbol"])
                    db.execute("UPDATE stockRecord SET qtyOnHand=:qtyOnHand WHERE user_id=:uid and symbol=:symbol", qtyOnHand=curr_qty[0]["qtyOnHand"] + int(request.form.get("shares")), uid=session["user_id"], symbol=quote["symbol"])
                #inform user transaction successful
                flash("Share bought!")
                # redirect user to home page
                return redirect(url_for("index"))
                

@app.route("/history")
@login_required
def history():
    """Show history of transactions."""
    if request.method == "GET":
        records = db.execute("SELECT * FROM purchaseRecord WHERE user_id = :uid UNION SELECT * FROM salesRecord WHERE user_id = :uid ORDER BY date_time DESC;", uid=session["user_id"])
        for i in range(len(records)):
            records[i]["price_paid"] = usd(float(records[i]["price_paid"]))
        return render_template("history.html", records = records)
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
        session["username"] = rows[0]["username"]
        
        #shares = db.execute("SELECT purchaseRecord.id, user_id, symbol, price_paid, date_time, sum(qty) as qty, Name, username, hash FROM purchaseRecord join users on user_id = users.id where user_id = :idd group by symbol", idd=session["user_id"])
        #redirect user to home page
        return redirect(url_for("index"))


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
            return apology("Lookup returned none.") 
   

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

@app.route("/chngPass", methods=["GET", "POST"])
@login_required
def chngPass():
    """Allows user to change password. """
    if request.method == "GET":
        return render_template("chngPass.html")
    else:
        if request.form.get("newPass") != request.form.get("newPass2"):
            return apology("Passwords do not match.")
        else:
            db.execute("UPDATE users SET hash = :h WHERE id = :uid", h=pwd_context.encrypt(request.form.get("newPass")), uid=session["user_id"])
        flash("Password changing successful!")
        return render_template("login.html")

 
 
@app.route("/forgotPass", methods=["GET", "POST"])
def forgotPass():
    if request.method == "GET":
        return render_template("forgotPass.html")
    else:
        msg = Message("Hello",
                sender="drakewei123@gmail.com",
                recipients=["tingwei3931@gmail.com"])
        msg.body = "HELLO TESTING TESTING" 
        mail.send(msg)
        flash("An email has been sent.")
        return render_template("login.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""
    if request.method == "GET":
        return render_template("sell.html")
    else:
        if request.form.get("symbol") == "" or request.form.get("shares") == "":
            return apology("Symbol or shares is empty.")
        
        if int(request.form.get("shares")) < 0:
            return apology("Shares must be a positive integer.")
            
        quote = lookup(request.form.get("symbol"))
        if quote == None:
            return apology("Symbol not Found")
        symbol = db.execute("SELECT symbol FROM stockRecord WHERE user_id=:uid AND symbol=:symbol", uid=session["user_id"], symbol=quote["symbol"])
        if len(symbol) == 0:
            return apology("User does not possess this symbol.")
        else:
            qty_on_hand = db.execute("SELECT qtyOnHand FROM stockRecord WHERE user_id = :uid AND symbol = :symbol", uid=session["user_id"], symbol=quote["symbol"])
            if qty_on_hand[0]["qtyOnHand"] < int(request.form.get("shares")):
                return apology("Insufficient stock to sell.")
            else:
                cash_on_hand = db.execute("SELECT cash FROM users WHERE id=:idd", idd=session["user_id"])
                #update user cash with the new balance added with the profit
                balance = cash_on_hand[0]["cash"] + int(request.form.get("shares")) * quote["price"]
                db.execute("UPDATE users SET cash = :balance WHERE id = :idd", balance=balance, idd=session["user_id"])
                #log the sales record
                db.execute("INSERT INTO salesRecord (user_id, symbol, price_sold, qty, name) VALUES (:user_id, :symbol, :price_sold, :qty, :name)", user_id=session["user_id"], symbol=quote["symbol"], price_sold=int(request.form.get("shares")) * quote["price"],
                qty=-1 * int(request.form.get("shares")), name=quote["name"])
                
                #subtract the qty sold from stockRecord
                curr_qty = db.execute("SELECT qtyOnHand FROM stockRecord WHERE user_id = :uid and symbol=:symbol", uid = session["user_id"], symbol=quote["symbol"])
                db.execute("UPDATE stockRecord SET qtyOnHand=:qtyOnHand WHERE user_id=:uid and symbol=:symbol", qtyOnHand=curr_qty[0]["qtyOnHand"] - int(request.form.get("shares")), uid=session["user_id"], symbol=quote["symbol"])
                flash("Share sold!")
                #redirect user to home page
                return redirect(url_for("index"))
                
                
    return render_template("sell.html")
