"""
Card 模块测试 - Service 层单元测试
"""
from app.modules.card.service.CardService import CardService
from app.modules.task.service.TaskService import TaskService
from app.modules.trip.service.TripService import TripService
from datetime import date, timedelta


class TestCardService:
    """Card Service 单元测试"""
    
    def test_generate_card_with_completed_tasks(self, db_session):
        """测试有已完成任务时生成卡片"""
        travel_date = date.today() + timedelta(days=7)
        trip = TripService.create_trip(db_session, 1, "重庆", travel_date)
        task = TaskService.create_task(db_session, 1, trip.id, "拍照", "描述")
        
        TaskService.complete_task_by_user(db_session, task.id, "完成")
        TaskService.complete_task_by_elder(db_session, task.id, "很好")
        
        card = CardService.generate_card(
            db_session,
            trip_id=trip.id,
            title="重庆之旅",
            image_url="https://example.com/image.jpg",
            trip_entity=trip
        )
        
        assert card is not None
        assert "拍照" in card.summary
    
    def test_generate_card_no_completed_tasks(self, db_session):
        """测试无已完成任务时生成卡片（测试 else 分支）"""
        travel_date = date.today() + timedelta(days=7)
        trip = TripService.create_trip(db_session, 1, "重庆", travel_date)
        
        card = CardService.generate_card(
            db_session,
            trip_id=trip.id,
            title="重庆之旅",
            image_url="https://example.com/image.jpg",
            trip_entity=trip
        )
        
        assert card is not None
        assert "none yet" in card.summary or "暂无" in card.summary
    
    def test_list_cards_by_elder(self, db_session):
        """测试按老人查询卡片"""
        travel_date = date.today() + timedelta(days=7)
        trip1 = TripService.create_trip(db_session, 1, "重庆", travel_date)
        trip2 = TripService.create_trip(db_session, 2, "北京", travel_date)
        
        CardService.generate_card(db_session, trip1.id, "卡片1", "url1", trip1)
        CardService.generate_card(db_session, trip1.id, "卡片2", "url2", trip1)
        CardService.generate_card(db_session, trip2.id, "卡片3", "url3", trip2)
        
        cards = CardService.list_cards_by_trip(db_session, trip_id=trip1.id)
        
        assert len(cards) == 2
    
    def test_get_card_by_id_exists(self, db_session):
        """测试查询存在的卡片"""
        travel_date = date.today() + timedelta(days=7)
        trip = TripService.create_trip(db_session, 1, "重庆", travel_date)
        card = CardService.generate_card(db_session, trip.id, "测试", "url", trip)
        
        found = CardService.get_card_by_id(db_session, card.id)
        
        assert found is not None
        assert found.id == card.id
    
    def test_get_card_by_id_not_exists(self, db_session):
        """测试查询不存在的卡片"""
        found = CardService.get_card_by_id(db_session, 999999)
        
        assert found is None
    
    def test_list_cards_empty(self, db_session):
        """测试查询空卡片列表"""
        cards = CardService.list_cards_by_trip(db_session, trip_id=999)
        
        assert cards == []
