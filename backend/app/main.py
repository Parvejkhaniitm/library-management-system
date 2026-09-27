from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.auth import router as auth_router
from app.api.v1.admin.students import router as admin_students_router
from app.api.v1.admin.rooms import router as admin_rooms_router
from app.api.v1.admin.seat_assignments import router as admin_seat_assignments_router
from app.api.v1.admin.membership_plans import router as admin_membership_plans_router
from app.api.v1.admin.lockers import router as admin_lockers_router
from app.api.v1.admin.memberships import router as admin_memberships_router
from app.api.v1.student.profile import router as student_profile_router
from app.api.v1.admin.locker_assignments import router as admin_locker_assignments_router




app = FastAPI(
    title="Library Management System API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(admin_students_router)
app.include_router(admin_rooms_router)
app.include_router(admin_seat_assignments_router)
app.include_router(admin_membership_plans_router)
app.include_router(admin_lockers_router)
app.include_router(admin_memberships_router)
app.include_router(student_profile_router)
app.include_router(admin_locker_assignments_router)


@app.get("/")
def read_root():
    return {"message": "Library Management System backend is running"}