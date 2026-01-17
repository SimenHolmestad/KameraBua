[Back to readme](../README.md)

# Developing
To run CameraHub with a camera connected, Raspberry PI and/or Linux is required. It is however possible to run the application without using a camera at all. When used this way, CameraHub will create dummy circle images, like the following:

![Dummy demo circle image](images/dummy_demo_image.png)

To run the application for development using dummy circle images, you must first make sure both python and node are installed on the system. Then, do the following to start the backend:
```
git clone https://github.com/SimenHolmestad/CameraHub.git
cd CameraHub
pip install -r python-requirements.txt
export FLASK_ENV=development
python3 run.py run_backend
```
To start the frontend, open a second terminal window and do:
```
cd CameraHub/frontend
npm install
npm start
```

# Running the tests
Currently, only the backend code is tested. To run the backend tests, navigate to the root directory of the project and do:
```
python3 -m unittest
```

**Note:** The tests uses pyzbar to check if the qr-codes are generated correctly. To install pyzbar, check <https://pypi.org/project/pyzbar/>.

Maybe one day the frontend will be tested as well, but that day has yet to come.

# Next steps

For more information about how the application works, see [architecture](architecture.md)
