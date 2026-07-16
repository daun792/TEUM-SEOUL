
def create_post(client, title="여름 축제 후기", password="1234"):
    return client.post(
        "/api/posts",
        json={
            "title": title,
            "content": "사람이 많았지만 공연이 좋았습니다.",
            "author": "익명",
            "password": password,
        },
    )


def test_post_crud_requires_matching_password(client):
    created = create_post(client)
    assert created.status_code == 201
    post_id = created.json()["id"]
    assert "password" not in created.json()

    wrong_update = client.put(
        f"/api/posts/{post_id}",
        json={"title": "수정 제목", "content": "수정 내용", "password": "wrong"},
    )
    assert wrong_update.status_code == 403

    updated = client.put(
        f"/api/posts/{post_id}",
        json={"title": "수정 제목", "content": "수정 내용", "password": "1234"},
    )
    assert updated.status_code == 200
    assert updated.json()["title"] == "수정 제목"

    wrong_delete = client.request(
        "DELETE", f"/api/posts/{post_id}", json={"password": "wrong"}
    )
    assert wrong_delete.status_code == 403

    deleted = client.request(
        "DELETE", f"/api/posts/{post_id}", json={"password": "1234"}
    )
    assert deleted.status_code == 204
    assert client.get(f"/api/posts/{post_id}").status_code == 404


def test_post_list_supports_search_and_pagination(client):
    create_post(client, title="한강 축제 후기")
    create_post(client, title="인사동 산책")
    create_post(client, title="서울숲 축제 후기")

    response = client.get("/api/posts", params={"q": "축제", "page": 1, "size": 1})

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 2
    assert body["page"] == 1
    assert body["size"] == 1
    assert body["pages"] == 2
    assert len(body["items"]) == 1
