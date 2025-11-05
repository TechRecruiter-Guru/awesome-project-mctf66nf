# Contributing to Task Manager MVP

First off, thank you for considering contributing to Task Manager MVP! It's people like you that make this project a great tool for everyone.

## 🎯 How Can I Contribute?

There are many ways you can contribute to this project:

- 🐛 **Report bugs** - Found a bug? Let us know!
- 💡 **Suggest features** - Have an idea? We'd love to hear it!
- 📝 **Improve documentation** - Help make our docs clearer
- 💻 **Write code** - Fix bugs or implement new features
- 🎨 **Design improvements** - Make the UI/UX better
- ✅ **Write tests** - Help us improve code quality

## 🚀 Getting Started

### Prerequisites

Make sure you have:
- Node.js (v16+)
- Python (v3.8+)
- Git
- A GitHub account

### Setup Your Development Environment

1. **Fork the repository**
   - Click the "Fork" button at the top right of this repository

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR-USERNAME/awesome-project-mctf66nf.git
   cd awesome-project-mctf66nf
   ```

3. **Add upstream remote**
   ```bash
   git remote add upstream https://github.com/ORIGINAL-OWNER/awesome-project-mctf66nf.git
   ```

4. **Install dependencies**

   Backend:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

   Frontend:
   ```bash
   cd frontend
   npm install
   ```

5. **Run the application**

   Backend (in one terminal):
   ```bash
   cd backend
   python app.py
   ```

   Frontend (in another terminal):
   ```bash
   cd frontend
   npm start
   ```

## 🔄 Making Changes

### 1. Create a Branch

Always create a new branch for your work:

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring
- `test/` - Adding or updating tests

### 2. Make Your Changes

- Write clear, concise code
- Follow the existing code style
- Comment your code when necessary
- Test your changes thoroughly

### 3. Commit Your Changes

Write meaningful commit messages:

```bash
git add .
git commit -m "Add feature: brief description of what you did"
```

Good commit message examples:
- ✅ `Add dark mode toggle to settings`
- ✅ `Fix: Resolve API timeout error on slow connections`
- ✅ `Docs: Update installation instructions for Windows`
- ❌ `Update stuff`
- ❌ `Fix bug`

### 4. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 5. Create a Pull Request

1. Go to your fork on GitHub
2. Click "New Pull Request"
3. Select your branch
4. Fill out the PR template
5. Click "Create Pull Request"

## 📋 Pull Request Guidelines

### Before Submitting

- [ ] Code runs without errors
- [ ] Tested on both frontend and backend (if applicable)
- [ ] Code follows existing style
- [ ] Commit messages are clear
- [ ] Documentation updated (if needed)

### PR Description

Your PR should include:

1. **What** - What does this PR do?
2. **Why** - Why is this change needed?
3. **How** - How did you implement it?
4. **Screenshots** - If UI changes, include before/after screenshots
5. **Testing** - How did you test this?

## 🐛 Reporting Bugs

### Before Submitting a Bug Report

- Check if the bug has already been reported in [Issues](../../issues)
- Try the latest version - the bug might already be fixed
- Collect information about the bug:
  - What were you trying to do?
  - What did you expect to happen?
  - What actually happened?
  - Steps to reproduce

### Bug Report Template

Use the bug report issue template and include:

1. **Description** - Clear description of the bug
2. **Steps to Reproduce** - Step-by-step instructions
3. **Expected Behavior** - What should happen
4. **Actual Behavior** - What actually happens
5. **Screenshots** - If applicable
6. **Environment**:
   - OS: [e.g., Windows 10, macOS 12, Ubuntu 20.04]
   - Browser: [e.g., Chrome 96, Firefox 95]
   - Node version: [e.g., 16.3.0]
   - Python version: [e.g., 3.9.0]

## 💡 Suggesting Features

We love new ideas! Before suggesting a feature:

1. Check if it's already been suggested in [Issues](../../issues)
2. Make sure it aligns with the project goals
3. Consider if it would benefit most users

### Feature Request Template

Use the feature request issue template and include:

1. **Problem** - What problem does this solve?
2. **Solution** - Your proposed solution
3. **Alternatives** - Alternative solutions you considered
4. **Additional Context** - Screenshots, mockups, examples

## 🎨 Code Style Guidelines

### JavaScript/React

- Use functional components with hooks
- Use meaningful variable names
- Keep components small and focused
- Use ES6+ features
- Format with Prettier (if configured)

Example:
```javascript
// ✅ Good
const [tasks, setTasks] = useState([]);

const handleDeleteTask = async (id) => {
  try {
    await axios.delete(`${API_URL}/api/items/${id}`);
    setTasks(tasks.filter(task => task.id !== id));
  } catch (error) {
    console.error('Error deleting task:', error);
  }
};

// ❌ Avoid
const [x, setX] = useState([]);
const f = (i) => { /* code */ };
```

### Python/Flask

- Follow PEP 8 style guide
- Use descriptive function names
- Add docstrings to functions
- Handle errors gracefully

Example:
```python
# ✅ Good
@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Delete a task by ID."""
    try:
        item = Item.query.get(item_id)
        if not item:
            return jsonify({'error': 'Item not found'}), 404

        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Item deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ❌ Avoid
@app.route('/api/items/<int:id>', methods=['DELETE'])
def d(id):
    i = Item.query.get(id)
    db.session.delete(i)
    db.session.commit()
    return jsonify({'msg': 'ok'})
```

## 🏷️ Good First Issues

New to open source? Look for issues labeled:
- `good first issue` - Perfect for beginners
- `help wanted` - We need help with these!
- `documentation` - Improve our docs

## 🤝 Code of Conduct

This project follows a Code of Conduct. By participating, you agree to uphold this code. Please report unacceptable behavior.

## 💬 Questions?

Have questions? Feel free to:
- Open a [Discussion](../../discussions)
- Create an issue with the `question` label
- Reach out to the maintainers

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## ⭐ Recognition

All contributors will be added to [CONTRIBUTORS.md](CONTRIBUTORS.md) and recognized in release notes!

Thank you for contributing! 🎉
