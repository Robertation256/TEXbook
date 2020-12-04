from peewee import MySQLDatabase

app_config = {
    "DEBUG": True,
    "SECRET_KEY": "JHASNJKFBSADFBBJBFJWEFWEB",   # app secret
}

user_config = {
    "AUTH_EMAIL": "",   # email for receiving token
    "SMTP_HOST": "smtp.163.com",    # email service host for sending token
    "SMTP_USER": "robertZhangSmtp@163.com",  # email user
    "SMTP_PASS": "JRILLCXVRBKLSLDF",    # pass for accessing pop3 service
}


db_credentials = {
    "DB_DATABASE": "texbook",
    "DB_HOST": "127.0.0.1",
    "DB_ORT": 3306,
}
