#!/usr/bin/env python
import jwt
import uuid
from requests import post
import os


key = os.environ["kongKey"]
secret = os.environ["kongSecret"]
kongadminapi = os.environ["kongAdminAPI"]
username = os.environ["UserName"]
writepassword = os.environ["WritePassword"]


def add_apis(username, kongadminapi):
    name = username + "-influxdb"
    upstream_url = "http://" + name + ".default"
    request_host = username + ".i.orangesys.io"
    posturl = kongadminapi + "/apis"
    data = {
        'name': name,
        'upstream_url': upstream_url,
        'request_host': request_host
    }
    return True if post(posturl, data=data).status_code == '201' else False


def enable_jwt(username, kongadminapi):
    posturl = kongadminapi + "/apis/" + username + "-influxdb/plugins"
    data = {'name': 'jwt'}
    return post(posturl, data=data)


def enable_correlation_id(username, kongadminapi):
    posturl = kongadminapi + "/apis/" + username + "-influxdb/plugins"
    data = {
        'name': 'correlation-id',
        'config.header_name': 'Orangesys-Request-ID',
        'config.generator': "uuid#counter",
        'config.echo_downstream': 'false'
    }
    return post(posturl, data=data)


def request_transformer(username, kongadminapi, writepassword):
    posturl = kongadminapi + "/apis/" + username + "-influxdb/plugins"
    querystring = "u:_write,p:" + writepassword
    data = {
        'name': 'request-transformer',
        'config.remove.querystring': 'jwt',
        'config.add.querystring': querystring
    }
    return post(posturl, data=data)


def add_consumer(username, kongadminapi):
    posturl = kongadminapi + "/consumers"
    data = { 'username': username}
    return True if post(posturl, data=data).status_code == '201' else False


def add_jwt(username, kongadminapi, key, secret):
    posturl = kongadminapi + "/consumers/" + username + "/jwt"
    data = {
        'key': key,
        'secret': secret
    }
    return post(posturl, data=data)


def main():
    if add_apis(username, kongadminapi):
        enable_jwt(username, kongadminapi)
        enable_correlation_id(username, kongadminapi)
        request_transformer(username, kongadminapi, writepassword)
    if add_consumer(username, kongadminapi):
        add_jwt(username, kongadminapi, key, secret)


if __name__ == '__main__':
    main()
