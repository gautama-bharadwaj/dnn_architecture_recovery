# dnn_architecture_recovery

## Installation

Clone the repository. Open a terminal & cd to the directory where ```requirements.txt``` is located. 

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required python libraries.

```bash
pip install -r requirements.txt
```

# Usage

In order to run the module, run

```bash
python3 wrapper.py -m=existing_model_name
```
Example:
```bash
python3 wrapper.py -m=densenet121

python3 wrapper.py -m=densenet169

python3 wrapper.py -m=densenet201

python3 wrapper.py -m=inception_resnet
```
