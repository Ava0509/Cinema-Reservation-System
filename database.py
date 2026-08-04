import mysql.connector as mc
import config

con = mc.connect(host = "localhost",            # Connection Object
                 user = "root",                 
                 password = config.PASSWORD,
                 database = "Cinema_DB")
