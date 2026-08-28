"""
Task 模块测试
"""
import pytest
from app.modules.task.service.TaskService import TaskService


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
        assert data["user_completed_at"] is not None
    
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
        assert data["elder_feedback"] == "很开心"
        assert data["elder_completed_at"] is not None
    
    def test_list_tasks(self, client, create_test_user, create_test_task):
        """测试获取任务列表"""
        response = client.get(
            "/api/user/tasks",
            headers=create_test_user["headers"]
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        # 列表不应该包含 feedback 和完成时间
        assert "user_feedback" not in data[0]
        assert "elder_feedback" not in data[0]
    
    def test_get_task_detail(self, client, create_test_user, create_test_task):
        """测试获取任务详情"""
        task_id = create_test_task["id"]
        
        response = client.get(
            f"/api/user/tasks/{task_id}",
            headers=create_test_user["headers"]
        )
        
        assert response.status_code == 200
        data = response.json()
        # 详情应该包含所有字段
        assert "user_feedback" in data
        assert "elder_feedback" in data
        assert "user_completed_at" in data
        assert "elder_completed_at" in data


class TestTaskService:
    """Task Service 单元测试"""
    
    def test_create_task(self, db_session):
        """测试创建任务"""
        task = TaskService.create_task(
            db_session,
            profile_id=1,
            trip_id=1,
            title="测试任务",
            description="这是一个测试任务"
        )
        
        assert task is not None
        assert task.title == "测试任务"
        assert task.user_completed is False
        assert task.elder_completed is False
    
    def test_complete_task_by_user(self, db_session):
        """测试子女完成任务"""
        task = TaskService.create_task(
            db_session, profile_id=1, trip_id=1,
            title="测试", description="测试"
        )
        
        completed_task = TaskService.complete_task_by_user(
            db_session, task.id, "已完成"
        )
        
        assert completed_task.user_completed is True
        assert completed_task.user_feedback == "已完成"
        assert completed_task.user_completed_at is not None
    
    def test_complete_task_by_elder(self, db_session):
        """测试老人完成任务"""
        task = TaskService.create_task(
            db_session, profile_id=1, trip_id=1,
            title="测试", description="测试"
        )
        
        completed_task = TaskService.complete_task_by_elder(
            db_session, task.id, "很棒"
        )
        
        assert completed_task.elder_completed is True
        assert completed_task.elder_feedback == "很棒"
        assert completed_task.elder_completed_at is not None
    
    def test_both_complete_task(self, db_session):
        """测试双方都完成任务"""
        task = TaskService.create_task(
            db_session, profile_id=1, trip_id=1,
            title="测试", description="测试"
        )
        
        TaskService.complete_task_by_user(db_session, task.id, "子女完成")
        completed_task = TaskService.complete_task_by_elder(db_session, task.id, "老人完成")
        
        assert completed_task.user_completed is True
        assert completed_task.elder_completed is True
