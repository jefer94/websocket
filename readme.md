# save deps
pip freeze -l -r ./requirements.txt > ./requirements.txt

# dev
python -m sanic websocket.main -r

# virtualenv
https://docs.python.org/3/library/venv.html#how-venvs-work
source ./venv/bin/activate