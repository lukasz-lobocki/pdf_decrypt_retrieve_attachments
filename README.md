# pdf_decrypt_retrieve_attachments

Decrypt and extract embedded pdf attachments.

## Credit

Based on <https://piep.tech/posts/automatic-password-removal-in-paperless-ngx/>

## Setup

### 1. Create a Dictionary File

The first step in creating a pre-consumption script is to create a dictionary file. This file will contain a list of all the passwords that you want to try to remove from the PDF files. To create a dictionary file:

1. Open a text editor.
2. Enter each password on a new line.
3. Save the file as `<paperless-ngx_root>/scripts/passwords.txt`.

    ```text
    123456
    123456789
    qwerty
    password
    12345
    qwerty123
    1q2w3e
    12345678
    ```

### 2. Write the Pre-Consumption Script

Next, you’ll need to write the pre-consumption script. This script will use the dictionary file to automatically remove the passwords and extract pdf attachments from the PDF files.

1. Open a text editor.
2. Copy `pre-consumption.py` script.
3. Save the file as `<paperless-ngx_root>/scripts/pre-consumption.py`.

### 3. Configure the pre-consumption script to be run

We need to configure the Python script to run, when a new files is processed by Paperless-ngx.

#### docker-compose.yml

1. Open your docker configuration file of Paperless-ngx. `<paperless-ngx_root>/docker-compose.yml`
2. :information_source: See the [example](docker-compose.yml). Make sure that the script folder is available to the docker container.

    ```text
    services.webserver.volumes:
        - <paperless-ngx_root>/scripts:/usr/src/paperless/scripts     
    ```

3. Make sure that the environment file is processed.

    ```text
    services.env_file: docker-compose.env
    ```

#### docker-compose.env

1. Open your docker environment file of Paperless-ngx. `<paperless-ngx_root>/docker-compose.env`
2. :information_source: See the [example](docker-compose.env). Set the script path.

    ```text
    PAPERLESS_PRE_CONSUME_SCRIPT=/usr/src/paperless/scripts/pre-consumption.py
    ```

### 4. Restart the Paperless-ngx docker container

```bash
docker-compose up -d
```

Check if environment variables were properly set.

```bash
docker exec -it paperless_webserver_1 printenv \
    | grep PAPERLESS_PRE_CONSUME_SCRIPT
```

Should yield.

```text
PAPERLESS_PRE_CONSUME_SCRIPT=/usr/src/paperless/scripts/pre-consumption.py
```
