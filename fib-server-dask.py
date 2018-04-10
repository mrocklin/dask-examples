import tornado.ioloop
import tornado.web
from distributed import Client, default_client

def fib(n):
    if n < 2:
        return n
    else:
        return fib(n - 1) + fib(n - 2)


class FibHandler(tornado.web.RequestHandler):
    async def get(self, n):
        n = int(n)
        future = client.submit(fib, n, pure=False)
        result = await future

        self.write({'n': n, 'fib': result})

def make_app():
    return tornado.web.Application([
        (r"/fib/(\d+)", FibHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(9000)
    client = Client(asynchronous=True)
    tornado.ioloop.IOLoop.current().start()
