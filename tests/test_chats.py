import pytest
from fastapi import status
from starlette.testclient import TestClient

def test_create_chat(client: TestClient):
    """Test chat creation"""
    response = client.post("/api/chats/", json={"title": "Test Chat"})
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == "Test Chat"
    assert "id" in data
    assert "created_at" in data
    assert isinstance(data["id"], int)

def test_create_message_in_chat(client: TestClient):
    """Test message creation"""
    chat_response = client.post("/api/chats/", json={"title": "Message Test"})
    chat_id = chat_response.json()["id"]
    
    message_data = {"text": "Hello, World!"}
    response = client.post(f"/api/chats/{chat_id}/messages/", json=message_data)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["text"] == "Hello, World!"
    assert data["chat_id"] == chat_id

def test_create_message_in_nonexistent_chat(client: TestClient):
    """Test: cannot create message in non-existent chat"""
    response = client.post("/api/chats/999/messages/", json={"text": "Test"})
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_get_chat_with_messages(client: TestClient):
    """Test getting chat with messages"""

    chat_response = client.post("/api/chats/", json={"title": "Get Test"})
    chat_id = chat_response.json()["id"]
    

    for i in range(5):
        client.post(f"/api/chats/{chat_id}/messages/", json={"text": f"Message {i}"})
    

    response = client.get(f"/api/chats/{chat_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == chat_id
    assert len(data["messages"]) == 5

    assert data["messages"][0]["text"] == "Message 4"

def test_get_chat_with_limit(client: TestClient):
    """Test message limit"""
    chat_response = client.post("/api/chats/", json={"title": "Limit Test"})
    chat_id = chat_response.json()["id"]
    

    for i in range(10):
        client.post(f"/api/chats/{chat_id}/messages/", json={"text": f"Msg {i}"})
    

    response = client.get(f"/api/chats/{chat_id}?limit=3")
    data = response.json()
    assert len(data["messages"]) == 3

def test_delete_chat(client: TestClient):
    """Test chat deletion"""

    chat_response = client.post("/api/chats/", json={"title": "Delete Test"})
    chat_id = chat_response.json()["id"]
    

    client.post(f"/api/chats/{chat_id}/messages/", json={"text": "Will be deleted"})
    

    response = client.delete(f"/api/chats/{chat_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    

    response = client.get(f"/api/chats/{chat_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_validation_title(client: TestClient):
    """Test chat title validation"""

    response = client.post("/api/chats/", json={"title": ""})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    

    long_title = "a" * 201
    response = client.post("/api/chats/", json={"title": long_title})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    

    response = client.post("/api/chats/", json={"title": "  Test  "})
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["title"] == "Test"

def test_validation_text(client: TestClient):
    """Test message text validation"""
    chat_response = client.post("/api/chats/", json={"title": "Validation Test"})
    chat_id = chat_response.json()["id"]
    

    response = client.post(f"/api/chats/{chat_id}/messages/", json={"text": ""})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    long_text = "a" * 5001
    response = client.post(f"/api/chats/{chat_id}/messages/", json={"text": long_text})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY