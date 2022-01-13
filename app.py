#Importing
import datetime 
from datetime import datetime
import re
from flask import Flask, redirect, url_for, render_template,request
from threading import Thread
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api,Resource
import random



#Global Variables
username=False
password=0
email=0
exsell_cash=0
item_id=False
person=False
classroom="None"
account="/"
#App
app = Flask(__name__)
#Api & Resources

#DB
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///exsell.db'
SQLALCHEMY_TRACK_MODIFICATIONS=False
db=SQLAlchemy(app)
#Items Table
class items(db.Model):
  id=db.Column(db.Integer,primary_key=True)
  title=db.Column(db.String,nullable=False)
  price=db.Column(db.Float,nullable=False)
  author=db.Column(db.String,nullable=False)
  img=db.Column(db.String,nullable=False)
  dis=db.Column(db.Text,nullable=False)
  cat=db.Column(db.String,nullable=False)
  amount=db.Column(db.Integer,nullable=False)
  #classroom ID
  classroom=db.Column(db.Integer,nullable=False,default="None")
  date_posted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
  return_day=db.Column(db.Integer,nullable=False,default=datetime.utcnow)
  def __repr__(self):
    return str(self.id)
#User Table
class users(db.Model):
  id=db.Column(db.Integer,primary_key=True)
  username=db.Column(db.String,nullable=False)
  password=db.Column(db.String,nullable=False)
  email=db.Column(db.String,nullable=False)
  #Classroom ID
  school_id=db.Column(db.Integer,nullable=False,default="None")
  classroom=db.Column(db.Integer,nullable=False,default="None")
  person=db.Column(db.String,nullable=False)
  exsell_cash=db.Column(db.Float,nullable=False)
  def __repr__(self):
    return str(self.id)
#Transactions
class tran(db.Model):
  id=db.Column(db.Integer,primary_key=True)
  buyer_id=db.Column(db.Integer,nullable=False)
  seller_id=db.Column(db.Integer,nullable=False)
  tran_date=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
  product=db.Column(db.String,nullable=False)
  price=db.Column(db.Float,nullable=False)
  def __repr__(self):
    return str(self.id)
#Notification
class notify(db.Model):
  id=db.Column(db.Integer,primary_key=True)
  user_id=db.Column(db.Integer,nullable=False)
  msg=db.Column(db.String,nullable=False)
  def __repr__(self):
    return str(self.id)
#Classrooms(All Classrooms)
class classrooms(db.Model):
  id=db.Column(db.Integer,primary_key=True)
  classroom=db.Column(db.Integer,nullable=False,default="None")
  teacher_id=db.Column(db.Integer,nullable=False)
  money_name=db.Column(db.String,nullable=False)
  class_code=db.Column(db.String,nullable=False)
  class_name=db.Column(db.String,nullable=False)
  school_id=db.Column(db.Integer,nullable=False,default="None")
  date_posted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
  def __repr__(self):
    return str(self.id)
#Classrooms(People)
class classroom_users(db.Model):
  #Class Room ID
  id=db.Column(db.Integer)
  #User_ID
  student_id=db.Column(db.Integer,nullable=False,primary_key=True)
  #The cash of the user in this classroom
  cash=db.Column(db.Float,nullable=False)

class schools(db.Model):
  id=db.Column(db.Integer,primary_key=True)
  admin_id=db.Column(db.Integer,nullable=False)
  school_code=db.Column(db.String,nullable=False)
  school_name=db.Column(db.String,nullable=False)
  date_posted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)


#Functions
def delete_item(id):
  db.session.delete(items.query.get(id))
  db.session.commit()
def filter_user(name):
  try:
    return users.query.filter_by(username=name).all()[0].password
  except:
    return "Sorry, couldn't find this account"
def filter_pass(name):
  try:
    return users.query.filter_by(password=name).all()[0]
  except:
    return "Sorry, couldn't find this account"

#Flask Routes
@app.route("/", methods=["POST", "GET"])
def home():
  global username
  if request.method=='POST':
    if username==False:
      return "Please Sign in to create an item..."
    else:
      title=request.form['title']
      price=request.form['price']
      img=request.form['img']
      dis=request.form['dis']
      new_item=items(title=title,price=price,img=img,dis=dis,return_day=7,author=username)
      db.session.add(new_item)
      db.session.commit()
      return "You have just published a new item"
  else:
    all_items=items.query.filter_by(classroom="None").order_by(items.date_posted).all()
    return render_template("index.html",items=all_items)

