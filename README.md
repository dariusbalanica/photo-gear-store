# Photo Gear Store
## About
Within this project I set out to create a minimalist implementation of a
photographic equipment store. It will have numerous photographic equipment,
grouped into categories, such as: cameras, photo lenses, tripods, studio
accessories, various accessories. Each item will be in one of the categories
mentioned above and will have associated a price and a lively quantity available
(a stock).
Services:
* Database (db) - manages and stores data (products, shopping cart, available stocks)
* Administration (administration) - can update the database through a minimalist graphical interface within the console (terminal), using queries
* Server (server) - implements the entire logic within the store, provides the information that is requested by the customers and performs the necessary updates and processing operations for the clients
* Client (client) - used by users to be able to perform operations within the store (listing of products, adding to the shopping cart, purchasing products); the interaction will be realized through the terminal associated with the client, through a minimalist interface
* Monitoring service (grafana) - provides relevant statistics on how the store was used
## Work in progress
* Database - **Done** (Initialized and populated with basic sets of data)
* Administration - **Done** (More features will be added if required)
* Server - **Done**
* Client - **Done**
* Monitoring service - **Done**
## How to
### Starting the services
1. Download the associated `docker-compose.yml` file
2. In a terminal (at the root path of the downloaded file):
   - Start all the services: `docker-compose up --build`
   - Get container IDs for each started service: `docker ps`
   - Attach to a service  `docker attach <container ID>`
3. After using the services, closing them is needed:
   - Kill the process that started all the services in the previous step
   - In a terminal: `docker-compose down`
### Using the services
* To connect to the administration or to the client, attach to their corresponding containers using the steps above (Note: client only partially implemented, see above)
* to see the menu for a service, simply type `ENTER` after attaching to it
* Each service contains instructions to navigate through the menus
* Each menu entry contains the format of the data to be inserted in order to perform a specific operation

### Swarm inside a cloud environment
1. Creating machines:
   - sudo docker-machine create --driver amazonec2 --amazonec2-region eu-west-2 --amazonec2-open-port 5000 --amazonec2-open-port 5002 --amazonec2-open-port 5001 --amazonec2-open-port 3000 --amazonec2-open-port 3306 --amazonec2-open-port 2377 --amazonec2-access-key <access key> --amazonec2-secret-key <secret key> myaws-1
   - same for second machine, but with a different name (myaws-2)
2. Initializing swarm:
   - Manager: sudo docker-machine ssh myaws-1 "sudo docker swarm init --advertise-addr 35.177.128.157"
   - Workers: sudo docker-machine ssh myaws-2 "docker swarm join --token <token> 35.177.128.157:2377"
3. Preparing infrastructure and starting services (after cloning repo, from the root path of the repo):
   - sudo docker-machine scp docker-compose.yml myaws-1:.
   - sudo docker-machine scp -r db myaws-1:.
   - sudo docker-machine scp -r grafana myaws-1:.
   - sudo docker-machine ssh myaws-1 "sudo docker stack deploy -c docker-compose.yml photogearstore"
   - sudo docker-machine ssh myaws-1 "sudo docker stack ps photogearstore"
