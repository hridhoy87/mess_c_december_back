from fastapi import FastAPI
from app.api.v1 import routers_stay, routes_auth, routes_dashboard, routes_folios, routes_guest_photos, routes_guests, routes_payments, routes_reservation_rooms, routes_reservations, routes_rooms, routes_users

def create_app() -> FastAPI:
    app = FastAPI(title="Mess C Backend", version="1.0.0")

    @app.get("/")
    def root():
        return {"ok": True, "service": "mess-back"}

    # V1 routes
    app.include_router(routes_auth.router, prefix="/api/v1")
    app.include_router(routes_dashboard.router, prefix="/api/v1")
    app.include_router(routes_guests.router, prefix="/api/v1")
    app.include_router(routes_reservations.router, prefix="/api/v1")
    app.include_router(routes_rooms.router, prefix="/api/v1")
    app.include_router(routes_folios.router, prefix="/api/v1")
    app.include_router(routes_payments.router, prefix="/api/v1")
    app.include_router(routers_stay.router, prefix="/api/v1")
    app.include_router(routes_reservation_rooms.router, prefix="/api/v1")
    app.include_router(routes_guest_photos.router, prefix="/api/v1")
    app.include_router(routes_users.router, prefix="/api/v1")

    return app

app = create_app()
