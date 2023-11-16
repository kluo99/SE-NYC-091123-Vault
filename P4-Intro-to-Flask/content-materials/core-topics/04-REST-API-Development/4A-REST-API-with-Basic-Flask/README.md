# Basic Flask REST API

This demo mini-project is designed to demonstrate the steps to develop and test a basic REST API for handling HTTP requests and responses from Python. 

As such, completion of this mini-project can produce an effective API that students can use for further development of a full-stack application by leveraging their React and JavaScript development capabilities. 

Here are some recommended steps to take from completion of the backend server API to extending the project with a frontend.

### Steps to Full-Stack Extension

1. Navigate back up to the general project folder (in this location, it's the folder titled `4A-REST-API-with-Basic-Flask`).

2. Run `npx create-react-app client` to produce a new folder called `client` that contains relevant React code for a boilerplate React application.

3. Navigate into your `client` subdirectory.

4. Immediately access your `package.json` configuration file.

5. Add a new attribute to the JSON file at its highest level (at the same level as attributes like `"name"`, `"version"`, and `"private"`) that contains the following data: 
   
    ```"proxy": "http://localhost:<PORT>"```

    ...where `<PORT>` is the port number for your backend server application. 
    
    **NOTE**: Depending on your specific OS configuration and development environment setup, you may need to replace `localhost` with the actual IP address of your backend server application, such as `127.0.0.1`. 

6. Access your `src/App.js` file within the `client` subdirectory.

7. Write a script to handle `fetch`ing from your backend server application into your frontend. (Ensure you return JSON-like data from your backend server and that you unpack the JSON data in your frontend using `fetch`'s Promise architecture.)

8. Render and use that data however you like! 