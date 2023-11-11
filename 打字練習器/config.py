from configparser import configparser

config_object = ConfigParser()
config_object.read("config.ini")

serinfo = config_object("PRACTICE_INFO")
print("Practice_time is {}".format(userinfo["password"]))