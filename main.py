
from flask import Flask, render_template, url_for, request, redirect,session,jsonify,json,g,Response
app = Flask(__name__,template_folder="templates")
app.secret_key = 'pranav'
from urllib.parse import urlparse, parse_qs
import pymongo
from pymongo import MongoClient
error_message=""



cluster =MongoClient("mongodb+srv://pranav292005:Pranav123@cluster0.ynepebw.mongodb.net/?retryWrites=true&w=majority")
db = cluster["newsletter"]

mycol=db["signup"]
mycol1=db["newsletter_details"]
# mycol1=db["project"]
# mycol2=db["finished_project"]

#
# cluster =MongoClient("mongodb+srv://pranav292005:Pranav123@cluster0.ynepebw.mongodb.net/?retryWrites=true&w=majority")
# db = cluster["employee"]



@app.route("/",methods=["GET","POST"])
def signin():

  return render_template('sign_in.html',error_message=error_message)

@app.route("/reviews",methods=["GET","POST"])
def reviews():
  x=[]
  feed=[]
  total=mycol1.find()
  for i in total:
    x=i['reviews']
    feed=i['feedback']



  return render_template('reviews.html',review=x,feed=feed)

@app.route("/product",methods=["GET","POST"])
def product():

  return render_template('products.html')

@app.route("/apply",methods=["GET","POST"])
def apply():

  return render_template('jobs.html')


@app.route("/feedback",methods=["GET","POST"])
def feedback():
  feedback_message=request.form.get("feedback")
  total=mycol1.find()
  x=[]
  for i in total:
    x=i['feedback']
  x.append(feedback_message)
  query = {}  # Empty query matches all documents
  update = {'$set': {'feedback': x}}  # Set the variable to a new value
  mycol1.update_one(query, update)

  msg="Feedback submitted successfully.... "
  error_message=''
  return render_template('sign_in.html',error_message=error_message,msg=msg)



@app.route("/sign_up.html",methods=["GET","POST"])
def signup():
  return render_template('sign_up.html')



@app.route("/complete_signup",methods=["GET","POST"])
def complete_signup():
  parsed_url = urlparse(request.url)
  query_params = parse_qs(parsed_url.query)

  # Get the value of a specific parameter
  param_name = 'form_name'
  form_name = query_params.get(param_name, None)
  st = ''


  if form_name:
    for i in form_name:
      st = i


    if st == 'form2':

      new_name = request.args.get("name")
      new_id = request.args.get("id")
      new_password = request.args.get("password")
      con_pass = request.args.get("password1")
      if (new_password != con_pass):
        message = "The passwords you entered do not match. Please try again."
        return render_template('sign_up.html', error=message)
      elif (len(new_password) < 8):
        message = "Password should be minimum of length 8 characters"
        return render_template('sign_up.html', error=message)
      else:
        cap_count = 0
        special_count = 0
        numeric_count = 0
        for i in new_password:
          if (i.isupper()):
            cap_count += 1
          elif (i.isnumeric()):
            numeric_count += 1
          elif (i in ['@', '#', '$', '*']):
            special_count += 1
        if (cap_count == 0):
          message = 'Password should contain atleast one capital letter'
          return render_template('sign_up.html', error=message)
        elif (special_count == 0):
          message = 'Password should contain atleast one special character'
          return render_template('sign_up.html', error=message)

        elif (numeric_count == 0):
          message = 'Password should contain atleast one numeric character'
          return render_template('sign_up.html', error=message)

      new_dic = {
        "name": new_name,
        "email": new_id,
        "password": new_password,
        "admin": 0
      }
      mycol.insert_one(new_dic)

      return render_template('sign_in.html', error_message='')
    elif st == 'form3':

      new_name = request.args.get("name")
      new_id = request.args.get("id")
      new_password = request.args.get("password")
      con_pass = request.args.get("password1")
      if (new_password != con_pass):
        message = "The passwords you entered do not match. Please try again."
        return render_template('sign_up.html', error=message)
      elif (len(new_password) < 8):
        message = "Password should be minimum of length 8 characters"
        return render_template('sign_up.html', error=message)
      else:
        cap_count = 0
        special_count = 0
        numeric_count = 0
        for i in new_password:
          if (i.isupper()):
            cap_count += 1
          elif (i.isnumeric()):
            numeric_count += 1
          elif (i in ['@', '#', '$', '*']):
            special_count += 1
        if (cap_count == 0):
          message = 'Password should contain atleast one capital letter'
          return render_template('sign_up.html', error=message)
        elif (special_count == 0):
          message = 'Password should contain atleast one special character'
          return render_template('sign_up.html', error=message)

        elif (numeric_count == 0):
          message = 'Password should contain atleast one numeric character'
          return render_template('sign_up.html', error=message)

      new_dic = {
        "name": new_name,
        "email": new_id,
        "password": new_password,
        "admin": 1
      }
      mycol.insert_one(new_dic)

      return render_template('sign_in.html', error_message='')




