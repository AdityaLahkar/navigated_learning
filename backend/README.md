# Learning Navigator Backend

## System Overview

Learning Navigator Backend is a graph-based adaptive learning system designed to model learner progression through interconnected educational topics.

The backend represents learning concepts as a Directed Acyclic Graph (DAG), where:
- topics act as graph nodes
- prerequisite relationships act as directed edges
- learners progress dynamically through the graph based on proficiency

The system tracks:
- learner proficiency
- learning activities
- prerequisite completion
- recommendation eligibility

The backend exposes REST APIs for:
- learner specific topic graph visualisation
- adaptive topic recommendations
- listing all available topics
- topic graph visulisation
- activity analytics
- teacher dashboards

The project is designed with:
- modular Flask architecture
- JWT-based authentication
- role-based access control
- bcrypt password hashing

---

## Architecture

The backend follows a layered architecture:

```text
Routes Layer
    ↓
Services Layer
    ↓
ORM Models
    ↓
MySQL Database
```

### Layers

| Layer | Responsibility |
|---|---|
| Routes | API endpoints and request handling |
| Services | Business logic and graph algorithms |
| Models | Database schema and ORM relationships |
| Middleware | Authentication and RBAC |
| Utils | Shared utility/helper functions |

### Core Architectural Features

- Directed graph-based learning model
- Modular Flask blueprint architecture
- JWT authentication
- Role-based authorization
- Recommendation engine based on prerequisite proficiency
- Analytics aggregation for learners and teachers
- Visualization-oriented API responses

## Database Schema

The backend models learning as a directed acyclic graph (DAG), where:

- Topics are represented as nodes
- Prerequisite relationships are represented as directed edges
- Learners progress through the graph over time
- Activities and proficiency values are tracked to generate learning insights and recommendations

The schema is normalized and designed to support:
- learner progress tracking
- prerequisite traversal
- recommendation generation
- activity aggregation
- visualization-friendly APIs


---

### 1. users

Stores platform users and supports role-based access control.

| Column | Type | Constraints |
|---|---|---|
| id | INT | PRIMARY KEY, AUTO_INCREMENT |
| name | VARCHAR(100) | NOT NULL |
| email | VARCHAR(255) | UNIQUE, NOT NULL |
| password_hash | VARCHAR(255) | NOT NULL |
| role | ENUM('learner', 'teacher') | NOT NULL |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |

#### Notes
- A single table is used for both learners and teachers.
- Role-based authorization is enforced at the API layer.


---

### 2. topics

Represents learning concepts/topics in the learning graph.

| Column | Type | Constraints |
|---|---|---|
| id | INT | PRIMARY KEY, AUTO_INCREMENT |
| name | VARCHAR(100) | UNIQUE, NOT NULL |
| description | TEXT | NULL |
| difficulty_level | ENUM('beginner', 'intermediate', 'advanced') | NOT NULL |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |

#### Notes
- Topics act as nodes in the learning graph.


---

### 3. topic_prerequisites

Represents directed prerequisite relationships between topics.

| Column | Type | Constraints |
|---|---|---|
| id | INT | PRIMARY KEY, AUTO_INCREMENT |
| prerequisite_topic_id | INT | FOREIGN KEY → topics(id), NOT NULL |
| next_topic_id | INT | FOREIGN KEY → topics(id), NOT NULL |

#### Constraints
- UNIQUE(prerequisite_topic_id, next_topic_id)

#### Notes
- This table models the learning graph as a Directed Acyclic Graph (DAG).
- Multiple prerequisites for a topic are supported.
- Example:
  - Linear Algebra → Probability
  - Probability → Neural Networks
  - Statistics → Neural Networks


---

### 4. learner_topic_progress

Tracks learner proficiency and progress for each topic.

| Column | Type | Constraints |
|---|---|---|
| id | INT | PRIMARY KEY, AUTO_INCREMENT |
| learner_id | INT | FOREIGN KEY → users(id), NOT NULL |
| topic_id | INT | FOREIGN KEY → topics(id), NOT NULL |
| proficiency_score | DECIMAL(3,2) | CHECK(proficiency_score >= 0 AND proficiency_score <= 1), default=0 |
| last_updated | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP |

#### Constraints
- UNIQUE(learner_id, topic_id)

#### Notes
- `proficiency_score` ranges from 0.00 to 1.00.
- This table represents the learner’s current knowledge state in the learning graph.
- Learner progress state is derived dynamically from proficiency values.


---

### 5. learning_activities

Defines learning activities associated with topics.

