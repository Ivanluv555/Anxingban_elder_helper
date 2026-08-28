"""
Trip 模块测试
"""
import pytest
from datetime import date, timedelta
from app.modules.trip.service.TripService import TripService


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
        # 列表不应该包含二维码
        assert "pass_token" not in data[0]
        assert "pass_qr_svg" not in data[0]
    
    def test_get_trip_detail_with_qr(self, client, create_test_user, create_test_trip):
        """测试获取行程详情（含二维码）"""
        trip_id = create_test_trip["id"]
        
        response = client.get(
            f"/api/user/trips/{trip_id}",
            headers=create_test_user["headers"]
        )
        
        assert response.status_code == 200
        data = response.json()
        # 详情应该包含二维码
        assert "pass_token" in data
        assert "pass_qr_svg" in data
        assert "<?xml" in data["pass_qr_svg"] or data["pass_qr_svg"].startswith("<svg")
    
    def test_delete_trip(self, client, create_test_user, create_test_trip):
        """测试删除行程"""
        trip_id = create_test_trip["id"]
        
        response = client.delete(
            f"/api/user/trips/{trip_id}",
            headers=create_test_user["headers"]
        )
        
        assert response.status_code == 200
        assert "成功" in response.json()["message"]


class TestTripService:
    """Trip Service 单元测试"""
    
    def test_create_trip(self, db_session):
        """测试创建行程"""
        travel_date = date.today() + timedelta(days=7)
        
        trip = TripService.create_trip(
            db_session,
            profile_id=1,
            destination="北京",
            travel_date=travel_date
        )
        
        assert trip is not None
        assert trip.destination == "北京"
        assert trip.pass_token is not None
        assert trip.pass_qr_svg is not None
        assert len(trip.pass_token) > 20
    
    def test_list_trips_by_profile(self, db_session):
        """测试按档案查询行程"""
        travel_date = date.today() + timedelta(days=7)
        
        TripService.create_trip(db_session, 1, "北京", travel_date)
        TripService.create_trip(db_session, 1, "上海", travel_date)
        TripService.create_trip(db_session, 2, "广州", travel_date)
        
        trips = TripService.list_trips_by_profile(db_session, profile_id=1)
        
        assert len(trips) == 2
        assert all(t.profile_id == 1 for t in trips)
