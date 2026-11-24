def test_all_orm_models_are_registered():
    from app.infrastructure.database.base import Base
    from app import models  # noqa: F401
    expected = {"users", "user_sessions", "client_profiles", "employee_profiles", "procedures", "procedure_sessions", "appointments"}
    assert expected.issubset(set(Base.metadata.tables.keys()))