| Column | Type | Constraints |
|---|---|---|
| id | INT | PRIMARY KEY, AUTO_INCREMENT |
| topic_id | INT | FOREIGN KEY → topics(id), NOT NULL |
| activity_type | ENUM('reading', 'coding', 'quiz', 'discussion') | NOT NULL |
| activity_name | VARCHAR(255) | NOT NULL |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |

#### Notes
- This table stores canonical learning activity definitions associated with topics.
- A topic can contain multiple activities of the same type.
  - Example:
    - Bayes Quiz 1
    - Bayes Quiz 2
    - Bayes Quiz 3
- Activities are categorized into:
  - reading
  - coding
  - quiz
  - discussion
- Separating activity definitions from learner interaction events improves normalization and supports:
  - reusable activity definitions
  - activity-level analytics
  - multiple activities per topic
  - frontend-friendly activity metadata
- Activities act as structured learning tasks that learners engage with over time.

---

### 6. learner_activities

Stores learner interaction events for learning activities.

| Column | Type | Constraints |
|---|---|---|
| id | INT | PRIMARY KEY, AUTO_INCREMENT |
| learner_id | INT | FOREIGN KEY → users(id), NOT NULL |
| activity_id | INT | FOREIGN KEY → learning_activities(id), NOT NULL |
| score | DECIMAL(5,2) | CHECK(score >= 0 AND score <= 100), NOT NULL |
| duration_minutes | INT | NULL |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |

#### Notes
- This table stores learner interaction events for learning activities.
- Each row represents a learner’s engagement or performance for a specific activity.
- `score` represents a normalized engagement/performance metric ranging from:
  - 0 → no completion/performance
  - 100 → full completion/performance
- Activity scores are interpreted uniformly across all activity types:
  - quiz/coding activities represent evaluation performance
  - reading/discussion activities represent completion-based engagement
- Learner proficiency values are dynamically recalculated using learner activity data.
- Multiple learner attempts across different activities within the same topic are supported.
- Activity data is used for:
  - proficiency calculation
  - recommendation generation
  - activity aggregation
  - learner engagement analytics

---

## Relationship Overview

```text
User (Learner)
   |
   |---- learner_topic_progress ---- Topic
   |
   |---- learner_activities ---- learning_activities ---- Topic

Topic
   |
   |---- topic_prerequisites ---- Topic
```

## API Documentation

The backend exposes REST APIs designed to support:
- learner progress visualization
- learning graph traversal
- recommendation generation
- activity analytics
- role-based access control

All APIs return JSON responses and follow consistent HTTP status conventions.

---

### Authentication

Authentication is implemented using JWT-based authorization.

Authenticated requests must include:

```http
Authorization: Bearer <jwt_token>
```

Role-based access control is enforced at the API layer.

---

### API Groups

| Group | Purpose |
|---|---|
| Auth APIs | Authentication and user management |
| Learner APIs | Learner dashboard and learning state |
| Activity APIs | Activity ingestion and proficiency updates |
| Topic APIs | Learning graph traversal and visualization |
| Teacher APIs | Aggregated learner analytics |

---

### Auth APIs

#### POST `/auth/register`

Registers a new user.

##### Request Body

```json
{
  "name": "Aditya",
  "email": "aditya@example.com",
  "password": "password123",
  "role": "learner"
}
```

##### Response

```json
{
  "token": "jwt_token",
  "user": {
    "id": 1,
    "name": "Aditya",
    "email": "aditya@test.com",
    "role": "learner"
  }
}
```

##### Status Codes

| Code | Meaning |
|---|---|
| 201 | User created successfully |
| 400 | Invalid request data |

#### Notes
- The user_id and role embedded in the jwt payload will be treated as the source of truth for the user_id and role.

---

#### POST `/auth/login`

Authenticates a user and returns a JWT token.

##### Request Body

```json
{
  "email": "aditya@example.com",
  "password": "password123"
}
```

##### Response

```json
{
  "token": "jwt_token",
  "user": {
    "id": 1,
    "name": "Aditya",
    "email": "aditya@test.com",
    "role": "learner"
  }
}
```

##### Status Codes

| Code | Meaning |
|---|---|
| 200 | Login successful |
| 401 | Invalid credentials |
| 400 | malformed request |

---

### Learner APIs

#### GET `/learners/<id>/map`

Returns learner topic proficiency and prerequisite graph data.

##### Authorization
- Learners can access only their own data.
- Teachers can access any learner's data.

##### Response

```json
{
  "learner_id": 1,
  "topics": [
    {
      "id": 1,
      "name": "Linear Algebra",
      "proficiency": 0.82
    },
    {
      "id": 2,
      "name": "Probability",
      "proficiency": 0.45
    }
  ],
  "edges": [
    {
      "from": 1,
      "to": 2
    }
  ]
}
```

