#!/usr/bin/env python
# -*- coding: utf-8 -*-
from requests import post
import os
import logging


key = os.environ["kongKey"]
secret = os.environ["kongSecret"]
kongadminapi = os.environ["kongAdminAPI"]
username = os.environ["UserName"]
writepassword = os.environ["WritePassword"]

logging.getLogger("requests").setLevel(logging.WARNING)


class CreateApis:
    def __init__(self, username, kongadminapi, writepassword):
        self.username = username
        self.kongadminapi = kongadminapi
        self.writepassword = writepassword

    def add_influxdb_apis(self):
        name = self.username + "-influxdb"
        upstream_url = "http://" + name + ".default"
        request_host = self.username + ".i.orangesys.io"
        posturl = self.kongadminapi + "/apis"
        data = {
            'name': name,
            'upstream_url': upstream_url,
            'request_host': request_host
        }
        return True if post(posturl, data=data).status_code == 201 else False

    def add_grafana_apis(self):
        name = self.username + "-grafana"
        upstream_url = "http://" + name + ".default"
        request_host = self.username + ".g.orangesys"
        posturl = self.kongadminapi + "/apis"
        data = {
            'name': name,
            'upstream_url': upstream_url,
            'request_host': request_host
        }
        return True if post(posturl, data=data).status_code == 201 else False

    def enable_jwt(self):
        posturl = self.kongadminapi + \
            "/apis/" + self.username + "-influxdb/plugins"
        data = {'name': 'jwt'}
        return True if post(posturl, data=data).status_code == 201 else False

    def enable_correlation_id(self):
        posturl = self.kongadminapi + \
            "/apis/" + self.username + "-influxdb/plugins"
        data = {
            'name': 'correlation-id',
            'config.header_name': 'Orangesys-Request-ID',
            'config.generator': "uuid#counter",
            'config.echo_downstream': 'false'
        }
        return True if post(posturl, data=data).status_code == 201 else False

    def request_transformer(self):
        posturl = self.kongadminapi + \
            "/apis/" + self.username + "-influxdb/plugins"
        querystring = "u:_write,p:" + self.writepassword
        data = {
            'name': 'request-transformer',
            'config.remove.querystring': 'jwt',
            'config.add.querystring': querystring
        }
        return True if post(posturl, data=data).status_code == 201 else False


class CreateJwtToken:
    def __init__(self, username, kongadminapi, key, secret):
        self.username = username
        self.kongadminapi = kongadminapi
        self.key = key
        self.secret = secret

    def add_consumer(self):
        posturl = self.kongadminapi + "/consumers"
        data = {'username': self.username}
        return True if post(posturl, data=data).status_code == 201 else False

    def add_jwt(self):
        posturl = self.kongadminapi + "/consumers/" + self.username + "/jwt"
        data = {
            'key': self.key,
            'secret': self.secret
        }
        return True if post(posturl, data=data).status_code == 201 else False


def main():
    FORMAT = '%(asctime)s %(levelname)s %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.INFO)
    c = CreateApis(username, kongadminapi, writepassword)
    if c.add_influxdb_apis() and c.add_grafana_apis():
        c.enable_jwt()
        c.enable_correlation_id()
        c.request_transformer()
        logging.info("create %s api to kong", username)
    j = CreateJwtToken(username, kongadminapi, key, secret)
    if j.add_consumer():
        j.add_jwt()
        logging.info("create %s jwt token to kong", username)


if __name__ == '__main__':
    main()
