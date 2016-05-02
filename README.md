# Enigma OpenVPN User System

Base on OurSustc-Node Enigma HTTP Authentication API.

## Usage

1. Modify your config:

```shell
$ chmod +x {auth,connect,disconnect}.py
$ cp config.example.conf config.conf
$ vi config.conf
```

2. Put below config to OpenVPN server config:

```
script-security 3
auth-user-pass-verify /path/to/auth.py via-env
client-connect /path/to/connect.py
client-disconnect /path/to/disconnect.py
```
