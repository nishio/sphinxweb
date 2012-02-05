
A Flask app demonstrating the usage of `Sphinx Web Support`_.


.. _Sphinx Web Support: http://sphinx.pocoo.org/websupport.html


How to Use?
------------------------

.. note::

    In the following steps, I am assuming that you copied sphinxweb to /var/www/sphinxweb and cd to it.


#. Install the requirements ::

    pip install -r requirements.txt

#. Build the docs and database ::

    python build.py

#. Run the development server ::

    python runserver.py

#. If you want to use a production server like Apache:

    #. Install and enable mod_wsgi module

    #. Change the ServerName and paths in deploy/sphinxweb.apache.conf

    #. Copy deploy/sphinxweb.apache.conf to /etc/apache2/sites-enabled

    #. Restart apache2

#. If you want to use a production server like Nginx:

    #. Install Nginx, uWSGI and Supervisor

    #. Copy deploy/sphinxweb.supervisor.conf to /etc/supervisor/conf.d

    #. Change the ServerName and paths in deploy/sphinxweb.nginx.conf

    #. Copy deploy/sphinxweb.nginx.conf to /etc/nginx/sites-enabled

    #. Restart Supervisor and Nginx
