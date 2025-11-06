from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin, ModelView
from app.core.database import Base, engine, SessionLocal
from app.models.user import User
from app.models.problem import Problem
from app.routers.problem_router import router as problem_router
from app.routers.appointment import router as appointment_router
from app.routers.real_estate import router as realestate_router
from app.routers.auth_router import router as auth_router
from app.routers.user_router import router as user_router
from app.core.openapi_config import customize_openapi
from app.core.security import get_password_hash

# -----------------------------------------
# 🚀 Initialize App
# -----------------------------------------
app = FastAPI(title="ANAND GROUPS CRM 1.0")

# Create all tables
Base.metadata.create_all(bind=engine)

# -----------------------------------------
# 🌍 CORS Middleware - MUST BE BEFORE ROUTERS
# -----------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# -----------------------------------------
# 🔗 Include Routers
# -----------------------------------------
app.include_router(auth_router)
app.include_router(problem_router, prefix="/api/problems", tags=["Problems"])
app.include_router(appointment_router, prefix="/api/appointments", tags=["Appointments"])
app.include_router(realestate_router, prefix="/api/real-estate", tags=["Real Estate"])
app.include_router(user_router, prefix="/api/users", tags=["Users"])

# -----------------------------------------
# ❤️ Health Check
# -----------------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

# -----------------------------------------
# 🧩 OpenAPI Customization
# -----------------------------------------
customize_openapi(app)

# -----------------------------------------
# 🧑‍💼 Auto-Create Super Admin
# -----------------------------------------
@app.on_event("startup")
def create_super_admin():
    db = SessionLocal()
    try:
        admin_email = "admin@anandgroups.com"
        admin_password = "Admin@123"
        admin_role = "superadmin"

        existing_admin = db.query(User).filter(User.email == admin_email).first()
        if not existing_admin:
            hashed_pw = get_password_hash(admin_password)
            admin = User(
                username="SuperAdmin",
                email=admin_email,
                hashed_password=hashed_pw,
                role=admin_role,
                is_active=True,
            )
            db.add(admin)
            db.commit()
            print(f"✅ Super admin created: {admin_email} / {admin_password}")
        else:
            print("⚙️ Super admin already exists — skipping creation.")
    finally:
        db.close()

# -----------------------------------------
# 🧭 SQLAdmin Dashboard (/admin)
# -----------------------------------------
class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.email, User.role, User.is_active, User.created_at]
    column_searchable_list = [User.username, User.email, User.role]
    column_sortable_list = [User.id, User.created_at]
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-users"

class ProblemAdmin(ModelView, model=Problem):
    column_list = [Problem.id, Problem.full_name, Problem.email, Problem.priority_level, Problem.created_at]
    column_searchable_list = [Problem.full_name, Problem.email, Problem.problem_category]
    column_sortable_list = [Problem.id, Problem.created_at]
    name = "Problem"
    name_plural = "Problems"
    icon = "fa-solid fa-headset"

admin = Admin(app, engine)
admin.add_view(UserAdmin)
admin.add_view(ProblemAdmin)