# 🛡️ AI Audit Trail System (Immutable Observability)

An enterprise-grade API interceptor designed to solve the "Black Box" problem of Large Language Models in highly regulated environments. This system proxies all requests to local or cloud LLMs, cryptographically hashing and logging every prompt, response, and token count to guarantee compliance and absolute auditability.

## 🏗️ Architecture
1. **The Interceptor:** A Python FastAPI gateway that catches outbound AI requests.
2. **The Cryptography:** SHA-256 hashing applied to the `{Prompt + Response + Timestamp}` to create an immutable record.
3. **The Ledger:** Stores the metadata and cryptographic signatures in a relational database for compliance officers to review.

## 🚀 How to Run Locally

### Prerequisites
1. **Ollama:** Must be running locally with the `llama3` model.
2. **Python:** 3.10+ installed.

### Execution Steps
1. Clone the repository and navigate to the directory.
2. Install the API and database dependencies:
    ```bash
   pip install fastapi uvicorn sqlalchemy requests
    ```
3. Initialize the local SQLite audit ledger:

```Bash
python src/database.py --init
```
4. Start the FastAPI Interceptor proxy:

```Bash
uvicorn src.interceptor:app --host 0.0.0.0 --port 8080 --reload
```
5. Send a request to your proxy instead of directly to the LLM. The proxy will hash it, log it, and return the LLM's answer:

```Bash
curl -X POST http://localhost:8080/generate -H "Content-Type: application/json" -d '{"user_id": "dev-01", "prompt": "Write a python script to parse logs."}'
