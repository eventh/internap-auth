#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
Implementation of the internap authentication token server.
'''
from __future__ import print_function

import logging

from spyne.service import ServiceBase
from spyne.decorator import rpc
from spyne.model.complex import ComplexModel
from spyne.model.primitive import Integer, Unicode
from spyne.util.simple import wsgi_soap_application


StringType = Unicode.customize(type_name='string', nillable=False)


class Authenticate(ComplexModel):
    strAccount = StringType
    strToken = StringType
    strReferrer = StringType
    strSourceURL = StringType
    strClientIP = StringType

    class Attributes(ComplexModel.Attributes):
        nillable = False
        min_occurs = 1


class AuthenticateResponse(ComplexModel):
    AuthenticateResult = Integer.customize(nillable=False, min_occurs=1)

    class Attributes(ComplexModel.Attributes):
        nillable = False
        min_occurs = 1


class Authentication(ServiceBase):

    @rpc(Authenticate, _returns=AuthenticateResponse, _body_style='bare')
    def Authentication(ctx, authenticate):
        return 1


def run():
    from wsgiref.simple_server import make_server
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)
    logging.info("listening to http://127.0.0.1:8000")
    logging.info("wsdl is at: http://localhost:8000/?wsdl")

    wsgi_app = wsgi_soap_application([Authentication],
            'http://vitalstream.com/webservices', name='AuthenticationSoap')
    server = make_server('127.0.0.1', 8000, wsgi_app)
    server.serve_forever()


if __name__ == '__main__':
    run()
