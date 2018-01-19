DROP TABLE IF EXISTS flat_price_analysis;

CREATE TABLE flat_price_analysis (
	id SERIAL4 PRIMARY KEY NOT NULL,
	description VARCHAR(100) NOT NULL,
	postcode_area VARCHAR(4) NULL,
	bedrooms INT NOT NULL,
	price INT NOT NULL,
	website VARCHAR(20) NULL,
	created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);