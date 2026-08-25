"""
SOS模块单元测试
"""
import pytest


class TestSOSAPI:
    """SOS API测试"""
    
    @pytest.fixture
    def profile_id(self, client):
        """创建测试档案"""
        response = client.post(
            "/api/profiles",
            json={
                "parent_name": "测试",
                "parent_phone": "13800138000",
                "child_name": "测试子",
                "child_phone": "13900139000",
            },
        )
        return response.json()["id"]
    
    def test_trigger_sos_success(self, client, profile_id):
        """测试触发SOS - 成功"""
        response = client.post(
            "/api/sos/trigger",
            json={
                "profile_id": profile_id,
                "location": "30.123456,104.654321",
                "timestamp": "2026-08-25T10:30:00Z",
            },
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["status"] in ["sent", "mock_sent"]
    
    def test_trigger_sos_invalid_profile(self, client):
        """测试触发SOS - 档案不存在"""
        response = client.post(
            "/api/sos/trigger",
            json={
                "profile_id": 99999,
                "location": "30.123456,104.654321",
                "timestamp": "2026-08-25T10:30:00Z",
            },
        )
        
        assert response.status_code == 404
    
    def test_list_sos_records(self, client, profile_id):
        """测试列出SOS记录"""
        # 触发多次SOS
        for i in range(3):
            client.post(
                "/api/sos/trigger",
                json={
                    "profile_id": profile_id,
                    "location": f"30.{i},104.{i}",
                    "timestamp": "2026-08-25T10:30:00Z",
                },
            )
        
        # 列出记录
        response = client.get(f"/api/profiles/{profile_id}/sos")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 3


class TestTaskAPI:
    """任务API测试"""
    
    @pytest.fixture
    def profile_id(self, client):
        response = client.post(
            "/api/profiles",
            json={
                "parent_name": "测试",
                "parent_phone": "13800138000",
                "child_name": "测试子",
                "child_phone": "13900139000",
            },
        )
        return response.json()["id"]
    
    def test_create_task(self, client, profile_id):
        """测试创建任务"""
        response = client.post(
            "/api/tasks",
            json={
                "profile_id": profile_id,
                "description": "一起拍张合照",
                "trip_id": None,
            },
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["description"] == "一起拍张合照"
    
    def test_complete_task(self, client, profile_id):
        """测试完成任务"""
        # 创建任务
        create_res = client.post(
            "/api/tasks",
            json={
                "profile_id": profile_id,
                "description": "测试任务",
            },
        )
        task_id = create_res.json()["id"]
        
        # 完成任务
        response = client.post(
            f"/api/tasks/{task_id}/complete",
            json={"completed_note": "已完成"},
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "completed"


class TestGuideAPI:
    """导游API测试"""
    
    def test_ask_guide(self, client):
        """测试问导游"""
        response = client.post(
            "/api/guide/ask",
            json={"question": "洪崖洞有什么历史？"},
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert len(data["answer"]) > 0


class TestCardAPI:
    """卡片API测试"""
    
    @pytest.fixture
    def trip_id(self, client):
        # 创建档案
        profile_res = client.post(
            "/api/profiles",
            json={
                "parent_name": "测试",
                "parent_phone": "13800138000",
                "child_name": "测试子",
                "child_phone": "13900139000",
            },
        )
        profile_id = profile_res.json()["id"]
        
        # 创建行程
        from datetime import date
        trip_res = client.post(
            "/api/trips",
            json={
                "profile_id": profile_id,
                "destination": "测试地点",
                "travel_date": str(date.today()),
            },
        )
        return trip_res.json()["id"]
    
    def test_generate_card(self, client, trip_id):
        """测试生成卡片"""
        response = client.post(
            "/api/cards/generate",
            json={
                "trip_id": trip_id,
                "title": "美好回忆",
                "content": "难忘的旅程",
            },
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["title"] == "美好回忆"
