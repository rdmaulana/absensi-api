# Dockerizing Simple Absensi API

## Build with Flask

Check out API Documentation [here](https://golden-mochi-2dc.notion.site/HR-API-System-1dd8578ab3f944ab915c3eb303738b49).

## How to run this project

1. Rename .env.sample to .env
2. Fill out required variable (SECRET_KEY)
3. Build the images and run the containers:

    ```sh
    $ docker-compose up -d --build
    ```

    Check it out at [http://localhost:5004](http://localhost:5004)

    Run application test 

    ```sh
    $ docker-compose exec web pytest
    ```