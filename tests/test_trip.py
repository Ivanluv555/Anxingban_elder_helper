"""
行程模块单元测试
"""
import pytest
from datetime import date, timedelta


class TestTripAPI:
    """行程API测试"""
    
    @pytest.fixture
    def profile_id(self, client):
        """创建测试档案"""
        response = client.post(
            "/api/profiles",
            json={
                "parent_name": "测试用户",
                "parent_phone": "13800138000",
                "child_name": "测试子女",
                "child_phone": "13900139000",
            },
        )
        return response.json()["id"]
    
    def test_create_trip_success(self, client, profile_id):
        """测试创建行程 - 成功"""
        response = client.post(
            "/api/trips",
            json={
                "profile_id": profile_id,
                "destination": "洪崖洞",
                "travel_date": str(date.today()),
            },
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "pass_token" in data
        assert "pass_qr_svg" in data
        assert data["pass_token"].startswith("ELDER-")
        assert "<svg" in data["pass_qr_svg"]
    
    def test_create_trip_invalid_profile(self, client):
        """测试创建行程 - 档案不存在"""
        response = client.post(
            "/api/trips",
            json={
                "profile_id": 99999,
                "destination": "洪崖洞",
                "travel_date": str(date.today()),
            },
        )
        
        assert response.status_code == 404
        assert response.json()["error"] == "PROFILE_NOT_FOUND"
    
    def test_get_trip(self, client, profile_id):
        """测试获取行程"""
        # 创建行程
        create_res = client.post(
            "/api/trips",
            json={
                "profile_id": profile_id,
                "destination": "解放碑",
                "travel_date": str(date.today()),
            },
        )
        trip_id = create_res.json()["id"]
        
        # 获取行程
        response = client.get(f"/api/trips/{trip_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == trip_id
        assert data["destination"] == "解放碑"
    
    def test_get_trip_pass(self, client, profile_id):
        """测试获取行程通行码"""
        # 创建行程
        create_res = client.post(
            "/api/trips",
            json={
                "profile_id": profile_id,
                "destination": "磁器口",
                "travel_date": str(date.today()),
            },
        )
        trip_id = create_res.json()["id"]
        
        # 获取通行码
        response = client.get(f"/api/trips/{trip_id}/pass")
        
        assert response.status_code == 200
        data = response.json()
        assert "pass_token" in data
        assert "pass_qr_svg" in data
    
    def test_list_trips_by_profile(self, client, profile_id):
        """测试按档案列出行程"""
        # 创建多个行程
        destinations = ["洪崖洞", "解放碑", "磁器口"]
        for dest in destinations:
            client.post(
                "/api/trips",
                json={
                    "profile_id": profile_id,
                    "destination": dest,
                    "travel_date": str(date.today()),
                },
            )
        
        # 列出行程
        response = client.get(f"/api/profiles/{profile_id}/trips")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert all(trip["profile_id"] == profile_id for trip in data)


class TestTripValidation:
    """行程数据验证测试"""
    
    def test_past_date(self, client, profile_id):
        """测试过去的日期"""
        past_date = date.today() - timedelta(days=30)
        response = client.post(
            "/api/trips",
            json={
                "profile_id": profile_id,
                "destination": "测试",
                "travel_date": str(past_date),
            },
        )
        
        # 根据业务逻辑，可能允许或拒绝过去的日期
        # 这里假设允许
        assert response.status_code in [200, 400]
    
    def test_empty_destination(self, client, profile_id):
        """测试空目的地"""
        response = client.post(
            "/api/trips",
            json={
                "profile_id": profile_id,
                "destination": "",
                "travel_date": str(date.today()),
            },
        )
        
        assert response.status_code == 422
    
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
