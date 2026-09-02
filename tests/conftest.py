"""
测试配置文件 - 提供测试数据库、fixtures 和工具函数
"""
import os
import pytest
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool 

# 设置测试数据库
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL", 
    "sqlite:///:memory:"
)

# 创建测试专用的数据库引擎
# 对于内存数据库，使用 StaticPool 确保所有连接使用同一个数据库实例
connect_args = {"check_same_thread": False} if "sqlite" in TEST_DATABASE_URL else {}
poolclass = StaticPool if TEST_DATABASE_URL == "sqlite:///:memory:" else None

test_engine = create_engine(
    TEST_DATABASE_URL, 
    connect_args=connect_args, 
    poolclass=poolclass,
    pool_pre_ping=True
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# 导入 Base 和实体
from app.utils.database import Base
from app.utils.database import import_all_entities

# 立即导入所有实体
import_all_entities()

# 导入 app（这会使用 .env 中的配置，但我们会覆盖 get_db）
from app.main import app
from app.utils.database import get_db


def override_get_db():
    """覆盖数据库依赖 - 使用测试数据库"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# 覆盖 FastAPI 的数据库依赖
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function", autouse=True)
def setup_test_database():
    """Function 级别：每个测试前重建数据库表结构"""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """Function 级别：提供独立的数据库会话"""
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client() -> TestClient:
    """Function 级别：提供测试客户端"""
    return TestClient(app)


@pytest.fixture(scope="function")
def clean_db(db_session):
    """清空所有表数据"""
    for table in reversed(Base.metadata.sorted_tables):
        db_session.execute(table.delete())
    db_session.commit()
    yield db_session


# ============= 测试数据 Fixtures =============

@pytest.fixture
def test_user_data():
    """测试用户数据"""
    return {
        "nickname": "TestUser",
        "phone": "13800138000",
        "password": "Test1234!@#"
    }


@pytest.fixture
def test_elder_data():
    """测试老人数据"""
    return {
        "name": "TestElder",
        "phone": "13900139000",
        "password": "Elder1234!@#",
        "health_info": '{"chronic_diseases": "none"}',
        "interests": "culture,food",
        "wechat_webhook_url": ""
    }


@pytest.fixture
def create_test_user(client, test_user_data):
    """创建测试用户并返回 token"""
    response = client.post("/api/auth/user/register", json=test_user_data)
    assert response.status_code == 200
    data = response.json()
    return {
        "user_id": data["user_id"],
        "token": data["access_token"],
        "headers": {"Authorization": f"Bearer {data['access_token']}"}
    }


@pytest.fixture
def create_test_elder(client, test_elder_data):
    """创建测试老人并返回 token"""
    response = client.post("/api/auth/elder/register", json=test_elder_data)
    assert response.status_code == 200
    data = response.json()
    return {
        "elder_id": data["user_id"],
        "token": data["access_token"],
        "headers": {"Authorization": f"Bearer {data['access_token']}"}
    }


@pytest.fixture
def create_test_profile(client, create_test_user, create_test_elder):
    """创建测试档案"""
    response = client.post(
        "/api/user/profiles",
        json={"elder_id": create_test_elder["elder_id"]},
        headers=create_test_user["headers"]
    )
    assert response.status_code == 200
    return response.json()


@pytest.fixture
def create_test_trip(client, create_test_user, create_test_profile):
    """创建测试行程"""
    from datetime import date, timedelta
    response = client.post(
        "/api/user/trips",
        json={
            "profile_id": create_test_profile["id"],
            "destination": "重庆",
            "travel_date": str(date.today() + timedelta(days=7))
        },
        headers=create_test_user["headers"]
    )
    assert response.status_code == 200
    return response.json()


@pytest.fixture
def create_test_task(client, create_test_user, create_test_profile, create_test_trip):
    """创建测试任务"""
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
    return response.json()
