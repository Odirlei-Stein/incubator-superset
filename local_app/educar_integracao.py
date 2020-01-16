from flask import redirect, g, flash, request,make_response,session
from flask_appbuilder.security.views import UserDBModelView,AuthDBView
from superset.security import SupersetSecurityManager
from flask_appbuilder.security.views import expose
from flask_appbuilder.security.manager import BaseSecurityManager
from flask_login import login_user, logout_user
import jwt
import os
import educar_connection
import logging
import re

def login_or_create(appbuilder,jwt_token):
    jwt_key = os.environ.get("APP_JWT_KEY_EDUCAR")
    jwt_audience = os.environ.get("APP_JWT_AUDIENCE_EDUCAR")
    try:
        jwt_data = jwt.decode(jwt_token, jwt_key ,algorithms=['HS256'],verify=True,audience=jwt_audience)
    except Exception as ex:
        log.error(str(ex))
        flash('Não foi possível autenticar. JWT inválido', 'warning')
        return None

    user_to_use = jwt_data["username"]+"_"+jwt_data["codigo_educar"]
    user = appbuilder.sm.find_user(username=user_to_use)
    
    if user is None:
        given_name = jwt_data["given_name"]
        first_name = given_name.split(" ")[0]
        last_name = " ".join(given_name.split(" ")[1:])

        new_user = appbuilder.sm.add_user(
            username=user_to_use,
            first_name=first_name,
            last_name=last_name,
            email=jwt_data["email"],
            role=appbuilder.sm.find_role("Educar"),
            password="".join(jwt_token[0:10])
        )
        if not new_user:
            flash('Não foi possível autenticar. Erro ao criar novo usuário', 'warning')
            return null
        user = new_user
        # user = self.appbuilder.sm.find_user(username=username)
        
    login_user(user, remember=False,force=True)
    return True
    
cache_dict = {}
def DB_CONNECTION_MUTATOR(uri, params, username, security_manager, source):
    if str(uri).endswith("educar"):
        #   self.drivername = drivername
        # self.username = username
        # self.password_original = password
        # self.host = host
        # if port is not None:
        #     self.port = int(port)
        # else:
        #     self.port = None
        # self.database = database
        # self.query = query or {}
        user = security_manager.find_user(username=username)
        regex = r"\_(\d+)$"
        result = re.findall(regex,security_manager.current_user.username)
        if len(result) > 0:
            tenant_id = result[0]
            #if tenant_id in cache_dict:
            #    connection_info = cache_dict[tenant_id]
            #else:
            #    connection_info = educar_connection.get_connection_info(tenant_id)
            #    cache_dict[tenant_id] = connection_info
            if connection_info:
                uri.username = connection_info["user"]
                uri.password_original = connection_info["password"]
                uri.host = connection_info["host"]
                uri.database = connection_info["db"]
                uri.port = connection_info["port"]
    return uri, params