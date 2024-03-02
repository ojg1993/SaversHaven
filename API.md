# 🗂 API Documentation

## Auth

Provides User Authentication related functionalities

### User Registration

`POST` api/auth/registration/

##### Parameters

| Field          | Type     | In   | Description                             |
|----------------|----------|------|-----------------------------------------|
| `email`        | `string` | body | Specifies the email of the user.        |
| `password1`    | `string` | body | Specifies the password of the user.     |
| `password2`    | `string` | body | Specifies the password confirmation.    |
| `nickname`     | `string` | body | Specifies the nickname of the user.     |
| `first_name`   | `string` | body | Specifies the first name of the user.   |
| `last_name`    | `string` | body | Specifies the last name of the user.    |
| `phone_number` | `string` | body | Specifies the phone number of the user. |

##### Request Example

``` http request
{
  "email": "user@example.com",
  "password1": "string",
  "password2": "string",
  "nickname": "string",
  "first_name": "string",
  "last_name": "string",
  "phone_number": "string"
}
```

##### Response Example

| Status Code       | Description                                                                            |
|-------------------|----------------------------------------------------------------------------------------|
| `201 Created`     | Indicates a successful registration. The sever sends a verification email to the user. |
| `400 Bad Request` | Indicates that the parameters provided are invalid.                                    |

``` http response
201
{
    "detail": "Verification e-mail sent."
}
```

```
400
{
    "email": [
        "A user is already registered with this e-mail address."
    ]
}
```

### Re-send Email Verification

`POST` api/auth/registration/resend-email/

##### Parameters

| Field   | Type     | In   | Description                      |
|---------|----------|------|----------------------------------|
| `email` | `string` | body | Specifies the email of the user. |

##### Request Example

``` http request
{
  "email": "user@example.com",
}
```

##### Status Codes

| Status Code | Description                                          |
|-------------|------------------------------------------------------|
| `200 OK`    | Indicates that email verification successfully sent. |

``` http response
200
{
  "detail": "ok"
}
```

### Confirm Email Verification

`POST` api/auth/registration/account-confirm-email/{key}/

##### Parameters

| Field | Type     | In   | Description                          |
|-------|----------|------|--------------------------------------|
| `key` | `string` | body | Specifies the email key of the user. |

##### Request Example

``` http request
{
  "key": "string",
}
```

##### Status Codes

| Status Code | Description                                          |
|-------------|------------------------------------------------------|
| `200 OK`    | Indicates that the account is verified successfully. |

### Reset Password

`POST` api/auth/password/reset/

##### Parameters

| Field   | Type     | In   | Description                      |
|---------|----------|------|----------------------------------|
| `email` | `string` | body | Specifies the email of the user. |

##### Request Example

``` http request
{
  "email": "user@example.com"
}
```

##### Response Example

| Status Code | Description                                                   |
|-------------|---------------------------------------------------------------|
| `200 OK`    | Indicates that a password reset link sent to the given email. |

``` http response
200
{
  "detail": "Password reset e-mail has been sent."
}
```

### Confirm Password Reset

`POST` api/auth/password/reset/confirm/{uid64}/{token}/

##### Parameters

| Field           | Type     | In   | Description                                |
|-----------------|----------|------|--------------------------------------------|
| `uid`           | `string` | body | Specifies the unique id verifying the user |
| `token`         | `string` | body | Specifies the verification token.          |
| `new_password1` | `string` | body | Specifies the new password of the user.    |
| `new_password2` | `string` | body | Specifies the password confirmation.       |

##### Request Example

``` http request
{
  "new_password1": "string",
  "new_password2": "string",
  "uid": "string",
  "token": "string"
}
```

##### Status codes

| Status Code       | Description                                                   |
|-------------------|---------------------------------------------------------------|
| `200 OK`          | Indicates that a password reset link sent to the given email. |
| `400 Bad Request` | Indicates the parameters provided are invalid.                |

``` http response
200
{
  "detail": "string"
}
```

### User Login

`POST` api/auth/login/

##### Parameters

| Field      | Type     | In   | Description                         |
|------------|----------|------|-------------------------------------|
| `email`    | `string` | body | Specifies the email of the user.    |
| `password` | `string` | body | Specifies the password of the user. |

##### Request Example

``` http request
{
  "email": "user@example.com",
  "password": "string",
}
```