##### Status Codes

| Code | Meaning |
|---|---|
| 200 | Success |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Learner not found |

---

#### GET `/learners/<id>/activities`

Returns aggregated learner activity analytics.

##### Response

```json
{
  "learner_id": 1,
  "activities": {
    "reading": 10,
    "coding": 4,
    "quiz": 3,
    "discussion": 2
  },
  "activity_diversity_score": 0.72,
  "dominant_activity": "reading"
}
```

##### Status Codes

| Code | Meaning |
|---|---|
| 200 | Success |
| 401 | Unauthorized |
| 403 | Forbidden |

---

#### GET `/learners/<id>/recommendations`

Returns dynamically generated topic recommendations.

##### Recommendation Logic
Topics are recommended when prerequisite proficiency thresholds are satisfied.

##### Response

```json
{
  "learner_id": 1,
  "recommendations": [
    {
      "topic_id": 5,
      "topic_name": "Neural Networks",
      "reason": "All prerequisites exceed 70% proficiency"
    }
  ]
}
```

##### Status Codes

| Code | Meaning |
|---|---|
| 200 | Success |
| 401 | Unauthorized |
| 403 | Forbidden |

---

### Activity APIs

- Not implemented for this task. but when implemented, activities api will trigger dynamic proficiency scores calulation.

##### Internal Backend Flow

```text
Store Learner Activity
        ↓
Fetch Activity Metadata
        ↓
Recalculate Topic Proficiency
        ↓
Update learner_topic_progress
```

---

### Topic APIs

#### GET `/topics`

Returns all learning topics.

##### Response

```json
{
  "topics": [
    {
      "id": 1,
      "name": "Programming Basics",
      "description": "Introduction to programming",
      "difficulty_level": "beginner"
    }
  ]
}
```

---

#### GET `/topics/graph`

Returns graph-oriented topic relationships for frontend visualization.

##### Response

```json
{
  "topics": [
    {
      "id": 1,
      "name": "Linear Algebra",
      "proficiency": 0.82
    },
    {
      "id": 2,
      "name": "Probability",
      "proficiency": 0.45
    }
  ],
  "edges": [
    {
      "from": 1,
      "to": 2
    }
  ]
}
```

##### Notes
- Designed for React + D3 visualization compatibility.
- Returns visualization-friendly graph structures.
- Transitive prerequisite traversal is implemented in the backend service layer using DFS/BFS graph traversal.

---

### GET `/teacher/dashboard`

Returns aggregated platform-level learning analytics for teachers.

#### Authentication
Requires JWT authentication.

#### Authorization
Accessible only to users with role:

```text
teacher
```

---

### Response

```json
{
  "total_learners": 3,

  "average_proficiency": 0.68,

  "most_popular_topic": {
    "topic_id": 1,
    "topic_name": "Programming Basics"
  },

  "activity_distribution": {
    "reading": 4,
    "coding": 5,
    "quiz": 6,
    "discussion": 0
  }
}
```

---

### Notes

- Only teachers can access this endpoint.
- Uses aggregated learner analytics.
- Designed for teacher dashboards and platform insights.

---

### Error Response Format

All APIs return consistent JSON error responses.

##### Example

```json
{
  "error": "Unauthorized access"
}
```

---

### HTTP Status Conventions

| Status Code | Meaning |
|---|---|
| 200 | Successful GET request |
| 201 | Resource created successfully |
| 400 | Invalid request |
| 401 | Authentication required |
| 403 | Access forbidden |
| 404 | Resource not found |
| 500 | Internal server error |

## Authentication & Authorization

The backend uses JWT (JSON Web Token) based authentication.

Authenticated requests must include the JWT token in the HTTP Authorization header:

```http
Authorization: Bearer <jwt_token>
```

Tokens are generated during:
- user registration
- user login

The frontend is expected to:
- store the JWT token in local storage
- attach the token in HTTP headers for protected requests

Cookies are not used for authentication in this project.

---

## JWT Payload

The JWT payload example:

```json
{
  "sub": "1",
  "role": "learner"
}
```

### Fields

| Field | Description |
|---|---|
| sub | Authenticated user ID |
| role | User role (`learner` or `teacher`) |

The backend treats the JWT payload as the source of truth for:
- authenticated user identity
- authorization decisions

---

## Role-Based Access Control (RBAC)

The system supports two roles:

| Role | Description |
|---|---|
| learner | Standard learning user |
| teacher | Administrative/analytics user |

Authorization is enforced at the API layer using:
- JWT verification
- role validation
- ownership checks

---

## Access Rules