@app.route("/signup", methods=["POST", "GET"])
def signup():
  if request.method=='POST':
      username=request.form['username']
      password=request.form['password']
      email=request.form['email']
      data=users(username=username,password=password,email=email,person="Student",exsell_cash=0)
      try:
        if users.query.filter_by(username=username).all()[0].username==username:
          return "Sorry, username has been taken."
      except:
        db.session.add(data)
        db.session.commit()
        return "Thankyou for creating an acount on ExSELL!"
  else:
      return render_template("sign_up.html")

@app.route("/student_account",methods=["POST","GET"])
def student_account():
  global username
  global classroom
  global account
  if username==False or account=="teacher_account":
    return redirect(account)
  else:

    if request.method=='POST':
      if username==False:
        return "Please Sign in to create an item..."
      else:
        title=request.form['title']
        price=request.form['price']
        img=request.form['img']
        dis=request.form['dis']
        cat=request.form['cat']
        amount=int(request.form['amount'])
        new_item=items(title=title,price=price,img=img,dis=dis,return_day=7,author=username,cat=cat,amount=amount,classroom=classroom)
        db.session.add(new_item)
        db.session.commit()
        return "You have just published a new item!"
    else:
      all_items=items.query.filter_by(classroom="None").order_by(items.date_posted).all()
      return render_template("student_account.html",items=all_items)

@app.route("/teacher_account",methods=["POST","GET"])
def teacher_account():
  global username
  global account
  global classroom
  if username==False or account=="student_account":
    return redirect(account)
  else:

    if request.method=='POST':
      if username==False:
        return "Please Sign in to create an item..."
      else:
        title=request.form['title']
        price=request.form['price']
        img=request.form['img']
        dis=request.form['dis']
        cat=request.form['cat']
        amount=int(request.form['amount'])
        new_item=items(title=title,price=price,img=img,dis=dis,return_day=7,author=username,cat=cat,amount=amount,classroom=classroom)
        db.session.add(new_item)
        db.session.commit()
        return "You have just published a new item!"
    else:
      all_items=items.query.filter_by(classroom="None").order_by(items.date_posted).all()
      return render_template("teacher_account.html",items=all_items,classroom=classroom)

@app.route("/signin", methods=["POST", "GET"])
def signin():
  global username
  global password
  global email
  global exsell_cash
  global classroom
  global person
  global account
  if request.method=='POST':
    username=request.form['username']
    password=request.form['password']
    password1=filter_user(username)
    if password1==password:
      exsell_cash=users.query.filter_by(username=username).all()[0].exsell_cash
      email=users.query.filter_by(username=username).all()[0].email
      person=users.query.filter_by(username=username).all()[0].person
      #classroom=users.query.filter_by(username=username).all()[0].classroom
      if person=="Student":
        account="student_account"
        return redirect("student_account")
        
      if person=="Teacher":
        account="teacher_account"
        return redirect("teacher_account")
      if person=="Admin":
        if users.query.filter_by(username=username).all()[0].school_id=="None":
          account="admin_account"
          return redirect("create_school")
        else:
          account="admin_account"
          return redirect("school")
      else:
        return redirect("/")
    else:
      username=False
      return "Sorry, couldn't find this account"
  else:
    return render_template("sign_in.html")

@app.route('/mystore',methods=["GET","POST"])
def mystore():
  global username
  if username==False:
    return "Please Sign-In First!"
  else:
    return render_template('mystore.html',items=items.query.filter_by(author=username).all(),classroom=classroom)

@app.route('/delete_item.html',methods=["GET","POST"])
def delete_item():
  global username
  if username==False:
    return "Please Sign-In First!"
  else:
    if request.method=='POST':
      id=request.form['id']
      id=int(id)
      if items.query.filter_by(id=id).all()[0].author==username:
        db.session.delete(items.query.get(id))
        db.session.commit()
        return render_template("/mystore.html",items=items.query.filter_by(author=username).all())
      else:
        return "This item was not deleted because you do not own it!"
    else:
      return render_template('delete_element.html')

