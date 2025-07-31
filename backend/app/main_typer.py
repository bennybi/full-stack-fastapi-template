import sentry_sdk
from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware
import uvicorn
from app.api.main import api_router
from app.core.config import settings
import typer

shell_app = typer.Typer()


def create_app():
    def custom_generate_unique_id(route: APIRoute) -> str:
        return f"{route.tags[0]}-{route.name}"

    if settings.SENTRY_DSN and settings.ENVIRONMENT != "local":
        sentry_sdk.init(dsn=str(settings.SENTRY_DSN), enable_tracing=True)

    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        generate_unique_id_function=custom_generate_unique_id,
    )

    # Set all CORS enabled origins
    if settings.all_cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.all_cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    app.include_router(api_router, prefix=settings.API_V1_STR)
    return app


@shell_app.command()
def run(
    host: str = typer.Option(
        default="0.0.0.0", help="监听主机IP，默认开放给本网络所有主机"
    ),
    port: int = typer.Option(default=8000, help="监听端口"),
):
    """
    启动项目

    factory: 在使用 uvicorn.run() 启动 ASGI 应用程序时，可以通过设置 factory 参数来指定应用程序工厂。
    应用程序工厂是一个返回 ASGI 应用程序实例的可调用对象，它可以在启动时动态创建应用程序实例。
    """
    print(f"启动项目：{settings.PROJECT_NAME}")

    uvicorn.run(
        app="main_typer:create_app",
        host=host,
        port=port,
        lifespan="on",
        factory=True,
        reload=True,
        workers=1,
    )


if __name__ == "__main__":
    shell_app()