| Endpoint | Learner Access | Teacher Access |
|---|---|---|
| GET `/topics` | ✅ | ✅ |
| GET `/topics/graph` | ✅ | ✅ |
| GET `/learners/<id>/map` | self only | any learner |
| GET `/learners/<id>/activities` | self only | any learner |
| GET `/learners/<id>/recommendations` | self only | any learner |
| GET `/teacher/dashboard` | ❌ | ✅ |

---

## Authentication Notes

### Multiple Tokens

The backend does not explicitly invalidate previously issued JWT tokens.

However:
- the frontend stores only the latest token
- old tokens naturally expire
- no functional issue occurs for assignment scope

### Register While Authenticated

Authenticated users may still access:
- `POST /auth/register`
- `POST /auth/login`

This is acceptable because:
- duplicate email registration fails
- login simply returns a new valid token

### Token Expiration

JWT expiration is configured using Flask-JWT-Extended settings.

Expired tokens automatically become invalid and protected endpoints reject them with:

```json
{
  "msg": "Token has expired"
}
```
- currently jwt token is set to expire after 1 hour.
- refresh tokens are not implemented for this assignment.

## Recommendation & Analytics Logic

The backend dynamically generates learner recommendations and analytics using learner activity and proficiency data.

---

## Recommendation Logic

Topic recommendations are generated using prerequisite satisfaction rules.

A topic becomes recommendable only when:

```text
all prerequisite topics have proficiency >= 0.70
```

### Example

```text
Linear Algebra ──→ Machine Learning
Probability ─────→ Machine Learning
```

Machine Learning becomes recommendable only if:

| Prerequisite | Required Proficiency |
|---|---|
| Linear Algebra | ≥ 0.70 |
| Probability | ≥ 0.70 |

---

## Proficiency Calculation

Learner proficiency is derived from activity performance within a topic.

### Formula

```text
proficiency_score =
(sum of normalized activity scores)
/
(total activities in topic)
```

Where:

```text
normalized_score = activity_score / 100
```

### Example

| Activity | Score |
|---|---|
| Quiz | 80 |
| Coding | 90 |

```text
(0.8 + 0.9) / 2 = 0.85
```

Final proficiency:

```text
0.85
```

### Notes

- proficiency values range from `0.00` to `1.00`
- multiple activities per topic are supported
- activity scores are normalized uniformly across activity types

---

## Activity Analytics

The backend aggregates learner activity engagement by category:

- reading
- coding
- quiz
- discussion

Example:

```json
{
  ...
  "reading": 4,
  "coding": 2,
  "quiz": 5,
  "discussion": 1
}
```

---

## Activity Diversity Score

The learner analytics API computes an activity diversity score using normalized Shannon entropy.

The metric rewards:
- balanced engagement across activity types
- diverse learning behavior

The metric penalizes:
- highly skewed activity participation

### Properties

| Behavior | Diversity Score |
|---|---|
| only quizzes | low |
| balanced reading/coding/quiz usage | high |

The diversity score is normalized between:

```text
0 → low diversity
1 → high diversity
```

---

## Graph Traversal

The prerequisite graph is traversed using graph traversal algorithms implemented in the service layer.

Supported traversal operations include:
- prerequisite discovery
- recommendation eligibility checks

## Project Structure

```
backend/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── extensions.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── topic.py
│   │   ├── topic_prerequisite.py
│   │   ├── learner_topic_progress.py
│   │   ├── learning_activity.py
│   │   └── learner_activity.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth_routes.py
│   │   ├── learner_routes.py
│   │   ├── topic_routes.py
│   │   └── teacher_routes.py
│   │
│   ├── services/
|   |   ├── auth_service.py
│   │   ├── __init__.py
│   │   ├── graph_service.py
│   │   ├── proficiency_service.py
│   │   └──  recommendation_service.py
│   │   
│   │
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── auth_middleware.py
│   │   └── role_middleware.py
│   │
│   └── utils/
|        ├── jwt_utils.py
|        ├── auth_utils.py
│        └── __init__.py  
│
├── migrations/
│
├── requirements.txt
├── run.py
├── .env
├── .gitignore
└── README.md
```

## Seed Data

The backend includes realistic seed data to demonstrate:

- learner progression
- prerequisite unlocking
- recommendation generation
- graph traversal
- proficiency tracking

---

## Seeded Users

| Name | Role |
|---|---|
| Beginner Learner | learner |
| Intermediate Learner | learner |
| Advanced Learner | learner |
| Teacher User | teacher |

---

## Seeded Topic Graph

```text
Programming Basics
        ↓
Data Structures
        ↓
Algorithms
        ↓
Dynamic Programming


Discrete Mathematics
        ↓
Probability
        ↓
Machine Learning
        ↑
Linear Algebra
```