##### Response Example

| Status Code       | Description                                                                                                                      |
|-------------------|----------------------------------------------------------------------------------------------------------------------------------|
| `200 OK`          | Indicates a successful credential validation returning access & refresh tokens with user information.                            |
| `400 Bad Request` | Indicates email verification is required or the parameters provided are invalid. Check the response body for additional details. |

``` http response
200
{
  "access_token": "string",
  "refresh_token": "string",
  "user": {
    "email": "user@example.com",
    "nickname": "string",
    "first_name": "string",
    "last_name": "string",
    "phone_number": "string"
  }
}
```

```
400
{
  "non_field_errors": [
    "E-mail is not verified."
  ]
}

or

400
{
  "non_field_errors": [
    "Unable to log in with provided credentials."
  ]
}
```

### Google(OAuth2) Login / Registration

`POST` api/auth/google/login/

▽

`POST` api/auth/google/login/callback/

▽

`POST` api/auth/google/login/finish/

##### Status codes

| Status Code       | Description                                                                  |
|-------------------|------------------------------------------------------------------------------|
| `200 OK`          | Indicates a successful login/registration with redirection to the main page. |
| `400 Bad Request` | Indicates that the given email is already registered but not a social user.  |

``` http response
400
{
    "err_msg": "email exists but not a google user"
}
```

### Change Password

`POST` api/auth/password/change/

##### Parameters

| Field           | Type     | In     | Description                             |
|-----------------|----------|--------|-----------------------------------------|
| `Authorization` | `string` | header | Specifies the bearer token of user.     |
| `new_password1` | `string` | body   | Specifies the new password of the user. |
| `new_password2` | `string` | body   | Specifies the password confirmation.    |

##### Request Example

``` http request
{
  "new_password1": "string",
  "new_password2": "string"
}
```

##### Status codes

| Status Code        | Description                                                                      |
|--------------------|----------------------------------------------------------------------------------|
| `200 OK`           | Indicates a successful password change.                                          |
| `401 Unauthorized` | Indicates that the token is invalid or expired.                                  |
| `400 Bad Request`  | Indicates email verification is required or the parameters provided are invalid. |

``` http response
200
{
  "detail": "string"
}
```

### Verify Token

`POST` api/auth/token/verify/

##### Parameters

| Field   | Type     | In   | Description                 |
|---------|----------|------|-----------------------------|
| `token` | `string` | body | Specifies the access token. |

##### Request Example

``` http request
{
  "token": "string"
}
```

##### Response Example

| Status Code        | Description                                        |
|--------------------|----------------------------------------------------|
| `200 OK`           | Indicates that the token is successfully verified. |
| `401 Unauthorized` | Indicates that the token is invalid or expired.    |

``` http response
401
{
  "detail": "Token is invalid or expired",
  "code": "token_not_valid"
}
```

### Refresh Token

`POST` api/auth/token/refresh/

##### Parameters

| Field     | Type     | In   | Description                  |
|-----------|----------|------|------------------------------|
| `refresh` | `string` | body | Specifies the refresh token. |

##### Request Example

``` http request
{
  "refresh": "string"
}
```

##### Response Example

| Status Code        | Description                                     |
|--------------------|-------------------------------------------------|
| `200 OK`           | Indicates that the access token is refreshed.   |
| `401 Unauthorized` | Indicates that the token is invalid or expired. |

``` http response
200
{
  "access": "string"
}
```

``` http response
401
{
  "detail": "Token is invalid or expired",
  "code": "token_not_valid"
}
```

### Get User Information

`GET` api/auth/user/

##### Parameters

| Field           | Type     | In     | Description                         |
|-----------------|----------|--------|-------------------------------------|
| `Authorization` | `string` | header | Specifies the bearer token of user. |

##### Response Example

| Status Code        | Description                                     |
|--------------------|-------------------------------------------------|
| `200 OK`           | Indicates a successful response.                |
| `401 Unauthorized` | Indicates that the token is invalid or expired. |

``` http response
200
{
  "email": "user@example.com",
  "nickname": "string",
  "first_name": "string",
  "last_name": "string",
  "phone_number": "string"
}
```

``` http response
401
{
  "detail": "Authentication credentials were not provided."
}
```

### Update User Information

`PUT` api/auth/user/

##### Parameters

