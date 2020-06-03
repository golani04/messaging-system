def test_messages_post(app):
    response = app.post(
        "/api/messages",
        json={"body": "Lorem ipsum test!!", "subject": "Test Post URL", "owner": 3, "recipient": 1},
    )

    assert response.status_code == 200
    res = response.get_json()
    assert res["id"] > 0
    # TODO: use freezegun to check created_at
    assert res["created_at"] is not None
