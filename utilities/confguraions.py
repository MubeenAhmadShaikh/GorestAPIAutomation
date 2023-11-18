import configparser


def get_config():
    config = configparser.ConfigParser()
    config.read("C:\\Users\\Mubeen\\PycharmProjects\\GorestApiAutomation\\conf.ini")
    return config