| Field           | Type     | In     | Description                         |
|-----------------|----------|--------|-------------------------------------|
| `Authorization` | `string` | header | Specifies the bearer token of user. |

##### Request Example

```
{
  "email": "user@example.com",
  "password": "stringstri",
  "nickname": "string",
  "first_name": "string",
  "last_name": "string",
  "phone_number": "string"
}
```

##### Response Example

| Status Code        | Description                                     |
|--------------------|-------------------------------------------------|
| `200 OK`           | Indicates a successful response.                |
| `401 Unauthorized` | Indicates that the token is invalid or expired. |

``` http response
200
{
  "email": "user@example.com",
  "nickname": "string",
  "first_name": "string",
  "last_name": "string",
  "phone_number": "string"
}
```

``` http response
401
{
  "detail": "Authentication credentials were not provided."
}
```

### Partial-update User Information

`PATCH` api/auth/user/

##### Parameters

| Field           | Type     | In     | Description                         |
|-----------------|----------|--------|-------------------------------------|
| `Authorization` | `string` | header | Specifies the bearer token of user. |

##### Request Example

```
{
  "nickname": "string",
}
```

##### Response Example

| Status Code        | Description                                     |
|--------------------|-------------------------------------------------|
| `200 OK`           | Indicates a successful response.                |
| `401 Unauthorized` | Indicates that the token is invalid or expired. |

``` http response
200
{
  "email": "user@example.com",
  "nickname": "string",
  "first_name": "string",
  "last_name": "string",
  "phone_number": "string"
}
```

``` http response
401
{
  "detail": "Authentication credentials were not provided."
}
```

## Address

Provides Address related CRUD functionalities

### Country CURD

| Method   | Path                          | Parameter             | Authorization | Description                                 |
|----------|-------------------------------|-----------------------|---------------|---------------------------------------------|
| `GET`    | `api/address/countries/`      |                       | All           | Get all countries available.                |
| `POST`   | `api/address/countries/`      | str: name             | IsAdmin       | Create a country.                           |
| `GET`    | `api/address/countries/{id}/` | int: id               | IsAdmin       | Get the country's information.              |
| `PUT`    | `api/address/countries/{id}/` | int: id<br/>str: name | IsAdmin       | Update the country's information.           |
| `PATCH`  | `api/address/countries/{id}/` | int: id               | IsAdmin       | Partially Update the country's information. |
| `DELETE` | `api/address/countries/{id}/` | int: id               | IsAdmin       | Delete the country.                         |

### County CURD

| Method   | Path                         | Parameter                                | Authorization | Description                                |
|----------|------------------------------|------------------------------------------|---------------|--------------------------------------------|
| `GET`    | `api/address/counties/`      | Parameter                                | All           | Get all counties available.                |
| `POST`   | `api/address/counties/`      | str: name<br/>int: countryId             | IsAdmin       | Create a county.                           |
| `GET`    | `api/address/counties/{id}/` | int: id                                  | IsAdmin       | Get the county's information.              |
| `PUT`    | `api/address/counties/{id}/` | int: id<br/>str: name<br/>int: countryId | IsAdmin       | Update the county's information.           |
| `PATCH`  | `api/address/counties/{id}/` | int: id                                  | IsAdmin       | Partially Update the county's information. |
| `DELETE` | `api/address/counties/{id}/` | int: id                                  | IsAdmin       | Delete the county.                         |

### City CRUD

| Method   | Path                       | Parameter                               | Authorization | Description                              |
|----------|----------------------------|-----------------------------------------|---------------|------------------------------------------|
| `GET`    | `api/address/cities/`      |                                         | All           | Get all cities available.                |
| `POST`   | `api/address/cities/`      | str: name<br/>int: countyId             | IsAdmin       | Create a city.                           |
| `GET`    | `api/address/cities/{id}/` | int: id                                 | IsAdmin       | Get the county's information.            |
| `PUT`    | `api/address/cities/{id}/` | int: id<br/>str: name<br/>int: countyId | IsAdmin       | Update the city's information.           |
| `PATCH`  | `api/address/cities/{id}/` | int: id                                 | IsAdmin       | Partially Update the city's information. |
| `DELETE` | `api/address/cities/{id}/` | int: id                                 | IsAdmin       | Delete the city.                         |

### Address CRUD

