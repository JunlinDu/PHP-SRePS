# You will need a mysql server installed to run this.
# I am using Xampp to run my mysql server
# I am running this via mysql workbench, but copy-pasting this to terminal should work too.

# Will need to comment out drop if database doesnt exist.
DROP DATABASE PHP_SRePS;

CREATE DATABASE PHP_SRePS;
USE PHP_SRePS;

CREATE TABLE items (
	item_id int(10) AUTO_INCREMENT UNIQUE NOT NULL,
	item_name varchar(30),
	PRIMARY KEY (item_id)
);

CREATE TABLE sales (
	sale_id int(10) AUTO_INCREMENT UNIQUE,
	item_id int(10),
	quantity int(10),
	PRIMARY KEY (sale_id),
	FOREIGN KEY (item_id) REFERENCES items(item_id)
);

INSERT INTO items (`item_name`) VALUES ('Panadol');
INSERT INTO items (`item_name`) VALUES ('Meat');
INSERT INTO items (`item_name`) VALUES ('Liquid');
INSERT INTO items (`item_name`) VALUES ('Pain');
INSERT INTO items (`item_name`) VALUES ('Guck');

INSERT INTO sales (`item_id`, `quantity`) VALUES (1, 10);
INSERT INTO sales (`item_id`, `quantity`) VALUES (2, 20);
INSERT INTO sales (`item_id`, `quantity`) VALUES (3, 30);
INSERT INTO sales (`item_id`, `quantity`) VALUES (4, 40);
INSERT INTO sales (`item_id`, `quantity`) VALUES (5, 50);
