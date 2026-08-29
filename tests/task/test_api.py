"""
Task 模块测试 - API 集成测试
"""


class TestTaskAPI:
    """Task API 集成测试"""
    
    def test_create_task_success(self, client, create_test_user, create_test_profile, create_test_trip):
        """测试创建任务成功"""
        response = client.post(
            "/api/user/tasks",
            json={
                "profile_id": create_test_profile["id"],
                "trip_id": create_test_trip["id"],
                "title": "拍照打卡",
                "description": "在解放碑拍照留念"
            },
            headers=create_test_user["headers"]
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "拍照打卡"
        assert data["user_completed"] is False
        assert data["elder_completed"] is False
    
    def test_create_task_profile_not_found(self, client, create_test_user, create_test_trip):
        """测试创建任务时档案不存在"""
        response = client.post(
            "/api/user/tasks",
            json={
                "profile_id": 999999,
                "trip_id": create_test_trip["id"],
                "title": "拍照打卡",
                "description": "描述"
            },
            headers=create_test_user["headers"]
        )
        
        assert response.status_code == 404
        assert "档案不存在" in response.json()["detail"]
    
    def test_create_task_trip_not_found(self, client, create_test_user, create_test_profile):
        """测试创建任务时行程不存在"""
        response = client.post(
            "/api/user/tasks",
            json={
                "profile_id": create_test_profile["id"],
                "trip_id": 999999,
                "title": "拍照打卡",
                "description": "描述"
            },
            headers=create_test_user["headers"]
        )
        
        assert response.status_code == 404
        assert "行程不存在" in response.json()["detail"]
    
    def test_complete_task_by_user(self, client, create_test_user, create_test_task):
        """测试子女完成任务"""
        task_id = create_test_task["id"]
        
        response = client.post(
            f"/api/user/tasks/{task_id}/complete",
            json={"feedback": "已完成拍照"},
            headers=create_test_user["headers"]
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["user_completed"] is True
        assert data["user_feedback"] == "已完成拍照"
    
    def test_complete_task_by_user_not_found(self, client, create_test_user):
        """测试完成不存在的任务"""
        response = client.post(
            "/api/user/tasks/999999/complete",
            json={"feedback": "已完成"},
            headers=create_test_user["headers"]
        )
        
        assert response.status_code == 404
        assert "任务不存在" in response.json()["detail"]
    
    def test_complete_task_by_elder(self, client, create_test_elder, create_test_task):
        """测试老人完成任务"""
        task_id = create_test_task["id"]
        
        response = client.post(
            f"/api/elder/tasks/{task_id}/complete",
            json={"feedback": "很开心"},
            headers=create_test_elder["headers"]
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["elder_completed"] is True
    
    def test_complete_task_by_elder_not_found(self, client, create_test_elder):
        """测试老人完成不存在的任务"""
        response = client.post(
            "/api/elder/tasks/999999/complete",
            json={"feedback": "很好"},
            headers=create_test_elder["headers"]
        )
        
        assert response.status_code == 404
        assert "任务不存在" in response.json()["detail"]
    
    def test_list_tasks(self, client, create_test_user, create_test_task):
        """测试获取任务列表（不含反馈）"""
        response = client.get(
            "/api/user/tasks",
            headers=create_test_user["headers"]
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert "user_feedback" not in data[0]
    
    def test_get_task_detail(self, client, create_test_user, create_test_task):
        """测试获取任务详情（含反馈）"""
        task_id = create_test_task["id"]
        
        response = client.get(
            f"/api/user/tasks/{task_id}",
            headers=create_test_user["headers"]
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "user_feedback" in data
        assert "elder_feedback" in data
    
    def test_get_task_not_found(self, client, create_test_user):
        """测试获取不存在的任务"""
        response = client.get(
            "/api/user/tasks/999999",
            headers=create_test_user["headers"]
        )
        
        assert response.status_code == 404
        assert "任务不存在" in response.json()["detail"]
    
    def test_delete_task(self, client, create_test_user, create_test_task):
        """测试删除任务"""
        task_id = create_test_task["id"]
        
        response = client.delete(
            f"/api/user/tasks/{task_id}",
            headers=create_test_user["headers"]
        )
        
        assert response.status_code == 200
        assert "成功" in response.json()["message"]
    
    def test_delete_task_not_found(self, client, create_test_user):
        """测试删除不存在的任务"""
        response = client.delete(
            "/api/user/tasks/999999",
            headers=create_test_user["headers"]
        )
        
        assert response.status_code == 404
        assert "任务不存在" in response.json()["detail"]
    
    def test_elder_get_task_detail(self, client, create_test_elder, create_test_task):
        """测试老人获取任务详情"""
        task_id = create_test_task["id"]
        
        response = client.get(
            f"/api/elder/tasks/{task_id}",
            headers=create_test_elder["headers"]
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "user_feedback" in data
    
    def test_elder_get_task_not_found(self, client, create_test_elder):
        """测试老人获取不存在的任务"""
        response = client.get(
            "/api/elder/tasks/999999",
            headers=create_test_elder["headers"]
        )
        
        assert response.status_code == 404
        assert "任务不存在" in response.json()["detail"]
