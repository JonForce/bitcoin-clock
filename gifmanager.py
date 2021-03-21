import os
import giphy_client
from giphy_client.rest import ApiException
import requests
import random

class GifManager:

    def __init__(self, base_dir, tmp_dir, config):
        self.config = config
        self.idling_dir = os.path.join(base_dir, "idling")
        self.tmp_dir = tmp_dir
        self.giphy = giphy_client.DefaultApi()

    def random_idling_gif(self):
        dir = os.path.join(self.idling_dir, f"{random.randint(0, 5)}.gif")
        return dir

    def grab_gif(self, query: str):
        try:
            api_response = self.giphy.gifs_search_get(self.config['DEFAULT']['SECRET_KEY_GIPHY'], query, limit=1, offset=random.randint(0, 9),
                                                 lang='en',
                                                 fmt='json')
            url = api_response.data[0].images.original.url
            path = os.path.join(self.tmp_dir, f"giphy.gif")
            with open(path, 'wb') as f:
                f.write(requests.get(url).content)
            return path
        except ApiException as e:
            print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)

    # def _create_top_gif_id(self):
    #     _top_gif_id = 0
    #     while os.path.exists(os.path.join(self.tmp_dir, f"{_top_gif_id}.gif")):
    #         _top_gif_id += 1
    #     return _top_gif_id