# fastapi-cloud-library

A FastAPI-based cloud library backend with JWT authentication, SQLite database integration, Docker deployment, Swagger API documentation, and future machine learning capabilities. 

## FEATURES
- FastAPI backend API
- SQLite database with SQLAlchemy models
- JWT authentication with OAuth2 password flow
- Protected create, update, and delete book routes
- Public book retrieval and search routes
- Docker-based deployment
- Example book seed script for demo data
- Swagger UI for interactive API testing

## PROJECT STRUCTURE
fastapi-cloud-library/
├── database/
│   ├── __init__.py
│   ├── database_engine.py
│   └── database_models.py
├── routers/
│   ├── __init__.py
│   ├── auth.py
│   └── books.py
├── Dockerfile
├── README.md
├── example_books.py
├── main.py
└── requirements.txt

## API ROUTES

### Health Check
GET /health
### Authentication
POST /auth/
POST /auth/token
### Books
GET    /books
GET    /books/{book_id}
POST   /books
PUT    /books/{book_id}
DELETE /books/{book_id}

POST, PUT, and DELETE book routes require authorization with a valid JWT token.

## DEPLOYMENT TUTORIALS

This doc will provide guidance and step-by-step on deploying the cloud library into production on an Ubuntu server.

### STEP 1. CLONE THE REPO TO LOCAL FOLDER

1. Inside the specified directory, run:
```bash
git clone https://github.com/Hellsmith-ops/fastapi-cloud-library.git
```
2. Enter the cloned repo folder:
```bash
cd fastapi-cloud-library
```


### STEP 2. CREATE AN .ENV FILE FOR SECRET KEY

- Storing secret keys and API tokens directly in the source code creates a security risk. To prevent exposing sensitive credentials, we should store the secret key in a .env file and make sure that file is not pushed to GitHub.

```bash
#1. generate a strong key with:
python3 -c "import secrets; print(secrets.token_hex(32))"
#2. create the .env file in the repo root:
nano .env
#3. paste the generated key using this format:
SECRET_KEY="replace_this_with_the_secret_key"
```

- For the initial setup, use the commands above to generate a secret key, which will be used for JWT and OAuth2 authentication. Without it, the app will fail during startup. 

### STEP 3. DEPLOY USING DOCKER

```bash
#1. Build the Docker image
docker build --no-cache -t fastapi-cloud-library . # also required for adjusting the container file 
#2. Start the Docker container
docker run -d --name fastapi-cloud-library --rm --env-file .env -p 8000:8000 fastapi-cloud-library
#3. Execute the example_books.py file inside the container
docker exec -it fastapi-cloud-library python example_books.py
#4. Open Swagger UI in a browser:
http://127.0.0.1:8000/docs
http://<server-ip>:8000/docs # if running on a remote server
![FastAPI UI](FastAPI_UI.png)
#5. Stop the container when finished:
docker stop fastapi-cloud-library
```
### STEP 4. DEMO WORKFLOW IN SWAGGER UI

After opening Swagger UI, test the API using the following workflow:

1. Run GET /health to confirm the API is running.
![API Health Checks](Healthcheck.png)

2. Run GET /books to view the seeded example books.
![Read_All_Endpoint](Read_All_Endpoint.png)
3. Click Authorize near the top right of Swagger UI.
![LoginUI](LoginUI.png)
4. Log in with the demo account:
```bash
username: demo_user
password: demo_password
```
After authorization, test the protected book routes:
- POST /books
- PUT /books/{book_id}
- DELETE /books/{book_id}
![Delete_Endpoint](Delete_Endpoint.png)

The GET routes are public, while create, update, and delete routes require JWT authorization.

### Optional: Run Locally with Python Virtual Environment

- A virtual environment is important because it keeps your project’s Python packages isolated from the rest of your system. This helps prevent package conflicts, keeps the development environment clean, and allows the project to be reproduced consistently using `requirements.txt`.

```bash
#1. install virt env dependency:
sudo apt install python3.10-venv 
#2. create a virtual env named ".venv":
python3 -m venv .venv
#3. activate the env:
source .venv/bin/activate
#4. make sure the package installer is up-to-date:
python3 -m pip install --upgrade pip 
#5. install required dependencies:
pip install -r requirements.txt 
#6. start the FastAPI server:
fastapi run main.py --host 0.0.0.0 --port 8000
#7. Open Swagger UI:
http://127.0.0.1:8000/docs
```








