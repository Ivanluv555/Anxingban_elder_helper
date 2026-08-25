from contextlib import asynccontextmanager
import time

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.config import settings
from app.database import Base, engine, import_all_entities, SessionLocal
from app.logger import get_logger, setup_logging
from app.error_codes import BusinessException, ErrorCode, get_error_response
from app.modules.profile.controller.ProfileController import router as profile_router
from app.modules.trip.controller.TripController import router as trip_router
from app.modules.task.controller.TaskController import router as task_router
from app.modules.sos.controller.SosController import router as sos_router
from app.modules.card.controller.CardController import router as card_router
from app.modules.guide.controller.GuideController import router as guide_router

# 初始化日志
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info(f"应用启动 - {settings.app_name} ({settings.environment})")
    logger.info(f"日志级别: {settings.log_level}")
    logger.info(f"日志文件: {settings.log_file}")
    
    import_all_entities()
    Base.metadata.create_all(bind=engine)
    
    logger.info("数据库表初始化完成")
    yield
    logger.info("应用关闭")


app = FastAPI(title=settings.app_name, lifespan=lifespan)


# 请求日志中间件
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # 记录请求
    logger.info(f"[REQUEST] {request.method} {request.url.path}")
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # 记录响应
        logger.info(
            f"[RESPONSE] {response.status_code} - "
            f"{request.method} {request.url.path} - "
            f"{process_time:.3f}s"
        )
        
        response.headers["X-Process-Time"] = str(process_time)
        return response
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(
            f"[ERROR] {request.method} {request.url.path} - "
            f"{process_time:.3f}s - {str(e)}",
            exc_info=True
        )
        raise


# 业务异常处理器
@app.exception_handler(BusinessException)
async def business_exception_handler(request: Request, exc: BusinessException):
    logger.warning(
        f"[BUSINESS_ERROR] {exc.error_code.value} - {exc.message} - "
        f"{request.method} {request.url.path}"
    )
    return JSONResponse(
        status_code=exc.http_status,
        content=get_error_response(exc.error_code, exc.detail)
    )


# 全局异常处理器
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(
        f"[UNHANDLED_ERROR] {str(exc)} - {request.method} {request.url.path}",
        exc_info=True
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=get_error_response(ErrorCode.INTERNAL_ERROR, str(exc))
    )


@app.get("/health")
def health_check():
    """健康检查端点"""
    try:
        # 测试数据库连接
        db = SessionLocal()
        try:
            db.execute(text("SELECT 1"))
            db.close()
            logger.debug("健康检查 - 数据库连接正常")
        except Exception as db_error:
            logger.error(f"健康检查失败 - 数据库连接错误: {str(db_error)}")
            raise HTTPException(
                status_code=503,
                detail=f"数据库连接失败: {str(db_error)}"
            )

        # 验证 TOKEN_SECRET
        if settings.environment == "production":
            if not settings.token_secret or settings.token_secret in [
                "replace-with-secure-random-string-in-production",
                "dev-secret-change-in-production"
            ]:
                logger.error("健康检查失败 - TOKEN_SECRET未正确配置")
                raise HTTPException(
                    status_code=503,
                    detail="TOKEN_SECRET 未在生产环境中正确配置"
                )

        return {
            "status": "healthy",
            "app_name": settings.app_name,
            "environment": settings.environment,
            "database": "connected",
            "version": "1.0.0"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"健康检查异常: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=503,
            detail=f"健康检查失败: {str(e)}"
        )


# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.environment == "development" else [
        "https://anxingban.com",
        "https://www.anxingban.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(profile_router, prefix="/api", tags=["档案管理"])
app.include_router(trip_router, prefix="/api", tags=["行程管理"])
app.include_router(task_router, prefix="/api", tags=["亲子任务"])
app.include_router(sos_router, prefix="/api", tags=["紧急求助"])
app.include_router(card_router, prefix="/api", tags=["回忆卡片"])
app.include_router(guide_router, prefix="/api", tags=["景点讲解"])

logger.info(f"应用初始化完成")
logger.info(f"API文档: http://localhost:{settings.port}/docs")
logger.info(f"健康检查: http://localhost:{settings.port}/health")