@app.route("/validate_signin",methods=["POST"])
def validate_signin():
  if request.method == "POST":
    userinfo=mycol.find()
    email=request.form.get("mail")
    password=request.form.get("password")


    for i in userinfo:
      if email == i['email']:

        if password == i['password']:

          admin=i['admin']

          if(admin==0):

              if mycol1.count_documents({}) == 0:
                  return render_template('index.html',top_performer="",job_openings="",reviews="",new_products="",manager_message="",best_team="",blogs="",about="")
              else:
                totals=mycol1.find()
                for total in totals:

                  top_performer=total['top_performer']
                  about = total['about']
                  job_openings=total['job_openings']
                  reviews=total['reviews']
                  new_products=total['new_products']
                  manager_message=total['manager_message']
                  best_team=total['best_team']
                  blogs=total['blogs']

                return render_template('index.html',about=about,top_performer=top_performer,job_openings=job_openings,reviews=reviews,new_products=new_products,manager_message=manager_message,best_team=best_team,blogs=blogs)
          else:
            totals = mycol1.find()
            if mycol1.count_documents({}) == 0:
              return render_template('admin.html',job_openings=[],reviews=[],new_products=[],blogs=[])
            else:
              for total in totals:

                top_performer = total['top_performer']
                job_openings = total['job_openings']
                reviews = total['reviews']
                new_products = total['new_products']
                manager_message = total['manager_message']
                best_team = total['best_team']
                blogs = total['blogs']
              return render_template('admin.html',job_openings=job_openings,reviews=reviews,new_products=new_products,blogs=blogs)
    else:
      return render_template('sign_in.html',error_message="Invalid Credentials")



