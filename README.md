# Messaging system

## DB

### Users
|id  |name |
|----|-----|
|int |str  |

### Mapper
|m_id   |s_id   |r_id   |
|-------|-------|-------|
|int(fk)|int(fk)|int(fk)|

### Messsages
|id |subject|body   |created_at|is_read|
|---|-------|-------|----------|-------|
|int|varchar|text   |date      |bool   |

## API
- Send a new message
  - POST /messages JSON{sender, recepient, subject, body}
- Show messages for a specific user
  - GET /messages?user\_id=<id>
  - GET /users/<user\_id>/messages
- Show unread messages for a specific user
  - GET /messages?user\_id=<id>&unread=1
  - GET /users/<user\_id>/messages?unread=1
- Read a message
  - GET /messages/<m\_id>
- Delete a message
  - DELETE /messages/<m\_id>

**Note**: As possible side effect when searching for messages of an user I can also return all messages
