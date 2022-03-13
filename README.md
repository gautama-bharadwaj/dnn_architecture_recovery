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
python3 wrapper.py -m=existing_model_name -i=number_of_iterations
python3 wrapper.py -model=existing_model_name -iterations=number_of_iterations
python3 wrapper.py -model=existing_model_name -iterations=number_of_iterations -visualize=True
```
The command has 2 mandatory arguments:
- -m or -model: For selecting the particular DNN model
- -i or -iterations: For selecting the number of iterations & datasets to generate

It has 1 optional argument:
- -v or -visualize: For plotting the final iteration of dataset using matplotlib


Example:
```bash
python3 wrapper.py -m=densenet121 -i=10

python3 wrapper.py -m=densenet169 -i=15

python3 wrapper.py -m=densenet201 -i=50 -v=True

python3 wrapper.py -m=inception_resnet -i=20 -v=True
```
