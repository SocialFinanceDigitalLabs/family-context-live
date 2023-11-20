web: gunicorn family_context.wsgi
release: sh -c 'npm install && npm run build' \
  && python manage.py migrate && python manage.py generate_dummy_data \
  && python manage.py data_intake './fixtures/Acute.csv' './fixtures/Adult Social Care.csv' \
  './fixtures/Community.csv' './fixtures/Childrens Social Care.csv' './fixtures/Housing.csv'