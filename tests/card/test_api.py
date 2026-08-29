"""
Card 模块测试 - API 集成测试
"""


class TestCardAPI:
    """Card API 集成测试"""
    
    def test_generate_card_success(self, client, create_test_elder, create_test_trip):
        """测试生成回忆卡片成功"""
        response = client.post(
            "/api/elder/cards/generate",
            json={
                "trip_id": create_test_trip["id"],
                "title": "重庆之旅",
                "image_url": "https://example.com/image.jpg"
            },
            headers=create_test_elder["headers"]
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "重庆之旅"
        assert "summary" in data
    
    def test_list_cards(self, client, create_test_elder):
        """测试获取卡片列表"""
        response = client.get(
            "/api/elder/cards",
            headers=create_test_elder["headers"]
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_card_detail(self, client, create_test_elder, create_test_trip):
        """测试获取卡片详情"""
        # 先生成一张卡片
        create_response = client.post(
            "/api/elder/cards/generate",
            json={
                "trip_id": create_test_trip["id"],
                "title": "测试卡片",
                "image_url": "https://example.com/test.jpg"
            },
            headers=create_test_elder["headers"]
        )
        card_id = create_response.json()["id"]
        
        response = client.get(
            f"/api/elder/cards/{card_id}",
            headers=create_test_elder["headers"]
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == card_id
