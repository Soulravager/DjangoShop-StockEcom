# 🛍️ Basic Django E-commerce Framework

A lightweight e-commerce platform built with Django that supports product management, order tracking, user reviews, search, and a customizable UI.

---

## 🚀 Key Features

- 🛒 Add, remove, and update products  
- 📦 Order tracking (Pending, Shipped, Delivered, Cancelled)  
- ❤️ Wishlist / Favorites  
- ⭐ Product reviews and 1–5 star ratings  
- 🔍 Keyword and category-based product search  
- 🎨 Easily customizable front-end UI  

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository_url>
cd <project_directory>
```

### 2. Set Up a Virtual Environment

- **macOS/Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

- **Windows:**
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a Superuser
```bash
python manage.py createsuperuser
```
Follow the prompts to set up admin login credentials.

### 6. Run the Development Server
```bash
python manage.py runserver
```
Open your browser and go to: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🔑 Admin Dashboard

Visit: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)  
Log in using your superuser credentials to manage:

- Products  
- Orders  
- Users  
- Reviews  

---

## 🧩 Feature Breakdown

| Feature               | Description                                                                 |
|-----------------------|-----------------------------------------------------------------------------|
| Product Management    | Admins can add, edit, or delete products from the catalog.                  |
| Order Tracking        | Users can see the status of their orders in real-time.                      |
| Wishlist / Favorites  | Save products for quick access and later purchase.                          |
| Ratings & Reviews     | Users can submit reviews and 1–5 star ratings for products.                 |
| Product Search        | Search by product name, description, or category.                           |
| UI Customization      | Easy to style with CSS or frontend frameworks (Bootstrap, Tailwind, etc.). |

---

## 📂 Folder Structure (Simplified)
```
project_directory/
│
├── app/                  # Main Django app
├── templates/            # HTML templates
├── static/               # Static assets (CSS/JS)
├── db.sqlite3            # Default SQLite database
├── manage.py             # Django project manager
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