@app.route("/edit_check",methods=["POST","GET"])
def edit_check():
  global username
  global item_id
  if username==False:
    return "Please Sign-In First!"
  else:
    if request.method=='POST':
      id=request.form['id']
      id=int(id)
      try:
        if items.query.filter_by(id=id).all()[0].author==username:
          item_id=id
          return redirect('edit')
        else:
          item_id=False
          return "You cannot edit this item because you do not own it!"
      except:
        item_id=False
        return "You cannot edit this item because you do not own it!"
    else:
      return render_template('check_edit.html')

@app.route("/edit",methods=['GET','POST'])
def edit():
  global item_id
  if item_id==False:
    return "Sorry,couldn't find this item"
  else:
    if request.method=='POST':
      item=items.query.filter_by(id=item_id).all()[0]
      item.title=request.form['title']
      item.img=request.form['img']
      item.dis=request.form['dis']
      db.session.commit()
      item_id=False
      return redirect('mystore')
    else:
      return render_template('edit.html',item=items.query.filter_by(id=item_id).all()[0])

@app.route('/buy//<string:id>')
def buy(id):
  global username
  global exsell_cash
  global account
  id=int(id)
  if username==False:
    return redirect("/")
  else:
    if items.query.filter_by(id=id).all()[0].classroom=="None":
      if items.query.filter_by(id=id).all()[0].price<exsell_cash:
        #Getting all values to put in DB (tran table)
        buyer_id=users.query.filter_by(username=username).all()[0].id
        author=items.query.filter_by(id=id).all()[0].author
        seller_id=users.query.filter_by(username=author).all()[0].id
        product_id=id
        #Adding/Subtracting X-Sell Cash
        new_buyer_xsell_cash=users.query.filter_by(username=username).all()[0].exsell_cash-items.query.filter_by(id=id).all()[0].price
        new_seller_xsell_cash=users.query.filter_by(username=author).all()[0].exsell_cash + items.query.filter_by(id=id).all()[0].price
        users.query.filter_by(username=username).all()[0].exsell_cash=new_buyer_xsell_cash
        users.query.filter_by(username=author).all()[0].exsell_cash=new_seller_xsell_cash
        #Adding to DB (tran table)
        db.session.add(tran(buyer_id=buyer_id,seller_id=seller_id,product_id=items.query.filter_by(id=product_id).all[0].title,price=items.query.filter_by(id=id).all()[0].price))
        db.session.commit()

      #Notify seller
        db.session.add(notify(user_id=users.query.filter_by(username=items.query.filter_by(id=id).all()[0].author).all()[0].id,msg=items.query.filter_by(id=id).all()[0].title+" has been bought by: "+username))
        db.session.commit()
      #Deleting Item
        items.query.filter_by(id=id).all()[0].amount=items.query.filter_by(id=id).all()[0].amount-1
        db.session.commit()
        if items.query.filter_by(id=id).all()[0].amount==0:
          db.session.delete(items.query.get(id))
          db.session.commit()
        return "Purchase has been successful"
      else:
        return "Sorry,you do not have enough Exsell Cash to buy this item."
    else:
      return redirect("/")

@app.route('/myaccount')
def myaccount():
  
  global username
  global password
  global classroom
  global email
  if username==False:
    return redirect('/')
  else:
    if classroom=="None":
      return render_template("myaccount.html",username=username,password=password,email=email,classroom="None",cash_name="N.A",cash="N.A",xsellcash=users.query.filter_by(username=username).all()[0].exsell_cash)
    else:
      return render_template("myaccount.html",username=username,password=password,email=email,cash_name="Classroom Cash",cash=classroom_users.query.filter_by(student_id=users.query.filter_by(username=username).all()[0].id).all()[0].cash,classroom=classrooms.query.filter_by(id=classroom).all()[0].class_name,xsellcash=users.query.filter_by(username=username).all()[0].exsell_cash)

@app.route('/notify')
def notify_page():
  global username
  if username==False:
    return redirect("/")
  else:
    return render_template("notify.html",notifys=notify.query.filter_by(user_id=users.query.filter_by(username=username).all()[0].id).all())

