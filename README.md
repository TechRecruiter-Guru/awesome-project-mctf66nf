# awesome-project-mctf66nf

## 📝 Task Manager MVP

A full-stack task management application built with modern web technologies. This MVP demonstrates CRUD operations with a beautiful, responsive UI.

## ✨ Features

- ✅ Create, Read, Update, and Delete tasks
- 📊 Track task completion status
- 🎨 Modern, responsive UI with gradient design
- 🔄 Real-time API status monitoring
- 💾 Persistent SQLite database storage
- 🚀 RESTful API architecture

## 🛠 Tech Stack

- **Frontend**: React 18 with Hooks
- **Backend**: Flask with SQLAlchemy
- **Database**: SQLite
- **Styling**: Custom CSS with modern design patterns
- **HTTP Client**: Axios

## 📋 Prerequisites

- Node.js (v16 or higher)
- Python (v3.8 or higher)
- pip (Python package manager)
- npm (Node package manager)

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd awesome-project-mctf66nf
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
python app.py
```

The backend server will start on `http://localhost:5000`

### 3. Frontend Setup
Open a new terminal:
```bash
cd frontend
npm install
npm start
```

The frontend will start on `http://localhost:3000` and automatically open in your browser.

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check endpoint |
| GET | `/api/items` | Get all tasks |
| POST | `/api/items` | Create a new task |
| PUT | `/api/items/:id` | Update a task |
| DELETE | `/api/items/:id` | Delete a task |

### Example API Usage

```bash
# Get all items
curl http://localhost:5000/api/items

# Create a new item
curl -X POST http://localhost:5000/api/items \
  -H "Content-Type: application/json" \
  -d '{"text":"My new task"}'

# Update an item (mark as completed)
curl -X PUT http://localhost:5000/api/items/1 \
  -H "Content-Type: application/json" \
  -d '{"completed":true}'

# Delete an item
curl -X DELETE http://localhost:5000/api/items/1
```

## 🎨 Features Overview

### Frontend
- **React Hooks**: Uses useState and useEffect for state management
- **Responsive Design**: Mobile-first approach with media queries
- **Error Handling**: Comprehensive error states and user feedback
- **Loading States**: Visual feedback during API operations
- **Task Statistics**: Real-time count of total and completed tasks

### Backend
- **RESTful API**: Standard HTTP methods and status codes
- **Database Models**: SQLAlchemy ORM for data persistence
- **CORS Enabled**: Cross-origin requests supported
- **Input Validation**: Request validation and error handling
- **Auto-initialization**: Database tables created automatically

## 🔧 Development

### Project Structure
```
awesome-project-mctf66nf/
├── frontend/
│   ├── public/
│   │   └── index.html
│   └── src/
│       ├── App.js          # Main React component
│       ├── App.css         # Component styles
│       ├── index.js        # React entry point
│       ├── index.css       # Global styles
│       └── package.json    # Frontend dependencies
├── backend/
│   ├── app.py             # Flask application
│   ├── requirements.txt   # Python dependencies
│   └── tasks.db           # SQLite database (auto-generated)
└── README.md
```

### Making Changes

**Frontend**: Edit files in `frontend/src/` - the app will hot-reload automatically.

**Backend**: Edit `backend/app.py` - restart the Python server to see changes.

## 🐳 Docker Support

Docker configuration files are included:
- `docker-compose.yml` - Orchestrates both services
- `frontend/Dockerfile` - Frontend container
- `backend/Dockerfile` - Backend container

## 🧪 Testing

The backend includes full CRUD functionality that can be tested via:
1. The React UI
2. API endpoints directly with curl
3. API testing tools like Postman

## 📝 License

MIT License

---

Built with ❤️ as an MVP demonstration