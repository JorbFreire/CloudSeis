from create_app import create_app

if __name__ == "main":
    app = create_app("production")
    app.run(debug=True)