@app.route("/signout")
def signout():
  global username
  username=False
  return redirect("/")

@app.route("/books")
def books():
  return render_template("catigory.html",items=items.query.filter_by(cat="Books",classroom="None").all())

@app.route("/notes")
def notes():
  return render_template("catigory.html",items=items.query.filter_by(cat="Notes",classroom="None").all())

@app.route("/tech")
def tech():
  return render_template("catigory.html",items=items.query.filter_by(cat="Tech",classroom="None").all())

@app.route("/toys")
def toys():
  return render_template("catigory.html",items=items.query.filter_by(cat="Toys",classroom="None").all())

@app.route("/clothing")
def clothing():
  return render_template("catigory.html",items=items.query.filter_by(cat="Clothing",classroom="None").all())

@app.route("/ss")
def ss():
  return render_template("catigory.html",items=items.query.filter_by(cat="School-Supplies",classroom="None").all())

@app.route("/sports")
def sports():
  return render_template("catigory.html",items=items.query.filter_by(cat="Sports",classroom="None").all())

@app.route("/gift")
def gift():
  global username
  if username==False:
    return redirect("/")
  else:
    if request.method=="POST":
      pass
    else:
      return render_template("gift.html")


@app.route("/search/<string:store>")
def search(store):
  try:
    a=items.query.filter_by(author=store).all()[0]
    return render_template("search.html",items=items.query.filter_by(author=store).all(),username=store)
  except:
    return "Sorry,we couldn't find this store. "

@app.route("/create_class",methods=["POST","GET"])
def create_class():
  global username
  global account
  if username==False:
    return redirect("/")
  else:
    if account=="teacher_account":
      if request.method=="POST":
        try:
          class_name=request.form["class_name"]
          money_name=request.form["money_name"]
          class_code=request.form["class_code"]
          test=classrooms.query.filter_by(class_code=class_code).all()[0].class_code
          return "Sorry,this class code has already been taken taken"
        except:
          teacher_id=users.query.filter_by(username=username).all()[0].id
          data=classrooms(teacher_id=teacher_id,class_name=class_name,money_name=money_name,class_code=class_code)
          db.session.add(data)
          db.session.commit()
          users.query.filter_by(username=username).all()[0].classroom=classrooms.query.filter_by(class_code=class_code).all()[0].id
          db.session.commit()
          return "Your new classroom's code is "+class_code
      else:
        return render_template("create_class.html")
    else:
      return redirect(account)

@app.route("/join_class/<string:classcode>",methods=["POST","GET"])
def join_class(classcode):
  global username
  global classroom
  if username==False:
    return "Please, Sign In to join a classroom."
  else:
    if users.query.filter_by(username=username).all()[0].classroom==classcode:
      return "You have already joined this classroom.."
    try:#IndexError: list index out of range
      test=classrooms.query.filter_by(class_code=classcode).all()[0]
      data=classroom_users(id=classrooms.query.filter_by(class_code=classcode).all()[0].id,student_id=users.query.filter_by(username=username).all()[0].id,cash=0)
      db.session.add(data)
      db.session.commit()
      users.query.filter_by(username=username).all()[0].classroom=classrooms.query.filter_by(class_code=classcode).all()[0].id
      db.session.commit()
      return redirect("/class")
    except:
      return "Sorry couldn't find classroom with class code:"+classcode

@app.route("/class",methods=["GET","POST"])
def classroom1():
  global username
  global classroom
  global account
  if username==False:
    return redirect("/")
  else:
    classroom=users.query.filter_by(username=username).all()[0].classroom
    if classroom=="None":
      return redirect("/")
    else:
      if request.method=='POST':
        if username==False:
          return "Please Sign in to create an item..."
        else:
          title=request.form['title']
          price=request.form['price']
          img=request.form['img']
          dis=request.form['dis']
          cat=request.form['cat']
          amount=int(request.form['amount'])
          new_item=items(title=title,price=price,img=img,dis=dis,return_day=7,author=username,cat=cat,amount=amount,classroom=classroom)
          db.session.add(new_item)
          db.session.commit()
          return "You have just published a new item!"
      else:
        all_items=items.query.filter_by(classroom=classroom).all()
        return render_template(account+".html",items=all_items,classroom=classroom)

