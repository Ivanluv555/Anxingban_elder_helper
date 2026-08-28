"""
Profile 模块测试
"""
import pytest
from app.modules.profile.service.ProfileService import ProfileService
from app.utils.error_codes import BusinessException


class TestProfileAPI:
    """Profile API 集成测试"""
    
    def test_create_profile_success(self, client, create_test_user, create_test_elder):
        """测试创建档案成功"""
        response = client.post(
            "/api/user/profiles",
            json={"elder_id": create_test_elder["elder_id"]},
            headers=create_test_user["headers"]
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["elder_id"] == create_test_elder["elder_id"]
        assert data["user_id"] == create_test_user["user_id"]
        assert "created_at" in data
    
    def test_create_profile_unauthorized(self, client, create_test_elder):
        """测试未授权创建档案"""
        response = client.post(
            "/api/user/profiles",
            json={"elder_id": create_test_elder["elder_id"]}
        )
        assert response.status_code == 403
    
    def test_list_profiles(self, client, create_test_user, create_test_profile):
        """测试获取档案列表"""
        response = client.get(
            "/api/user/profiles",
            headers=create_test_user["headers"]
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["id"] == create_test_profile["id"]
    
    def test_delete_profile(self, client, create_test_user, create_test_profile):
        """测试删除档案"""
        profile_id = create_test_profile["id"]
        
        response = client.delete(
            f"/api/user/profiles/{profile_id}",
            headers=create_test_user["headers"]
        )
        
        assert response.status_code == 200
        assert "成功" in response.json()["message"]
        
        # 验证已删除
        response = client.get(
            "/api/user/profiles",
            headers=create_test_user["headers"]
        )
        data = response.json()
        assert len(data) == 0


class TestProfileService:
    """Profile Service 单元测试"""
    
    def test_create_profile(self, db_session):
        """测试创建档案"""
        profile = ProfileService.create_profile(db_session, elder_id=1, user_id=1)
        
        assert profile is not None
        assert profile.elder_id == 1
        assert profile.user_id == 1
        assert profile.created_at is not None
    
    def test_list_profiles_by_user(self, db_session):
        """测试按用户查询档案"""
        ProfileService.create_profile(db_session, elder_id=1, user_id=1)
        ProfileService.create_profile(db_session, elder_id=2, user_id=1)
        ProfileService.create_profile(db_session, elder_id=3, user_id=2)
        
        profiles = ProfileService.list_profiles(db_session, user_id=1, limit=10)
        
        assert len(profiles) == 2
        assert all(p.user_id == 1 for p in profiles)
    
    def test_delete_profile(self, db_session):
        """测试删除档案"""
        profile = ProfileService.create_profile(db_session, elder_id=1, user_id=1)
        profile_id = profile.id
        
        ProfileService.delete_profile(db_session, profile_id)
        
        deleted_profile = ProfileService.get_profile_by_id(db_session, profile_id)
        assert deleted_profile is None
