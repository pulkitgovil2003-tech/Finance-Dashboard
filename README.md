# Finance Dashboard 

A backend REST API for a finance dashboard system built with **FastAPI**, **Motor (async MongoDB)**, and **Poetry**.

## Live API
🚀 **Deployed URL:** https://finance-dashboard-r79x.onrender.com

📖 **API Docs:** https://finance-dashboard-r79x.onrender.com/docs


## Tech Stack

- **Language:** Python 3.12+
- **Framework:** FastAPI
- **Database:** MongoDB Atlas (via Motor - async driver)
- **Authentication:** JWT (JSON Web Tokens)
- **Package Manager:** Poetry

## Project Structure
```
finance-dashboard/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Environment variables & settings
│   ├── database.py          # MongoDB connection (Motor)
│   ├── models/              # Pydantic models
│   │   ├── user.py
│   │   ├── record.py
│   │   └── dashboard.py
│   ├── routes/              # API route handlers
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── records.py
│   │   └── dashboard.py
│   ├── services/            # Business logic
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── record_service.py
│   │   └── dashboard_service.py
│   ├── middleware/          # Auth & role middleware
│   │   └── auth_middleware.py
│   └── utils/               # Helper functions
│       └── response.py
├── .env                     # Environment variables (not committed)
├── pyproject.toml
└── README.md
```

## Roles & Permissions

| Action | Viewer | Analyst | Admin |
|--------|--------|---------|-------|
| Login / View profile | ✅ | ✅ | ✅ |
| View dashboard summary | ✅ | ✅ | ✅ |
| View recent activity | ✅ | ✅ | ✅ |
| View all records | ❌ | ✅ | ✅ |
| Category breakdown & trends | ❌ | ✅ | ✅ |
| Create/Edit/Delete records | ❌ | ❌ | ✅ |
| Manage users | ❌ | ❌ | ✅ |

> **Note:** First registered user is automatically assigned the **Admin** role.

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/your-username/finance-dashboard.git
cd finance-dashboard
```

### 2. Install dependencies
```bash
poetry install
```

### 3. Create `.env` file
```env
MONGODB_URI=your_mongodb_atlas_uri
JWT_SECRET=your_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=2880
```

### 4. Run the server
```bash
poetry run uvicorn app.main:app --reload
```

### 5. Open API docs
```
http://localhost:8000/docs
```

## API Endpoints

### Auth
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | `/api/auth/register` | Register new user | Public |
| POST | `/api/auth/login` | Login & get token | Public |
| GET | `/api/auth/me` | Get current user | All logged in |

### Users
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/api/users` | List all users | Admin |
| GET | `/api/users/{id}` | Get user by ID | Admin |
| PATCH | `/api/users/{id}/role` | Update user role | Admin |
| PATCH | `/api/users/{id}/status` | Update user status | Admin |
| DELETE | `/api/users/{id}` | Delete user | Admin |

### Financial Records
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | `/api/records` | Create record | Admin |
| GET | `/api/records` | List records (with filters) | Analyst, Admin |
| GET | `/api/records/{id}` | Get record by ID | Analyst, Admin |
| PATCH | `/api/records/{id}` | Update record | Admin |
| DELETE | `/api/records/{id}` | Soft delete record | Admin |

### Dashboard
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/api/dashboard/summary` | Total income, expenses, balance | All roles |
| GET | `/api/dashboard/category-breakdown` | Category wise totals | Analyst, Admin |
| GET | `/api/dashboard/monthly-trends` | Monthly income vs expense | Analyst, Admin |
| GET | `/api/dashboard/recent-activity` | Last 10 transactions | All roles |

## Key Features

- JWT based authentication
- Role based access control (Viewer, Analyst, Admin)
- Financial records with soft delete
- Dashboard analytics using MongoDB aggregation pipelines
- Pagination and filtering for records
- IST timezone support
- Consistent API response format

## Assumptions

- First registered user automatically becomes Admin
- Soft delete is used for records (data is never permanently lost)
- All timestamps are stored in UTC and returned in IST
- Viewers can only see dashboard summary and recent activity
- Analysts can view records and detailed analytics but cannot modify data

## Response Format

All APIs return a consistent response:
```json
{
    "status": "SUCCESS",
    "message": "Operation successful",
    "data": {}
}
```
```json
{
    "status": "FAILURE",
    "message": "Error description",
    "data": null
}
```