# Y2K Luxury Watch Store 🕐

A modern, minimalist e-commerce web application for luxury watches built with Flask and featuring a sleek black and white design aesthetic.

## 🌟 Features

### 🔐 User Authentication
- Secure user registration and login system
- Password hashing with Werkzeug security
- Session management for user state
- Protected routes requiring authentication

### 🛍️ E-commerce Functionality
- **Product Catalog**: Browse luxury watch collections
- **Shopping Cart**: Add/remove items with AJAX functionality
- **Checkout System**: Complete order processing
- **Order Management**: Order confirmation and success pages
- **Real-time Notifications**: Custom popup notifications for cart actions

### 🎨 Design & UI/UX
- **Monochromatic Theme**: Sophisticated black and white design
- **Responsive Design**: Optimized for desktop, tablet, and mobile
- **Mobile-First Navigation**: Burger menu for mobile and tablet screens
- **Smooth Animations**: CSS transitions and hover effects
- **Professional Typography**: Playfair Display and Roboto fonts

### 📱 Responsive Features
- Adaptive hero images for all screen sizes
- Mobile-optimized burger menu navigation
- Responsive product grid layout
- Touch-friendly interface elements

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Database**: MySQL with PyMySQL connector
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Styling**: Custom CSS with CSS Grid and Flexbox
- **Icons**: Font Awesome 6
- **Security**: Werkzeug password hashing

## 📁 Project Structure

```
login-system/
├── app.py                 # Main Flask application
├── static/
│   ├── css/
│   │   └── style.css     # Main stylesheet
│   └── images/           # Product and UI images
├── templates/
│   ├── base.html         # Base template
│   ├── index.html        # Homepage
│   ├── products.html     # Product catalog
│   ├── cart.html         # Shopping cart
│   ├── checkout.html     # Checkout page
│   ├── order_success.html # Order confirmation
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   ├── about.html        # About page
│   └── contact.html      # Contact page
└── requirements.txt      # Python dependencies
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7+
- MySQL Server
- pip (Python package manager)

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/y2k-luxury-watches.git
cd y2k-luxury-watches
```

### 2. Create Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r login-system/requirements.txt
```

### 4. Database Setup
```bash
# Create MySQL database
mysql -u root -p
CREATE DATABASE login_db;
exit
```

### 5. Configure Database Connection
Update the database connection settings in `login-system/app.py`:
```python
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='your_username',
        password='your_password',
        database='login_db',
        cursorclass=pymysql.cursors.DictCursor
    )
```

### 6. Run the Application
```bash
cd login-system
python app.py
```

The application will be available at `http://localhost:5000`

## 📊 Database Schema

The application uses the following database tables:

- **users**: User authentication data
- **products**: Product catalog information
- **cart**: Shopping cart items
- **orders**: Order records
- **order_items**: Individual order line items

Tables are automatically created when the application starts.

## 🎯 Key Features Explained

### Responsive Navigation
- **Desktop (>992px)**: Horizontal navigation bar
- **Tablet (768px-992px)**: Burger menu with 60% width overlay
- **Mobile (≤768px)**: Full-screen burger menu

### Cart Notifications
- AJAX-powered add-to-cart functionality
- Custom popup notifications with product names
- Auto-hide after 4 seconds with manual close option
- Error handling for failed requests

### Image Optimization
- Responsive hero images that scale with screen size
- Grayscale filters with color reveal on hover
- Optimized loading for different viewport sizes

## 🔧 Customization

### Adding New Products
Products are automatically seeded when the application starts. To add new products:

1. Add images to `login-system/static/images/`
2. Update the product data in `app.py` in the `init_db()` function
3. Restart the application

### Styling Modifications
The main stylesheet is located at `login-system/static/css/style.css`. Key CSS variables:

```css
:root {
    --black: #0e0e0e;
    --white: #f9f9f9;
    --gray-dark: #1c1c1c;
    --gray-light: #b5b5b5;
    --border: rgba(255, 255, 255, 0.15);
}
```

## 📱 Browser Support

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+
- Mobile browsers (iOS Safari, Chrome Mobile)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Font Awesome for icons
- Google Fonts for typography
- Unsplash for placeholder images
- Flask community for excellent documentation

## 📞 Contact

- **Project Link**: [https://github.com/yourusername/y2k-luxury-watches](https://github.com/yourusername/y2k-luxury-watches)
- **Demo**: [Live Demo Link](https://your-demo-link.com)

---

⭐ **Star this repository if you found it helpful!**