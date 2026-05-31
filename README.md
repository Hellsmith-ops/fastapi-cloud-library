# fastapi-web-deployments

FastAPI web deployment projects showcasing Python backend APIs, database integration, authentication, and production-ready deployment workflows.

## DEPLOYMENT TUTORIALS

This doc will provide guidance and step-by-step on deploying the cloud library into production on an Ubuntu server.

### STEP 1. CLONE THE REPO TO LOCAL FOLDER

1. Inside the specified directory, run:
```bash
git clone https://github.com/Hellsmith-ops/fastapi-cloud-library.git
```
2. Enter the cloned repo folder:
```bash
cd .\fastapi-cloud-library\
```
### STEP 2. CREATE A PYTHON VIRTUAL ENV

- A virtual environment is important because it keeps your project’s Python packages isolated from the rest of your system. This helps prevent package conflicts, keeps the development environment clean, and allows the project to be reproduced consistently using `requirements.txt`.

```bash
sudo apt install python3.10-venv #install virt env dependency
python3 -m venv .venv #create an virtual env named "venv"
source .venv/bin/activate #enable the env
python3 -m pip install --upgrade pip #make sure the package installer is up-to-date
pip install -r requirements.txt #install required dependencies for this repo
```

### STEP 3. CREATE AN .ENV FILE FOR SECRET KEY

- Storing secret keys and API tokens directly in the source code creates a security risk. To prevent exposing sensitive credentials, we should store the secret key in a .env file and make sure that file is not pushed to GitHub.

```bash
#1. generate a strong key with:
python3 -c "import secrets; print(secrets.token_hex(32))"
#2. create the .env file in the repo root:
nano .env
#3. paste the generated key using this format:
SECRET_KEY="replace_this_with_the_secret_key"
```
- For the initial setup, use the commands above to generate a secret key, which will be used for JWT and OAuth2 authentication. Without it, Docker will throw an error while building the image. 

### METHOD 1: DEPLOYMENT USING DOCKER

```bash
# Step 1: Build the Docker image
docker build --no-cache -t fastapi-cloud-library . # also required for adjusting the container file 
# Step 2: Start the Docker image
docker run -d --name fastapi-cloud-library --env-file .env -p 8000:8000 fastapi-cloud-library
# Step 3: Execute the example_books.py file inside the container
docker exec -it fastapi-cloud-library python example_books.py
```









