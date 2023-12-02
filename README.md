
  * ### Run It
      ### keep it in mind
  * each command need to run in new terminal
  * each time you open new terminal need to activate virtual environment
      ### Runserver
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
        
               

                
            
               

                
            
            
