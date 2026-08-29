"""
Auth 模块测试 - API 集成测试
"""


class TestAuthUserAPI:
    """用户认证 API 集成测试"""
    
    def test_register_user_api(self, client):
        """测试用户注册 API"""
        response = client.post("/api/auth/user/register", json={
            "nickname": "TestUser",
            "phone": "13800138000",
            "password": "Test1234!@#"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "user_id" in data
    
    def test_login_user_api(self, client, create_test_user):
        """测试用户登录 API"""
        response = client.post("/api/auth/user/login", json={
            "phone": "13800138000",
            "password": "Test1234!@#"
        })
        
        assert response.status_code == 200
        assert "access_token" in response.json()
    
    def test_get_user_info(self, client, create_test_user):
        """测试获取用户信息"""
        response = client.get(
            "/api/auth/user/me",
            headers=create_test_user["headers"]
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["phone"] == "13800138000"


class TestAuthElderAPI:
    """老人认证 API 集成测试"""
    
    def test_register_elder_api(self, client):
        """测试老人注册 API"""
        response = client.post("/api/auth/elder/register", json={
            "name": "TestElder",
            "phone": "13900139000",
            "password": "Elder1234!@#",
            "health_info": '{}',
            "interests": "culture"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
    
    def test_login_elder_api(self, client, create_test_elder):
        """测试老人登录 API"""
        response = client.post("/api/auth/elder/login", json={
            "phone": "13900139000",
            "password": "Elder1234!@#"
        })
        
        assert response.status_code == 200
        assert "access_token" in response.json()
    
    def test_get_elder_info_with_qr(self, client, create_test_elder):
        """测试获取老人信息（含二维码）"""
        response = client.get(
            "/api/auth/elder/me",
            headers=create_test_elder["headers"]
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "qr_code_svg" in data
        assert "<?xml" in data["qr_code_svg"] or "<svg" in data["qr_code_svg"]