@app.route("/newsletter_details",methods=["GET","POST"])
def newsletter_details():
  deleted_job=request.form.getlist('deleted_job')
  deleted_blog=request.form.getlist('deleted_blog')
  deleted_review=request.form.getlist('deleted_review')
  deleted_prod=request.form.getlist('deleted_prod')


  error_message=''
  top_performer = request.form.get("top_performer")
  total_jobs = request.form.get("no_job")
  total_reviews = request.form.get("no_reviews")
  total_products = request.form.get("no_prod")
  message_manager = request.form.get("message_manager")
  best_team = request.form.get("best_team")
  total_blogs = request.form.get("no_blog")
  about_company = request.form.get("about_company")



  job_data = []
  reviews_data = []
  products_data=[]
  blogs_data=[]

  if(len(total_jobs)!=0):
    for i in range(int(total_jobs)):
      job_data.append(request.form[f'input-{i + 1}'])
  if (len(total_reviews) != 0):
    for i in range(int(total_reviews)):
      reviews_data.append(request.form[f'step-{i + 1}'])
  if (len(total_products) != 0):
    for i in range(int(total_products)):
      products_data.append(request.form[f'Prod-{i + 1}'])
  if (len(total_blogs) != 0):
    for i in range(int(total_blogs)):
      blogs_data.append(request.form[f'Blog-{i + 1}'])

  if mycol1.count_documents({})==0:
    ans=[]

    details={
      "top_performer":top_performer,
      "job_openings":job_data,
      "reviews":reviews_data,
      "new_products":products_data,
      "manager_message":message_manager,
      "best_team":best_team,
      "blogs":blogs_data,
      "about":about_company,
      "feedback":ans

    }
    mycol1.insert_one(details)
    return render_template('sign_in.html', error_message=error_message)

  else:
    if (len(about_company) != 0):
      query = {}  # Empty query matches all documents
      update = {'$set': {'about': about_company}}  # Set the variable to a new value
      mycol1.update_one(query, update)
    if(len(top_performer)!=0):
      query = {}  # Empty query matches all documents
      update = {'$set': {'top_performer':top_performer}}  # Set the variable to a new value
      mycol1.update_one(query, update)
    if(len(job_data)!=0 or len(deleted_job)!=0):
      query = {}  # Empty query matches all documents
      total=mycol1.find()
      for i in total:

        initial_jobs=i['job_openings']

      if len(deleted_job) != 0:

        for value in deleted_job:
          if value in initial_jobs:
            initial_jobs.remove(value)
      if len(job_data) != 0:
        for i in job_data:
          initial_jobs.append(i)




      update = {'$set': {'job_openings': initial_jobs}}  # Set the variable to a new value
      mycol1.update_one(query, update)

    if(len(reviews_data)!=0 or len(deleted_review)!=0):
      query = {}  # Empty query matches all documents

      total = mycol1.find()
      for i in total:
        initial_reviews = i['reviews']

      if len(deleted_review) != 0:

        for value in deleted_review:
          if value in initial_reviews:
            initial_reviews.remove(value)
      if len(reviews_data) != 0:
        for i in reviews_data:
          initial_reviews.append(i)

      update = {'$set': {'reviews': initial_reviews}}  # Set the variable to a new value
      mycol1.update_one(query, update)


    if (len(products_data) != 0 or len(deleted_prod) !=0):
      query = {}  # Empty query matches all documents

      total = mycol1.find()
      for i in total:
        initial_prod = i['new_products']

      if len(deleted_prod) != 0:

        for value in deleted_prod:
          if value in initial_prod:
            initial_prod.remove(value)
      if len(products_data) != 0:
        for i in products_data:
          initial_prod.append(i)

      update = {'$set': {'new_products': initial_prod}}  # Set the variable to a new value
      mycol1.update_one(query, update)

    if (len(message_manager) != 0):
      query = {}  # Empty query matches all documents
      update = {'$set': {'manager_message': message_manager}}  # Set the variable to a new value
      mycol1.update_one(query, update)

    if (len(best_team) != 0):
      query = {}  # Empty query matches all documents
      update = {'$set': {'best_team': best_team}}  # Set the variable to a new value
      mycol1.update_one(query, update)
    if (len(blogs_data) != 0 or len(deleted_blog)!=0):
      query = {}  # Empty query matches all documents

      total = mycol1.find()
      for i in total:
        initial_blogs = i['blogs']

      if len(deleted_blog) != 0:

        for value in deleted_blog:
          if value in initial_blogs:
            initial_blogs.remove(value)
      if len(blogs_data) != 0:
        for i in blogs_data:
          initial_blogs.append(i)

      update = {'$set': {'blogs': initial_blogs}}  # Set the variable to a new value
      mycol1.update_one(query, update)
    return render_template('sign_in.html', error_message=error_message)







@app.route("/sign_out",methods=["GET","POST"])
def signout():

    error_message=''
    return render_template('sign_in.html',error_message=error_message)


if __name__ == "__main__":
  app.run(debug=True)