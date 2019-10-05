# /usr/bin/env python

# from do import create_app
from do import app

# app = create_app()

#keep Flask server running when being run locally
if __name__ == "__main__":
    app.run(debug=True)
