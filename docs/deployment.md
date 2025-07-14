

1. Provision VM
2. Pull dotrc.git & install
3. Pull enso.git
4. Setup virtualenv
5. Pip install requirements
6. Install nginx
7. Install certbot
8. Configure DNS
9. Configure nginx
    - Remove default config from /etc/nginx/sites-available/default
    - Add new nginx config file (/etc/nginx/sites-available/enso.masterwho.in)
    - Link to sites-enabled directory
    - Reload nginx. You should be able to access it on the http endpoint now.
10. Use certbot to install SSL certificate for domain
11. Setup gunicorn as system service