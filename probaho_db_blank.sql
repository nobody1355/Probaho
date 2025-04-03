-- Drop and Create Databases
DROP DATABASE IF EXISTS dbprobaho_master;
CREATE DATABASE dbprobaho_master;

DROP DATABASE IF EXISTS dbprobaho_res_dha;
CREATE DATABASE dbprobaho_res_dha;

DROP DATABASE IF EXISTS dbprobaho_gro_dha;
CREATE DATABASE dbprobaho_gro_dha;

DROP DATABASE IF EXISTS dbprobaho_phar_dha;
CREATE DATABASE dbprobaho_phar_dha;

DROP DATABASE IF EXISTS dbprobaho_res_bar;
CREATE DATABASE dbprobaho_res_bar;

DROP DATABASE IF EXISTS dbprobaho_gro_bar;
CREATE DATABASE dbprobaho_gro_bar;

DROP DATABASE IF EXISTS dbprobaho_phar_bar;
CREATE DATABASE dbprobaho_phar_bar;

-- Use dbprobaho_master for creating users table
USE dbprobaho_master;

-- users table (with AUTO_INCREMENT in dbprobaho_master)
CREATE TABLE IF NOT EXISTS users (
    userID INT PRIMARY KEY AUTO_INCREMENT,
    userName VARCHAR(100) NOT NULL,
    userPass VARCHAR(255) NOT NULL,
    userImage VARCHAR(255),
    userEmail VARCHAR(255) NOT NULL,
    reset_token VARCHAR(255),
    verification_token VARCHAR(255),
    verified BOOLEAN DEFAULT FALSE
);

-- businessTypes table (in dbprobaho_master)
CREATE TABLE IF NOT EXISTS businessTypes (
    businessTypeName VARCHAR(100),
    userID INT,
    FOREIGN KEY (userID) REFERENCES users(userID)
);

-- locations table (in dbprobaho_master)
CREATE TABLE IF NOT EXISTS locations (
    locationName VARCHAR(100),
    userID INT,
    FOREIGN KEY (userID) REFERENCES users(userID)
);

-- Now create the tables in other databases without AUTO_INCREMENT for userID
-- Using dbprobaho_res_dha
USE dbprobaho_res_dha;

