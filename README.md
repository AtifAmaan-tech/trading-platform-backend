A Flask-based REST API providing authentication, trading operations, and portfolio management.

### Features

- **User Authentication**: Secure session-based authentication with login/signup/logout.
- **Trading Operations**: Buy/sell cryptocurrencies with real-time price data.
- **Portfolio Management**: Track balances, assets, and transaction history.
- **Database Integration**: PostgreSQL with SQLAlchemy ORM.

### Tech Stack

- **Framework**: [Flask](https://flask.palletsprojects.com/)
- **Language**: Python
- **Database**: PostgreSQL 
- **Authentication**: Flask-Session with cookie-based sessions

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/register` | POST | Create new user account |
| `/login` | POST | Authenticate user |
| `/logout` | POST | End user session |
| `/auth-status` | GET | Check authentication status |
| `/balance` | GET | Get user's USDT balance |
| `/total-balance` | GET | Get total portfolio value |
| `/get_tokens_qty` | GET | Get all token holdings |
| `/create-transaction` | POST | Execute a trade |

### Getting Started

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/AtifAmaan-tech/trading-platform-backend.git
    cd trading-platform-backend
    ```

2.  **Create virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Environment Setup**:
    Create a `.env` file with your database credentials:
    ```env
    DATABASE_URL=postgresql://username:password@localhost:5432/tradex
    SECRET_KEY=your-secret-key
    ```

5.  **Run the Server**:
    ```bash
    python app.py
    ```

    The API will be available at `http://127.0.0.1:5000`.

---

## Full Stack Setup

To run the complete application:

1. Start the **backend** server (runs on port 5000)
2. Start the **frontend** dev server (runs on port 5173)
3. Ensure the frontend `.env` points to the backend URL

---

## License

MIT License - feel free to use this project for learning and development.
