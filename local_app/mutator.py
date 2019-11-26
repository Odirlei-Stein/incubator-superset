import flask_login
from pprint import pprint

from flask import Flask, render_template, session
def replace_table_sql(sql,new_name_table,table,sql_table):
    sql = sql.replace(table,new_name_table)
    sql = sql.replace("FROM "+new_name_table,"FROM ({0}) as {1}".format(sql_table,new_name_table))
    return sql

def SQL_QUERY_MUTATOR(sql, username, security_manager,database):
    if str(database) == "Agenda":
        if not security_manager.current_user:
            raise EnvironmentError("User is required to be authenticated")
        sql = replace_table_sql(sql,"agenda_bi_temp","public.agenda_bi","select * from public.agenda_bi where emp_id in (select emp_id from usuario_empresa where usu_id = (select usuario.id from usuario where email ilike '{0}'))".format(security_manager.current_user.email))
    print(database)
    print("MUTATE",sql)
    return sql