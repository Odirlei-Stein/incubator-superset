from flask import redirect, g, flash, request,make_response,session
from flask_appbuilder.security.views import UserDBModelView,AuthDBView
from superset.security import SupersetSecurityManager
from flask_appbuilder.security.views import expose
from flask_appbuilder.security.manager import BaseSecurityManager
from flask_login import login_user, logout_user
import jwt
import os
import logging

class CustomAuthDBView(AuthDBView):
    login_template = 'appbuilder/general/security/login_db.html'

    @expose('/login/', methods=['GET', 'POST'])
    def login(self):
        log = logging.getLogger(__name__)

        redirect_url = self.appbuilder.get_url_for_index
        if request.args.get('redirect') is not None:
            redirect_url = request.args.get('redirect') 

        # if request.args.get("username") and request.args.get("password"):

        if request.args.get('jwt') is not None:
            jwt_token = request.args.get('jwt')
            jwt_key = os.environ.get("APP_JWT_KEY")
            jwt_audience = os.environ.get("APP_JWT_AUDIENCE")
            
            try:
                jwt_data = jwt.decode(jwt_token, jwt_key ,algorithms=['HS256'],verify=True,audience=jwt_audience)
            except Exception as ex:
                log.error(str(ex))
                flash('Não foi possível autenticar. JWT inválido', 'warning')
                return super(CustomAuthDBView,self).login()
 
            user = self.appbuilder.sm.find_user(email=jwt_data["email"])
            
            if user is None:
                given_name = jwt_data["given_name"]
                first_name = given_name.split(" ")[0]
                last_name = " ".join(given_name.split(" ")[1:])

                new_user = self.appbuilder.sm.add_user(
                    username=jwt_data["email"],
                    first_name=first_name,
                    last_name=last_name,
                    email=jwt_data["email"],
                    role=self.appbuilder.sm.find_role("Agenda"),
                    password="".join(jwt_token[0:10])
                )
                if not new_user:
                    flash('Não foi possível autenticar. Erro ao criar novo usuário', 'warning')
                    return super(CustomAuthDBView,self).login()
                user = new_user
                # user = self.appbuilder.sm.find_user(username=username)
                
            login_user(user, remember=False,force=True)
           
            return redirect(redirect_url)
        elif g.user is not None and g.user.is_authenticated:
            return redirect(redirect_url)
        else:
            # flash('Unable to auto login', 'warning')
            return super(CustomAuthDBView,self).login()

class CustomSecurityManager(SupersetSecurityManager):
    authdbview = CustomAuthDBView
    def __init__(self, appbuilder):
        super(CustomSecurityManager, self).__init__(appbuilder)
