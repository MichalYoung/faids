import flask
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask import current_app
from flask import g
import json
import logging

import CONFIG

###
# Globals
###
app = flask.Flask(__name__)
app.secret_key = CONFIG.key
app.jinja_env.line_statement_prefix = "--JUSTDONT--"

###
# URL handlers
###

@app.route("/")
@app.route("/index")
def index():
  app.logger.debug("Entering index")
  g.s0 = { "kill": "The kill set",
           "out": "The out set",
           "gen": "The in set" }
  return render_template("cfg1.svg")

import avail_questionable  # Figure 6.10

@app.route("/fig6_10")
def fig610():
  app.logger.debug("Figure 6.10, page 89")
  changed, g.out = avail_questionable.init()
  app.logger.debug("g.out: {}".format(g.out))
  return flask.render_template("questionable.svg")
  
@app.route("/advance6_10")
def fig610_advance():
  app.logger.debug("SteppingFigure 6.10, page 89")  
  changed, g.out = avail_questionable.advance()
  app.logger.debug("g.out: {}".format(g.out))
  return flask.render_template("questionable.svg")


###################
#   Error handlers
###################
@app.errorhandler(404)
def error_404(e):
  app.logger.warning("++ 404 error: {}".format(e))
  return render_template('404.html'), 404

@app.errorhandler(500)
def error_500(e):
  app.logger.warning("++ 500 error: {}".format(e))
  assert app.debug == False  # Crash me now! 
  return render_template('500.html'), 500

@app.errorhandler(400)
def error_400(e):
  app.logger.warning("++ 400 error: {}".format(e))
  return render_template('400.html'), 400

#################
#
# Filters used within the templates
#
#################



###
# Other functions (not handlers)
###


print("Deciding whether to run as main")
if __name__ == "__main__":
    print("Running as main")
    from logging import FileHandler
    file_handler = FileHandler("errlog")
    app.logger.setLevel(logging.DEBUG)
    app.logger.addHandler(file_handler)
    app.debug = True
    app.run(port=CONFIG.PORT,host="0.0.0.0")
else:
    print("Running NOT as main")
    from logging import FileHandler
    app.secret_key = '2f3b2716-588c-4c15-a981-0569d91a5b9e'
    file_handler = FileHandler("errlog")
    app.logger.addHandler(file_handler)
    app.debug = True
    
  

    
