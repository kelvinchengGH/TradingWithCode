# Run "source ./start-venv.sh" to use this script.


# Start up the virtual environment.
source ./.venv/bin/activate

# Add the modules in this project to the Python path
export PYTHONPATH="$PYTHONPATH:$PWD/src"
