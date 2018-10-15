# RNN Builder #

## Project status: ##

[![Generic badge](https://img.shields.io/badge/Build-failed-red.svg)](https://shields.io/) [![Documentation Status](https://readthedocs.org/projects/ansicolortags/badge/?version=latest)](http://ansicolortags.readthedocs.io/?badge=latest)

RNN builder to generate tree from scratch. Any more description can goes here!

### Pre instructions for setup ###

1.**System Requirements:**

| O.S           | Minimun Memory | Suported      |
| ------------- |:--------------:|:-------------:|
| Ubuntu        | 8 Gb | :white_check_mark:      |
| Mac OSX       | 8 Gb | :no_entry_sign:         |
| Windows       | 8 Gb | :white_check_mark:      |

2.**Dependencies**

Builder needs a few depencies to run. the follwing command will install all deps in system target!

***Update package list***

```shell
sudo apt update
```

***Download python framework tools***

```shell
sudo apt install python-3.6
```

***Setup virtual enviroment***(*env*)

```shell
virtualenv -p 'python-3.6' env
```

3.**Instalation**
Builder use all tensorflow deps. but they're are bundled in setup script so no need worry about. Just type this command on system console.

```shell
(env) python setup.py install
```

The script will install all required package to your system.

4.**Usage**
builder comes with intregated documentation. To build the documentation with     sphinx-build program, type this:

```shell
$ sphinx-build -b html sourcedir builddir
where sourcedir is the source directory, and builddir is the directory in which you want to place the built documentation. The -b option selects a builder; in this example Sphinx will build HTML files.
```

---

## Builder - Using Deep learning with GPU ##

> TO-DO: Include this procediment in the requirements.txt. It was needed to use protoc later in the tutorial

```zsh
sudo apt install protobuf-compiler python-pil python-lxml python-tk
```

## Installing tensorflow object detection api ##

1.**Register submodule tensorflow's repository to root.**

```zsh
    git add submodule https://github.com/tensorflow/models.git
```

**Obersvation** 
If you wanna just clone all models to ur project root folder use this commands!

```bash
cd <path_to_project_root_folder> && git clone https://github.com/tensorflow/models.git
```

2.**Compile with protobuf.**

```zsh
cd models/research/
protoc object_detection/protos/*.proto --python_out=.
```

3.**Add to PYTHONPATH.**
> To make the changes permanent (not needing to type every terminal you create, DO NOT FORGET of the command source). So, if you use zsh:
```zsh
cd path_to_project/models/research && echo "export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim" >> ~/.zshrc
source ~/.zshrc
```
> OR if you use bash
```bash
cd path_to_project/models/research && echo "export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim" >> ~/.bashrc
source ~/.bashrc
```
