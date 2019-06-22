import cherrypy
from jinja2 import Environment, FileSystemLoader

from stocks import RedisStore
from config import TEMPLATES_DIR, BASE_DIR, HOST, PORT

env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))


class Server:
    def __init__(self):
        self.redis_store = RedisStore()

    @cherrypy.expose
    def index(self, name=None):
        if cherrypy.request.method == "POST":
            redis_data = self.redis_store.search_stock_by_name(name)
            seq = len(redis_data["ID"])
        else:
            redis_data = self.redis_store.get_top_redis_data()
            seq = len(redis_data["ID"])
        return env.get_template("index.html").render(
            redis_data=redis_data, seq=seq)


if __name__ == "__main__":

    config = {
        "global": {
            "server.socket_host": HOST,
            "server.socket_port": int(PORT)},
        "/assets": {
            "tools.staticdir.root": BASE_DIR,
            "tools.staticdir.on": True,
            "tools.staticdir.dir": "assets",
        },
    }

    cherrypy.quickstart(Server(), "/", config=config)
