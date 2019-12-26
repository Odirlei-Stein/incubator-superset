import psycopg2
import rijndael
import base64
import os



def get_connection_string(oru_codigo):
    connection = None
    try:
        connection = psycopg2.connect(user =  os.environ["EDUCAR_CONNECTION_USER"],
                                    password = os.environ["EDUCAR_CONNECTION_PASSWORD"],
                                    host =os.environ["EDUCAR_CONNECTION_HOST"],
                                    port = os.environ["EDUCAR_CONNECTION_PORT"],
                                    database =os.environ["EDUCAR_CONNECTION_DATABASE"])

        cursor = connection.cursor()
        # Print PostgreSQL Connection properties
        educar_key = os.environ["EDUCAR_PASSWORD_KEY"]
        educar_iv = os.environ["EDUCAR_PASSWORD_IV"]
        # Print PostgreSQL version
        cursor.execute("""select adm_bancodedados.nome as db,adm_servidorbd.host, adm_servidorbd.porta, adm_servidorbd.usuario, convert_from(decrypt_iv(decode(senha,'base64'),digest('{0}','md5'),'{1}','aes'),'utf-8')   from adm_orgaogovernamental
inner join adm_bancodedados on adm_orgaogovernamental.bancosite_id = adm_bancodedados.id
inner join adm_servidorbd on adm_servidorbd.id = adm_bancodedados.servidor_id
where codigoeducar = %s""".format(educar_key,educar_iv),(str(oru_codigo),))
        record = cursor.fetchone()
        if not record:
            return None
        return record

    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
        return None
    finally:
        #closing database connection.
            if(connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")

def get_connection_info(oru_codigo):
    data_in_db = get_connection_string(oru_codigo)
    if not data_in_db:
        return None
    print(data_in_db)
    return {
        'db':data_in_db[0],
        'host':data_in_db[1],
        'port':data_in_db[2],
        'user':data_in_db[3],
        'password':data_in_db[4]
    }