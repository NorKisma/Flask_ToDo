# Flask_ToDo
This Project For Module 3  FullStackDevloper Program Course

A simple todo-list web application which provides the following functionality:
• A list of todos
• Create a new todo item
• Mark a todo item as done or undone
• Edit a todo item
• Delete a todo item
• Mark everything as completed
  
Create Simple  in Mysql Databases
 
 
 CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL
);

CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    description TEXT NOT NULL,
    deadline DATE NOT NULL,
    created_date DATE NOT NULL,
    priority VARCHAR(50) NOT NULL
);


The project makes use of Python3, Flask, mysql, Bootstrap and JQuery.
