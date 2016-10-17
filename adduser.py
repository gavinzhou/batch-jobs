#!/usr/bin/env python
import jwt
import uuid
import urllib
import urllib2
import os


key = os.environ["kongKey"]
secret = os.environ["kongSecret"]
kongadminapi = os.environ["kongAdminAPI"]
username = os.environ["UserName"]
write-password = os.environ["Write-Password"]
username-api = username + "-influxdb"

def post(url, data):
    req = urllib2.Request(url)
    data = urllib.urlenode(data)
    response = urllib2.urlopen(req)
    return response.getcode()


def create_apis(username, kongadminapi):
    name = username + "-influxdb"
    upstream_url = name + "default"
    request_host = username + ".i.orangesys.io"
    posturl = kongadminapi + "/apis"
    data = {
        'name': username,
        'upstream_url': upstream_url,
        'request_host': request_host
    }
    return post(posturl, data)


def enable_jwt(kongadminapi):
    posturl = kongadminapi + "/apis"
    data = { 'name': 'jwt'}
    return post(posturl, data)


def enable_correlation_id(username, kongadminapi):
    posturl = kongadminapi + "/apis/" + username + "-influxdb/plugins"
    data = {
        'name': 'correlation-id',
        'config.header_name': 'Orangesys-Request-ID',
        'config.generator': "uuid#counter",
        'config.echo_downstream': 'false'
    }
    return post(posturl, data)


def request_transformer(username, kongadminapi, write-password):
    posturl = kongadminapi + "/apis/" + username + "-influxdb/plugins"
    querystring = "u:_write,p:" + write-password
    data = {
        'name': 'request-transformer',
        'config.remove.querystring': 'jwt',
        'config.add.querystring': querystring
    }
    return post(posturl, data)


def add_consumer(username, kongadminapi):
    posturl = kongadminapi + "/consumers"
    data = { 'username': username}
    return post(posturl, data)


def add_jwt(username, kongadminapi, key, secret):
    posturl = kongadminapi + "/consumers" + username + "/jwt"
    data = {
        'key': key,
        'secret': secret
    }
    return post(posturl, data)


def main():
    print create_apis(username, kongadminapi)
    print enable_jwt(kongadminapi)
    print enable_correlation_id(username, kongadminapi)
    print request_transformer(username, kongadminapi, write-password)
    print add_consumer(username, kongadminapi)
    print add_jwt(username, kongadminapi, key, secret)


if __name__ == '__main__'
    main()
