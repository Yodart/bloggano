# Bloggano

![Flask](https://img.shields.io/badge/Flask-Web%20Framework-brightgreen)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![SQL](https://img.shields.io/badge/SQL-PostgreSQL-blue)
![JWT](https://img.shields.io/badge/JWT-Authentication-yellow)

This API is built using Flask, a lightweight web application framework in Python. It provides a comprehensive set of features for managing a blogging platform. With built-in JWT (JSON Web Token) authentication, users can create, edit, and delete articles. Additionally, users can comment on articles, like posts, and follow their favorite creators.
Rather than using traditional Object-Relational Mappers (ORMs), Bloggano employs the psycopg2 library to interact with the PostgreSQL database directly. This approach offers more control and flexibility over database operations.
The API is designed to be robust, secure, and easily extensible, making it a suitable foundation for building a dynamic blogging platform.

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/Bloggano-API.git

# Navigate to the project directory
cd Bloggano-API

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Authentication

To access protected routes, you need to authenticate using JWT (JSON Web Tokens). Follow these steps:

1. **Register a User**: Send a POST request to `/user` with a JSON payload containing `username` and `password` to create a new user.
2. **Login**: Send a GET request to `/auth/login` with Basic Authentication (username: `username`, password: `password`). You will receive a JWT token in response.
3. **Use the JWT Token**: Include the JWT token in the `x-access-token` header when making requests to protected routes, such as `/articles`.

### Article Operations

- **Create an Article**: Send a POST request to `/article` with a JSON payload containing `creator` and `content` to create a new article.
- **Read a Single Article**: Send a GET request to `/article/<article_id>` to retrieve article details by article ID.
- **Get Articles for a User**: Send a GET request to `/articles/<user_id>` to retrieve a list of all articles for a specific user. You can specify the `limit` and `offset` as query parameters for pagination.

### User Operations

- **Create a User**: Send a POST request to `/user` with a JSON payload containing `username` and `password` to create a new user.
- **Read a Single User**: Send a GET request to `/user/<user_id>` to retrieve user details by user ID.
- **Update a User**: Send a PUT request to `/user/<user_id>` with a JSON payload containing `name` and/or `last_name` to update user details.
- **Delete a User**: Send a DELETE request to `/user/<user_id>` to delete a user.
- **Get All Users**: Send a GET request to `/users` to retrieve a list of all users. You can specify the `limit` and `offset` as query parameters for pagination.

## Endpoints

### Authentication

- **Login**
  - Endpoint: `/auth/login`
  - Method: GET
  - Description: Logs in a user and provides a JWT token for authentication.
  - Authentication: Basic Authentication (username and password)

### Articles

- **Create an Article**
  - Endpoint: `/article`
  - Method: POST
  - Description: Create a new article.
  - Authentication: JWT token required
  - Request Body: JSON with `creator` and `content` fields.

- **Read a Single Article**
  - Endpoint: `/article/<article_id>`
  - Method: GET
  - Description: Retrieve a single article by its ID.
  - Authentication: JWT token required

- **Get Articles for a User**
  - Endpoint: `/articles/<user_id>`
  - Method: GET
  - Description: Retrieve a list of articles for a specific user.
  - Authentication: JWT token required
  - Query Parameters: `limit` (pagination limit), `offset` (pagination offset)

### Users

- **Create a User**
  - Endpoint: `/user`
  - Method: POST
  - Description: Create a new user.
  - Authentication: Not required
  - Request Body: JSON with `username` and `password` fields.

- **Read a Single User**
  - Endpoint: `/user/<user_id>`
  - Method: GET
  - Description: Retrieve user details by user ID.
  - Authentication: JWT token required

- **Update a User**
  - Endpoint: `/user/<user_id>`
  - Method: PUT
  - Description: Update user details (name and/or last name).
  - Authentication: JWT token required
  - Request Body: JSON with `name` and/or `last_name` fields.

- **Delete a User**
  - Endpoint: `/user/<user_id>`
  - Method: DELETE
  - Description: Delete a user.
  - Authentication: JWT token required

- **Get All Users**
  - Endpoint: `/users`
  - Method: GET
  - Description: Retrieve a list of all users.
  - Authentication: JWT token required
  - Query Parameters: `limit` (pagination limit), `offset` (pagination offset)

