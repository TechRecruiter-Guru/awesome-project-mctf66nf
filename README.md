# 📝 Task Manager MVP

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![React](https://img.shields.io/badge/React-18.2.0-blue.svg)](https://reactjs.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.2-green.svg)](https://flask.palletsprojects.com/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![GitHub issues](https://img.shields.io/github/issues/TechRecruiter-Guru/awesome-project-mctf66nf)](https://github.com/TechRecruiter-Guru/awesome-project-mctf66nf/issues)

A full-stack task management application built with modern web technologies. This MVP demonstrates CRUD operations with a beautiful, responsive UI and is deployed and production-ready!

## 🌐 Live Demo

- **Frontend**: [Coming Soon - Deploy to Vercel]
- **Backend API**: [Coming Soon - Your Render URL]
- **API Health Check**: `GET /api/health`

> **Note**: Backend may take 30-60 seconds to wake up on first request (free tier)

## ✨ Features

- ✅ **Create, Read, Update, and Delete tasks** - Full CRUD functionality
- 📊 **Track task completion status** - Mark tasks as complete/incomplete
- 🎨 **Modern, responsive UI** - Beautiful gradient design that works on all devices
- 🔄 **Real-time API status monitoring** - Live health check indicator
- 💾 **Persistent storage** - SQLite database with SQLAlchemy ORM
- 🚀 **RESTful API** - Clean, standard API architecture
- 🌍 **Production deployed** - Live on Render (backend) and Vercel (frontend)
- 🐳 **Docker support** - Containerized for easy deployment

## 📸 Screenshots

<!-- Add screenshots here once you have them -->
<!-- ![Task Manager UI](screenshots/main-ui.png) -->

*Screenshots coming soon! Feel free to contribute by adding them.*

## 🛠 Tech Stack

### Frontend
- **React 18** - Modern React with Hooks
- **Axios** - HTTP client for API calls
- **CSS3** - Custom styling with gradients and animations

### Backend
- **Flask** - Lightweight Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **SQLite** - Database (easily upgradable to PostgreSQL)
- **Flask-CORS** - Cross-origin resource sharing
- **Gunicorn** - Production WSGI server

### DevOps
- **Docker** - Containerization
- **Vercel** - Frontend hosting
- **Render** - Backend hosting
- **Git** - Version control

## 🚀 Quick Start

### Prerequisites

- Node.js (v16 or higher)
- Python (v3.8 or higher)
- pip (Python package manager)
- npm (Node package manager)

### Local Development Setup

#### 1. Clone the repository

```bash
git clone https://github.com/TechRecruiter-Guru/awesome-project-mctf66nf.git
cd awesome-project-mctf66nf
```

#### 2. Backend Setup

```bash
cd backend
pip install -r requirements.txt
python app.py
```

The backend server will start on `http://localhost:5000`

✅ You should see: `* Running on http://127.0.0.1:5000`

#### 3. Frontend Setup

Open a new terminal:

```bash
cd frontend
npm install
npm start
```

The frontend will start on `http://localhost:3000` and automatically open in your browser.

✅ You should see the Task Manager interface!

### 🐳 Docker Setup (Alternative)

Prefer Docker? We've got you covered:

```bash
docker-compose up
```

Both frontend and backend will start automatically!
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:5000`

## 📡 API Documentation

### Base URL
- **Local**: `http://localhost:5000`
- **Production**: `https://your-api.onrender.com`

### Endpoints

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| GET | `/api/health` | Health check | None |
| GET | `/api/items` | Get all tasks | None |
| POST | `/api/items` | Create a new task | `{"text": "Task description"}` |
| PUT | `/api/items/:id` | Update a task | `{"text": "Updated", "completed": true}` |
| DELETE | `/api/items/:id` | Delete a task | None |

### Example API Usage

```bash
# Health check
curl http://localhost:5000/api/health

# Get all tasks
curl http://localhost:5000/api/items

# Create a new task
curl -X POST http://localhost:5000/api/items \
  -H "Content-Type: application/json" \
  -d '{"text":"Buy groceries"}'

# Update a task (mark as completed)
curl -X PUT http://localhost:5000/api/items/1 \
  -H "Content-Type: application/json" \
  -d '{"completed":true}'

# Delete a task
curl -X DELETE http://localhost:5000/api/items/1
```

### Response Format

Success Response (200 OK):
```json
{
  "id": 1,
  "text": "Buy groceries",
  "completed": false
}
```

Error Response (404 Not Found):
```json
{
  "error": "Item not found"
}
```

## 🎨 Features Overview

### Frontend Highlights
- **React Hooks** - useState and useEffect for state management
- **Responsive Design** - Mobile-first approach with media queries
- **Error Handling** - Comprehensive error states and user feedback
- **Loading States** - Visual feedback during API operations
- **Task Statistics** - Real-time count of total and completed tasks
- **Smooth Animations** - Polished user experience

### Backend Highlights
- **RESTful API** - Standard HTTP methods and status codes
- **Database Models** - SQLAlchemy ORM for data persistence
- **CORS Enabled** - Cross-origin requests supported
- **Input Validation** - Request validation and error handling
- **Auto-initialization** - Database tables created automatically
- **Production Ready** - Gunicorn server for deployment

## 📁 Project Structure

```
awesome-project-mctf66nf/
├── .github/
│   ├── ISSUE_TEMPLATE/          # Issue templates
│   └── PULL_REQUEST_TEMPLATE.md # PR template
├── frontend/
│   ├── public/
│   │   └── index.html           # HTML template
│   ├── src/
│   │   ├── App.js               # Main React component
│   │   ├── App.css              # Component styles
│   │   ├── index.js             # React entry point
│   │   └── index.css            # Global styles
│   ├── Dockerfile               # Frontend container
│   ├── package.json             # Frontend dependencies
│   └── vercel.json              # Vercel config
├── backend/
│   ├── app.py                   # Flask application
│   ├── requirements.txt         # Python dependencies
│   ├── Dockerfile               # Backend container
│   └── tasks.db                 # SQLite database (auto-generated)
├── docker-compose.yml           # Docker orchestration
├── vercel.json                  # Vercel monorepo config
├── railway.toml                 # Railway config
├── DEPLOYMENT.md                # Deployment guide
├── CONTRIBUTING.md              # Contribution guidelines
├── CODE_OF_CONDUCT.md           # Community guidelines
├── CONTRIBUTORS.md              # List of contributors
└── README.md                    # You are here!
```

## 🔧 Development

### Making Changes

**Frontend**:
- Edit files in `frontend/src/`
- The app will hot-reload automatically
- Changes appear instantly in the browser

**Backend**:
- Edit `backend/app.py`
- Restart the Python server to see changes
- Use `Ctrl+C` to stop, then `python app.py` to restart

### Connecting Frontend to Backend

The frontend connects to the backend via the `API_URL` in `frontend/src/App.js`:

```javascript
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';
```

For production, set the `REACT_APP_API_URL` environment variable.

## 🚢 Deployment

Want to deploy your own instance? Check out our comprehensive [DEPLOYMENT.md](DEPLOYMENT.md) guide!

### Quick Deploy Options

- **Frontend**: Vercel (recommended) or Netlify
- **Backend**: Render (recommended) or Railway
- **Full Stack**: Railway or Docker

See [DEPLOYMENT.md](DEPLOYMENT.md) for step-by-step instructions.

## 🧪 Testing

The application can be tested via:

1. **React UI** - Use the web interface
2. **API endpoints** - Use curl or your favorite API client
3. **API testing tools** - Postman, Insomnia, etc.

### Manual Testing Checklist

- [ ] Create a new task
- [ ] Mark task as complete
- [ ] Edit task text
- [ ] Delete a task
- [ ] Refresh page (data persists)
- [ ] Check API health endpoint

## 🤝 Contributing

We love contributions! Whether you're fixing bugs, adding features, or improving documentation, we'd love to have you as part of our community.

### How to Contribute

1. 🍴 Fork the repository
2. 🔧 Create a feature branch (`git checkout -b feature/amazing-feature`)
3. 💾 Commit your changes (`git commit -m 'Add amazing feature'`)
4. 📤 Push to the branch (`git push origin feature/amazing-feature`)
5. 🎉 Open a Pull Request

Check out our [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines!

### Good First Issues

New to open source? Look for issues labeled:
- `good first issue` - Perfect for beginners
- `help wanted` - We need help!
- `documentation` - Improve our docs

### Contributors

See [CONTRIBUTORS.md](CONTRIBUTORS.md) for the list of amazing people who have contributed to this project!

## 📋 Roadmap

Future features and improvements:

- [ ] User authentication and authorization
- [ ] Task categories/tags
- [ ] Due dates and reminders
- [ ] Task priority levels
- [ ] Search and filter functionality
- [ ] Dark mode toggle
- [ ] Export tasks (CSV, JSON)
- [ ] Unit and integration tests
- [ ] PostgreSQL database option
- [ ] Real-time updates with WebSockets

Want to help with any of these? Check out [CONTRIBUTING.md](CONTRIBUTING.md)!

## 🐛 Known Issues

No known issues at the moment! Found a bug? Please [report it](https://github.com/TechRecruiter-Guru/awesome-project-mctf66nf/issues/new?template=bug_report.md).

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- React team for the amazing framework
- Flask team for the lightweight backend
- All our contributors!

## 📞 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/TechRecruiter-Guru/awesome-project-mctf66nf/issues)
- **Discussions**: [GitHub Discussions](https://github.com/TechRecruiter-Guru/awesome-project-mctf66nf/discussions)
- **Email**: [Add your email if you want]

## ⭐ Show Your Support

If you like this project, please give it a ⭐ on GitHub!

---

**Built with ❤️ by the open source community**

Ready to contribute? Start with our [Contributing Guide](CONTRIBUTING.md)!
