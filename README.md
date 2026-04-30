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

Install dependencies:

```bash
pip install fastapi uvicorn requests
```

Run the server:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## 🌐 API Endpoints

### 🔍 POST `/search`

Performs a web search using Tavily and returns results in LangSearch format.

**Headers:**

```
Authorization: Bearer <TAVILY_API_KEY>
Content-Type: application/json
```

**Body:**

```json
{
  "query": "example search"
}
```

---

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

---

## 📄 License

MIT
