import functools
import yaml, os, json
from .util import dict_property

# default config directory if none specified in environment
DEFAULT_CONFIG_DIR = "config"



        

class Config:
    def __init__(self):
        self.data = None
        self.creds = None
        self.loaded = False
        self.read_config()

    @dict_property("config.update-frequency")
    def update_frequency(self): pass
    
    @dict_property("config.server-uri")
    def server_uri(self): pass

    @dict_property("config.default-port")
    def default_port(self): pass

    @dict_property("discord.channel-id")
    def channel_id(self): pass


    def get_token(self):
        return self.creds["token"]


    def read_config(self):
        env_config_dir = os.getenv("RENEGADE_CONFIG_DIR")
        config_dir = env_config_dir if (env_config_dir is not None) else DEFAULT_CONFIG_DIR

        with open(config_dir + "/config.yml", "r") as file:
            self.data = yaml.safe_load(file)
        with open(config_dir + "/creds.yml", "r") as file:
            self.creds = yaml.safe_load(file)

        self.loaded = True


# single config instance
__config = Config()

def get_config():
    global __config
    if __config is None:
        __config = Config()
    return __config

        
        

if __name__ == "__main__":
    DEFAULT_CONFIG_DIR = "../config"
    c = Config()
    print(c.update_frequency)
    c.update_frequency = 5