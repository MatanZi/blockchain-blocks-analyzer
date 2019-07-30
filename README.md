# blockchain-blocks-analyzer
blockchain blocks analyzer, is an open source tool for analyze Bitcoin wallet address
 transaction. The main propose of the tool is to track suspicious addresses
 transaction from income to to outcome and keep track the next wallet, which received
 money from the suspicious address. Moreover, we create a Graph database, Neo4j, which 
 represent a flow graph which starts with the income of the suspicious addresses
  until the last "interesting" wallet. The meaning of graph flow is to connect 
  between other wallet to the suspicious wallet, Type of money laundering.

![image](https://user-images.githubusercontent.com/32271159/62113476-59670e80-b2bd-11e9-9a0e-2df8e6786ac1.png)

# Prerequisites

## Python
Python 3.* [download here](https://www.python.org/downloads/)

## Neo4j
Graph database platform. ([Official site](https://neo4j.com/))  
Download:  
* For PC (Windows, linux or MAC): [Here](https://neo4j.com/download/)  
* Docker: [DockerHub](https://hub.docker.com/_/neo4j)  
        or run:  
        ```
        []~$ docker run -d --publish=7474:7474 --publish=7687:7687 --volume=$HOME/neo4j/data:/data neo4j
        ```  
        
## Blockchain API
Use [Blockchain API](https://www.blockchain.com/api) according the
 [term of service](https://www.blockchain.com/legal/api-terms) and request limits.

## Requirements
* pandas
* py2neo
* requests

# Usage

## Environment variables
NEO4J_USER and NEO4J_PASS <b>must</b> being configure.  
* <b>Windows - (make sure you Run as administrator so you're able to add a system environment variable).</b>
    ```
    setx -m NEO4J_USER "<user_name>"
    setx -m NEO4J_PASS "<password>"
    ```
* <b>Linux or MAC - (recommended to add to ~/.bash_profile)</b>
    ```
    $ export NEO4J_USER=<user_name>
    $ export NEO4J_PASS=<password>
    ```

## Cli
Setup instruction:
* Install Cli:
    ```
    $ python3 -m pip install https://github.com/MatufA/blockchain-blocks-analyzer.git
    ```
* Print help:
    ```
    $ btc-analyzer --help
    ```
* Track wallet transaction:
    ```
    $ btc-analyzer -tr "<wallet_hash>"
    ```

## Library
Clone and setup requirements:   
```
$ git clone https://github.com/MatufA/blockchain-blocks-analyzer.git  
$ cd blockchain-blocks-analyzer  
$ python3 -m pip install -r requirements.txt  
```
### Classes
<b>Main classes and function description:</b>
* [Config.py](blockchain_blocks_analyzer/Config.py) - a configuration file with common function.
    * conf_logger - a function to configure a logger.
    * print_json_to_file - a function to print output json beautify.
* [node_builder.py](blockchain_blocks_analyzer/node_builder.py) - a class which responsible to link all the project.
    * create_node - a function to keep track suspicious wallet.
    * nodes_builder - a function to analyze suspicious wallet and draw a money flow.
* [neo4j_handler.py](blockchain_blocks_analyzer/neo4j_handler.py) - a handler function to communicate with Neo4j database.
    * connect_db - a function to create a connection to db.
    * generate_graph - a function to generate a graph database from json file.
* [blockchain_track](blockchain_blocks_analyzer/blockchain_track.py) - a handler function to track a money flow of a wallet.
    * get_single_address - a function to fetch all transactions information of a wallet.
    * generate_record - a function to generate a record of wallet transaction.

# Authors
* [Saimon lankry](https://github.com/Saimon9852)
* [Matan Zilka](https://github.com/MatanZi)
* [Adiel Matuf](https://github.com/MatufA/)

# Licence
GNU General Public License v3.0
