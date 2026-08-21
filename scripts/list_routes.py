from app.main import app

routes = []
for route in app.routes:
    if hasattr(route, 'methods') and hasattr(route, 'path'):
        for method in route.methods:
            if method != 'HEAD':
                routes.append((method, route.path))

routes.sort()
for method, path in routes:
    print(f'{method:6} {path}')
