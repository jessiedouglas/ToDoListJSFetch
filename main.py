import webapp2
import os
import json
import jinja2
from google.appengine.ext import ndb

jinja_current_directory = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class ListItem(ndb.Model):
    content = ndb.TextProperty()

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_current_directory.get_template(
            'templates/fetch_list.html')
        self.response.write(template.render())

class ListItemsHandler(webapp2.RequestHandler):
    def get(self):
        """Gets a list of all list items from the database
        and sends it back as json.
        """
        list_items = ListItem.query().fetch()

        # ListItem objects are too complicated for json!
        # Just send back content strings
        list_items_strings = []
        for item in list_items:
            list_items_strings.append(item.content)

        # Turn our list into a json response string that the
        # browser can recognize when we send it
        list_items_json = json.dumps(list_items_strings)
        # Let the browser know we're sending back json
        self.response.headers['Content-Type'] = 'application/json'
        # Send the information!
        self.response.write(list_items_json)

        print 'We sent the json!!!!'

class ToDoHandler(webapp2.RequestHandler):
    def get(self):
        template_vars = {
            'list_items': ListItem.query().fetch()
        }
        template = jinja_current_directory.get_template(
            'templates/todo_list.html')
        self.response.write(template.render(template_vars))

    def post(self):
        item_text = self.request.get('list_item')
        list_item = ListItem(content=item_text)
        list_item.put()

        """Everything below this line is old news"""
        # all_list_items = ListItem.query().fetch()
        #
        # Need to append new list item ourselves because
        # Datastore isn't immediately consistent
        # all_list_items.append(list_item)
        #
        # template_vars = {
        #     'list_items': all_list_items
        # }
        # template = jinja_current_directory.get_template(
        #     'templates/todo_list.html')
        # self.response.write(template.render(template_vars))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/todo', ToDoHandler),
    ('/list_items', ListItemsHandler),
], debug=True)
