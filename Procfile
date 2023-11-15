web: gunicorn family_context.wsgi
release: sh -c 'npm install && npm run build' \
  && python manage.py migrate && python manage.py generate_dummy_data \
  && python manage.py data_intake ./fixtures/acute.csv ./fixtures/ASC.csv \
  ./fixtures/community.csv ./fixtures/CSC.csv ./fixtures/housing.csv