CREATE TABLE IF NOT EXISTS users (
    userID INT PRIMARY KEY,
    userName VARCHAR(100) NOT NULL,
    userPass VARCHAR(255) NOT NULL,
    userImage VARCHAR(255),
    userEmail VARCHAR(255) NOT NULL,
    reset_token VARCHAR(255),
    verification_token VARCHAR(255),
    verified BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS businessTypes (
    businessTypeName VARCHAR(100),
    userID INT,
    FOREIGN KEY (userID) REFERENCES users(userID)
);

CREATE TABLE IF NOT EXISTS locations (
    locationName VARCHAR(100),
    userID INT,
    FOREIGN KEY (userID) REFERENCES users(userID)
);

CREATE TABLE IF NOT EXISTS category (
    catID INT AUTO_INCREMENT,
    catName VARCHAR(50),
    PRIMARY KEY (catID),
    userID INT,
    FOREIGN KEY (userID) REFERENCES users(userID)
);

CREATE TABLE IF NOT EXISTS products (
productID INT AUTO_INCREMENT PRIMARY KEY,
    productName VARCHAR(255),
    productPrice DECIMAL(10, 2),
    productStock INT,
    productDescription TEXT,
    catID INT,
    barcode_id VARCHAR(255),
    productImage VARCHAR(255),
    listingDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    expiryDate DATETIME ,  
    userID INT,
    FOREIGN KEY (userID) REFERENCES users(userID),
    FOREIGN KEY (catID) REFERENCES category(catID)
);

CREATE TABLE IF NOT EXISTS bills (
    billID INT AUTO_INCREMENT PRIMARY KEY,
    userID INT,                                  -- Reference to the user who generated the bill
    totalAmount DECIMAL(10, 2) NOT NULL,         -- Total amount of the bill
    billDate DATETIME DEFAULT CURRENT_TIMESTAMP, -- Date and time of the bill
    paymentMethod VARCHAR(50),                   -- Payment method used (e.g., cash, card)
    customerName VARCHAR(255),                   -- Optional: Name of the customer
    customerContact VARCHAR(50),
    customerAddress VARCHAR(100),    
    customerEmail VARCHAR(100),           
    FOREIGN KEY (userID) REFERENCES users(userID) -- Reference to the users table
);

CREATE TABLE IF NOT EXISTS bill_items (
    billItemID INT AUTO_INCREMENT PRIMARY KEY,
    billID INT,                                  -- Reference to the related bill
    productID INT,                               -- Reference to the sold product
    quantity INT NOT NULL,                       -- Quantity sold
    pricePerUnit DECIMAL(10, 2) NOT NULL,        -- Price per unit of the product
    totalPrice DECIMAL(10, 2) NOT NULL,          -- Total price for this item (quantity * pricePerUnit)
    FOREIGN KEY (billID) REFERENCES bills(billID), -- Reference to the bills table
    FOREIGN KEY (productID) REFERENCES products(productID) -- Reference to the products table
);

CREATE TABLE IF NOT EXISTS staff (
    StaffID INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Position VARCHAR(50),
    Email VARCHAR(100) UNIQUE,
    PhoneNumber VARCHAR(15),
    HireDate DATE,
    Salary DECIMAL(10, 2),
    userID INT,
    FOREIGN KEY (userID) REFERENCES users(userID) -- Reference to the users table
);


-- Using dbprobaho_res_bar
USE dbprobaho_res_bar;

CREATE TABLE IF NOT EXISTS users (
    userID INT PRIMARY KEY,
    userName VARCHAR(100) NOT NULL,
    userPass VARCHAR(255) NOT NULL,
    userImage VARCHAR(255),
    userEmail VARCHAR(255) NOT NULL,
    reset_token VARCHAR(255),
    verification_token VARCHAR(255),
    verified BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS businessTypes (
    businessTypeName VARCHAR(100),
    userID INT,
    FOREIGN KEY (userID) REFERENCES users(userID)
);

CREATE TABLE IF NOT EXISTS locations (
    locationName VARCHAR(100),
    userID INT,
    FOREIGN KEY (userID) REFERENCES users(userID)
);

CREATE TABLE IF NOT EXISTS category (
    catID INT AUTO_INCREMENT,
    catName VARCHAR(50),
    PRIMARY KEY (catID),
    userID INT,
    FOREIGN KEY (userID) REFERENCES users(userID)
);

CREATE TABLE IF NOT EXISTS products (
productID INT AUTO_INCREMENT PRIMARY KEY,
    productName VARCHAR(255),
    productPrice DECIMAL(10, 2),
    productStock INT,
    productDescription TEXT,
    catID INT,
    barcode_id VARCHAR(255),
    productImage VARCHAR(255),
    listingDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    expiryDate DATETIME ,  
    userID INT,
    FOREIGN KEY (userID) REFERENCES users(userID),
    FOREIGN KEY (catID) REFERENCES category(catID)
);

CREATE TABLE IF NOT EXISTS bills (
    billID INT AUTO_INCREMENT PRIMARY KEY,
    userID INT,                                  -- Reference to the user who generated the bill
    totalAmount DECIMAL(10, 2) NOT NULL,         -- Total amount of the bill
    billDate DATETIME DEFAULT CURRENT_TIMESTAMP, -- Date and time of the bill
    paymentMethod VARCHAR(50),                   -- Payment method used (e.g., cash, card)
    customerName VARCHAR(255),                   -- Optional: Name of the customer
    customerContact VARCHAR(50),
    customerAddress VARCHAR(100),    
    customerEmail VARCHAR(100),           
    FOREIGN KEY (userID) REFERENCES users(userID) -- Reference to the users table
);

CREATE TABLE IF NOT EXISTS bill_items (
    billItemID INT AUTO_INCREMENT PRIMARY KEY,
    billID INT,                                  -- Reference to the related bill
    productID INT,                               -- Reference to the sold product
    quantity INT NOT NULL,                       -- Quantity sold
    pricePerUnit DECIMAL(10, 2) NOT NULL,        -- Price per unit of the product
    totalPrice DECIMAL(10, 2) NOT NULL,          -- Total price for this item (quantity * pricePerUnit)
    FOREIGN KEY (billID) REFERENCES bills(billID), -- Reference to the bills table
    FOREIGN KEY (productID) REFERENCES products(productID) -- Reference to the products table
);

CREATE TABLE IF NOT EXISTS staff (
    StaffID INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Position VARCHAR(50),
    Email VARCHAR(100) UNIQUE,
    PhoneNumber VARCHAR(15),
    HireDate DATE,
    Salary DECIMAL(10, 2),
    userID INT,
    FOREIGN KEY (userID) REFERENCES users(userID) -- Reference to the users table
);


-- Using dbprobaho_gro_dha
USE dbprobaho_gro_dha;

CREATE TABLE IF NOT EXISTS users (
    userID INT PRIMARY KEY,
    userName VARCHAR(100) NOT NULL,
    userPass VARCHAR(255) NOT NULL,
    userImage VARCHAR(255),
    userEmail VARCHAR(255) NOT NULL,
    reset_token VARCHAR(255),
    verification_token VARCHAR(255),
    verified BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS businessTypes (
    businessTypeName VARCHAR(100),
    userID INT,
    FOREIGN KEY (userID) REFERENCES users(userID)
);

CREATE TABLE IF NOT EXISTS locations (
    locationName VARCHAR(100),
    userID INT,
    FOREIGN KEY (userID) REFERENCES users(userID)
);

CREATE TABLE IF NOT EXISTS category (
    catID INT AUTO_INCREMENT,
    catName VARCHAR(50),
    PRIMARY KEY (catID),
    userID INT,
    FOREIGN KEY (userID) REFERENCES users(userID)
);

CREATE TABLE IF NOT EXISTS products (
productID INT AUTO_INCREMENT PRIMARY KEY,
    productName VARCHAR(255),
    productPrice DECIMAL(10, 2),
    productStock INT,
    productDescription TEXT,
    catID INT,
    barcode_id VARCHAR(255),
    productImage VARCHAR(255),
    listingDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    expiryDate DATETIME ,  
    userID INT,
    FOREIGN KEY (userID) REFERENCES users(userID),
    FOREIGN KEY (catID) REFERENCES category(catID)
);

CREATE TABLE IF NOT EXISTS bills (
    billID INT AUTO_INCREMENT PRIMARY KEY,
    userID INT,                                  -- Reference to the user who generated the bill
    totalAmount DECIMAL(10, 2) NOT NULL,         -- Total amount of the bill
    billDate DATETIME DEFAULT CURRENT_TIMESTAMP, -- Date and time of the bill
    paymentMethod VARCHAR(50),                   -- Payment method used (e.g., cash, card)
    customerName VARCHAR(255),                   -- Optional: Name of the customer
    customerContact VARCHAR(50),
    customerAddress VARCHAR(100),    
    customerEmail VARCHAR(100),           
    FOREIGN KEY (userID) REFERENCES users(userID) -- Reference to the users table
);

CREATE TABLE IF NOT EXISTS bill_items (
    billItemID INT AUTO_INCREMENT PRIMARY KEY,
    billID INT,                                  -- Reference to the related bill
    productID INT,                               -- Reference to the sold product
    quantity INT NOT NULL,                       -- Quantity sold
    pricePerUnit DECIMAL(10, 2) NOT NULL,        -- Price per unit of the product
    totalPrice DECIMAL(10, 2) NOT NULL,          -- Total price for this item (quantity * pricePerUnit)
    FOREIGN KEY (billID) REFERENCES bills(billID), -- Reference to the bills table
    FOREIGN KEY (productID) REFERENCES products(productID) -- Reference to the products table
);

CREATE TABLE IF NOT EXISTS staff (
    StaffID INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Position VARCHAR(50),
    Email VARCHAR(100) UNIQUE,
    PhoneNumber VARCHAR(15),
    HireDate DATE,
    Salary DECIMAL(10, 2),
    userID INT,
    FOREIGN KEY (userID) REFERENCES users(userID) -- Reference to the users table
);

USE dbprobaho_gro_bar;

CREATE TABLE IF NOT EXISTS users (
    userID INT PRIMARY KEY,
    userName VARCHAR(100) NOT NULL,
    userPass VARCHAR(255) NOT NULL,
    userImage VARCHAR(255),
    userEmail VARCHAR(255) NOT NULL,
    reset_token VARCHAR(255),
    verification_token VARCHAR(255),
    verified BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS businessTypes (
    businessTypeName VARCHAR(100),
    userID INT,
    FOREIGN KEY (userID) REFERENCES users(userID)
);

CREATE TABLE IF NOT EXISTS locations (
    locationName VARCHAR(100),
    userID INT,
    FOREIGN KEY (userID) REFERENCES users(userID)
);

CREATE TABLE IF NOT EXISTS category (
    catID INT AUTO_INCREMENT,
    catName VARCHAR(50),
    PRIMARY KEY (catID),
    userID INT,
    FOREIGN KEY (userID) REFERENCES users(userID)
);

CREATE TABLE IF NOT EXISTS products (
productID INT AUTO_INCREMENT PRIMARY KEY,
    productName VARCHAR(255),
    productPrice DECIMAL(10, 2),
    productStock INT,
    productDescription TEXT,
    catID INT,
    barcode_id VARCHAR(255),
    productImage VARCHAR(255),
    listingDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    expiryDate DATETIME ,  
    userID INT,
    FOREIGN KEY (userID) REFERENCES users(userID),
    FOREIGN KEY (catID) REFERENCES category(catID)
);

CREATE TABLE IF NOT EXISTS bills (
    billID INT AUTO_INCREMENT PRIMARY KEY,
    userID INT,                                  -- Reference to the user who generated the bill
    totalAmount DECIMAL(10, 2) NOT NULL,         -- Total amount of the bill
    billDate DATETIME DEFAULT CURRENT_TIMESTAMP, -- Date and time of the bill
    paymentMethod VARCHAR(50),                   -- Payment method used (e.g., cash, card)
    customerName VARCHAR(255),                   -- Optional: Name of the customer
    customerContact VARCHAR(50),
    customerAddress VARCHAR(100),    
    customerEmail VARCHAR(100),           
    FOREIGN KEY (userID) REFERENCES users(userID) -- Reference to the users table
);

CREATE TABLE IF NOT EXISTS bill_items (
    billItemID INT AUTO_INCREMENT PRIMARY KEY,
    billID INT,                                  -- Reference to the related bill
    productID INT,                               -- Reference to the sold product
    quantity INT NOT NULL,                       -- Quantity sold
    pricePerUnit DECIMAL(10, 2) NOT NULL,        -- Price per unit of the product
    totalPrice DECIMAL(10, 2) NOT NULL,          -- Total price for this item (quantity * pricePerUnit)
    FOREIGN KEY (billID) REFERENCES bills(billID), -- Reference to the bills table
    FOREIGN KEY (productID) REFERENCES products(productID) -- Reference to the products table
);

CREATE TABLE IF NOT EXISTS staff (
    StaffID INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Position VARCHAR(50),
    Email VARCHAR(100) UNIQUE,
    PhoneNumber VARCHAR(15),
    HireDate DATE,
    Salary DECIMAL(10, 2),
    userID INT,
    FOREIGN KEY (userID) REFERENCES users(userID) -- Reference to the users table
);

-- Using dbprobaho_phar_dha
USE dbprobaho_phar_dha;

CREATE TABLE IF NOT EXISTS users (
    userID INT PRIMARY KEY,
    userName VARCHAR(100) NOT NULL,
    userPass VARCHAR(255) NOT NULL,
    userImage VARCHAR(255),
    userEmail VARCHAR(255) NOT NULL,
    reset_token VARCHAR(255),
    verification_token VARCHAR(255),
    verified BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS businessTypes (
    businessTypeName VARCHAR(100),
    userID INT,
    FOREIGN KEY (userID) REFERENCES users(userID)
);

CREATE TABLE IF NOT EXISTS locations (
    locationName VARCHAR(100),
    userID INT,
    FOREIGN KEY (userID) REFERENCES users(userID)
);

CREATE TABLE IF NOT EXISTS category (
    catID INT AUTO_INCREMENT,
    catName VARCHAR(50),
    PRIMARY KEY (catID),
    userID INT,
    FOREIGN KEY (userID) REFERENCES users(userID)
);

CREATE TABLE IF NOT EXISTS products (
productID INT AUTO_INCREMENT PRIMARY KEY,
    productName VARCHAR(255),
    productPrice DECIMAL(10, 2),
    productStock INT,
    productDescription TEXT,
    catID INT,
    barcode_id VARCHAR(255),
    productImage VARCHAR(255),
    listingDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    expiryDate DATETIME ,  
    userID INT,
    FOREIGN KEY (userID) REFERENCES users(userID),
    FOREIGN KEY (catID) REFERENCES category(catID)
);

CREATE TABLE IF NOT EXISTS bills (
    billID INT AUTO_INCREMENT PRIMARY KEY,
    userID INT,                                  -- Reference to the user who generated the bill
    totalAmount DECIMAL(10, 2) NOT NULL,         -- Total amount of the bill
    billDate DATETIME DEFAULT CURRENT_TIMESTAMP, -- Date and time of the bill
    paymentMethod VARCHAR(50),                   -- Payment method used (e.g., cash, card)
    customerName VARCHAR(255),                   -- Optional: Name of the customer
    customerContact VARCHAR(50),
    customerAddress VARCHAR(100),    
    customerEmail VARCHAR(100),           
    FOREIGN KEY (userID) REFERENCES users(userID) -- Reference to the users table
);

CREATE TABLE IF NOT EXISTS bill_items (
    billItemID INT AUTO_INCREMENT PRIMARY KEY,
    billID INT,                                  -- Reference to the related bill
    productID INT,                               -- Reference to the sold product
    quantity INT NOT NULL,                       -- Quantity sold
    pricePerUnit DECIMAL(10, 2) NOT NULL,        -- Price per unit of the product
    totalPrice DECIMAL(10, 2) NOT NULL,          -- Total price for this item (quantity * pricePerUnit)
    FOREIGN KEY (billID) REFERENCES bills(billID), -- Reference to the bills table
    FOREIGN KEY (productID) REFERENCES products(productID) -- Reference to the products table
);

CREATE TABLE IF NOT EXISTS staff (
    StaffID INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Position VARCHAR(50),
    Email VARCHAR(100) UNIQUE,
    PhoneNumber VARCHAR(15),
    HireDate DATE,
    Salary DECIMAL(10, 2),
    userID INT,
    FOREIGN KEY (userID) REFERENCES users(userID) -- Reference to the users table
);

USE dbprobaho_phar_bar;

CREATE TABLE IF NOT EXISTS users (
    userID INT PRIMARY KEY,
    userName VARCHAR(100) NOT NULL,
    userPass VARCHAR(255) NOT NULL,
    userImage VARCHAR(255),
    userEmail VARCHAR(255) NOT NULL,
    reset_token VARCHAR(255),
    verification_token VARCHAR(255),
    verified BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS businessTypes (
    businessTypeName VARCHAR(100),
    userID INT,
    FOREIGN KEY (userID) REFERENCES users(userID)
);

CREATE TABLE IF NOT EXISTS locations (
    locationName VARCHAR(100),
    userID INT,
    FOREIGN KEY (userID) REFERENCES users(userID)
);

CREATE TABLE IF NOT EXISTS category (
    catID INT AUTO_INCREMENT,
    catName VARCHAR(50),
    PRIMARY KEY (catID),
    userID INT,
    FOREIGN KEY (userID) REFERENCES users(userID)
);

CREATE TABLE IF NOT EXISTS products (
productID INT AUTO_INCREMENT PRIMARY KEY,
    productName VARCHAR(255),
    productPrice DECIMAL(10, 2),
    productStock INT,
    productDescription TEXT,
    catID INT,
    barcode_id VARCHAR(255),
    productImage VARCHAR(255),
    listingDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    expiryDate DATETIME ,  
    userID INT,
    FOREIGN KEY (userID) REFERENCES users(userID),
    FOREIGN KEY (catID) REFERENCES category(catID)
);

CREATE TABLE IF NOT EXISTS bills (
    billID INT AUTO_INCREMENT PRIMARY KEY,
    userID INT,                                  -- Reference to the user who generated the bill
    totalAmount DECIMAL(10, 2) NOT NULL,         -- Total amount of the bill
    billDate DATETIME DEFAULT CURRENT_TIMESTAMP, -- Date and time of the bill
    paymentMethod VARCHAR(50),                   -- Payment method used (e.g., cash, card)
    customerName VARCHAR(255),                   -- Optional: Name of the customer
    customerContact VARCHAR(50),
    customerAddress VARCHAR(100),    
    customerEmail VARCHAR(100),           
    FOREIGN KEY (userID) REFERENCES users(userID) -- Reference to the users table
);

CREATE TABLE IF NOT EXISTS bill_items (
    billItemID INT AUTO_INCREMENT PRIMARY KEY,
    billID INT,                                  -- Reference to the related bill
    productID INT,                               -- Reference to the sold product
    quantity INT NOT NULL,                       -- Quantity sold
    pricePerUnit DECIMAL(10, 2) NOT NULL,        -- Price per unit of the product
    totalPrice DECIMAL(10, 2) NOT NULL,          -- Total price for this item (quantity * pricePerUnit)
    FOREIGN KEY (billID) REFERENCES bills(billID), -- Reference to the bills table
    FOREIGN KEY (productID) REFERENCES products(productID) -- Reference to the products table
);

CREATE TABLE IF NOT EXISTS staff (
    StaffID INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Position VARCHAR(50),
    Email VARCHAR(100) UNIQUE,
    PhoneNumber VARCHAR(15),
    HireDate DATE,
    Salary DECIMAL(10, 2),
    userID INT,
    FOREIGN KEY (userID) REFERENCES users(userID) -- Reference to the users table
);


COMMIT;