| Method   | Path                          | Parameter                                                                                                  | Authorization   | Description                                 |
|----------|-------------------------------|------------------------------------------------------------------------------------------------------------|-----------------|---------------------------------------------|
| `GET`    | `api/address/addresses/`      |                                                                                                            | IsAuthenticated | Get all addresses available.                |
| `POST`   | `api/address/addresses/`      | str: name<br/>str: post_code<br/>int:city_id<br/>str: street_address1<br/>str: street_address2             | IsAuthenticated | Create an address.                          |
| `GET`    | `api/address/addresses/{id}/` | int: id                                                                                                    | IsAuthenticated | Update the address's information.           |
| `PUT`    | `api/address/addresses/{id}/` | int: id<br/>str: name<br/>str: post_code<br/>int:city_id<br/>str: street_address1<br/>str: street_address2 | IsAuthenticated | Update the address's information.           |
| `PATCH`  | `api/address/addresses/{id}/` | int: id                                                                                                    | IsAuthenticated | Partially Update the address's information. |
| `DELETE` | `api/address/addresses/{id}/` | int: id                                                                                                    | IsAuthenticated | Delete the address.                         |

## Product

Provides Product related CRUD functionalities

- Category CRUD
- Product CRUD
- Product favorite / Undo favorite

### Category CRUD

| Method   | Path                           | Parameter                                                                                                  | Authorization     | Description                                  |
|----------|--------------------------------|------------------------------------------------------------------------------------------------------------|-------------------|----------------------------------------------|
| `GET`    | `api/product/categories/`      |                                                                                                            | IsAdminOrReadOnly | Get all categories available.                |
| `POST`   | `api/product/categories/`      | str: name<br/>str: post_code<br/>int:city_id<br/>str: street_address1<br/>str: street_address2             | IsAdminOrReadOnly | Create a category.                           |
| `GET`    | `api/product/categories/{id}/` | int: id                                                                                                    | IsAdminOrReadOnly | Update the category's information.           |
| `PUT`    | `api/product/categories/{id}/` | int: id<br/>str: name<br/>str: post_code<br/>int:city_id<br/>str: street_address1<br/>str: street_address2 | IsAdminOrReadOnly | Update the category's information.           |
| `PATCH`  | `api/product/categories/{id}/` | int: id                                                                                                    | IsAdminOrReadOnly | Partially Update the category's information. |
| `DELETE` | `api/product/categories/{id}/` | int: id                                                                                                    | IsAdminOrReadOnly | Delete the category.                         |

### Get a list of products

`GET` api/product/products/

##### Response Example

| Status Code | Description                      |
|-------------|----------------------------------|
| `200 OK`    | Indicates a successful response. |

``` http response
200
[
  {
    "id": 0,
    "seller": 0,
    "category": 0,
    "title": "string",
    "price": "0.00",
    "description": "string",
    "images": [
      {
        "image": "string"
      }
    ],
    "bookmark_cnt": 0,
    "created_at": "2024-02-26T13:08:10.518Z",
    "modified_at": "2024-02-26T13:08:10.518Z"
  },
]
```

### Upload a product

`POST` api/product/products/

##### Parameters

| Field             | Type      | In     | Description                                    |
|-------------------|-----------|--------|------------------------------------------------|
| `Authorization`   | `string`  | header | Specifies the bearer token of user.            |
| `category`        | `integer` | body   | Specifies the category the product belongs to. |
| `title`           | `string`  | body   | Specifies title of the product.                |
| `price`           | `string`  | body   | Specifies price of the product.                |
| `description`     | `string`  | body   | Specifies description of the product.          |
| `uploaded_images` | `file`    | body   | Specifies image files of the product.          |

##### Request Example

``` http request
{
  "category": 0,
  "title": "string",
  "price": "0.00",
  "description": "string",
  "uploaded_images": [
    {
      "file",
      "file2"
    }
  ]
}
```

##### Response Example

| Status Code        | Description                                     |
|--------------------|-------------------------------------------------|
| `201 Created`      | Indicates a successful response.                |
| `401 Unauthorized` | Indicates that the token is invalid or expired. |

``` http response
201
{
    "id": 0,
    "seller": 0,
    "category": 0,
    "title": "string",
    "price": "0.00",
    "description": "string",
    "images": [
        {
            "image": "file",
            "image": "file2"

        }
    ],
    "is_sold": false,
    "bookmark_cnt": 0,
    "created_at": "2024-02-26T13:35:01.084818Z",
    "modified_at": "2024-02-26T13:35:01.084818Z"
}
```

