# recontent
Content recommendation API
Using Python3


## Running the app with Docker
  1. Install Docker, see https://www.docker.com/products/docker#/mac for the instructions to install it on a Mac.
  2. Then, in the top directory of this repository, you should be able to run the app using docker-compose. Just type ```docker-compose up --build```. This will download the needed packages and run the app in the foreground.
  3. The first time you run the container, it will download and crunch the simple_wiki example. This will take about 10 minutes. You will see ```Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)``` when it is done.
  4. Browse to localhost:5000, you should see 'Content recommendation rocks!' as message.
  5. Try out the test API by using curl: ```curl localhost:5000/api/recommend/v1.0 -X GET -d 'url=http://www.symmetrymagazine.org/article/scientists-salvage-insights-from-lost-satellite'```, you should see a json document returned which holds the bow_vector for the url.
