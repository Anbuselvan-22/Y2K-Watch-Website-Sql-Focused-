# 🚀 Y2K Watch E-commerce - How to Run the Application

## 📋 Prerequisites

Before running the app, make sure you have:
- ✅ Python 3.x installed
- ✅ MySQL server running
- ✅ Virtual environment activated (optional but recommended)

---

## 🎯 Quick Start (Simple Method)

### **Step 1: Navigate to the project directory**
```bash
cd login-system
```

### **Step 2: Run the application**
```bash
python app.py
```

### **Step 3: Open in browser**
```
http://127.0.0.1:8000
```

---

## 📦 Complete Setup (First Time)

### **1. Install Dependencies**
```bash
cd login-system
pip install -r requirements.txt
```

### **2. Verify MySQL is Running**
```bash
# Check if MySQL is running
mysql -u root -p
# Press Enter for password (it's empty)
# Type: EXIT; to quit
```

### **3. Initialize Database (Automatic)**
The database will be created automatically when you run the app for the first time.

### **4. Run the Application**
```bash
python app.py
```

You should see:
```
* Serving Flask app 'app'
* Debug mode: on
* Running on http://127.0.0.1:8000
```

---

## 🔧 Alternative Running Methods

### **Method 1: Direct Python**
```bash
cd login-system
python app.py
```

### **Method 2: Using Python Module**
```bash
cd login-system
python -m flask run --host=0.0.0.0 --port=8000
```

### **Method 3: With Virtual Environment**
```bash
# Activate virtual environment first
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate  # On Windows

# Then run
cd login-system
python app.py
```

### **Method 4: Background Process**
```bash
cd login-system
nohup python app.py > app.log 2>&1 &
```

---

## 🌐 Access the Application

Once running, open your browser and go to:

- **Main URL**: `http://127.0.0.1:8000`
- **Alternative**: `http://localhost:8000`
- **Network Access**: `http://YOUR_IP:8000` (check terminal output for your IP)

---

## 🔑 Test Login Credentials

**Username**: `testuser`  
**Password**: `testpass`

Or create a new account using the Register page.

---

## 🛠️ Useful Commands

### **Check if App is Running**
```bash
lsof -ti:8000
```

### **Stop the Application**
```bash
# If running in terminal: Press Ctrl+C

# If running in background:
lsof -ti:8000 | xargs kill -9
```

### **Restart the Application**
```bash
# Stop first
lsof -ti:8000 | xargs kill -9

# Then start
cd login-system
python app.py
```

### **View Application Logs**
```bash
# If running in terminal, logs appear directly

# If running in background:
tail -f app.log
```

---

## 🗄️ Database Management

### **View Database Tables**
```bash
cd login-system
python show_tables.py
```

### **Create Test User**
```bash
cd login-system
python create_test_user.py
```

### **Create Sample Orders**
```bash
cd login-system
python create_sample_orders.py
```

### **Update Stock Levels**
```bash
cd login-system
python check_stock.py
```

---

## 📱 Application Features

Once running, you can access:

- **Home Page** (`/home`) - Hero section with watch collections
- **Products** (`/products`) - Browse all watches with filters
- **Cart** (`/cart`) - View shopping cart
- **Wishlist** (`/wishlist`) - Saved favorite items
- **Checkout** (`/checkout`) - Complete purchase
- **About** (`/about`) - Company information
- **Contact** (`/contact`) - Contact form

---

## 🐛 Troubleshooting

### **Problem: Port 8000 already in use**
```bash
# Find and kill the process
lsof -ti:8000 | xargs kill -9

# Or change port in app.py (line at bottom):
# app.run(debug=True, host='0.0.0.0', port=5000)
```

### **Problem: MySQL connection error**
```bash
# Check if MySQL is running
mysql -u root

# If not running, start MySQL:
# macOS: brew services start mysql
# Linux: sudo systemctl start mysql
# Windows: Start MySQL service from Services
```

### **Problem: Module not found**
```bash
# Install missing dependencies
pip install flask pymysql werkzeug
```

### **Problem: Database doesn't exist**
```bash
# The app creates it automatically, but you can create manually:
mysql -u root -e "CREATE DATABASE IF NOT EXISTS login_db;"
```

---

## 🔄 Development Workflow

### **1. Start Development**
```bash
cd login-system
python app.py
```

### **2. Make Changes**
- Edit files in your code editor
- Flask auto-reloads when files change (debug mode)

### **3. Test Changes**
- Refresh browser to see changes
- Check terminal for errors

### **4. Stop Development**
- Press `Ctrl+C` in terminal

---

## 📊 Quick Status Check

Run this to check everything:
```bash
# Check Python
python --version

# Check MySQL
mysql -u root -e "SELECT VERSION();"

# Check if port is free
lsof -ti:8000 || echo "Port 8000 is available"

# Check dependencies
pip list | grep -E "Flask|pymysql"
```

---

## 🎯 Production Deployment (Optional)

For production, use a proper WSGI server:

### **Using Gunicorn**
```bash
pip install gunicorn
cd login-system
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### **Using uWSGI**
```bash
pip install uwsgi
cd login-system
uwsgi --http 0.0.0.0:8000 --wsgi-file app.py --callable app
```

---

## 📝 Environment Variables (Optional)

Create a `.env` file for configuration:
```bash
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=1
DATABASE_HOST=localhost
DATABASE_USER=root
DATABASE_PASSWORD=
DATABASE_NAME=login_db
PORT=8000
```

---

## 🎉 Success!

If you see this in your terminal:
```
* Running on http://127.0.0.1:8000
* Running on http://YOUR_IP:8000
```

**Your app is running successfully!** 🚀

Open `http://127.0.0.1:8000` in your browser and start shopping!

---

## 📞 Need Help?

- Check the terminal for error messages
- Review `MYSQL_TERMINAL_GUIDE.md` for database queries
- Check `mysql_queries.sql` for SQL examples
- Ensure MySQL is running and accessible

---

**Happy Shopping! 🛍️**
