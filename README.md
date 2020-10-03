# Messaging system

## Deployment to Heroku

Address [Messaging system](https://polar-brushlands-03833.herokuapp.com/)

### Requirements

- I chose to us **gunicorn** with heroku
- runtime.txt: Specify python version
- Procfile: Call command to up a server
- requirements.txt: Show which app to install
  - Heroku don't support poetry. Run this command to export it

    ```sh
    poetry export --without-hashes -f requirements.txt > requirements.txt
    ```

- `heroku config:set KEY=VALUE` or add in project folder on heroku
  - Set all environments variables

### GIT

- Git log as a _graph_: `$ git log --all --decorate --oneline --graph`

## DB

### Users

|id  |fullname |email |password |
|----|---------|------|---------|
|int |str      |str   |bcrypt   |

### Mapper

|m_id   |r_id   |
|-------|-------|
|int(fk)|int(fk)|

### Messsages

|id |subject|body   |created_at|is_read|owner |
|---|-------|-------|----------|-------|------|
|int|varchar|text   |date      |bool   |int   |

## API

- Login
  - [x] POST /auth/login JSON{email, password}
  - [x] GET /api/messages Headers{Authoriazation: Bearer {token}}

**NOTE**: to test logged in users use email: janedoe@test.com or johndoe@test.com, password: password.\
Postman: Call first /auth/login route it will save token and then call /api/messages route.

- Send a new message
  - [x] POST /api/messages JSON{sender, recipient, subject, body}
- Show messages for a specific user
  - [x] GET /api/messages?user\_id=\<id>
  - [x] GET /api/users/<user\_id>/messages
- Show unread messages for a specific user
  - [x] GET /api/messages?user\_id=\<id>&unread=1
  - [x] GET /api/users/<user\_id>/messages?unread=1
- Read a message
  - [x] GET /api/messages/<m\_id>
  - [x] GET /api/users/<user\_id>/messages/1
- Delete a message
  - [x] DELETE /api/messages/<m\_id>

**NOTE**: All messages are returned by recipient not by owner if recipient provided or user_id.
