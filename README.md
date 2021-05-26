# data-pump-service
Docker data pump docker service to fetch SQS queue message count and 

## Usage
1. Place your service environment configurations in **env** file
2. Run docker on your local machine
3. Open ***cmd*** in the project directory
4. Build docker image
	```
	docker build --tag data-pump-service .
	```
5. Run docker image
		This command will take default service frequency (in mins) from env file <br />
		```
		docker run --env-file env data-pump-service
		```<br />
	**or**<br />
		This command will take the frequency value (in mins) given in ***frequency=*** cmd variable<br />
		```
		docker run --env-file env -e frequency=5 data-pump-service
		```
	