``` http response
401
{
  "detail": "Authentication credentials were not provided."
}
```

### Get a single product

`GET` api/product/products/{id}/

#### Parameters

| Field | Type      | In     | Description                      |
|-------|-----------|--------|----------------------------------|
| `id`  | `integer` | header | Specifies the id of the product. |

##### Response Example

| Status Code     | Description                                              |
|-----------------|----------------------------------------------------------|
| `200 OK`        | Indicates a successful response.                         |
| `404 Not found` | Indicates that the product with given id does not exist. |

``` http response
200
{
    "id": 0,
    "seller": 0,
    "category": 0,
    "title": "string",
    "price": "0.00",
    "description": "string",
    "images": [],
    "is_sold": false,
    "bookmark_cnt": 0,
    "created_at": "2024-02-21T11:57:39.370325Z",
    "modified_at": "2024-02-21T11:57:39.370325Z",
    "hit_cnt": 0,
    "favorite": false
}
```

``` http response
404
{
  "detail": "Not found."
}
```

### Update a single product

`PUT`|`PATCH` api/product/products/{id}/

##### Parameters

| Field           | Type      | In     | Description                                                                     |
|-----------------|-----------|--------|---------------------------------------------------------------------------------|
| `id`            | `integer` | header | Specifies the id of the product.                                                |
| `Authorization` | `string`  | header | Specifies the bearer token of user. Only owner of the product or admin allowed. |

##### Request Example

``` http request
{
    "price": "100.00",
}
```

##### Response Example

| Status Code     | Description                                                         |
|-----------------|---------------------------------------------------------------------|
| `200 OK`        | Indicates a successful response.                                    |
| `403 Forbidden` | Indicates that current auth user is not allowed to the such action. |
| `404 Not found` | Indicates that the product with given id does not exist.            |

``` http response
200
{
    "id": 0,
    "seller": 0,
    "category": 0,
    "title": "string",
    "price": "100.00",
    "description": "string",
    "images": [],
    "is_sold": false,
    "bookmark_cnt": 0,
    "created_at": "2024-02-21T11:57:39.370325Z",
    "modified_at": "2024-02-21T11:57:39.370325Z",
    "hit_cnt": 0,
    "favorite": false
}
```

``` http response
403
{
    "detail": "You do not have permission to perform this action."
}
```

``` http response
404
{
  "detail": "Not found."
}
```

### Delete a single product

`DELETE` api/product/products/{id}/

##### Parameters

| Field           | Type      | In     | Description                                                                     |
|-----------------|-----------|--------|---------------------------------------------------------------------------------|
| `id`            | `integer` | header | Specifies the id of the product.                                                |
| `Authorization` | `string`  | header | Specifies the bearer token of user. Only owner of the product or admin allowed. |

##### Response Example

| Status Code        | Description                                              |
|--------------------|----------------------------------------------------------|
| `204 No Content`   | Indicates a successful response.                         |
| `401 Unauthorized` | Indicates that the token is invalid or expired.          |
| `404 Not found`    | Indicates that the product with given id does not exist. |

``` http response
204
```

``` http response
401
{
  "detail": "Token is invalid or expired",
  "code": "token_not_valid"
}
```

``` http response
404
{
  "detail": "Not found."
}
```

### Save a favorite product

`POST` api/product/products/{id}/favorite/

##### Parameters

| Field           | Type      | In     | Description                                          |
|-----------------|-----------|--------|------------------------------------------------------|
| `id`            | `integer` | header | Specifies the id of the product intending to update. |
| `Authorization` | `string`  | header | Specifies the bearer token of user.                  |

##### Response Example

| Status Code        | Description                                                               |
|--------------------|---------------------------------------------------------------------------|
| `201 Created`      | Indicates a successful response.                                          |
| `400 Bad Request`  | Indicates that the product with given id does not exist or already saved. |
| `401 Unauthorized` | Indicates that the token is invalid or expired.                           |

``` http response
201
{
    "message": "Favorite saved"
}
```

``` http response
400
{
    "message": "Already saved as a favorite"
}

or

{
    "product": [
        "Invalid pk \"id\" - object does not exist."
    ]
}
```

