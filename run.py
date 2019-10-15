"""
@File : run.py
@Author: Zyeoh
@Desc :
@Date : 2019/9/18
"""
from app import create_app

app = create_app()


if __name__ == "__main__":
    app.run(debug=app.config['DEBUG'])
