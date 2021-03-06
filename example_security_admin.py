from flask import Flask
from config import configure_app
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_security import current_user, roles_required
from data.model import db

'''
This example shows how you can restrict access to the flask-admin pages with flask-security.
It assumes there is a database defined in the data/model.py file that has typical users, roles, etc.
'''

app = Flask(__name__)

configure_app(app)
db.init_app(app)


class AdminIndex(AdminIndexView):
    @expose('/')
    @roles_required('admin')
    def index(self):
        return self.render('admin/index.html')

admin = Admin(app, name='Kelvin', template_mode='bootstrap3', index_view=AdminIndex())


class RoleAdmin(ModelView):
    # Prevent administration unless the currently logged-in user has the "admin" role
    def is_accessible(self):
        return current_user.has_role('admin')


show_tables = ['User', 'Role', 'CatPictures']
for table in show_tables:
    admin.add_view(RoleAdmin(getattr(data.model, table), db.session))


if __name__ == '__main__':
    try:
        app.run(debug=app.config['DEBUG'], host=app.config['HOST'], port=app.config['PORT'])
    except Exception as e:
        print e