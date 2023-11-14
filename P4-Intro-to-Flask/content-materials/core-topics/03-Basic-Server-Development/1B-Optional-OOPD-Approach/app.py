"""
Can run using the following command:
    > `python(3) app.py`
"""

def main():
    from wrapper import FlaskWrapper
    run_server = FlaskWrapper()
    run_server(debug=True, port=1234)

if __name__ == "__main__":
    main()