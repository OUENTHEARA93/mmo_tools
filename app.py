from myapp import app

if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()  # Ensure the database tables are created inside the application context
    app.run(debug=1, host='0.0.0.0')
