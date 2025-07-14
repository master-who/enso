## Step-by-Step Deployment Instructions for Flask API Server on Ubuntu 24.04 LTS (Azure VM)

### 1. Provision the Virtual Machine
- Create a new Ubuntu 24.04 LTS VM on Azure.
- Open ports 22 (SSH), 80 (HTTP), and 443 (HTTPS) in the Azure Network Security Group.

### 2. SSH into the VM
```sh
ssh <your-username>@<vm-public-ip>
```

### 3. Install System Dependencies
```sh
sudo apt update
sudo apt upgrade -y
sudo apt install -y git python3 python3-venv python3-pip nginx
```

### 4. Clone dotrc.git and Install Dotfiles (if applicable)
```sh
git clone https://github.com/master-who/dotrc.git ~/dotrc
cd ~/dotrc
./install.sh  # Or follow your dotrc setup instructions
```

### 5. Clone the Flask API Repository
```sh
git clone https://github.com/master-who/enso.git ~/enso
cd ~/enso
```

### 6. Set Up Python Virtual Environment
```sh
python3 -m venv venv
source venv/bin/activate
```

### 7. Install Python Requirements
```sh
pip install --upgrade pip
pip install -r requirements.txt
```

### 8. Install and Configure Nginx
```sh
sudo systemctl enable nginx
sudo systemctl start nginx
```
- Remove the default site:
    ```sh
    sudo rm /etc/nginx/sites-enabled/default
    ```
- Create a new Nginx config file `/etc/nginx/sites-available/enso.masterwho.in`:
    ```nginx
    server {
            listen 80;
            server_name enso.masterwho.in;

            location / {
                    proxy_pass http://127.0.0.1:8000;
                    proxy_set_header Host $host;
                    proxy_set_header X-Real-IP $remote_addr;
                    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                    proxy_set_header X-Forwarded-Proto $scheme;
            }
    }
    ```
- Enable the new site:
    ```sh
    sudo ln -s /etc/nginx/sites-available/enso.masterwho.in /etc/nginx/sites-enabled/
    sudo nginx -t
    sudo systemctl reload nginx
    ```

### 9. Configure DNS
- Point your domain (`enso.masterwho.in`) to the VM's public IP address using your DNS provider.

### 10. Obtain SSL Certificate with Certbot
```sh
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d enso.masterwho.in
```
- Follow prompts to enable HTTPS.

### 11. Set Up Gunicorn as a Systemd Service
- Create `/etc/systemd/system/enso.service`:
    ```ini
    [Unit]
    Description=Gunicorn instance to serve Enso API
    After=network.target

    [Service]
    User=<your-username>
    Group=www-data
    WorkingDirectory=/home/<your-username>/enso/src/api
    Environment="PATH=/home/<your-username>/enso/venv/bin"
    ExecStart=/home/<your-username>/enso/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 api:api

    [Install]
    WantedBy=multi-user.target
    ```
- Reload systemd and start Gunicorn:
    ```sh
    sudo systemctl daemon-reload
    sudo systemctl start enso
    sudo systemctl enable enso
    sudo systemctl status enso
    ```

### 5. Clone the Flask API Repository
```sh
git clone https://github.com/master-who/enso.git ~/enso
cd ~/enso
```

### 12. Verify Deployment
- Visit `https://enso.masterwho.in` in your browser.
- Check logs for errors:
    ```sh
    sudo journalctl -u enso
    sudo tail -f /var/log/nginx/error.log
    ```

**Your Flask API server should now be running securely behind Nginx with Gunicorn in a virtual environment.**