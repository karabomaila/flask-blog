# Blog posts

## Install
- pip install -e .

Init commands
- python -m flask --app blog init-db
- python -m flask --app blog run

## Running on Docker
- docker build -t blog:1.0 .  
- docker run -d -p 5000:5000 blog:1.0
- access the blog at http://127.0.0.1:5000

## Code coverage
- coverage run -m pytest
- coverage report
- access the report in the browser at ~/flask-blog/htmlcov/index.html