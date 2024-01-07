import psycopg2
from flask import flash


def connect():
    return psycopg2.connect(user="postgres",
                            password="postgres",
                            host="127.0.0.1",
                            port="5432",
                            database="sarkovka_db")

def get_goods(typecode):
    conn=connect()
    cursor = conn.cursor()
    cursor.execute(f'''select gs.goodsid, gs.goodspicture, gs.goodsprice, gt.goodstypename, gt.goodstypevaluesale, gt.goodstypesale from goods as gs
join goodstype gt on 
gs.goodstypeid=gt.goodstypeid
where gt.goodstypecode='{typecode}' ''')
    goods = cursor.fetchall()
    cursor.close()
    conn.close()
    return goods

def addappointment(tel, msg, items):
    conn=connect()
    cursor = conn.cursor()
    cursor.execute(f'''insert into appointments(clientnumber, msg)
values('{tel}', '{msg}')''')
    conn.commit()
    if len(items)>0:
        cursor.execute(f''' select appointmentid from appointments
    where msg='{msg}' and clientnumber='{tel}'
    order by appointmentid desc
    limit 1;''')
        appid=cursor.fetchone()
        for item in items:
            cursor.execute(f''' insert into appconsist(appointmentid, goodsid)
    values({appid[0]}, 
        (select goodsid from goods
        where goodspicture='{item}'
        limit 1)); ''')
            conn.commit()
    cursor.close()
    conn.close()

def getUserByLogin(login):
    conn=connect()
    cursor = conn.cursor()
    try:
        cursor.execute(f'''select * from admins where login='{login}' limit 1''')
        res = cursor.fetchone()
        if not res:
            return False
        return res
    except:
        flash("Ошибка получения данных")
        return False


def getUser(user_id):
    conn=connect()
    cursor = conn.cursor()
    try:
        cursor.execute(f'''select * from admins where admin_id={user_id} limit 1''')
        res = cursor.fetchone()
        if not res:
            return False
        return res
    except:
        flash("Ошибка получения данных")
        return False
    
def getApps(status):
    conn=connect()
    cursor = conn.cursor()
    try:
        cursor.execute(f'''select appointmentid, msg, clientnumber, adata, DATE_TRUNC('second', atime)
from appointments where status={status}''')
        apps = cursor.fetchall()
        cursor.close()
        conn.close()
        return apps
    except:
        flash("Ошибка получения данных")
        return []

def getImgs(id):
    conn=connect()
    cursor = conn.cursor()
    try:
        cursor.execute(f'''select goods.goodspicture
from appconsist
join goods on appconsist.goodsid=goods.goodsid
where appointmentid={id}''')
        imgs = cursor.fetchall()
        cursor.close()
        conn.close()
        return imgs
    except:
        flash("Ошибка получения данных")
        return False
    
def getEmp():
    conn=connect()
    cursor = conn.cursor()
    try:
        cursor.execute(f'''select * from employees''')
        imgs = cursor.fetchall()
        cursor.close()
        conn.close()
        return imgs
    except:
        flash("Ошибка получения данных")
        return False

def admitapp(appid, empid):
    conn=connect()
    cursor = conn.cursor()
    try:
        cursor.execute(f'''UPDATE appointments
SET employeeid = {empid},
status = true
WHERE appointmentid = {appid};
''')
        conn.commit()
        cursor.close()
        conn.close()
    except:
        flash("Ошибка обновления данных")

def getSkills(empid):
    conn=connect()
    cursor = conn.cursor()
    cursor.execute(f'''SELECT  goodstype.goodstypename from employeeskills
join goodstype on goodstype.goodstypeid=employeeskills.goodstypeid
where employeeid = {empid} ''')
    skills = cursor.fetchall()
    cursor.close()
    conn.close()
    return skills

def registration(login, password):
    conn=connect()
    cursor = conn.cursor()
    try:
        cursor.execute(f'''insert into admins(login,pass)
values ('{login}','{password}')
''')
        conn.commit()
        cursor.close()
        conn.close()
    except:
        flash("Ошибка добавления пользователя")