``` http response
401
{
  "detail": "Token is invalid or expired",
  "code": "token_not_valid"
}
```

### Delete a favorite product

`DELETE` api/product/products/{id}/favorite/

##### Parameters

| Field           | Type      | In     | Description                                          |
|-----------------|-----------|--------|------------------------------------------------------|
| `id`            | `integer` | header | Specifies the id of the product intending to update. |
| `Authorization` | `string`  | header | Specifies the bearer token of user.                  |

##### Response Example

| Status Code        | Description                                           |
|--------------------|-------------------------------------------------------|
| `204 No Content`   | Indicates a successful response.                      |
| `400 Bad Request`  | Indicates that the product has not saved as favorite. |
| `401 Unauthorized` | Indicates that the token is invalid or expired.       |

``` http response
204
{
    "message": "Favorite removed"
}
```

``` http response
400
{
    "message": "Not saved as a favorite"
}

```

``` http response
401
{
  "detail": "Token is invalid or expired",
  "code": "token_not_valid"
}
```

## Chat

Provides live messaging between two users functionality

### Get a list of related chat rooms

`GET` api/chat/rooms/

##### Response Example

| Status Code        | Description                                     |
|--------------------|-------------------------------------------------|
| `200 OK`           | Indicates a successful response.                |
| `401 Unauthorized` | Indicates that the token is invalid or expired. |

``` http response
200
[
    {
        "id": 0,
        "product": 0,
        "seller": 0,
        "buyer": 0,
        "latest_message": null,
        "messages": []
    }
]
```

``` http response
401
{
  "detail": "Token is invalid or expired",
  "code": "token_not_valid"
}
```

## Chat

Provides live messaging between two users functionality

### Get a list of related chat rooms

`GET` api/chat/rooms/

##### Response Example

| Status Code        | Description                                     |
|--------------------|-------------------------------------------------|
| `200 OK`           | Indicates a successful response.                |
| `401 Unauthorized` | Indicates that the token is invalid or expired. |

``` http response
200
[
    {
        "id": 0,
        "product": 0,
        "seller": 0,
        "buyer": 0,
        "latest_message": null,
        "messages": []
    }
]
```

``` http response
401
{
  "detail": "Token is invalid or expired",
  "code": "token_not_valid"
}
```

### Get or Create a chat room with the product owner

`POST` api/chat/rooms/

##### Parameters

| Field        | Type      | In   | Description                                                |
|--------------|-----------|------|------------------------------------------------------------|
| `product_id` | `integer` | body | Specifies the id of the  product that the user interested. |

##### Response Example

| Status Code        | Description                                                                   |
|--------------------|-------------------------------------------------------------------------------|
| `200 OK`           | Indicates that chat room already exists. Returning the chat room information. |
| `201 Created`      | Indicates that chat room does not exist. Creating a chat room                 |
| `401 Unauthorized` | Indicates that the token is invalid or expired.                               |

``` http response
200 or 201
[
    {
        "id": 0,
        "product": 0,
        "seller": 0,
        "buyer": 0,
        "latest_message": null,
        "messages": []
    }
]
```

``` http response
401
{
  "detail": "Token is invalid or expired",
  "code": "token_not_valid"
}
```

### Get a list of messages belonging to the chatroom

`POST` api/chat/rooms/{room_id}/

##### Parameters

| Field     | Type      | In     | Description                       |
|-----------|-----------|--------|-----------------------------------|
| `room_id` | `integer` | header | Specifies the id of the chatroom. |

##### Response Example

| Status Code     | Description                                                                   |
|-----------------|-------------------------------------------------------------------------------|
| `200 OK`        | Indicates that chat room already exists. Returning the chat room information. |
| `404 Not Found` | Indicates that message does not exists in the given chatroom.                 |

``` http response
200
[
    {
        "id": 0,
        "sender": "string",
        "text": "string",
        "created_at": "2024-02-26T14:27:52.044217Z",
        "room": 0
    }
]
```

``` http response
400
{
    "detail": "Not found."
}
```

### Establish a connection to a chatroom

`GET` ws://localhost:8000/ws/rooms/{room_id}/

##### Parameters

| Field     | Type      | In     | Description                       |
|-----------|-----------|--------|-----------------------------------|
| `room_id` | `integer` | header | Specifies the id of the chatroom. |

##### Request Example

