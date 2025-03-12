# Application configuration settings

# API Configuration
API_BASE_URL = "http://localhost:5039/api"  # Replace with your ASP.NET backend URL

# API Endpoints
ENDPOINTS = {
    "login": "/auth/query/signin",
    "register": "/auth/command/signup",
    "user_profile": "/users/profile",
    "portfolio": "/portfolio",
    "stocks": "/stocks",
    "stock_details": "/stocks/{stock_id}",
    "transactions": "/transactions",
}

# UI Configuration
THEME = {
    "primary_color": "#4C6FFF",
    "secondary_color": "#5851DB",
    "background_color": "#F8F9FA",
    "text_color": "#333333",
    "error_color": "#FF5252",
    "success_color": "#4CAF50",
    "warning_color": "#FFC107",
    "border_color": "#EAEAEA",
}

# Default chart settings
CHART_SETTINGS = {
    "default_days": 30,
    "theme": "light",
}