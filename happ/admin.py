from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView

from happ import db, app
from flask_login import current_user, logout_user
from happ.models import UserRole
from flask_admin import BaseView, expose
from flask import redirect
import dao

class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/')

    def is_accessible(self) -> bool:
        return current_user.is_authenticated

class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')



admin = Admin(app=app, name="Clinic Admin", index_view=MyAdminIndexView())
admin.add_view(LogoutView(name='Logout'))