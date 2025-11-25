# FastAPI Dependency Injection Example

This repository demonstrates how **Dependency Injection (DI)** works in FastAPI using realistic examples.

---

## Features
- Function-based dependencies
- Class-based dependencies (settings)
- Router-based modular structure
- Testable via dependency overrides
- Clean code separation (services, routers, dependencies)

---

## Running the Project

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Start the server:**
```bash
uvicorn app.main:app --reload
```

**Test the endpoint:**
```bash
curl http://127.0.0.1:8000/users/profile
```
Or open in browser: `http://127.0.0.1:8000/docs`

**Test the endpoint wiht Authorization:**
```bash
curl -H "Authorization: admin-token-123" http://127.0.0.1:8000/users/dashboard
```

---

## 🧪 Running Tests

```bash
pytest -v -s
```

The tests demonstrate how to override dependencies for testing, which is one of the key benefits of FastAPI's DI system.

---

## 🎯 Key Concepts

- **Depends()**: FastAPI's dependency injection decorator
- **Dependency Overrides**: Replace real dependencies with mocks in tests
- **Service Layer**: Separation of business logic from routing logic
- **Type Hints**: Enable proper IDE support and validation

---

## 📖 Learn More

- [FastAPI Dependencies Documentation](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [Testing with Overrides](https://fastapi.tiangolo.com/advanced/testing-dependencies/)
