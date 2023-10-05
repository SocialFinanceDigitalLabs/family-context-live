# Certificates
Place your SSL certificates here.

Please do the following when configuring SSL:
1. Place your crt file and key file in this folder
2. In the parent folder:
   1. Update the nginx.conf file to have the correct file names for the ssl certificate:
```nginx
server {
    ...
    # Make sure the right filenames are specified here
    ssl_certificate     /etc/nginx/certs/cert.crt;
    ssl_certificate_key /etc/nginx/certs/cert.key;
    ...
}
```
3. The docker compose (prod) file will mount the certs in this directory onto the nginx image in the above location.
You will need to run a docker compose build to make sure the configuration is correct before bringing up the images.

```commandline
docker compose -f docker-compose.prod.yaml build
docker compose -f docker-compose.prod.yaml up
```

## Things to note 
This configuration will allow you to put your own certificate into the setup,
but be aware that if a certificate expires, a new one will need to be put
into the system and the service restarted (and possibly any cached certificates
cleared).  Look into using [certbot](https://certbot.eff.org/) to automate this process