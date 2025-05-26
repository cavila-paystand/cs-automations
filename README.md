# CS Automations

A Flask-based web service that runs on port 5001, containerized with Docker.

## Prerequisites

- Docker and Docker Compose
- Python 3.9+ (for local development)
- Google Cloud credentials (account_service_credentials.json)


## Environment Variables

The following environment variables are required:
- `API_KEY`: Your API key for securing the service endpoints
- `FLASK_APP`: Set to `app.py`
- `FLASK_ENV`: Set to `production`

## Project Structure 

## API Endpoints

### GET /get-google-token

Retrieves a Google API access token for the service account.

**Headers Required:**
- `X-API-Key`: Your API key for authentication

**Response:**
```json
{
    "access_token": "ya29.abc123..."
}
```

**Error Responses:**
- 401 Unauthorized: Invalid or missing API key
- 500 Internal Server Error: Issues with Google credentials or token generation

**Token Scopes:**
The token provides access to:
- Google Drive API
- Google Sheets API

## Running the Application

### Using Docker (Recommended)

1. Ensure you have Docker and Docker Compose installed
2. Set up Google Cloud credentials:
   - Create a service account in Google Cloud Console
   - Download the service account key as `account_service_credentials.json`
   - Place it in the project root
3. Create a `.env` file with your `API_KEY`:
   ```
   API_KEY=your_secure_api_key_here
   ```
4. Build and run the containers:
   ```bash
   docker-compose build
   docker-compose up
   ```
5. The service will be available at `http://localhost:5001`

### Local Development

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   export API_KEY=your_api_key  # On Windows: set API_KEY=your_api_key
   export FLASK_APP=app.py
   export FLASK_ENV=development
   ```

4. Run the application:
   ```bash
   gunicorn --bind 0.0.0.0:5001 wsgi:app
   ```

## Docker Configuration

The application runs in a Python 3.9 slim container with:
- Gunicorn as the WSGI server
- Port 5001 exposed
- Google Cloud credentials mounted as a read-only volume
- Automatic restart on failure

## Security Notes

- The `account_service_credentials.json` file is mounted as read-only in the container
- Environment variables are used for sensitive configuration
- The service runs in production mode with appropriate security settings
- API endpoints are protected with API key authentication
- Service account credentials are securely stored and accessed

## Error Handling

The service implements the following error handling:
- Invalid API keys return 401 Unauthorized
- Missing credentials return appropriate error messages
- Token refresh failures are handled gracefully

## Monitoring and Logs

- Docker logs can be accessed using:
  ```bash
  docker-compose logs -f
  ```
- Application logs are output to stdout/stderr
- Container health can be monitored through Docker's health check system
