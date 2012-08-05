import tornado.ioloop
from tornado.web import *
from memes_db import *
import stamper
import os

#########################
# Set up sqlite3        #
#########################

#########################
# Configuration options #
#########################

tornado_settings = {
  'debug': True,        # server reloads code, don't have to manually restart
  'port' : 8888,
  'cookie_secret': '61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=',

   # Paths
   'template_path' : os.path.join(os.path.dirname(__file__), "templates"),
   'static_path'   : os.path.join(os.path.dirname(__file__), "static"),
}

#########################
# Handlers              #
#########################

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class MainHandler(BaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
        name = tornado.escape.xhtml_escape(self.current_user)
        self.redirect("user/" + name)
        
class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html")
            
    def post(self):
        self.set_secure_cookie("user", self.get_argument("name"))
        self.redirect("/")
        
class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect("/")

class MemeHandler(BaseHandler):
    def get(self,name):
        meme = cursor.execute("""
              select * from pictures
              where owner = '{0}'
              order by id desc
              limit 1
              """.format(name)).fetchone()
        self.render("show_memes.html",name=name,meme=meme)
        
    def post(self,name):
        top_text = self.get_argument("top")
        bottom_text = self.get_argument("bottom")
        img_path = self.get_argument("chosen_picture")
        img = stamper.meme_stamp(img_path,top_text,bottom_text)
       
        row = cursor.execute("""
            select max(id) from pictures
        """).fetchone()
        
        max_id = row["max(id)"]
        if max_id == None:
            max_id = 1
        
        img_name = "/static/img/user_memes/" + name + str(max_id)
        img.save(os.getcwd() + img_name,"JPEG")
        cursor.execute("""
          insert into pictures
          VALUES (NULL,'{0}', '{1}')
          """.format(name,img_name))
        connection.commit
        self.redirect("/user/" + name)

############################
# Routes                   #
############################

application = tornado.web.Application(
  [
    # Handlers
    (r"/", MainHandler),
    (r"/login", LoginHandler),
    (r"/logout", LogoutHandler),
    (r"/user/([a-zA-Z0-9]+)", MemeHandler)
  ],
    # App settings
    **tornado_settings
)

if __name__ == "__main__":
    application.listen(tornado_settings['port'])
    tornado.ioloop.IOLoop.instance().start()
