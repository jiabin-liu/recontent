# recontent
Content recommendation API
Using Python3


## Running the app with Docker
  1. Install Docker, see https://www.docker.com/products/docker#/mac for the instructions to install it on a Mac.
  2. Then, in the top directory of this repository, you should be able to run the app using docker-compose. Just type ```docker-compose up --build```. This will download the needed packages and run the app in the foreground.
  3. Browse to localhost:5000, you should see 'Content recommendation rocks!' as message.
  4. Try out the test API by using curl: ```curl -i http://localhost:5000/api/recommend/test```, you should see a json document returned.

## Running the app without Docker
  0. Make sure to use Python3
  1. Install Flask, you should be able to install it using pip: ```pip install flask```
  2. Just run ```python app.py```, it should start the app. See steps above to test it.
