"""
单元测试配置文件
"""
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 设置测试环境
os.environ["ENVIRONMENT"] = "test"
os.environ["LOG_LEVEL"] = "ERROR"  # 测试时只记录错误

# 测试数据库配置
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "mysql+pymysql://root:password@localhost:3306/anxingban_test?charset=utf8mb4"
)

from app.database import Base, get_db, import_all_entities
from app.main import app

# 创建测试引擎
test_engine = create_engine(TEST_DATABASE_URL, pool_pre_ping=True)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    """覆盖数据库依赖"""
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """创建测试数据库表"""
    import_all_entities()
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client():
    """创建测试客户端"""
    return TestClient(app)


@pytest.fixture(scope="function")
def db_session():
    """创建数据库会话"""
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function", autouse=True)
def reset_database():
    """每个测试后清理数据"""
    yield
    session = TestSessionLocal()
    try:
        # 清空所有表
        for table in reversed(Base.metadata.sorted_tables):
            session.execute(table.delete())
        session.commit()
    finally:
        session.close()
