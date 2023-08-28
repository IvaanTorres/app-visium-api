# App Visium API 

# Installation for dev
- Create a .env from the .env.example
- Run the docker containers
```bash
npm run docker:dev
```

# Run commands of dependencies (Alembic, etc)
```bash
docker exec -it <container-name> <command>
```

# Things that can be improved
- Create CI/CD Pipelines where the project is tested (unit and e2e) and push the Docker image to the registry
- Create a reverse proxy as a load balancer to don't let the app gets exposed by using 0.0.0.0 (specially in prod)
- Use pipenv where all the dependencies are well managed (+ scripts) instead of the traditional requirements.txt
- Instead of having a general preferences/settings table, create also the preferencesGroups table and link it. After that, link this same table with a Options table creating a polymorphic relationship/inheritance so there can be several types of options structures for every section/group of settings. This is better for scaling the arch.
- For bigger projects where there are hundreds of foreign keys, it's better to create different unique table files for them and then, make an order of run.
- Instead of using just 1 JWT, use 2 (Access token and refresh token):
    - The refresh token is stored in db and has the ability to let generate access tokens. It can be revoked manually (during logouts, for example). It is stored in the client side part as a httpOnly secure lax/strict cookie so we can check it on server side automatically and don't put it in danger.
    - The access token is stored if possible in memory so everytime we refresh the page, a new acces token will be requested. This is a short life time token (15 min for example unlike the refresh one, which can be much longer).
- Add a CSRF token with double token system:
    - While we store the refresh token securely in a httponly cookie, there can be problems regarding the CSRF attacks. Using a random string token as CSRF token, we attach it to the header of the request and the server will validate if it corresponds with the one which is stored in a httponly cookie as is sent automatically (Double token system).