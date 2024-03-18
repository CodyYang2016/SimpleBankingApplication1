Project overview and setup instructions


# How to test APIs:



curl -X POST http://localhost:8000/customers/ \
  -H 'Content-Type: application/json' \
  -d '{"first_name": "Jane", "last_name": "Doe", "email": "jane.doe@example.com", "raw_password": "s3cr3t"}'