@app.route("/buy/<int:classroom1>/<int:item_id>")
def class_buy(classroom1,item_id):
  global account
  global username
  id=int(item_id)
  my_cash=classroom_users.query.filter_by(student_id=users.query.filter_by(username=username).all()[0].id).all()[0].cash
  if username==False:
    return redirect("/")
  else:

      if my_cash>items.query.filter_by(id=id).all()[0].price:
        #Subtracting & Adding Cash
        my_cash=my_cash-items.query.filter_by(id=id).all()[0].price
        author=classroom_users.query.filter_by(student_id=users.query.filter_by(username=items.query.filter_by(id=id).all()[0].author).all()[0].id)
        author_cash=classroom_users.query.filter_by(student_id=users.query.filter_by(username=items.query.filter_by(id=id).all()[0].author).all()[0].id).all()[0].cash
        author_cash=author_cash+items.query.filter_by().all()[0].price
        items.query.filter_by().all()[0].amount=items.query.filter_by().all()[0].amount-1
        db.session.commit()
        #Adding to Transaction
        db.session.add(tran(buyer_id=users.query.filter_by(username=username).all()[0].id,seller_id=users.query.filter_by(username=author).all()[0].id,product_id=id,price=items.query.filter_by(id=id).all()[0].price,classroom=users.query.filter_by(username=username).all()[0].classroom))
        db.session.commit()

        #Deleting Item
        if items.query.filter_by().all()[0].amount==0:
          db.session.delete(items.query.get(id))
          db.session.commit()
        return redirect(account)
      else:
        return "Sorry, you don't have enough cash to buy this item."


@app.route("/join_school/<string:code>")
def join_school(code):
  global username
  global account
  if username==False:
    return redirect("/")
  else:
    try:#If school code exists ; is valid
      school_id=schools.query.filter_by(school_code=code).all()[0].id
      #Adding to users table school_id
      users.query.filter_by(username=username).all()[0].school_id=school_id
      db.session.commit()
      #Making student a teacher
      users.query.filter_by(username=username).all()[0].person="Teacher"
      #Commit data
      db.session.commit()
      #Change Account
      account="teacher_account"
      #Return as teacher
      return redirect("teacher_account")
    except:
      return "Sorry,this school dosn't exist."
#If school isn't created
@app.route("/create_school",methods=["POST","GET"])
def create_school():
  global username
  global account
  if account=="admin_account":
    if users.query.filter_by(username=username).all()[0].school_id=="None":
      if request.method=="POST":
        school_name=request.form["school_name"]
        school_code=request.form["school_code"]
      #Put in DB(schools)
        try:#If this id dosn't exist then it can't get first value
          a=schools.query.filter_by(school_code=school_code).all()[0]
          return "Sorry, this code was already taken."
        except:
          #Add to school table
          db.session.add(schools(admin_id=users.query.filter_by(username=username).all()[0].id,school_code=school_code,school_name=school_name))
          db.session.commit()
          #Add to user table
          users.query.filter_by(username=username).all()[0].school_id=schools.query.filter_by(school_code=school_code).all()[0].id
          db.session.commit()
          return redirect("/school")
      else:
        return render_template("create_school.html")
    else:
      return redirect(account)
  else:
    return redirect(account)
@app.route("/school",methods=["POST","GET"])
def school():
  global username
  global account
  if username==False:
    return redirect("/")
  if account=="student_account":
    return redirect("student_account")
  if account=="teacher_account":
    return redirect("teacher_account")
  if users.query.filter_by(username=username).all()[0].school_id=="None":
    return redirect("create_school")     
  else:
    return render_template("admin_account.html",teachers=users.query.filter_by(school_id=users.query.filter_by(username=username).all()[0].school_id).all())


@app.route("/class_tranascation")
def class_tran():
  global username
  global account
  if username=="False":
    return redirect("/")
  if account=="teacher_account":
    classroom=users.query.filter_by(usrename=username).all()[0].classroom
    transaction=tran.query.filter_by(classroom=classroom).all()
    return render_template("class_transaction.html",transactions=transaction)





def run():
  app.run(host='0.0.0.0', port=8080) 
def keep_alive():  
    t = Thread(target=run)
    t.start()
keep_alive()