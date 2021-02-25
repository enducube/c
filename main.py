#burgus ababfhjebhfjbvewhfvwefvwhdfhsfgwgy

"""
swgdfsdfx
"""
from flask import Flask, render_template, abort, Response, url_for, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, HiddenField
from wtforms.validators import InputRequired
import sqlite3 as sql3 
import random


class  createPost(FlaskForm):
    title = StringField('title',validators=[InputRequired()])
    content = TextAreaField('cont',validators=[InputRequired()])

class replyToPost(FlaskForm):
    idd = HiddenField()
    content = StringField('cont',validators=[InputRequired()])

class  deletePost(FlaskForm):
    id = HiddenField()

app = Flask(__name__)
app.config['WTF_CSRF_ENABLED'] = False



@app.route("/",methods=['get','POST'])
def index():

    con = sql3.connect('db/posts.db')
    cur = con.cursor()


    form = createPost()
    deltform = deletePost()
    rform = replyToPost()


    if form.validate_on_submit(): #create post
        print(form.title.data)
        cur.execute("INSERT INTO posts VALUES (?,?,?)",(None,form.title.data,form.content.data))
        con.commit()
        return redirect(url_for('index'))
    if rform.validate_on_submit(): #reply
      cur.execute("INSERT INTO replies VALUES (?,?,?)",(None, rform.idd.data,rform.content.data))
      con.commit()
      return redirect(url_for('index'))

    if deltform.validate_on_submit():
      print(deltform.id.data + " was delted")
      cur.execute("DELETE FROM posts WHERE id=?",(deltform.id.data,))
      cur.execute("DELETE FROM replies WHERE post_id=?",(deltform.id.data,))
      con.commit()
      return redirect(url_for('index'))
    
    cur.execute("SELECT * FROM posts")
    data = cur.fetchall()
    data.reverse()
    cur.execute("SELECT * FROM replies")
    rdata = cur.fetchall()
    cur.close()
    return render_template('index.html', form=form,deltform=deltform,rform=rform,data=data,rdata=rdata)

@app.route('/posts',methods=['get','POST'])
def posts():
    con = sql3.connect('db/posts.db')
    cur = con.cursor()
    deltform = deletePost()
    rform = replyToPost()

    if rform.validate_on_submit(): #reply
      cur.execute("INSERT INTO replies VALUES (?,?,?)",(None, rform.idd.data,rform.content.data))
      con.commit()
      return redirect(url_for('index'))

    if deltform.validate_on_submit():
      print(deltform.id.data + " was delted")
      cur.execute("DELETE FROM posts WHERE id=?",(deltform.id.data,))
      cur.execute("DELETE FROM replies WHERE post_id=?",(deltform.id.data,))
      con.commit()
      return redirect(url_for('index'))
    
    cur.execute("SELECT * FROM posts")
    data = cur.fetchall()
    data.reverse()
    cur.execute("SELECT * FROM replies")
    rdata = cur.fetchall()
    cur.close()
  
    return render_template('cool.html',rdata=rdata,rform=rform,deltform=deltform,data=data)



app.run(port=5000)