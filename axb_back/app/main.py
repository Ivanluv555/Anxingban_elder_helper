"""FastAPI 应用入口"""
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.database import init_db
from app.logger import logger
from app.utils.error_codes import BusinessException

# 导入路由
from app.modules.auth.controller.AuthController import router as auth_router
from app.modules.card.controller.CardController import router as card_router
from app.modules.card.controller.CardElderController import router as card_elder_router
from app.modules.profile.controller.ProfileController import router as profile_router
from app.modules.profile.controller.ProfileElderController import router as profile_elder_router
from app.modules.trip.controller.TripController import router as trip_router
from app.modules.trip.controller.TripElderController import router as trip_elder_router
from app.modules.task.controller.TaskController import router as task_router
from app.modules.task.controller.TaskElderController import router as task_elder_router
from app.modules.sos.controller.SOSController import router as sos_router
from app.modules.sos.controller.SOSElderController import router as sos_elder_router
from app.modules.guide.controller.GuideController import router as guide_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    logger.info("应用启动中...")
    logger.info(f"环境: {settings.environment}")
    logger.info(f"数据库: {settings.database_url.split('@')[1] if '@' in settings.database_url else '***'}")

    # 初始化数据库（可选，生产环境建议使用迁移工具）
    # init_db()

    yield

    # 关闭时执行
    logger.info("应用关闭中...")


# 创建FastAPI应用
app = FastAPI(
    title=settings.app_name,
    description="安行伴后端API - 帮助子女与长辈实现协同建档、行程安全保障、代际互动和回忆沉淀",
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 全局异常处理
@app.exception_handler(BusinessException)
async def business_exception_handler(request: Request, exc: BusinessException):
    """处理业务异常"""
    logger.warning(f"业务异常: {exc.error_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error_code": exc.error_code,
            "detail": exc.detail,
            "path": str(request.url)
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """处理通用异常"""
    logger.error(f"未处理的异常: {type(exc).__name__} - {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error_code": "INTERNAL_ERROR",
            "detail": "服务器内部错误",
            "path": str(request.url)
        }
    )


# 注册路由
# 认证
app.include_router(auth_router)

# 档案
app.include_router(profile_router)
app.include_router(profile_elder_router)

# 行程
app.include_router(trip_router)
app.include_router(trip_elder_router)

# 任务
app.include_router(task_router)
app.include_router(task_elder_router)

# 紧急求助
app.include_router(sos_router)
app.include_router(sos_elder_router)

# 回忆卡片
app.include_router(card_router)
app.include_router(card_elder_router)

# 景点讲解
app.include_router(guide_router)


@app.get("/", tags=["健康检查"])
async def root():
    """根路径 - 健康检查"""
    return {
        "status": "ok",
        "app": settings.app_name,
        "environment": settings.environment,
        "message": "安行伴后端服务运行中"
    }


@app.get("/health", tags=["健康检查"])
async def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "environment": settings.environment
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=settings.environment == "development"
    )
