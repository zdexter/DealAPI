import tornado.ioloop
import tornado.web
import pyes
from tornado.escape import json_encode
from tornado.options import define, options

# In Tornado, each Python module can define some command-line options.
# Here, the elasticsearch server is running on localhost:9200 by default.
define("es", default="127.0.0.1:9200", help="Host:port to the elasticsearch server")

class MainHandler(tornado.web.RequestHandler):
    def initialize(self, es):
        # TODO:  Investigate connection model more and optimize this.
        self.conn = pyes.ES(options.es, timeout=2)
    
    def get(self, merchant_name):
        """
        Takes a merchant name, and returns application/json content
        with a list of the (product,savings) pairs that on file
        for that merchant in our backend.
        """
        try:
            status = self.request.arguments.get('status')[0]
        except TypeError:
            status = None
        
        query = pyes.TermQuery("merchant", merchant_name)
        results = self.conn.search(query=query)
        output = {}
        
        # TODO:  Either show lowest available savings for any given product,
        #           or decide to disallow duplicate entries for the same product.
        for r in results:
            output[r['product']] = r['savings']
        
        self.set_header("Content-Type", "application/json")
        self.write(json_encode(output))
        self.flush()
        self.finish()
        
application = tornado.web.Application([
    (r"/(\w+)", MainHandler, dict(es=options.es)), # Match /merchant_name in URL and pass elasticsearch server to handler
])

if __name__ == "__main__":
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()