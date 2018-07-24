import webapp2
import os
import jinja2
from google.appengine.ext import ndb

jinja_current_directory = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class ListItem(ndb.Model):
    content = ndb.TextProperty()

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

        all_list_items = ListItem.query().fetch()
        # Need to append new list item ourselves because
        # Datastore isn't immediately consistent
        all_list_items.append(list_item)

        template_vars = {
            'list_items': all_list_items
        }
        template = jinja_current_directory.get_template(
            'templates/todo_list.html')
        self.response.write(template.render(template_vars))

app = webapp2.WSGIApplication([
    ('/', ToDoHandler),
    ('/todo', ToDoHandler),
], debug=True)