---

## Seeded Topics

| Topic | Difficulty |
|---|---|
| Programming Basics | beginner |
| Data Structures | beginner |
| Algorithms | intermediate |
| Dynamic Programming | advanced |
| Discrete Mathematics | beginner |
| Probability | intermediate |
| Linear Algebra | intermediate |
| Machine Learning | advanced |

---

## Seeded Learning Activities

The seed data includes:
- reading activities
- quizzes
- coding exercises
- multiple activities for the same topic

Example:

| Topic | Activity |
|---|---|
| Probability | Bayes Quiz 1 |
| Probability | Bayes Quiz 2 |
| Algorithms | Sorting Algorithms Quiz |
| Data Structures | Linked List Implementation |

---

## Seeded Learner States

### Beginner Learner
- completed only foundational topics

### Intermediate Learner
- partially progressed through programming path

### Advanced Learner
- high proficiency across multiple prerequisite chains

---

## Proficiency Generation

Proficiency values are derived from seeded learner activity scores.

```text
Seed Learner Activities
        ↓
Calculate Proficiency Scores
        ↓
Seed learner_topic_progress
```

### Formula

```text
proficiency_score =
(sum of normalized activity scores)
/
(total activities in topic)
```

---

## Current Limitation

`POST /activities` is intentionally not implemented for this task.

Currently:
- learner activities are seeded statically
- proficiency scores are generated during seeding
- recommendation logic operates on seeded learner state

## Running Locally

### 1. Clone Repository

```bash
git clone <repository_url>

cd backend
```

---

### 2. Create Virtual Environment

```bash
python3 -m venv venv
```

Activate virtual environment:

#### Linux / macOS

```bash
source venv/bin/activate
```

#### Windows

```bash
venv\Scripts\activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
FLASK_APP=run.py

SECRET_KEY=your_secret_key

JWT_SECRET_KEY=your_jwt_secret_key

DATABASE_URL=mysql+pymysql://<mysql_username>:<mysql_password>@localhost:3306/learning_navigator
```

---

### 5. Create Database

Inside MySQL:

```sql
CREATE DATABASE learning_navigator;
```

---

### 6. Run Database Migrations

```bash
flask db upgrade
```

---

### 7. Seed Database

```bash
python seed.py
```

This populates:
- users
- topics
- prerequisite graph
- learning activities
- learner activity history
- learner proficiency values

---

### 8. Start Development Server

```bash
flask run
```

Backend runs on:

```text
http://127.0.0.1:5000
```

---


## API Testing Using cURL

### Register User

```bash
curl -X POST http://127.0.0.1:5000/auth/register \
-H "Content-Type: application/json" \
-d '{
  "name": "Aditya",
  "email": "aditya@test.com",
  "password": "password123",
  "role": "learner"
}'
```

---

### Login User

```bash
curl -X POST http://127.0.0.1:5000/auth/login \
-H "Content-Type: application/json" \
-d '{
  "email": "aditya@test.com",
  "password": "password123"
}'
```

Copy the returned JWT token.

---

### Get Topics

```bash
curl http://127.0.0.1:5000/topics \
-H "Authorization: Bearer <jwt_token>"
```

---

### Get Topic Graph

```bash
curl http://127.0.0.1:5000/topics/graph \
-H "Authorization: Bearer <jwt_token>"
```

---

### Get Learner Map
- for this use token for a seeded learner as a new registered learner will not have the required seedings to get any response other than empty response.
- you can use the previous curl login url with one of these seeded emails (beginner@test.com, intermediate@test.com, advanced@test.com , teacher@test.com) as the email and 'password123' as the password to get a new jwt token and use that in the below curl commands.

```bash
curl http://127.0.0.1:5000/learners/1/map \
-H "Authorization: Bearer <jwt_token>"
```

---

### Get Learner Recommendations

```bash
curl http://127.0.0.1:5000/learners/1/recommendations \
-H "Authorization: Bearer <jwt_token>"
```

---

### Get Learner Activities

```bash
curl http://127.0.0.1:5000/learners/1/activities \
-H "Authorization: Bearer <jwt_token>"
```

---

### Get Teacher Dashboard

Requires teacher role token.
- use the curl login command with the email 'teacher@test.com' and password 'password123'

```bash
curl http://127.0.0.1:5000/teacher/dashboard \
-H "Authorization: Bearer <teacher_jwt_token>"
```

## Assumptions
- The prerequisite graph is assumed to be acyclic (DAG).
- Cycle validation is not enforced at the database layer for simplicity and assignment scope.




