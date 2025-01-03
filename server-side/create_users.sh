
#!/bin/bash
# Register Visitor
curl -X POST "http://localhost:8000/api/auth/register/" \
  -H "Content-Type: application/json" \
  --data '{
    "email": "visitor@example.com",
    "name": "Visitor Name",
    "role": "visitor",
    "password": "deneme"
  }'

# Register Secretary
curl -X POST "http://localhost:8000/api/auth/register/" \
  -H "Content-Type: application/json" \
  --data '{
    "email": "secretary@example.com",
    "name": "Secretary Name",
    "role": "secretary",
    "password": "deneme"
  }'

# Register Guide
curl -X POST "http://localhost:8000/api/auth/register/" \
  -H "Content-Type: application/json" \
  --data '{
    "email": "guide@example.com",
    "name": "Guide Name",
    "role": "guide",
    "password": "deneme"
  }'

# Register Advisor
curl -X POST "http://localhost:8000/api/auth/register/" \
  -H "Content-Type: application/json" \
  --data '{
    "email": "advisor@example.com",
    "name": "Advisor Name",
    "role": "advisor",
    "password": "deneme"
  }'

# Register Director
curl -X POST "http://localhost:8000/api/auth/register/" \
  -H "Content-Type: application/json" \
  --data '{
    "email": "director@example.com",
    "name": "Director Name",
    "role": "director",
    "password": "deneme"
  }'