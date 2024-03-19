# personal_assistant_api
API endpoint for personal assistant written in python

## Docker build step to use as container image
docker build -t --no-cache {name} .

# Personal Assistant API Documentation

Welcome to the Personal Assistant API! This API provides endpoints to retrieve information about IP addresses, check ports, and perform DNS lookups.

## Getting Started

To get started with the API, you can use the following endpoints:

- `/ipinfo`: Retrieve information about the IP address.
- `/portchecker`: Check if a port is open on a specified IP address.
- `/dnschecker`: Perform a DNS lookup for a given domain name.

## Endpoints

### IP Information

#### Get Information about IP Address

Endpoint: `/ipinfo/8.8.8.8`

Method: `GET`

Query Parameters:
- `ip`: The IP address to get information about.

Example:

Response:
```json
{
  "ip": "8.8.8.8",
  "city": "Mountain View",
  "country": "US"
}
