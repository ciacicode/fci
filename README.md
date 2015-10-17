#FCI

This is a python project to create an application that calculates a London area's Fried Chicken Index (FCI).
The FCI is calculated based on instances of fried chicken shops in the area. The front-end of this app is done with flask and can be found in the khaleesicode repo

## Installation with Anaconda

### 1. Install Anaconda
Follow instructions at http://docs.continuum.io/anaconda/install

### 2. Create your virtual environment with Conda
http://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/20/conda/

### 3. Clone this repository
Open your terminal, navigate to the directory where you want to save this project and execute:```git clone https://github.com/ciacicode/fci.git```

### 4. Install requirements
Activate your virtual environment, make sure you are in the fci folder and then execute from the terminal ```pip install -r requirements.txt```
This command tells pip to install recursively all the rows of the file requirements.txt which includes packages I use for my environment.

## Running
While your environment is active, you can populate all databases with the necessary information with only one function. This is a lengthy process so leave the computer connected for a while (up to 1 hour) while the function executes. In your terminal now activate the python interpreter of your virtual environment:
```(myenv)user@mylinuxmachine:~ /MyPath/to/the/project$ python ```
Then within your interpreter:
```
    >>>  from db_models import *
    >>>  fci_set_up()
```
Now let the function run. When the process is over you can query the value of teh fried chicken index for your London postcode as
```
    >>> fci_return("<london_postcode>")
```

### Notes
This works only for London and Greater Londona areas




