"""列出所有路由的脚本"""
from app.main import app


def list_routes():
    """列出所有API路由"""
    print("=" * 80)
    print("安行伴 API 路由列表")
    print("=" * 80)

    routes = []
    for route in app.routes:
        if hasattr(route, 'methods'):
            methods = ','.join(sorted(route.methods))
            path = route.path
            name = route.name
            routes.append((methods, path, name))

    # 按路径排序
    routes.sort(key=lambda x: x[1])

    # 打印路由
    for methods, path, name in routes:
        print(f"{methods:15} {path:50} {name}")

    print("=" * 80)
    print(f"总计: {len(routes)} 个路由")


if __name__ == "__main__":
    list_routes()
