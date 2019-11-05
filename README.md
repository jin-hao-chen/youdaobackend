![logo](assets/logo.png)
---
**This Youdao backend is a  toy project which has no relationship with the offical [Youdao](https://www.youdao.com/) and it's just a project for study**



# Contents

* [Introduction](##introduction)

* [Installation](##installation)
  * [pip](###pip)
  * [docker](###docker)
 
* [Test](##test)
* [TODO](##todo)



## Introduction



## Installation

### pip

#### requirements

1. require `Python>=3.7.4`

#### installation

1. `pip install -r requirements.txt`
2. on *nix like system, run `./product.sh`, if you are using Windows, run `.\product.bat` or double click the file; besides, you can directly modify run.sh or run.bat file to change the number of workers and listening port.

## test

1. run `dev.bat` in cmd if you are using Windows, otherwise run `dev.sh` in Terminal
2. access `http://localhost:8080/api/v1/translation` if you see `Hello, world!` that means success

### docker

