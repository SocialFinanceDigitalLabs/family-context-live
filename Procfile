web: gunicorn family_context.wsgi
release: sh -c 'npm install && npm run build' && python manage.py migrate && python manage.py generate_dummy_data && python manage.py data_intake ./fixtures/acute.csv && python manage.py data_intake ./fixtures/ASC.csv && python manage.py data_intake ./fixtures/community.csv && python manage.py data_intake ./fixtures/CSC.csv && python manage.py data_intake ./fixtures/housing.csv