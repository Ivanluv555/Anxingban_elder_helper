"""
档案模块单元测试
"""
import pytest


class TestProfileAPI:
    """档案API测试"""
    
    def test_create_profile_success(self, client):
        """测试创建档案 - 成功"""
        response = client.post(
            "/api/profiles",
            json={
                "parent_name": "张三",
                "parent_phone": "13800138000",
                "child_name": "张小明",
                "child_phone": "13900139000",
            },
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["parent_name"] == "张三"
        assert data["parent_phone"] == "13800138000"
    
    def test_create_profile_invalid_phone(self, client):
        """测试创建档案 - 手机号格式错误"""
        response = client.post(
            "/api/profiles",
            json={
                "parent_name": "张三",
                "parent_phone": "invalid_phone",
                "child_name": "张小明",
                "child_phone": "13900139000",
            },
        )
        
        assert response.status_code == 422  # 验证失败
    
    def test_get_profile_success(self, client):
        """测试获取档案 - 成功"""
        # 先创建
        create_res = client.post(
            "/api/profiles",
            json={
                "parent_name": "李四",
                "parent_phone": "13800138001",
                "child_name": "李小红",
                "child_phone": "13900139001",
            },
        )
        profile_id = create_res.json()["id"]
        
        # 再获取
        response = client.get(f"/api/profiles/{profile_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == profile_id
        assert data["parent_name"] == "李四"
    
    def test_get_profile_not_found(self, client):
        """测试获取档案 - 不存在"""
        response = client.get("/api/profiles/99999")
        
        assert response.status_code == 404
        data = response.json()
        assert data["error"] == "PROFILE_NOT_FOUND"
    
    def test_list_profiles(self, client):
        """测试列出档案"""
        # 创建多个档案
        for i in range(3):
            client.post(
                "/api/profiles",
                json={
                    "parent_name": f"测试{i}",
                    "parent_phone": f"1380013800{i}",
                    "child_name": f"子女{i}",
                    "child_phone": f"1390013900{i}",
                },
            )
        
        # 列出档案
        response = client.get("/api/profiles")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 3
    
    def test_update_profile(self, client):
        """测试更新档案"""
        # 创建档案
        create_res = client.post(
            "/api/profiles",
            json={
                "parent_name": "王五",
                "parent_phone": "13800138002",
                "child_name": "王小六",
                "child_phone": "13900139002",
            },
        )
        profile_id = create_res.json()["id"]
        
        # 更新档案
        response = client.put(
            f"/api/profiles/{profile_id}",
            json={
                "parent_name": "王五更新",
                "parent_phone": "13800138002",
                "child_name": "王小六",
                "child_phone": "13900139002",
            },
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["parent_name"] == "王五更新"


class TestProfileValidation:
    """档案数据验证测试"""
    
    def test_missing_required_fields(self, client):
        """测试缺少必填字段"""
        response = client.post(
            "/api/profiles",
            json={
                "parent_name": "测试",
                # 缺少其他字段
            },
        )
        
        assert response.status_code == 422
    
    def test_empty_strings(self, client):
        """测试空字符串"""
        response = client.post(
            "/api/profiles",
            json={
                "parent_name": "",
                "parent_phone": "13800138000",
                "child_name": "",
                "child_phone": "13900139000",
            },
        )
        
        assert response.status_code == 422
