from __future__ import annotations


def create_post(client, title="대학로 공연 후 코스", category="공연 후 코스"):
    response = client.post(
        "/api/posts",
        json={
            "title": title,
            "content": "공연 후 산책하기 좋았습니다.",
            "category": category,
            "password": "1234",
            "performance_name": "테스트 공연",
            "available_minutes": 90,
        },
    )
    assert response.status_code == 201
    return response.json()


def test_post_crud_rejects_wrong_password(client):
    post = create_post(client)
    response = client.put(
        f"/api/posts/{post['id']}",
        json={
            "title": "변경 제목",
            "content": "변경 내용",
            "category": "공연 후 코스",
            "password": "wrong",
            "performance_name": "테스트 공연",
            "available_minutes": 90,
        },
    )
    assert response.status_code == 403


def test_detail_increments_view_count(client):
    post = create_post(client)
    first = client.get(f"/api/posts/{post['id']}").json()
    second = client.get(f"/api/posts/{post['id']}").json()
    assert second["view_count"] == first["view_count"] + 1


def test_search_and_category_filter(client):
    create_post(client, "대학로 산책", "공연 후 코스")
    create_post(client, "예술의전당 준비", "공연 전 코스")

    response = client.get("/api/posts", params={"q": "대학로", "category": "공연 후 코스"})

    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["items"][0]["title"] == "대학로 산책"


def test_like_toggle_does_not_duplicate(client):
    post = create_post(client)
    headers = {"X-Client-ID": "browser-a"}

    first = client.post(f"/api/posts/{post['id']}/likes/toggle", headers=headers).json()
    second = client.post(f"/api/posts/{post['id']}/likes/toggle", headers=headers).json()

    assert first == {"liked": True, "like_count": 1}
    assert second == {"liked": False, "like_count": 0}


def test_posts_can_be_queried_by_bookmark_ids(client):
    first = create_post(client, "첫 글")
    second = create_post(client, "두 번째 글")

    response = client.get("/api/posts", params={"ids": f"{second['id']}"})

    assert response.status_code == 200
    assert [item["id"] for item in response.json()["items"]] == [second["id"]]
