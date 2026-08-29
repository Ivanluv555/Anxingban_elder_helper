"""
Profile 模块测试 - Service 层单元测试
"""
from app.modules.profile.service.ProfileService import ProfileService


class TestProfileService:
    """Profile Service 单元测试"""
    
    def test_create_profile(self, db_session):
        """测试创建档案"""
        profile = ProfileService.create_profile(db_session, elder_id=1, user_id=1)
        
        assert profile is not None
        assert profile.elder_id == 1
        assert profile.user_id == 1
    
    def test_list_profiles_by_user(self, db_session):
        """测试按用户查询档案"""
        ProfileService.create_profile(db_session, elder_id=1, user_id=1)
        ProfileService.create_profile(db_session, elder_id=2, user_id=1)
        ProfileService.create_profile(db_session, elder_id=3, user_id=2)
        
        profiles = ProfileService.list_profiles(db_session, user_id=1, limit=10)
        
        assert len(profiles) == 2
        assert all(p.user_id == 1 for p in profiles)
    
    def test_get_profile_by_id_exists(self, db_session):
        """测试查询存在的档案"""
        profile = ProfileService.create_profile(db_session, elder_id=1, user_id=1)
        
        found = ProfileService.get_profile_by_id(db_session, profile.id)
        
        assert found is not None
        assert found.id == profile.id
    
    def test_get_profile_by_id_not_exists(self, db_session):
        """测试查询不存在的档案"""
        found = ProfileService.get_profile_by_id(db_session, 999999)
        
        assert found is None
    
    def test_delete_profile_exists(self, db_session):
        """测试删除存在的档案"""
        profile = ProfileService.create_profile(db_session, elder_id=1, user_id=1)
        profile_id = profile.id
        
        ProfileService.delete_profile(db_session, profile_id)
        
        deleted_profile = ProfileService.get_profile_by_id(db_session, profile_id)
        assert deleted_profile is None
    
    def test_delete_profile_not_exists(self, db_session):
        """测试删除不存在的档案（不应抛出异常）"""
        ProfileService.delete_profile(db_session, 999999)
    
    def test_list_profiles_empty(self, db_session):
        """测试查询空列表"""
        profiles = ProfileService.list_profiles(db_session, user_id=999, limit=10)
        
        assert profiles == []
