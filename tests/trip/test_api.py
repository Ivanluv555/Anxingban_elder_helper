"""
Trip 模块测试 - API 集成测试
"""
from datetime import date, timedelta


class TestTripAPI:
    """Trip API 集成测试"""
    
    def test_create_trip_success(self, client, create_test_user, create_test_profile):
        """测试创建行程成功"""
        travel_date = str(date.today() + timedelta(days=7))
        
        response = client.post(
            "/api/user/trips",
            json={
                "profile_id": create_test_profile["id"],
                "destination": "成都",
                "travel_date": travel_date
            },
            headers=create_test_user["headers"]
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["destination"] == "成都"
        assert data["travel_date"] == travel_date
        assert "pass_token" in data
        assert "pass_qr_svg" in data
    
    def test_create_trip_profile_not_found(self, client, create_test_user):
        """测试创建行程时档案不存在"""
        travel_date = str(date.today() + timedelta(days=7))
        
        response = client.post(
            "/api/user/trips",
            json={
                "profile_id": 999999,
                "destination": "成都",
                "travel_date": travel_date
            },
            headers=create_test_user["headers"]
        )
        
        assert response.status_code == 404
        assert "不存在" in response.json()["detail"]
    
    def test_list_trips_no_qr(self, client, create_test_user, create_test_trip):
        """测试获取行程列表（不含二维码）"""
        response = client.get(
            "/api/user/trips",
            headers=create_test_user["headers"]
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert "pass_token" not in data[0]
        assert "pass_qr_svg" not in data[0]
    
    def test_list_trips_empty(self, client, create_test_user):
        """测试获取空行程列表"""
        response = client.get(
            "/api/user/trips",
            headers=create_test_user["headers"]
        )
        
        assert response.status_code == 200
        assert response.json() == []
    
    def test_get_trip_detail_with_qr(self, client, create_test_user, create_test_trip):
        """测试获取行程详情（含二维码）"""
        trip_id = create_test_trip["id"]
        
        response = client.get(
            f"/api/user/trips/{trip_id}",
            headers=create_test_user["headers"]
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "pass_token" in data
        assert "pass_qr_svg" in data
        assert "<?xml" in data["pass_qr_svg"] or data["pass_qr_svg"].startswith("<svg")
    
    def test_get_trip_not_found(self, client, create_test_user):
        """测试获取不存在的行程"""
        response = client.get(
            "/api/user/trips/999999",
            headers=create_test_user["headers"]
        )
        
        assert response.status_code == 404
        assert "不存在" in response.json()["detail"]
    
    def test_delete_trip(self, client, create_test_user, create_test_trip):
        """测试删除行程"""
        trip_id = create_test_trip["id"]
        
        response = client.delete(
            f"/api/user/trips/{trip_id}",
            headers=create_test_user["headers"]
        )
        
        assert response.status_code == 200
        assert "成功" in response.json()["message"]
    
    def test_delete_trip_not_found(self, client, create_test_user):
        """测试删除不存在的行程"""
        response = client.delete(
            "/api/user/trips/999999",
            headers=create_test_user["headers"]
        )
        
        assert response.status_code == 404
        assert "不存在" in response.json()["detail"]


class TestTripElderAPI:
    """老人端行程 API 测试"""
    
    def test_elder_get_trip_detail(self, client, create_test_elder, create_test_trip):
        """测试老人获取行程详情"""
        trip_id = create_test_trip["id"]
        
        response = client.get(
            f"/api/elder/trips/{trip_id}",
            headers=create_test_elder["headers"]
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "pass_token" in data
    
    def test_elder_get_trip_not_found(self, client, create_test_elder):
        """测试老人获取不存在的行程"""
        response = client.get(
            "/api/elder/trips/999999",
            headers=create_test_elder["headers"]
        )
        
        assert response.status_code == 404
        assert "不存在" in response.json()["detail"]
    
    def test_elder_list_trips(self, client, create_test_elder):
        """测试老人获取行程列表"""
        response = client.get(
            "/api/elder/trips",
            headers=create_test_elder["headers"]
        )
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
