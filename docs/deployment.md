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

### 5. Clone the Flask API Repository to `/var/www/enso/`
```sh
sudo mkdir -p /var/www/enso
sudo chown $USER:$USER /var/www/enso
git clone https://github.com/master-who/enso.git /var/www/enso
cd /var/www/enso
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

### 11. Set Up Supervisor (in Virtualenv) as a Systemd Service

- The Supervisor configuration is located at `/var/www/enso/conf/supervisord.conf` and is set up to manage Gunicorn.
- The systemd service file for Supervisor is at `/var/www/enso/conf/enso.service`.

```sh
# Link the systemd service file
sudo ln -s /var/www/enso/conf/enso.service /etc/systemd/system/enso.service

# Reload systemd to recognize the new service
sudo systemctl daemon-reload

# Enable the service to start on boot
sudo systemctl enable enso

# Start the Supervisor service
sudo systemctl start enso

# (Optional) Stop the service
sudo systemctl stop enso

# Check the status of the service
sudo systemctl status enso

# Check systemd logs for the Supervisor-managed Gunicorn service
sudo journalctl -u enso

# Check Supervisor logs (paths may vary based on your supervisord.conf)
tail -f /var/www/enso/logs/supervisord.log

# Check Nginx error logs
sudo tail -f /var/log/nginx/error.log
```

**Your Flask API server should now be running securely behind Nginx, with Gunicorn managed by Supervisor (running as a systemd service) in a virtual environment.**