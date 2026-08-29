"""
Trip 模块测试 - Service 层单元测试
"""
from datetime import date, timedelta
from app.modules.trip.service.TripService import TripService


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
    
    def test_get_trip_by_id_exists(self, db_session):
        """测试查询存在的行程"""
        travel_date = date.today() + timedelta(days=7)
        trip = TripService.create_trip(db_session, 1, "北京", travel_date)
        
        found = TripService.get_trip_by_id(db_session, trip.id)
        
        assert found is not None
        assert found.id == trip.id
    
    def test_get_trip_by_id_not_exists(self, db_session):
        """测试查询不存在的行程"""
        found = TripService.get_trip_by_id(db_session, 999999)
        
        assert found is None
    
    def test_delete_trip_exists(self, db_session):
        """测试删除存在的行程"""
        travel_date = date.today() + timedelta(days=7)
        trip = TripService.create_trip(db_session, 1, "北京", travel_date)
        trip_id = trip.id
        
        TripService.delete_trip(db_session, trip_id)
        
        deleted_trip = TripService.get_trip_by_id(db_session, trip_id)
        assert deleted_trip is None
    
    def test_delete_trip_not_exists(self, db_session):
        """测试删除不存在的行程"""
        TripService.delete_trip(db_session, 999999)
    
    def test_list_trips_empty(self, db_session):
        """测试查询空行程列表"""
        trips = TripService.list_trips_by_profile(db_session, profile_id=999)
        
        assert trips == []
