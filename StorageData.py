import json
import os
import sys
import sqlite3

keys = ('Id', 'name', 'RG', 'address', 'password')
banco = sqlite3.connect('database.db')
cursor = sqlite3.Cursor(banco)
# cursor.execute('CREATE TABLE user(Id INTEGER PRIMARY KEY,name TEXT NOT NULL,RG INTEGER NOT NULL, address '
#                'TEXTNOT NULL, password TEXT NOT NULL)')
# banco.commit()

users = []
pathname = os.path.dirname(sys.argv[0])
print(pathname)


def create_user(requisition_body):
    user_data = json.loads(requisition_body)
    try:
        params = (
            user_data.get('Id'), user_data.get('name'), user_data.get('RG'), user_data.get('address'),
            user_data.get('password'))
        cursor.execute("INSERT INTO user VALUES(?,?,?,?,?)", params)
        banco.commit()
        cursor.execute("SELECT * FROM user")
        print(cursor.fetchall())
        return (201, "Usuario " + user_data.get('name') + " cadastrado")
    except Exception as e:
        print(e.__str__())
        return (500, e.__str__())


def update_user(requisition_body):
    user_data = json.loads(requisition_body)
    print(user_data)
    if cursor.execute('SELECT * FROM user WHERE Id = ' + user_data.get('Id')).fetchone():
        print(cursor.execute('SELECT * FROM user WHERE Id = ' + user_data.get('Id')).fetchone())
        if user_data.get('name'):
            cursor.execute('UPDATE user SET name = ? WHERE Id = ?', (user_data.get('name'), user_data.get('Id')))
        if user_data.get('rg'):
            cursor.execute('UPDATE user SET RG = ? WHERE Id = ?', (user_data.get('RG'), user_data.get('Id')))
        if user_data.get('address'):
            cursor.execute('UPDATE user SET address = ? WHERE Id = ?', (user_data.get('address'), user_data.get('Id')))
        banco.commit()
        
        print(cursor.execute('SELECT * FROM user WHERE Id = ' + user_data.get('Id')).fetchone())
        return(200, "Dados do usuario " + user_data.get('name') + " Atualizados")
    else:
        return (404, "Usuario " + user_data.get('Id') + " não encontrado")


def list_all_users():
    print("Listall users")
    try:
        cursor.execute("SELECT * FROM user")
        rows = cursor.fetchall()
        print(rows)
        # try:
        result = []
        for row in rows:
            result.append(dict(zip(keys, row)))
        return (200,json.dumps(result))
    except Exception as e:
        print(e.__str__())
        return (500, e.__str__())


def list_one_user(id):
    try:
        print("SELECT * FROM user WHERE Id = " + id)
        cursor.execute("SELECT * FROM user WHERE Id = " + id)
        row = cursor.fetchone()
        return (200, json.dumps(dict(zip(keys, row))))
    except Exception as e:
        print(e.__str__())
        return (404,"Usuario Não Encontrado")



def delete_user(id):
    try:
        name = cursor.execute("SELECT name FROM user WHERE id = " + id).fetchone()
        print(name)
        if name:
            print("deletar")
            print(name[0])
            cursor.execute("DELETE FROM user WHERE Id = " + id)
            cursor.execute("SELECT * FROM user")
            banco.commit()
            return(200,"Usuario "+ name[0] + " deletado")
        else:
            return (404, "Usuario Não Encontrado")
    except Exception as e:
        print(e.__str__())
        return (500,e.__str__())


def check_password(requisition_body):
    try:
        requisition_json = json.loads(requisition_body)
        print(requisition_json.get('Id'))
        password = cursor.execute("SELECT password FROM user WHERE Id = " + requisition_json.get('Id')).fetchone()
        print(password[0])
        print(requisition_json.get('Password'))
        if password:
            if requisition_json.get('Password') == password[0]:
                return (200,"Autenticado")
            else:
                return (400, "Não Autenticado Senhas não conferem")
        else:
            return (404, "Usuario Não Encontrado")

    except Exception as e:
        print(e.__str__())
        return (500,e.__str__())


def update_password(requisition_body):
    try:
        requisition_json = json.loads(requisition_body)
        password = cursor.execute("SELECT  password FROM user WHERE Id = " + requisition_json.get('Id')).fetchone()[0]
        if password:
            if requisition_json.get('oldPassword') == password:
                print(cursor.execute('SELECT * FROM user WHERE Id = ' + requisition_json.get('Id')).fetchone())
                cursor.execute(
                    'UPDATE user SET password = ' + requisition_json.get('NewPassword') + ' WHERE Id = ' + requisition_json.get(
                        'Id'))
                banco.commit()
                print(cursor.execute('SELECT * FROM user WHERE Id = ' + requisition_json.get('Id')).fetchone())
            else:
                return (401, "A senha antiga precisa estar correta para que seja atualizada")

        else:
            return (404, "Usuario Não Encontrado")
    except Exception as e:
        print(e.__str__())
        return (500,e.__str__())
