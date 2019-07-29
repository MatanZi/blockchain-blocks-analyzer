# blockchain-blocks-analyzer
blockchain blocks analyzer, is an open source tool for analyze Bitcoin wallet address
 transaction. The main propose of the tool is to track suspicious addresses
 transaction from income to to outcome and keep track the next wallet, which received
 money from the suspicious address. Moreover, we create a Graph database, Neo4j, which 
 represent a flow graph which starts with the income of the suspicious addresses
  until the last "interesting" wallet. The meaning of graph flow is to connect 
  between other wallet to the suspicious wallet, Type of money laundering.

# Prerequisites

## Python
Python 3.*  
[download here](https://www.python.org/downloads/)

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

# Cli Usage

# Authors
* [Saimon lankry](https://github.com/Saimon9852)
* [Matan Zilka](https://github.com/MatanZi)
* [Adiel Matuf](https://github.com/MatufA/)

# Licence
GNU General Public License v3.0
