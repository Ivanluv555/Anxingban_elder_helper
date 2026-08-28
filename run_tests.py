"""
测试运行脚本
"""
#!/usr/bin/env python3
import sys
import subprocess
import os


def run_tests():
    """运行所有测试"""
    # 设置测试数据库环境变量
    os.environ["TEST_DATABASE_URL"] = os.getenv(
        "TEST_DATABASE_URL",
        "mysql+pymysql://root:123456@localhost:3306/anxingban_test"
    )
    
    print("=" * 60)
    print("开始运行测试套件")
    print("=" * 60)
    print(f"测试数据库: {os.environ['TEST_DATABASE_URL']}")
    print()
    
    # 运行 pytest
    cmd = [
        "pytest",
        "-v",
        "--tb=short",
        "--cov=app",
        "--cov-report=html",
        "--cov-report=term-missing",
        "tests/"
    ]
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print("\n" + "=" * 60)
        print("✅ 所有测试通过！")
        print("=" * 60)
        print("📊 覆盖率报告: htmlcov/index.html")
    else:
        print("\n" + "=" * 60)
        print("❌ 测试失败")
        print("=" * 60)
        sys.exit(1)


def run_unit_tests():
    """只运行单元测试"""
    cmd = ["pytest", "-v", "-m", "unit", "tests/"]
    subprocess.run(cmd)


def run_integration_tests():
    """只运行集成测试"""
    cmd = ["pytest", "-v", "-m", "integration", "tests/"]
    subprocess.run(cmd)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "unit":
            run_unit_tests()
        elif sys.argv[1] == "integration":
            run_integration_tests()
        else:
            print(f"未知参数: {sys.argv[1]}")
            print("用法: python run_tests.py [unit|integration]")
            sys.exit(1)
    else:
        run_tests()
