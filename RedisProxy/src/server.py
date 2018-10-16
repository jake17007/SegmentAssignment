from redis_proxy import app as application

"""
Executed by Gunicorn to run the Flask application
"""
if __name__ == '__main__':
    application.run()
