# SAWA Troubleshooting Guide

## Quick Start (No Database Required)

If you're having trouble accessing the documentation, try the simplified version first:

```bash
# Install minimal dependencies
pip install fastapi uvicorn

# Run the simple test server
python test_simple.py
```

Then visit: http://localhost:8000/docs

## Common Issues and Solutions

### 1. "Failed to access documentation"

**Problem**: Can't access http://localhost:8000/docs

**Solutions**:
1. **Check if the server is running**:
   ```bash
   # Look for output like:
   # INFO:     Uvicorn running on http://0.0.0.0:8000
   ```

2. **Try the simple version first**:
   ```bash
   python test_simple.py
   ```

3. **Check port availability**:
   ```bash
   # On macOS/Linux
   lsof -i :8000
   
   # On Windows
   netstat -ano | findstr :8000
   ```

4. **Try a different port**:
   ```bash
   uvicorn app.main_simple:app --port 8001
   ```

### 2. Import Errors

**Problem**: `ModuleNotFoundError` or import errors

**Solutions**:
1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Check Python version** (requires 3.8+):
   ```bash
   python --version
   ```

3. **Use virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

### 3. Database Connection Issues

**Problem**: Database-related errors

**Solutions**:
1. **Use the simple version** (no database required):
   ```bash
   python test_simple.py
   ```

2. **Set up SQLite** (easier than PostgreSQL):
   ```bash
   # Edit .env file
   DATABASE_URL=sqlite:///./sawa.db
   ```

3. **Skip database setup** for testing:
   - Use `app/main_simple.py` instead of `app/main.py`

### 4. OpenAI API Issues

**Problem**: OpenAI-related errors

**Solutions**:
1. **The app works without OpenAI** - it will use rule-based analysis
2. **Add your API key** to `.env`:
   ```
   OPENAI_API_KEY=your_key_here
   ```

### 5. Permission Errors

**Problem**: Permission denied errors

**Solutions**:
1. **Check file permissions**:
   ```bash
   chmod +x run_server.py
   chmod +x test_simple.py
   ```

2. **Run with proper permissions**:
   ```bash
   python test_simple.py
   ```

## Step-by-Step Testing

### Step 1: Test Basic Installation
```bash
python -c "import fastapi; print('FastAPI installed successfully')"
```

### Step 2: Test Simple Server
```bash
python test_simple.py
```

### Step 3: Test Documentation Access
1. Open browser
2. Go to http://localhost:8000/docs
3. You should see the FastAPI documentation interface

### Step 4: Test API Endpoints
```bash
# Test root endpoint
curl http://localhost:8000/

# Test health endpoint
curl http://localhost:8000/health

# Test prompts endpoint
curl http://localhost:8000/api/prompts/
```

## Alternative Setup Methods

### Method 1: Docker (Recommended)
```bash
# If you have Docker installed
docker-compose up
```

### Method 2: Minimal Installation
```bash
pip install fastapi uvicorn
python test_simple.py
```

### Method 3: Full Setup
```bash
# Run the setup script
python setup.py

# Then run the server
python run_server.py
```

## Getting Help

### Check Server Logs
Look for error messages in the terminal where you started the server.

### Test Individual Components
```bash
# Test imports
python -c "from app.main_simple import app; print('App imported successfully')"

# Test FastAPI
python -c "import fastapi; print(f'FastAPI version: {fastapi.__version__}')"
```

### Common Error Messages

1. **"Address already in use"**:
   - Port 8000 is busy, try port 8001
   - Kill the process using port 8000

2. **"No module named 'app'"**:
   - Make sure you're in the correct directory
   - Check your Python path

3. **"Connection refused"**:
   - Server isn't running
   - Check if the server started successfully

## Success Indicators

You'll know it's working when:
- ✅ Server starts without errors
- ✅ You can access http://localhost:8000/docs
- ✅ You see the FastAPI documentation interface
- ✅ You can test API endpoints

## Next Steps

Once the simple version works:
1. Try the full version with database
2. Add your OpenAI API key
3. Set up PostgreSQL for production use
4. Customize prompts and feedback

## Still Having Issues?

1. **Check the logs** in your terminal
2. **Try the simple version** first
3. **Verify your Python version** (3.8+)
4. **Check your internet connection** (for pip installs)
5. **Try a different port** if 8000 is busy
