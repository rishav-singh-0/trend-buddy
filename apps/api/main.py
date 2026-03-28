from __future__ import annotations

import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from apps.api.routers.market_data import DEFAULT_SYMBOL, build_market_snapshot, router as market_data_router
from apps.api.routers.portfolio import router as portfolio_router
from packages.shared.config.settings import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="Trend Buddy API",
        summary="Typed REST and realtime endpoints for the Trend Buddy dashboard spike.",
        version="0.1.0",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(market_data_router)
    app.include_router(portfolio_router)

    @app.get("/", tags=["system"])
    async def root() -> dict[str, str]:
        return {
            "name": "Trend Buddy API",
            "docs": "/docs",
            "health": "/health",
            "market_data": "/market-data",
            "portfolio": "/portfolio",
            "websocket": "/ws/market-data",
        }

    @app.get("/health", tags=["system"])
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.websocket("/ws/market-data")
    async def market_data_stream(websocket: WebSocket) -> None:
        await websocket.accept()
        symbol = websocket.query_params.get("symbol", DEFAULT_SYMBOL)
        tick = 0
        try:
            while True:
                snapshot = build_market_snapshot(symbol=symbol, tick=tick)
                await websocket.send_json(snapshot.model_dump(mode="json"))
                tick += 1
                await asyncio.sleep(1)
        except WebSocketDisconnect:
            return

    return app


app = create_app()
