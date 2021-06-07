#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pymysql.cursors
import os


# Возвращает строку типа DATE для SQL
def get_date_type(date):
    if date['bday'] == 0:
        return "`0'"
    return str(date['byear']) + '-' + str(date['bmonth']) + '-' + str(date['bday'])


# Информация из config
def get_con_info():
    path = os.path.abspath('')
    info = {}
    path = path[:path.rfind('/')] + '/config.env'
    file = open(path)
    for line in file:
        if line.find('=') != -1:
            info[line[:line.find('=')]] = line[line.find('"')+1:line.rfind('"')]
    return info


def get_connection(info):
    return pymysql.connect(
        host=info['host'],
        user=info['username'],
        password=info['password'],
        db=info['base_name'],
    )


# Сохранение + миграция + комит
def mySQL_save(people, info=None):
    if info == None:
        info_con = get_con_info()
    else:
        info_con = info
    con = get_connection(info_con)
    with con.cursor() as cursor:
        cursor.execute(f"DROP TABLE IF EXISTS `{info_con['temporary_table']}`;")
        cursor.execute(f"CREATE TABLE `{info_con['temporary_table']}` (`last_name` varchar(50) NOT NULL, `first_name` varchar(50) NOT NULL, `middle_name` varchar(50) NOT NULL, `birth_date` date NOT NULL, `position_id` int unsigned NOT NULL, `image_url` varchar(255) DEFAULT NULL, `url` varchar(255) NOT NULL, PRIMARY KEY (`last_name`,`first_name`,`middle_name`,`birth_date`,`position_id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;")
        for person in people:
            sql = f"INSERT IGNORE INTO `{info_con['temporary_table']}` (`last_name`, `first_name`, `middle_name`, `birth_date`, `position_id`, `image_url`, `url`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (person['last_name'][0].upper() + person['last_name'][1:],
                                 person['first_name'][0].upper() + person['first_name'][1:],
                                 person['middle_name'][0].upper() + person['middle_name'][1:],
                                 get_date_type({'bday': person['bday'], 'bmonth': person['bmonth'], 'byear': person['byear']}),
                                 person['position_id'],
                                 person['image_link'],
                                 person['link']
                                 )
                           )
        cursor.execute(f"DELETE LOW_PRIORITY FROM `{info_con['permanent_table']}`;")
        cursor.execute(f"INSERT INTO {info_con['base_name']}.{info_con['permanent_table']} SELECT * FROM {info_con['base_name']}.{info_con['temporary_table']};")
        cursor.execute(f"DROP TABLE IF EXISTS `{info_con['temporary_table']}`;")
    con.commit()


def get_len():
    info = get_con_info()
    con = get_connection(info)
    with con.cursor() as cursor:
        cursor.execute(f"SELECT COUNT(*) FROM `{info['permanent_table']}`")
        length = cursor.fetchall()
    return length[0][0]


a = get_con_info()
