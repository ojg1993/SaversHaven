# 🗂 API Documentation

## Auth

Provides User Authentication related functionality

### User Registration

`POST` api/auth/registration/

##### Parameters

| Path           | Type     | In   | Description                             |
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

| Path    | Type     | In   | Description                      |
|---------|----------|------|----------------------------------|
| `email` | `string` | body | Specifies the email of the user. |

##### Request Example

``` http request
{
  "email": user@example.com,
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

| Path  | Type     | In   | Description                          |
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

| Path    | Type     | In   | Description                      |
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

| Path            | Type     | In   | Description                                |
|-----------------|----------|------|--------------------------------------------|
| `new_password1` | `string` | body | Specifies the new password of the user.    |
| `new_password2` | `string` | body | Specifies the password confirmation.       |
| `uid`           | `string` | body | Specifies the unique id verifying the user |
| `token`         | `string` | body | Specifies the verification token.          |

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

| Path       | Type     | In   | Description                         |
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
```

```
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
err_msg: "email exists but not a google user"
}
```

### Change Password 

`POST` api/auth/password/change/

##### Parameters

| Path            | Type     | In     | Description                             |
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

| Status Code        | Description                                                                                        |
|--------------------|----------------------------------------------------------------------------------------------------|
| `200 OK`           | Indicates a successful password change.                                                            |
| `401 Unauthorized` | Indicates that request has not been authenticated. Check the response body for additional details. |
| `400 Bad Request`  | Indicates email verification is required or the parameters provided are invalid.                   |

``` http response
200
{
  "detail": "string"
}
```

### Verify Token 

`POST` api/auth/token/verify/

##### Parameters

| Path    | Type     | In   | Description                 |
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
200
{}
```

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

| Path      | Type     | In   | Description                  |
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

| Path            | Type     | In     | Description                         |
|-----------------|----------|--------|-------------------------------------|
| `Authorization` | `string` | header | Specifies the bearer token of user. |

##### Response Example

| Status Code        | Description                                          |
|--------------------|------------------------------------------------------|
| `200 OK`           | Indicates a successful response.                     |
| `401 Unauthorized` | Indicates that the authentication were not provided. |

``` http response
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

| Path            | Type     | In     | Description                         |
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

| Status Code        | Description                                          |
|--------------------|------------------------------------------------------|
| `200 OK`           | Indicates a successful response.                     |
| `401 Unauthorized` | Indicates that the authentication were not provided. |

``` http response
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

| Path            | Type     | In     | Description                         |
|-----------------|----------|--------|-------------------------------------|
| `Authorization` | `string` | header | Specifies the bearer token of user. |

##### Request Example

```
{
  "nickname": "string",
}
```

##### Response Example

| Status Code        | Description                                          |
|--------------------|------------------------------------------------------|
| `200 OK`           | Indicates a successful response.                     |
| `401 Unauthorized` | Indicates that the authentication were not provided. |

``` http response
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

Provides Address related CRUD functionality

### Country CURD

| Method   | Path                          | Parameter | Authorization | Description                                 |
|----------|-------------------------------|-----------|---------------|---------------------------------------------|
| `GET`    | `api/address/countries/`      |           | All           | Get all countries available.                |
| `POST`   | `api/address/countries/`      | str: name | Admin         | Create a country.                           |
| `GET`    | `api/address/countries/{ID}/` | int: id   | Admin         | Get the country's information.              |
| `PUT`    | `api/address/countries/{ID}/` | int: id   | Admin         | Update the country's information.           |
| `PATCH`  | `api/address/countries/{ID}/` | int: id   | Admin         | Partially Update the country's information. |
| `DELETE` | `api/address/countries/{ID}/` | int: id   | Admin         | Delete the country.                         |

### County CURD

| Method   | Path                         | Parameter                    | Authorization | Description                                |
|----------|------------------------------|------------------------------|---------------|--------------------------------------------|
| `GET`    | `api/address/counties/`      | Parameter                    | All           | Get all counties available.                |
| `POST`   | `api/address/counties/`      | str: name<br/>int: countryId | Admin         | Create a county.                           |
| `GET`    | `api/address/counties/{ID}/` | int: id                      | Admin         | Get the county's information.              |
| `PUT`    | `api/address/counties/{ID}/` | int: id                      | Admin         | Update the county's information.           |
| `PATCH`  | `api/address/counties/{ID}/` | int: id                      | Admin         | Partially Update the county's information. |
| `DELETE` | `api/address/counties/{ID}/` | int: id                      | Admin         | Delete the county.                         |

### City CRUD

| Method   | Path                       | Parameter                   | Authorization | Description                              |
|----------|----------------------------|-----------------------------|---------------|------------------------------------------|
| `GET`    | `api/address/cities/`      |                             | All           | Get all cities available.                |
| `POST`   | `api/address/cities/`      | str: name<br/>int: countyId | Admin         | Create a city.                           |
| `GET`    | `api/address/cities/{ID}/` | int: id                     | Admin         | Get the county's information.            |
| `PUT`    | `api/address/cities/{ID}/` | int: id                     | Admin         | Update the city's information.           |
| `PATCH`  | `api/address/cities/{ID}/` | int: id                     | Admin         | Partially Update the city's information. |
| `DELETE` | `api/address/cities/{ID}/` | int: id                     | Admin         | Delete the city.                         |

### Address CRUD

| Method   | Path                          | Parameter | Authorization | Description                                 |
|----------|-------------------------------|-----------|---------------|---------------------------------------------|
| `GET`    | `api/address/addresses/`      | Parameter | All           | Get all addresses available.                |
| `POST`   | `api/address/addresses/`      | Parameter | Admin         | Create an address.                          |
| `PUT`    | `api/address/addresses/{ID}/` | Parameter | Admin         | Update the address's information.           |
| `PATCH`  | `api/address/addresses/{ID}/` | Parameter | Admin         | Partially Update the address's information. |
| `DELETE` | `api/address/addresses/{ID}/` | Parameter | Admin         | Delete the address.                         |