```
// WebSocket connection
var socket = new WebSocket("ws://localhost:8000/ws/rooms/{room_id}/");
```

##### Response Example

| Status Code             | Description                                                         |
|-------------------------|---------------------------------------------------------------------|
| `WebSocket HANDSHAKING` | Indicates that the client and server are establishing a connection. |
| `WebSocket CONNECT`     | Indicates that connection is successfully established.              |

<br>

![image](https://github.com/ojg1993/SaversHaven/assets/61238157/31febeb4-5194-4b5b-8cdb-3da368ea2579)

### Send a message to the chatroom

ws://localhost:8000/ws/rooms/{room_id}/

##### Parameters

| Field     | Type      | In   | Description                       |
|-----------|-----------|------|-----------------------------------|
| `room_id` | `integer` | body | Specifies the id of the chatroom. |
| `message` | `string`  | body | Specifies message content.        |
| `sender`  | `string`  | body | Specifies nickname of the sender. |

##### Request Example

```
// Messaging function
function sendMessage(message) {
    var messageObject = {
        type: "message",
        content: message,
        sender: "admin",
        room_id: 1
    };
    // Serializing to json format ans sending it to the server
    socket.send(JSON.stringify(messageObject));
}

// calling messaging function
sendMessage("WebSocket api documentation!");
```

##### Response Example

![image](https://github.com/ojg1993/SaversHaven/assets/61238157/52304d2f-0832-4e5e-820a-3b86a8af1541)

## Direct Transactions

Provides Direct Transaction CRUD functionalities

### Get a list of related direct transactions

`GET` api/transaction/direct-transactions/

##### Parameters

| Field           | Type     | In     | Description                         |
|-----------------|----------|--------|-------------------------------------|
| `Authorization` | `string` | header | Specifies the bearer token of user. |

##### Response Example

| Status Code        | Description                                     |
|--------------------|-------------------------------------------------|
| `200 OK`           | Indicates a successful response.                |
| `401 Unauthorized` | Indicates that the token is invalid or expired. |

``` http response
200
[
    {
        "id": 0,
        "title": "string",
        "price": "0.00",
        "chatroom": 0,
        "time": "2024-02-22-13:30",
        "location": 0,
        "location_detail": "string",
        "status": "reserved",
        "created_at": "2024-02-21-12:31:56",
        "modified_at": "2024-02-21-12:31:56"
    }
]
```

```http response
401
{
    "detail": "Authentication credentials were not provided."
}
```

### Book a direct transaction

`POST` api/transaction/direct-transactions/

##### Parameters

| Field             | Type      | In     | Description                                           |
|-------------------|-----------|--------|-------------------------------------------------------|
| `Authorization`   | `string`  | header | Specifies the bearer token of user.                   |
| `chatroom`        | `integer` | body   | Specifies the chatroom the transaction book occurred. |
| `location`        | `integer` | body   | Specifies city location.                              |
| `location_detail` | `string`  | body   | Specifies detailed location.                          |
| `time`            | `string`  | body   | Specifies time of direct transaction.                 |

##### Request Example

``` http request
{
    "chatroom": 0,
    "time": "2024-02-24-18:30",
    "location": 0,
    "location_detail": "string",
}
```

##### Response Example

| Status Code        | Description                                     |
|--------------------|-------------------------------------------------|
| `201 Created`      | Indicates a successful response.                |
| `401 Unauthorized` | Indicates that the token is invalid or expired. |

``` http response
201
{
    "id": 0,
    "title": "string",
    "price": "0.00",
    "chatroom": 0,
    "time": "2024-02-24-18:30",
    "location": 0,
    "location_detail": "string",
    "status": "string",
    "created_at": "2024-02-26-15:26:24",
    "modified_at": "2024-02-26-15:26:24"
}
```

``` http response
401
{
  "detail": "Authentication credentials were not provided."
}
```

### Get a single direct transaction information

`GET` api/transaction/direct-transactions/{id}/

#### Parameters

| Field           | Type      | In     | Description                                                                     |
|-----------------|-----------|--------|---------------------------------------------------------------------------------|
| `Authorization` | `string`  | header | Specifies the bearer token of user. Only owner of the product or admin allowed. |
| `id`            | `integer` | header | Specifies the id of the direct transaction.                                     |

##### Response Example

| Status Code     | Description                                                  |
|-----------------|--------------------------------------------------------------|
| `200 OK`        | Indicates a successful response.                             |
| `404 Not found` | Indicates that the transaction with given id does not exist. |

``` http response
200
{
    "id": 0,
    "title": "string",
    "price": "0.00",
    "chatroom": 0,
    "time": "2024-02-24-18:30",
    "location": 0,
    "location_detail": "string",
    "status": "string",
    "created_at": "2024-02-26-15:26:24",
    "modified_at": "2024-02-26-15:26:24"
}
```

``` http response
404
{
  "detail": "Not found."
}
```

### Update a product information and status

`PUT`|`PATCH` api/transaction/direct-transactions/{id}/

##### Parameters

| Field           | Type      | In     | Description                                                                     |
|-----------------|-----------|--------|---------------------------------------------------------------------------------|
| `Authorization` | `string`  | header | Specifies the bearer token of user. Only owner of the product or admin allowed. |
| `id`            | `integer` | header | Specifies the id of the product.                                                |

##### Request Example

``` http request
{
    "status": "complete"
}
```

##### Response Example

| Status Code     | Description                                                                        |
|-----------------|------------------------------------------------------------------------------------|
| `200 OK`        | Indicates a successful response.                                                   |
| `404 Not found` | Indicates that the transaction with given id belonging to the user does not exist. |

``` http response
200
{
    "id": 0,
    "title": "string",
    "price": "0.00",
    "chatroom": 0,
    "time": "2024-02-24-18:30",
    "location": 0,
    "location_detail": "string",
    "status": "complete",
    "created_at": "2024-02-26-15:26:24",
    "modified_at": "2024-02-26-15:26:24"
}
```

``` http response
404
{
  "detail": "Not found."
}
```

## Review

Provides Review CRUD functionalities

### Get a list of related reviews

`GET` api/review/reviews/

##### Parameters

| Field           | Type     | In     | Description                         |
|-----------------|----------|--------|-------------------------------------|
| `Authorization` | `string` | header | Specifies the bearer token of user. |

##### Response Example

| Status Code        | Description                                     |
|--------------------|-------------------------------------------------|
| `200 OK`           | Indicates a successful response.                |
| `401 Unauthorized` | Indicates that the token is invalid or expired. |

``` http response
[
    {
        "id": 0,
        "transaction": 0,
        "reviewer": 0,
        "receiver": 0,
        "product_title": "string",
        "review": "string",
        "rating": 0,
        "created_at": "2024-02-26T15:37:56.267003Z"
    }
]
```

```http response
401
{
    "detail": "Authentication credentials were not provided."
}
```

### Leave a reviews to the opponent user

`POST` api/transaction/transactions/{id}/review/

##### Parameters

| Field           | Type      | In     | Description                                                |
|-----------------|-----------|--------|------------------------------------------------------------|
| `Authorization` | `string`  | header | Specifies the bearer token of user.                        |
| `review`        | `string`  | body   | Specifies the review message sending to the opponent user. |
| `rating`        | `integer` | body   | Specifies the rating score of the transaction.             |

##### Request Example

``` http resquest
{
  "review": "string."
  "rating": 0
}
```

##### Response Example

| Status Code       | Description                                |
|-------------------|--------------------------------------------|
| `201 Created`     | Indicates a successful response.           |
| `400 Bad Request` | Indicates that user already left a review. |

``` http response
200
{
    "message": "Review sent."
}
```

```http response
400
{
    "message": "Review already exists."
}
```

### Get a review detail

`POST` api/reviews/{id}

##### Parameters

| Field           | Type     | In     | Description                                                |
|-----------------|----------|--------|------------------------------------------------------------|
| `Authorization` | `string` | header | Specifies the bearer token of user.                        |
| `id`            | `string` | header | Specifies the review message sending to the opponent user. |

##### Response Example

| Status Code     | Description                                    |
|-----------------|------------------------------------------------|
| `200 OK`        | Indicates a successful response.               |
| `404 Not Found` | Indicates review with given id does not exist. |

``` http response
200
{
    "id": 0,
    "transaction": 0,
    "reviewer": 0,
    "receiver": 0,
    "product_title": "string",
    "review": "string",
    "rating": 0,
    "created_at": "2024-02-26T15:37:56.267003Z"
}
```

```http response
404
{
    "detail": "Not found."
}
```