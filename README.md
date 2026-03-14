# 🛒 Price Comparator

A Python web scraper that searches for a product across **Amazon**, **MediaMarkt** and **El Corte Inglés** and returns the best price.

## Features

- Searches 3 major Spanish retailers simultaneously
- Ranks results by price and displays the best deal
- Handles cookie banners automatically

## Requirements

- Python 3.x
- Google Chrome installed
- ChromeDriver (matching your Chrome version)

## Setup

```bash
pip install -r requirements.txt
```

> ChromeDriver is bundled with `selenium >= 4.6`. No manual setup needed.

## Usage

```bash
python price_comparator.py
```

Then enter the product name when prompted:

```
Introduce el nombre del producto a buscar: iphone 16
```

### Example output

```
El mejor precio para el producto "iphone 16" es 769.0 € en la siguiente tienda:
- Amazon: Apple iPhone 16 de 128 GB...
Otras opciones disponibles:
- MediaMarkt: 799.0 € - Apple iPhone 16 128GB Negro
- El Corte Inglés: 829.0 € - Apple iPhone 16 128GB
```

## Tech stack

- [Selenium](https://selenium-python.readthedocs.io/) — browser automation
- ChromeDriver — headless Chrome control
