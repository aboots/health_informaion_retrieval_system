# Health Retrieval System
A sophisticated search engine designed to retrieve health and medical-related content from a variety of sources including news articles, blogs, and other publications. The system utilizes advanced techniques such as Boolean search, TF-IDF, FastText, Transformers, and Elasticsearch models for efficient information retrieval. It also incorporates classification, clustering, and link analysis methods to organize the crawled data. The system features a user-friendly interface with distinct back-end and front-end components, and is capable of being deployed on online servers for wider accessibility.


In order to work with this system, you need to start a react app for front-end and a Django app for back-end.
This project consists of 3 parts. Front-end, Back-end, and Development. Development mainly consists of notebooks that we train our models based on them. You can review them if you want to train new models.

## Run Django Server
To run Django App first go to the backend directory. Create a virtual environment and then install requirements. You can install requirements with:
### `pip install -r requirements.txt`

You need to have elastic search installed on your local. At the end of the file elastic_search.py in information_retrieval/health_retrieval directory put your elastic path like this:
##### `elastic_model = ElasticSearch(elasticsearch_path="C:\\elasticsearch\\elasticsearch-7.3.2\\bin\\elasticsearch.bat")`
Note that for the back-end you need a models directory near the root of back-end that contains models. (For security reasons we don't push them here)

You can download models [here](https://drive.google.com/drive/folders/1hfMy0i3KUqeGr9P2Kar8kgSaXndpuhj5?usp=sharing).

Now, you can run server with this command.
### `python manage.py runserver`
It's time to run the front-end project.

## Run React App
To run the front-end project go to frontend directory. If you don't have nodejs and npm on your pc, first install them.
Then for first time run:
### `npm install`

Now you can run:
### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

## Usage
This Service contains 4 main parts. The first is query retrieval that is based on 5 methods. You can enter query and see similar results for that. You can select how many results do you need and does the model do query expansion or not. Second one, is classification where you can enter a query and see what category of health it belongs to. You can also see the results of our classifiers there too. The third one, You can enter input and see the nearest neighbors of documents that are in the same cluster with it. Here you can see our clustering kmeans evaluation parameters. In the next part, you can see the link analyses part. For each category, we show the most and least important sentences of it. All of documents placed in development/documents folder.

Now enjoy :))
