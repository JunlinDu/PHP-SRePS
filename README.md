# Public Health Pharmacy Digital Sales System

Note: The current password for the database in the config.py file is **password**.  If the error **"AttributeError: 'NoneType' object has no attribute 'cursor'"** appears, check the following:
~~~
* Your Local MySQL database server is running.
* The password in the config file matchup with your local MySQL database password.
~~~

--Current file structure
```
PHP-SRePS/
│
├── app/
├── ├── CSVs/
│   │   ├── batch.csv
│   │   ├── customer.csv
│   │   ├── inventory.csv
│   │   ├── manufacturer.csv
│   │   ├── product.csv
│   │   ├── sale_items.csv
│   │   └── sales.csv
│   │   
├── ├── UserInterface/
├── ├── ├── Pages/
│   │   │   ├── BatchDialog.ui
│   │   │   ├── EditBatchDialog.ui
│   │   │   ├── EditProductDialog.ui
│   │   │   ├── MainMenu.ui
│   │   │   ├── ProductDialog.ui
│   │   │   ├── SalesWindow.ui
│   │   │   └── StockWindow.ui
│   │   │   
│   │   ├── Resources
│   │   │   ├── SourceImages
│   │   │   │   ├── Bin.png
│   │   │   │   ├── Book.png
│   │   │   │   ├── Box.png
│   │   │   │   ├── Dollar.png
│   │   │   │   ├── Pencil.png
│   │   │   │   ├── Plus.png
│   │   │   │   └── Report.png
│   │   │   │
│   │   │   ├── Images.py
│   │   │   └── Imgages.qrc
│   │   │   
│   │   ├── SalesMenu.py
│   │   ├── StockMenu.py
│   │   └── UiHandler.py
│   │
│   ├── connect.py
│   ├── delete.py
|   ├── exportCSV.py
│   ├── insert.py
│   ├── main.py
│   ├── read.py
│   └── update.py
│
├── .gitignore
├── datebase.sql
└── README.md

```
