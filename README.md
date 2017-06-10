# Password delivery meets Vernam

It's a POC intended to show a practical approach to use [Vernam encryption software](https://github.com/millaguie/Vernam).

## Build the docker image

To build the docker image just follow this steps:
```
$ git clone https://github.com/millaguie/passworddeliverymeetsvernam.git
$ cd passworddeliverymeetsvernam
$ docker build . --tag passworddeliverymeetsvernam:0.0.1
```
## Generate and catalog key

To use vernam encryption you need a key file distributed between you and your clients, once the file is fully used, server will start to fail because of it, so change your key as needed.

```
$ dd if=/dev/urandom of=keyfile bs=1024 count=2 iflag=fullblock
$ docker run -t -v $PWD:/keys/ --entrypoint python passworddeliverymeetsvernam:0.0.1 -m vernam --catalog -i /keys/keyfile
```

## Run docker image as a service

To run docker image just ensure your passwords.yaml is on the correct place and run the docker as follows:
```
docker run -d --restart=always -v $PWD/passwords.yaml:/server/passwords.yaml -v $PWD/keyfile:/server/keyfile -v $PWD/keyfile.yaml:/server/keyfile.yaml -p 8080:8180 passworddeliverymeetsvernam:0.0.1
```

## Test everything is working:

This is an example of how the client side works:
```
user@laptop:~/safeplacewithkey$ curl http://127.0.0.1:8080/v1.0/passwords
[
  "manuel", 
  "jose", 
  "andres", 
  "admin", 
  "root"
]
user@laptop:~/safeplacewithkey$ curl http://127.0.0.1:8080/v1.0/password/jose -o passwordfile
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   128  100   128    0     0   1030      0 --:--:-- --:--:-- --:--:--  1040
user@laptop:~/safeplacewithkey$ docker run -t -v $PWD:/keys/ --entrypoint python passworddeliverymeetsvernam:0.0.1 -m vernam -d -i /keys/passwordfile -o /keys/clearpassword -k /keys/keyfile
Could not find config file, creating a default one
input file: /keys/passwordfile, output file: /keys/clearpassword, config file: config.yaml, key file: /keys/keyfile, operation mode: raw
12 of 2048 bytes will be in use after this action
user@laptop:~/safeplacewithkey$ cat clearpassword && echo  ""
thoh6QuaeTei
user@laptop:~/safeplacewithkey$ 

```
