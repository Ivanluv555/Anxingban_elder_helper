"""
集成测试 - 完整业务流程
"""
import pytest
from datetime import date, timedelta


class TestFullWorkflow:
    """完整业务流程测试"""
    
    def test_complete_family_workflow(self, client, test_user_data, test_elder_data):
        """测试完整的家庭协同流程"""
        
        # 1. 注册子女用户
        user_response = client.post("/api/auth/user/register", json=test_user_data)
        assert user_response.status_code == 200
        user_data = user_response.json()
        user_headers = {"Authorization": f"Bearer {user_data['access_token']}"}
        
        # 2. 注册老人用户
        elder_response = client.post("/api/auth/elder/register", json=test_elder_data)
        assert elder_response.status_code == 200
        elder_data = elder_response.json()
        elder_headers = {"Authorization": f"Bearer {elder_data['access_token']}"}
        
        # 3. 子女扫码创建档案
        profile_response = client.post(
            "/api/user/profiles",
            json={"elder_id": elder_data["user_id"]},
            headers=user_headers
        )
        assert profile_response.status_code == 200
        profile = profile_response.json()
        
        # 4. 老人查看档案列表
        elder_profiles = client.get("/api/elder/profiles", headers=elder_headers)
        assert elder_profiles.status_code == 200
        assert len(elder_profiles.json()) == 1
        
        # 5. 子女创建行程
        trip_response = client.post(
            "/api/user/trips",
            json={
                "profile_id": profile["id"],
                "destination": "重庆",
                "travel_date": str(date.today() + timedelta(days=7))
            },
            headers=user_headers
        )
        assert trip_response.status_code == 200
        trip = trip_response.json()
        
        # 6. 老人查看行程详情（含通行码）
        elder_trip = client.get(f"/api/elder/trips/{trip['id']}", headers=elder_headers)
        assert elder_trip.status_code == 200
        assert "pass_qr_svg" in elder_trip.json()
        
        # 7. 子女创建任务
        task_response = client.post(
            "/api/user/tasks",
            json={
                "profile_id": profile["id"],
                "trip_id": trip["id"],
                "title": "拍照打卡",
                "description": "在解放碑拍照"
            },
            headers=user_headers
        )
        assert task_response.status_code == 200
        task = task_response.json()
        
        # 8. 子女完成任务
        user_complete = client.post(
            f"/api/user/tasks/{task['id']}/complete",
            json={"feedback": "已完成拍照"},
            headers=user_headers
        )
        assert user_complete.status_code == 200
        assert user_complete.json()["user_completed"] is True
        
        # 9. 老人完成任务
        elder_complete = client.post(
            f"/api/elder/tasks/{task['id']}/complete",
            json={"feedback": "照片很棒"},
            headers=elder_headers
        )
        assert elder_complete.status_code == 200
        completed_task = elder_complete.json()
        assert completed_task["user_completed"] is True
        assert completed_task["elder_completed"] is True
        
        # 10. 老人生成回忆卡片
        card_response = client.post(
            "/api/elder/cards/generate",
            json={
                "trip_id": trip["id"],
                "title": "重庆之旅",
                "image_url": "https://example.com/image.jpg"
            },
            headers=elder_headers
        )
        assert card_response.status_code == 200
        card = card_response.json()
        assert "重庆" in card["summary"]
    
    def test_authorization_checks(self, client, create_test_user, create_test_elder, create_test_profile):
        """测试权限控制"""
        
        # 子女不能访问老人端接口
        response = client.get(
            "/api/elder/profiles",
            headers=create_test_user["headers"]
        )
        assert response.status_code == 403
        
        # 老人不能访问子女端接口
        response = client.post(
            "/api/user/profiles",
            json={"elder_id": 1},
            headers=create_test_elder["headers"]
        )
        assert response.status_code == 403
        
        # 未登录不能访问受保护接口
        response = client.get("/api/user/profiles")
        assert response.status_code == 403
    
    def test_data_isolation(self, client, test_user_data, test_elder_data):
        """测试数据隔离"""
        
        # 创建两个用户
        user1 = client.post("/api/auth/user/register", json=test_user_data).json()
        
        test_user_data2 = test_user_data.copy()
        test_user_data2["phone"] = "13800138001"
        user2 = client.post("/api/auth/user/register", json=test_user_data2).json()
        
        # 创建老人
        elder = client.post("/api/auth/elder/register", json=test_elder_data).json()
        
        # 用户1创建档案
        headers1 = {"Authorization": f"Bearer {user1['access_token']}"}
        profile1 = client.post(
            "/api/user/profiles",
            json={"elder_id": elder["user_id"]},
            headers=headers1
        ).json()
        
        # 用户2不应该看到用户1的档案
        headers2 = {"Authorization": f"Bearer {user2['access_token']}"}
        profiles2 = client.get("/api/user/profiles", headers=headers2).json()
        
        assert len(profiles2) == 0
        
        # 用户2不能删除用户1的档案
        response = client.delete(
            f"/api/user/profiles/{profile1['id']}",
            headers=headers2
        )
        assert response.status_code == 403
