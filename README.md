# Basic Django Framework for E-commerce Site

## Features:
1. Add, remove, and modify products.
2. Order tracking.
3. Wishlist/Favorites.
4. Reviews and ratings.
5. Search functionality for products.
6. Customize UI.

# Installation and Setup

# 1. Clone the Repository
# Clone the repository to your local machine (if not already done).
# Replace <repository_url> with the actual URL of your repository.
git clone <repository_url>
cd <project_directory>

# 2. Set up a Virtual Environment
# For macOS/Linux:
python3 -m venv venv
source venv/bin/activate

# For Windows:
python -m venv venv
venv\Scripts\activate

# 3. Install Dependencies
# Install the required Python packages listed in the requirements.txt file.
pip install -r requirements.txt

# 4. Set Up the Database
# Run migrations to set up the database.
python manage.py makemigrations
python manage.py migrate

# 5. Create a Superuser
# To create a superuser for accessing the admin dashboard.
python manage.py createsuperuser
# Follow the prompts to create the superuser.

# 6. Run the Development Server
# Start the development server.
python manage.py runserver
# The site will be accessible at http://127.0.0.1:8000/.

# 7. Admin Dashboard
# Log in at http://127.0.0.1:8000/admin/ using the superuser credentials
# to manage products, orders, and other site features.

# Features Breakdown:
# - Add/Remove/Modify Products: Admin users can add new products, modify existing products, and remove products.
# - Order Tracking: Track orders by their status (e.g., Pending, Shipped, Delivered, Cancelled).
# - Wishlist/Favorites: Users can save products to their wishlist for easy access later.
# - Reviews and Ratings: Users can rate and review products with a 1 to 5 star system.
# - Search Functionality for Products: Users can search for products based on keywords or categories.
# - Customize UI: The site’s user interface is customizable to match the desired design.
