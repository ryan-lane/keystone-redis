
import redis
import ssl


class Connection(redis.Connection):


    def __init__(self, *args, **kwargs):
        super(Connection, self).__init__(*args, **kwargs)
        self.ca_certs = kwargs.get('ca_certs', None)
        self.cert_reqs = kwargs.get('cert_reqs', ssl.CERT_REQUIRED)
        self.keyfile = kwargs.get('keyfile', None)
        self.certfile = kwargs.get('certfile', None)


    def _connect(self):
        sock = super(Connection, self)._connect()
        ssl_sock = ssl.wrap_socket(sock, keyfile=self.keyfile,
                                         certfile=self.certfile,
                                         ca_certs=self.ca_certs,
                                         cert_reqs=self.cert_reqs)
        return ssl_sock


# vim:et:fdm=marker:sts=4:sw=4:ts=4
