# social-media-backend

## Instructions

1. Clone repository. 

2. Create a new virtual environment:
  ```shell
  $ virtualenv <name>
  ```

3. Activate it
  ```shell
  $ source /path/to/<name>/bin/activate
  ```

4. Install with `pip` all python packages required in the project

  ```shell
  $ pip install -r requirements.txt
  ```
5. Run migrations for database
 
  ```shell 
  $ python manage.py migrate
  ```

6. Crete superuser in the same folder as `manage.py`, this will permit you to access to admin database using `localhost:8000/admin`:

  ```shell
  $ python manage.py createsuperuser
  ```

7. Start backend service, in the same folder as `manage.py`:
  ```shell
  $ cd <project-name>
  $ python manage.py runserver
  ```
