# Docker
`Docker` is a tool that makes it easy to run applications in containers. Containers provide isolation and security like virtual machines, but they’re much smaller because they run in the host machine’s system.

The Docker client and Docker daemon are parts of the Docker Engine, which is the client-server application now running on your Mac. The daemon is the server, and the client is the docker command line interface (CLI).

A Docker image consists of layers — lower layers (OS or programming language) are used by higher layers (API or app). Running an image creates a container — a thin read-write layer on top of the read-only layers of the image.  The image’s top read-only layer specifies the command to run in the container

Docker commands are similar to Unix commands, but they start with “docker”, like docker run, docker image, docker container, docker network.
Most commands have several options, and many options have shorthand versions. The full name of the option is --something, with two dashes, like --name or --publish. The shorthand version is -abbrev, with one dash, like `-p` for `--publish`.

`docker images` --- The output lists the Docker images on your system
`docker ps -a` --- show all docker containers on your system
You can remove a container by specifying its name or its ID or just the first 3 characters of its ID
`docker rm <container-id>`

`docker run --name helloWorld hello-world` --- assigns a name "helloword" to container hello-world
`docker ps -a -q -f status=exited` --- will display all container ids becasue of -q (--quite) flag & -f (--filter) with status exited
`docker rm $(docker ps -a -q -f status=exited)` --- remove output containers of second command

`docker rmi hello-world` ---- will remove the image name hello-world

you can publish your app to a port by using --publish followed by two port numbers, separated by a colon, first value is for the host here, and the second value is for the container

* `docker container ls`
* `docker volume prune`			// deletes all volumes used by docker images
* `docker container stop webserver`
* `docker container ls -a`
* `docker ps -aq`			// List all containers (only IDs)
* `docker stop $(docker ps -aq)`		//Stop all running containers
* `docker rm $(docker ps -aq)`			//Remove all containers
* `docker rmi $(docker images -q)`		//Remove all images
* `Stop the container(s) using the following command: `docker-compose down`
* `Delete all containers using the following command: `docker rm -f $(docker ps -a -q)`
* `Delete all volumes using the following command: `docker volume rm $(docker volume ls -q)`
* `docker volume rm $(docker volume ls -q)`		//remove all volumes 
* `docker restart container_name` 	// restart given container 
* `docker cp <containerID>:/file/path/within/container /host/path/target` copy files from container to host 
* `docker cp foo.txt <containerID>:/foo.txt`		copy files from host to container
* `docker cp 46b276fb92b6:~/.ssh/id_rsa.pub ~/.ssh/id_rsa.pub`
* `docker cp ~/.ssh/id_rsa.pub 88acbb2377ef:~/.ssh/id_rsa.pub`



* `docker container rm webserver`
* `docker image ls`
* `docker image rm nginx`
* `docker run image_name`	// runs the image, if not available downloads first.
* `docker run image_name:4.0`	// will download 4.0 version of the image
* `docker stop image_name` 	// stops a running image
* `docker pull image_name` 	// pull the image name to run later
* `docker run -d image_name` 	// runs the image & detaches the terminal to use for further commands.
* `docker run -it image_name`	// will run the image with interactive mode + terminal of the image
* `docker run -it --rm image_name /bin/bash`		// will remove the container after interactive session ends
* `docker exec -it container_name bash`				// will open interactive session for a running container
* `docker run -p 50:80000`		// assigns a port to image
* `docker run -v file_path image_name`	// maps docker container storage on the given path so data is synched with this location 
* `docker inspect image_name`		// displays all the information regarding a an image
* `docker run -e varible=value image_name` 		// runs an image & passes variable as evnironment to the image container
* `docker volume create volume_name`			// creates a data volume to be share with a docker image
* `docker run -v volume_path image_name`		// shares the mentioned volume with started continer
* `docker create network network_name` 			// creates a network with default bridge driver
* `docker network prune`						// will delete all the networks not used by any container 
* `docker logs -f container_name` 				// will display the logs of the container
* `docker prune volume` 						// will remove unused volumes
* `docker network connect network_name container_names_or_ids`	// connects given list of cotainers to the desired network
* `docker network disconnect network_name container_names_or_ids`	// disconnects given list of cotainers to the desired network
* `docker compose` is used to start multiple containers from 1 file.
* `docker-compose up -d .` 	// will up the docker componse file in current directory 
* `docker-compose -p name -f file_name -up -d --scale service_name=n` // starts given file name with the name in p while number of instance equal to n
