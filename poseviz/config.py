import pickle

PICKLE_FILE = './poseviz_config.pickle'

class Config:
    def __init__(self):
        # a dict to store the config data
        self.data = {}

        # load the config data from pickle file
        self._load_config()

    def set(self, key, value):
        self.data[key] = value
        self._save_config()

    def get(self, key):
        return self.data.get(key, None)
    
    def _save_config(self):
        # save the config data to pickle file
        with open(PICKLE_FILE, 'wb') as f:
            pickle.dump(self.data, f)

    def _load_config(self):
        # attempt to load the config data from pickle file
        try:
            with open(PICKLE_FILE, 'rb') as f:
                self.data = pickle.load(f)
        except:
            # not doing anything if the file does not exist
            pass