# Messaging system

## Deployment to Heroku

Address [Messaging system](https://polar-brushlands-03833.herokuapp.com/)

For this I choose to use gunicorn to serve my app.

- Install **gunicorn**: `poetry add gunicorn`

### Requirements

- runtime.txt: Specify python version
- Procfile: Call command to up a server
- requirements.txt: Show which app to install
  - Heroku don't support poetry. Run this command to export it

    ```sh
    poetry export -f requirements.txt > requirements.txt
    ```

- `heroku config:set KEY=VALUE` or add in project folder on heroku
  - Set all environments variables

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

- Send a new message
  - [x] POST /messages JSON{sender, recipient, subject, body}
- Show messages for a specific user
  - [x] GET /messages?user\_id=\<id>
  - [x] GET /users/<user\_id>/messages
- Show unread messages for a specific user
  - [x] GET /messages?user\_id=\<id>&unread=1
  - [x] GET /users/<user\_id>/messages?unread=1
- Read a message
  - [x] GET /messages/<m\_id>
- Delete a message
  - [x] DELETE /messages/<m\_id>
