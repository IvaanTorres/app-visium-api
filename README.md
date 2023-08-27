# App Visium API 

# Installation for dev
```bash
npm run docker:start
docker exec -it app-visium-api alembic upgrade head
```

# Run commands of dependencies (Alembic, etc)
```bash
docker exec -it <container-name> <command>
```

# Things that can be improved
- Instead of manual migrations, autogenerate them using Alembic and Models
- Create CI/CD Pipelines where the project is tested (unit and e2e) and push the Docker image to the registry
- Create a proxy to don't let the app gets exposed by using 0.0.0.0 (specially in prod)
- Use pipenv where all the dependencies are well managed (+ scripts) instead of the traditional requirements.txt
- Instead of having a general preferences/settings table, create also the preferencesGroups table and link it. After that, link this same table with a Options table creating a polymorphic relationship/inheritance so there can be several types of options structures for every section/group of settings. This is better for scaling the arch.
- For bigger projects where there are hundreds of foreign keys, it's better to create different unique files for them and then, make an order of run.
- Set up .env variables inside the alembic.ini migrations setup + docker-compose files
- Instead of Alembic for migration, use sqlalchemy built-in models.