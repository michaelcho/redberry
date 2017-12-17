# Redberry CMS

Redberry is a Blueprint for adding CMS functionality into your Flask app. 
It is intended to be registered into an existing Flask app, not as a standalone application.

## Features
- Start using Redberry in your Flask app in 3 lines
- Display posts and categories
- Create, update, and delete in the included admin panel
- Includes rich text editor
- Customizable templates
- Built with Bootstrap for easy modification, and mobile-optimized / responsive
- Automatically generated sitemap
- Automatically generated [Accelerated Mobile Pages](https://www.ampproject.org) versions of all pages. Just add `.amp` to the end of URLs for posts and categories.
- Automatically included [JSON-LD](http://json-ld.org/) meta data for improved SEO

## Installation
`pip install redberry`

## Usage
```
from redberry.blueprint import cms

# Pass a SQLAlchemy object as db
app.config['redberry.config'] = {'db': db}

## EITHER
## If you create your db object using `db.init_app(app)` you will need:
with app.app_context():
    # Set the url_prefix for where your CMS should be served from
    app.register_blueprint(cms, url_prefix='/content')

## OR
## If you create your db object using `db = SQLAlchemy(app, session_options={...})`
app.register_blueprint(cms, url_prefix='/blog')

....

# Ensure your user instances implement an is_admin() method
# eg models/user.py
class User:
    def is_admin(self):
        return self.role == 'ADMIN'
```

When you start your app, Redberry checks that any required database tables are present. 
If not, it will run migrations and create a sample post and category.

You can now access the Redberry frontend at `/blog` (or whatever you entered as the url_prefix).

To generate a sitemap, use your browser to visit:
- http://yourdomain.com/blog/sitemap (this will generate an XML sitemap)
- http://yourdomain.com/blog/redberry/sitemap.xml (this is the generated file)

## Admin Panel
**Certain routes requires your user instance to be logged in and implement an `is_admin()` method.**

Redberry ships with a basic admin panel for editing posts and categories. This is available at `/blog/admin`. 

If your user is not logged in or `is_admin()` returns False, you will be redirected when trying 
to access the admin panel.


## Customizing
Redberry templates are fully customizable.

Templates can be modified by placing jinja files in your app's templates/redberry directory:
- templates/redberry/index.html
- templates/redberry/admin/index.html
- and so on

Only place template files here that you want to override, it is not necessary to copy all files.

By default, Redberry looks for a css file in your app's static directory at /static/redberry/css/redberry.css. 
Create a file here to override any default styling.

## Screenshots
![Index Page](/docs/assets/index.png "Index Page")

![Category Page](/docs/assets/category.png "Category Page")

![Post Page](/docs/assets/post.png "Post Page")

![Admin Page](/docs/assets/admin-index.png "Admin Page")

![Editing Page](/docs/assets/admin-form.png "Editing Page")

## Running tests
Unit tests are included in the redberry/tests folder when you clone this repo. 
Tests will run with a local sqlite database.

If you want to run unit tests locally:
- `pip install -r redberry/tests/requirements.txt`
- `py.test redberry/tests`

 
### Developer Notes
To update the package:
- run tests
- bump VERSION
- update CHANGELOG.txt
- Manually pull request dev/0.0.7.6 (or latest version) branch and merge to master on Github
- `./distribute.sh`




