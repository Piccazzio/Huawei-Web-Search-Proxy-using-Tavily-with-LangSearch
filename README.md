# Tavily to LangSearch Bridge API

## 📌 Overview

This project provides a simple API bridge that connects Tavily search with systems expecting the LangSearch response format, such as Pangu Brain.

It receives search queries, forwards them to Tavily, converts the response into a compatible structure, and returns it to the client.

---

## 🚀 Features

* Tavily → LangSearch response transformation
* Built with FastAPI
* In-memory caching (24h TTL)
* Monthly quota control (1000 requests)
* Simple and lightweight architecture
* Ready for deployment with Nginx and HTTPS

---

## ▶️ Running the API

### Install dependencies:

sudo apt update

sudo apt install python3 python3-pip -y

sudo apt install python3-venv -y

sudo apt install nginx -y

...

python3 -m venv venv

source venv/bin/activate

### Install the virtual environment

pip install fastapi uvicorn requests

...

### Create the file and paste the python code: main.py

nano main.py

...

### Create the NGINX file 

sudo nano /etc/nginx/sites-available/api

### Copy and paste the following text and replace the HTTPS_DOMAIN and the EIP

server {
    server_name HTTPS_DOMAIN;

    location / {
        proxy_pass http://EIP:8000;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    listen 443 ssl;
    ssl_certificate /etc/letsencrypt/live/HTTPS_DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/HTTPS_DOMAIN/privkey.pem;
}

sudo ln -s /etc/nginx/sites-available/api /etc/nginx/sites-enabled/

sudo nginx -t

sudo systemctl restart nginx

### Install certbot ssl

sudo apt install certbot python3-certbot-nginx -y         

### Generate certificate (replace the HTTPS_DOMAIN) and then enter an email and accept the instructions

sudo certbot --nginx -d HTTPS_DOMANIN

### Run the server

uvicorn main:app --host 0.0.0.0 --port 8000 

### Run the following command for testing (replace the HTTPS_DOMAIN and enter you TAVILY_API)

curl -X POST https://HTTPS_DOMAIN/search \
-H "Content-Type: application/json" \
-H "Authorization: Bearer TAVILY_API" \
-d '{"query": "Quais são os principais conceitos da Inteligência Artificial?"}'


### ❤️ GET `/health`

Returns API status, quota usage, and cache information.

---

## ⚙️ How It Works

1. Receives a search request
2. Normalizes and checks cache
3. Validates monthly quota
4. Sends request to Tavily API
5. Transforms the response into LangSearch format
6. Returns structured results to the client

---

## 🔐 Security Notes

* No API keys are stored in the code
* Authorization is passed via request headers
* Recommended to restrict access in production environments

---

## 📦 Use Case

This API is useful when integrating Tavily into systems that require a LangSearch-compatible interface, without modifying the original system.
