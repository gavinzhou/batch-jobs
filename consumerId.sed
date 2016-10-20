  - host: ID.i.orangesys.io
    http:
      paths:
      - backend:
          serviceName: orangesys-kong-proxy
          servicePort: 80
        path: /
