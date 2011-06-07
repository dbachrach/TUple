# TUple

**TUple** is an easy to use, open-source Placement Exam system for universities or businesses. TUple is currently in active development.

## Requirements

* Django 1.3+
* Python 2.6+

## Dependencies

TUple takes advantage of some great tools, which are included in this distribution. 

* MathJax
* JQuery
* CSS Tabs
* Appraise

## Setup

After installing TUple, you will need to configure a few things for your server. First edit the settings.py file:

	mate TUple/settins.py

Edit the DATABASES dictionary to connect to your database. TUple should work fine with any of Django's database backends. (http://docs.djangoproject.com/en/dev/ref/settings/?from=olddocs#std:setting-DATABASES)[This page] has more information on the database options Django offers.

You will also want to modify the SECRET_KEY field. You can generate a key by running the following python script (thanks to (http://mylesbraithwaite.com/journal/2007/10/secret-key/)[Myles Braithwaite]).

	import string
	from random import choice
	
	print ''.join([choice(string.letters + string.digits + string.punctuation) for i in range(50)])

By default, TUple uses a file-based cache. If you want to use a different backend or change where the file cache is stored, you need to edit the CACHES dictionary. More information available (http://docs.djangoproject.com/en/dev/topics/cache/)[here].

You're now ready to connect Django to your database and set up all the tables.

	cd TUple
	python manage.py syncdb

You will be asked to create an admin user. This user will be the admin user that you will use to login to view grades and create exam sessions.



## Customization

TUple was created for Trinity University, and the provided resources reflect that. You'll want to change these. I have tried to strip as much Trinity material from the package, but you will want to change the header image, which is at TUple/media/images/header.png.

Otherwise, everything else should be configurable in the administration pages.

The text on the exam pages is hardcoded into the template files, so you will likely need to modify them to suit your needs. A cursory knowledge of HTML will be useful. The main files to edit are:

* finished.html
* home.html
* instructions.html

After you have completely installed TUple and it is running on your server, open the site in your browser. Login as an admin user. Click the Settings tab. Fill in the name of the Exam, the copyright owner, the date that the copyright begins, and a contact email. Then click save.

Next, you will want to create an exam session. Click the Sessions tab, and click the Create New Session button. Fill out the settings, add students, and create the problem set.

## License

Copyright (c) 2010 Dustin Bachrach

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
