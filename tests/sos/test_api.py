"""
SOS 模块测试 - API 集成测试
"""


class TestSosAPI:
    """SOS API 测试"""
    
    def test_trigger_sos_success(self, client, create_test_elder, create_test_profile):
        """测试触发 SOS 成功"""
        response = client.post(
            "/api/elder/sos/trigger",
            json={
                "profile_id": create_test_profile["id"],
                "trip_id": 1,
                "latitude": 29.5647,
                "longitude": 106.5507,
                "network_status": "online"
            },
            headers=create_test_elder["headers"]
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["profile_id"] == create_test_profile["id"]
        assert data["latitude"] == 29.5647
    
    def test_trigger_sos_profile_not_found(self, client, create_test_elder):
        """测试触发 SOS 时档案不存在"""
        response = client.post(
            "/api/elder/sos/trigger",
            json={
                "profile_id": 999999,
                "trip_id": 1,
                "latitude": 29.5647,
                "longitude": 106.5507,
                "network_status": "online"
            },
            headers=create_test_elder["headers"]
        )
        
        assert response.status_code in [400, 404, 500]
        response_data = response.json()
        if "detail" in response_data and response_data["detail"]:
            assert "档案" in response_data["detail"] or "PROFILE" in str(response_data)
    
    def test_list_sos_records(self, client, create_test_user):
        """测试获取 SOS 记录列表"""
        response = client.get(
            "/api/user/sos",
            headers=create_test_user["headers"]
        )
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_list_sos_by_profile(self, client, create_test_user, create_test_profile):
        """测试按档案获取 SOS 记录"""
        profile_id = create_test_profile["id"]
        
        response = client.get(
            f"/api/user/sos/profile/{profile_id}",
            headers=create_test_user["headers"]
        )
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_elder_list_sos(self, client, create_test_elder):
        """测试老人获取 SOS 记录列表"""
        response = client.get(
            "/api/elder/sos",
            headers=create_test_elder["headers"]
        )
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
