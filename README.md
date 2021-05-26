#data-pump-service
Docker data pump service to fetch SQS message count and send it to a webhook

##Usage
1. Place your service environment configurations in **env** file
2. Run docker on your local machine
3. Open ***cmd*** in the project directory
4. Build docker image
    ```commandline
    docker build --tag data-pump-service
    ```
5. Run docker image <br/>
    This command will take deafult service frequency (in mins) from env file <br/>
   ```commandline
    docker run --env-file env data-pump-service
   ```
   <br/>**or**<br/>
    ```commandline
    docker run --env-file env -e frequency=5 data-pump-service
    ```
    
    
   