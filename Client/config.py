# Application configuration settings

# API Configuration
API_BASE_URL = "http://localhost:5039/api"  # Replace with your ASP.NET backend URL

# API Endpoints
ENDPOINTS = {
    "signin": "/auth/query/signin",
    "signup": "/auth/command/signup",

    "holdings": "/trading/query/holdings/{user_id}",
    "transactions": "/trading/query/trades/{user_id}",
    "cash_balance": "/trading/query/cashbalance/{user_id}",


    "stock_details": "/transaction/query/getDetails",

    "buy_stock": "/transaction/command/buy",
    "sell_stock": "/transaction/command/sell",
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
