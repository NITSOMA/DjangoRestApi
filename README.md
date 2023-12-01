# DjangoRestApi
Project written in Django used django rest framework. 
it is small project for people who would like to see easy
examples of integration django, redis and celery.
project consists of three component

#### scrapper
#### worker 
#### backand 


* client can reach our api and through api request some information about particular book.
* scrapper collects data from target website, reaches endpoints, implemented
  by us, checks existing data and depend on results, posts or updates data(information about particular book)
  used celery  worker and celery beat for background, scheduled  tasks, redis broker
  and docker to run redis.


## Technologies used
* [Django](https://www.djangoproject.com/): 
* [DRF](https://www.django-rest-framework.org/): 
* [Celery](https://docs.celeryq.dev/en/stable/)
* [Redis](https://redis.com/solutions/use-cases/messaging/)
* [docker](https://www.docker.com/products/docker-desktop/)


## Installation
* first ensure you have python globally installed in your computer. If not, you can get python [here](https://www.python.org").
* create virtual environment
    ```bash
      python -m venv env
        $ 
    ```
  * Then, clone this repository to your computer
   ```bash
    $ git clone https://github.com/NITSOMA/DjangoRestApi.git
    ```

* #### Dependencies
  * move into cloned repository
      ```bash
          $ cd DjangoRestApi
      ```
  * activate virtual environment:
      ```bash
         $ source env/bin/activate
      ```
      #### Install the dependencies needed to run the app:
      ```bash
          $ pip install -r requirements.txt
      ```
      #### Make migrations and migrate
    
      ```bash
      $ python manage.py makemigrations
      $ python manage.py migrate
       ```

  * #### Run It
      runserver 
      ```bash
          $ python manage.py runserver
      ```
    pull redis image and run redis through docker
    ```bash
        $ docker run -d -p 6379:6379 redis
    ```
    in case you don't use docker you can run redis server 
    ```bash
          $ redis-server
    ```
    run celery worker
    ```bash
          $ celery -A BOOKS worker loglevel=info
      ```
    run celery beat 
    ```bash
        $ celery -A BOOKS beat loglevel=info
    ```

     ### You can now access the server
     for post request, add data of book 
    ```
         http://localhost:8000/api/books
     ```
     for get or put request. get or update info of particular book, by book_id
    ```
         http://localhost:8000/api/books/book_id
     ```
     for post request. post desire url to scrape 
                    
     ```
         http://localhost:8000/api/appraisal_request
     ```
    for get request. get appraisal_request info 
     ```
         http://localhost:8000/api/appraisal_request/request_id
     ```
        
               

                
            
            