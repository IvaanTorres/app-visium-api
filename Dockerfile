FROM python:3.9-slim as main
WORKDIR /app
EXPOSE 8000

FROM main as prod
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/
# It would be a good idea to implement in this production env a proxy so we don't expose the host (security issues, etc)
# Remove the --host 0.0.0.0
CMD ["uvicorn", "app.main:app", "--port", "8000", "--host", "0.0.0.0"]


# I don't know how can we do this in a way that I can update the dependencies in dev without rebuilding the image
# In nodejs we can use volumes to do this (node_modules), here however I didn't get it to work
FROM main as dev
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
# Since it's the dev env, it's not that important to expose the host using 0.0.0.0
CMD ["uvicorn", "app.main:app", "--reload", "--port", "8000", "--host", "0.0.0.0"]
