__author__ = 'tyxie'

import ssl as ssl_lib


# TODO: Add support for other type of encryption (SSLv2/SSLv3)
def wrap_socket_patched(sock, keyfile=None, certfile=None,
                        server_side=False, cert_reqs=ssl_lib.CERT_NONE,
                        ssl_version=ssl_lib.PROTOCOL_TLSv1_2, ca_certs=None,
                        do_handshake_on_connect=True,
                        suppress_ragged_eofs=True, ciphers=None):
    return ssl_lib.wrap_socket(sock, keyfile, certfile, server_side,
                            cert_reqs, ssl_version, ca_certs,
                            do_handshake_on_connect,
                            suppress_ragged_eofs, ciphers)