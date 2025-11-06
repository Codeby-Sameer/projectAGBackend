from fastapi.openapi.utils import get_openapi

def customize_openapi(app):
    """
    Injects OAuth2 (JWT) configuration and custom branding into the Swagger UI.
    Should be called once in main.py after app creation.
    """

    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema

        # Base OpenAPI metadata
        openapi_schema = get_openapi(
            title="ANAND GROUPS Client Problem Resolution System",
            version="0.1.0",
            description=(
                "Backend API for ANAND GROUPS — Client Problem Resolution System.\n\n"
                "This API supports **JWT authentication** with role-based access control.\n\n"
                "Use the `Authorize` button in the top-right corner to log in via `/auth/token`.\n"
                "Each user role determines which endpoints are accessible:\n\n"
                "- 🧾 **Receptionist/Staff** → Can submit problems only\n"
                "- 🧍‍♂️ **Admin Personnel** → Manage problems, appointments, finance, notifications\n"
                "- 🧑‍💼 **Manager** → Manage cases, appointments, and reports\n"
                "- ⚙️ **Administrator** → Full system access"
            ),
            routes=app.routes,
        )

        # OAuth2 Password Flow for Swagger “Authorize” modal
        openapi_schema["components"]["securitySchemes"] = {
            "OAuth2PasswordBearer": {
                "type": "oauth2",
                "flows": {
                    "password": {
                        "tokenUrl": "/auth/token",
                        "scopes": {
                            "Receptionist/Staff": "Can submit problems",
                            "Admin Personnel": "Can manage appointments, finance, and notifications",
                            "Manager": "Can manage cases, reports, analytics",
                            "Administrator": "Full access to all modules",
                        },
                    }
                },
            }
        }

        # Apply OAuth2 globally — all endpoints can use it if required
        openapi_schema["security"] = [{"OAuth2PasswordBearer": []}]

        # Optional: Custom contact, license, or terms
        openapi_schema["info"]["contact"] = {
            "name": "ANAND GROUPS Support",
            "email": "support@anandgroups.com",
        }

        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi
