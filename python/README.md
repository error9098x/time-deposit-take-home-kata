# Time Deposit Refactoring Kata

This project implements a REST API for managing time deposits, built with Python, FastAPI, and SQLAlchemy. It is a refactored solution based on an initial domain model, focusing on clean architecture, robustness, and maintainability.

## How to Run

1.  **Set up a virtual environment:**
    ```sh
    python3 -m venv .venv
    source .venv/bin/activate
    ```

2.  **Install dependencies:**
    ```sh
    pip install -r python/requirements.txt
    ```

3.  **Seed the database with initial data:**
    The application uses a local SQLite database (`python/data/time_deposits.db`).
    ```sh
    cd python && python -m app.scripts.seed
    ```

4.  **Run the API server:**
    ```sh
    uvicorn app.main:app --reload
    ```

5.  **Access the API:**
    - The API will be available at `http://127.0.0.1:8000`.
    - Interactive documentation (Swagger UI) is available at `http://127.0.0.1:8000/docs`.

## API Endpoints

- `GET /time-deposits`: Retrieves a list of all time deposits and their withdrawals.
- `POST /time-deposits/update-balances`: Calculates interest for all deposits, updates their balances, and returns the updated list.

## Project Structure and Design Decisions

This solution is structured following the principles of **Clean Architecture** to ensure separation of concerns, testability, and maintainability.

- **Domain Layer (`app/domain`):** Contains the core business logic. The original `TimeDeposit` class and `TimeDepositCalculator` are preserved here, as per the assignment constraints. This layer has no dependencies on any other layer.

- **Application Layer (`app/application`):** Contains the application-specific use cases. It orchestrates the flow of data between the domain and infrastructure layers.

- **Infrastructure Layer (`app/infrastructure`):** Contains the implementation details for external concerns like the database. It includes SQLAlchemy models and the **Repository Pattern**, which abstracts data access from the rest of the application.

- **API Layer (`app/api`):** The entry point to the application, built with FastAPI. It handles HTTP requests, data validation (using Pydantic schemas), and serialization.

### Key Technical Decisions

1.  **Data Integrity:** All monetary values are handled using Python's `Decimal` type within the database and API layers to prevent floating-point precision errors. Conversion to `float` happens only at the boundary when interacting with the legacy domain model.

2.  **Transactional Integrity:** The balance update operation is wrapped in a single database transaction (`with db.begin():`). This ensures that the entire operation is **atomic**—it either completes fully or not at all, preventing partial updates and data corruption.

3.  **Dependency Inversion:** The application services depend on a repository abstraction, not a concrete implementation. This allows the data source to be swapped out with minimal changes to the core logic.

### Future Improvements

Given more time, the following improvements would be considered:

- **Refactor Domain Logic:** The `TimeDepositCalculator` would be refactored using the **Strategy Pattern** to make interest calculation rules more extensible and adhere to the Open/Closed Principle.
- **Scalability:** The `GET` endpoint would be updated with pagination to efficiently handle large numbers of records.
- **Concurrency:** For a multi-user environment, optimistic or pessimistic locking would be implemented to handle concurrent balance update requests safely.
- **Testing:** A comprehensive test suite using `pytest` and **Test Containers** has been added to ensure the reliability of the database interactions and business logic.

## Testing

The project includes both unit and integration tests:

To run the tests, first install the test dependencies:
   ```sh
   pip install -r python/requirements-test.txt
   ```

1. **Unit Tests:** Test the domain logic in isolation
   ```sh
   cd python && python -m unittest discover -s tests -p "test_*.py"
   ```

2. **Integration Tests with Testcontainers:** Test the full API against a real Postgres database
   ```sh
   cd python && pytest tests/test_integration_api.py -v
   ```
   
   **Note:** Integration tests require Docker to be running. To skip them:
   ```sh
   cd python && SKIP_INTEGRATION=1 pytest -q
   ```

## Project Structure

```
python/
├── app/
│   ├── api/              # FastAPI routers, schemas, dependencies
│   ├── application/      # Use cases, ports, services
│   ├── domain/           # Core business logic (entities, services)
│   ├── infrastructure/   # Database, repositories, external adapters
│   ├── scripts/          # Utility scripts (seeding, etc.)
│   └── main.py          # FastAPI application entry point
├── tests/               # Unit and integration tests
├── data/               # Database files (SQLite)
├── requirements.txt    # Production dependencies
└── requirements-test.txt # Test dependencies
```

Made By Aviral (error9098x)