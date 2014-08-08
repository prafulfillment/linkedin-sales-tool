
How it works


1. A user issues a request for a domain's root URL / to go to its home page
2. routes.py maps the URL / to a Python function
3. The Python function finds a web template living in the templates/ folder.
4. A web template will look in the static/ folder for any images, CSS, or JavaScript files it needs as it renders to HTML
5. Rendered HTML is sent back to routes.py
6. routes.py sends the HTML back to the browser
