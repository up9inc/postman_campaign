# UP9 Mocks

This directory contains generated mocks for your services using [UP9](https://up9.com) [Mockintosh](https://github.com/up9inc/mockintosh) mock engine

### File structure 

- [mockintosh.yml](/mockintosh.yml) - main file with all mocked endpoints
- [mock-data](/mock-data) - a directory that contains response payloads.
- [docker-compose.yml](/docker-compose.yml) - Easy way to spin up all services as mocks

## Running Mockintosh as single process

### Using Docker
Each service will use a different port from 8000 and above, be sure to supply enough ports to docker command:

1. ``docker run -it -p 8000-8005:8000-8005 -v `pwd`:/tmp testrio/mockintosh /tmp/mockintosh.yml``

### Running locally
Each service will use a different port from 8000 and above.

Install the software and run mockintosh:
1. `pip3 install mockintosh`
2. `mockintosh mockintosh.yml`

### Sample
```>> mockimockintosh mockintosh.yml
[2021-02-02 13:34:17,775 root INFO] Mockintosh v0.6.2 is starting...
[2021-02-02 13:34:17,775 root INFO] Reading configuration file from path: mockintosh.yml
[2021-02-02 13:34:17,810 root INFO] Configuration file is a valid YAML file.
[2021-02-02 13:34:17,817 root INFO] Configuration file is valid according to the JSON schema.
[2021-02-02 13:34:17,920 root INFO] Serving at http://localhost:8001 the mock for 'http://carts'
...
[2021-02-02 13:34:17,921 root INFO] Serving at http://localhost:8008 the mock for 'http://user'
[2021-02-02 13:34:17,921 root INFO] Serving at http://localhost:8009 the mock for 'http://zipkin'
[2021-02-02 13:34:17,921 root INFO] Mock server is ready!
```

## Running Mockintosh as multiple services

We provide out-of-the-box instructions with Docker Compose. Instructions for Kubernetes and others are coming.

### Using Docker Compose
Docker compose mimics a user docker-compose file with each service ready-to-be replaced by an actual service.
`docker-compose up -d`

### Sample
```
>> docker-compose up
Creating network "mocks_default" with the default driver
Creating mocks_orders_1      ... done
...
Creating mocks_catalogue_1   ... done
Creating mocks_kafka_1       ... done
Attaching to mocks_edge-router_1, mocks_shipping_1, mocks_kafka_1, mocks_user_1, mocks_catalogue_1, mocks_zipkin_1, mocks_orders_1, mocks_front-end_1, mocks_payment_1, mocks_carts_1
edge-router_1  | [2021-02-02 21:42:01,778 root INFO] Mockintosh v0.6.2 is starting...
kafka_1        | [2021-02-02 21:42:01,786 root INFO] Mockintosh v0.6.2 is starting...
```

## Contact
Email us at info@up9.com

