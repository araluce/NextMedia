#Makefile

clean:
	rm -rf *~* && find . -name '*.pyc' -exec rm {} \;
	
install:
	python setup.py install

test: 
	python manage.py test NextMedia/
	
run:
	sudo service mongodb start
	python manage.py migrate
	python manage.py runserver
	
doc:
	pycco NextMedia/*.py
