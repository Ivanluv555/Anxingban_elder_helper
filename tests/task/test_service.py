"""
Task 模块测试 - Service 层单元测试
"""
from app.modules.task.service.TaskService import TaskService


class TestTaskService:
    """Task Service 单元测试"""
    
    def test_create_task(self, db_session):
        """测试创建任务"""
        task = TaskService.create_task(
            db_session, profile_id=1, trip_id=1,
            title="测试任务", description="描述"
        )
        
        assert task is not None
        assert task.user_completed is False
        assert task.elder_completed is False
    
    def test_complete_task_by_user_only(self, db_session):
        """测试只有子女完成任务"""
        task = TaskService.create_task(
            db_session, profile_id=1, trip_id=1,
            title="测试", description="测试"
        )
        
        completed = TaskService.complete_task_by_user(db_session, task.id, "已完成")
        
        assert completed.user_completed is True
        assert completed.elder_completed is False
        assert completed.user_feedback == "已完成"
        assert completed.user_completed_at is not None
        assert completed.elder_completed_at is None
    
    def test_complete_task_by_elder_only(self, db_session):
        """测试只有老人完成任务"""
        task = TaskService.create_task(
            db_session, profile_id=1, trip_id=1,
            title="测试", description="测试"
        )
        
        completed = TaskService.complete_task_by_elder(db_session, task.id, "很棒")
        
        assert completed.elder_completed is True
        assert completed.user_completed is False
        assert completed.elder_feedback == "很棒"
        assert completed.elder_completed_at is not None
        assert completed.user_completed_at is None
    
    def test_both_complete_task(self, db_session):
        """测试双方都完成任务"""
        task = TaskService.create_task(
            db_session, profile_id=1, trip_id=1,
            title="测试", description="测试"
        )
        
        TaskService.complete_task_by_user(db_session, task.id, "子女完成")
        completed = TaskService.complete_task_by_elder(db_session, task.id, "老人完成")
        
        assert completed.user_completed is True
        assert completed.elder_completed is True
    
    def test_get_task_not_found(self, db_session):
        """测试查询不存在的任务"""
        task = TaskService.get_task_by_id(db_session, 999999)
        
        assert task is None
    
    def test_list_tasks_empty(self, db_session):
        """测试查询空任务列表"""
        tasks = TaskService.list_all_tasks(db_session, limit=10)
        
        assert tasks == []
    
    def test_list_tasks_by_profile(self, db_session):
        """测试按档案查询任务"""
        TaskService.create_task(db_session, 1, 1, "任务1", "描述1")
        TaskService.create_task(db_session, 1, 1, "任务2", "描述2")
        TaskService.create_task(db_session, 2, 1, "任务3", "描述3")
        
        tasks = TaskService.list_tasks_by_profile(db_session, profile_id=1)
        
        assert len(tasks) == 2
