def test_health(client):
    assert client.get("/health").get_json() == {"status": "ok"}


def test_register_login_flow(client):
    r = client.post("/register", json={"username": "ani", "password": "pass12345"})
    assert r.status_code == 201
    assert client.post(
        "/register", json={"username": "ani", "password": "pass12345"}
    ).status_code == 409
    assert client.post("/register", json={"username": "x", "password": "p"}).status_code == 400
    assert client.post(
        "/login", json={"username": "ani", "password": "salah"}
    ).status_code == 401
    ok = client.post("/login", json={"username": "ani", "password": "pass12345"})
    assert "token" in ok.get_json()


def test_notes_require_auth(client):
    assert client.get("/notes").status_code == 401
    assert client.get("/notes", headers={"Authorization": "Bearer x.y"}).status_code == 401


def test_note_crud_and_search(client, auth_headers):
    created = client.post(
        "/notes", json={"title": "Belanja", "content": "susu"}, headers=auth_headers
    )
    assert created.status_code == 201
    note_id = created.get_json()["id"]
    client.post("/notes", json={"title": "Rapat", "content": "jam 9"}, headers=auth_headers)

    assert len(client.get("/notes", headers=auth_headers).get_json()) == 2
    found = client.get("/notes?q=Bel", headers=auth_headers).get_json()
    assert len(found) == 1 and found[0]["title"] == "Belanja"
    assert client.get(f"/notes/{note_id}", headers=auth_headers).status_code == 200
    assert client.delete(f"/notes/{note_id}", headers=auth_headers).status_code == 204
    assert client.get(f"/notes/{note_id}", headers=auth_headers).status_code == 404
    assert client.delete(f"/notes/{note_id}", headers=auth_headers).status_code == 404


def test_note_validation_error(client, auth_headers):
    r = client.post("/notes", json={"title": "", "content": "x"}, headers=auth_headers)
    assert r.status_code == 400


def test_user_cannot_read_other_users_note(client, auth_headers):
    nid = client.post(
        "/notes", json={"title": "Rahasia", "content": "x"}, headers=auth_headers
    ).get_json()["id"]
    client.post("/register", json={"username": "citra", "password": "pass12345"})
    tok = client.post(
        "/login", json={"username": "citra", "password": "pass12345"}
    ).get_json()["token"]
    other = {"Authorization": f"Bearer {tok}"}
    assert client.get(f"/notes/{nid}", headers=other).status_code == 404


def test_unknown_endpoint(client):
    assert client.get("/tidak-ada").status_code == 404
