from app import get_application

app = get_application()
server = app.server

if __name__ == "__main__":
    app.run(debug=True, port=8080)
