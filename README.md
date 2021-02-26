E-commerce shop - online meals delivery system with QR codes.

<b> Application created for my engineering thesis - <i>Development and implementation of online meal ordering system with QR code reader</i></b>

This app allows users to order a meal and scan QR codes which return information such as glycemic index and calories of given dish.
QR codes can be scaned by using a button or via smartphone scanner.

Technologies used - Django, Python, GeoPy, PostgreSQL, HTML, CSS, Bootstrap, JS

![mainpage](https://i.imgur.com/uStU4cO.png)

<b>Restaurants<b>
 
 ![restaurants](https://i.imgur.com/LYZMFxh.png)
 
 List of products and QR codes, if you hover your mouse button over a code, a button with onclick function will pop up and will scan the code.
 
 ![food_qr](https://i.imgur.com/GGhX9sf.png)
 ![scanned_qr_food](https://i.imgur.com/SGKCSzg.png)
 
You can add products to cart by using "Dodaj do koszyka" button, but to finish the order process you need to register or log in.
[Cart](https://i.imgur.com/h54KUTh.png)

After creating an account user will recieve an e-mail. To finish the order process, user has to add his delivey address, which will generate a QR code with a link to google maps service with coordinates of given address.
User can add multiple addresses.

[Adding new address](https://i.imgur.com/NgZ05Zu.png)

[Selecting delivery address](https://i.imgur.com/f2HvkJw.png)

After finishing new order, the number of orders from given city (Cracow, Poland in this case) district will be updated - agregation.

[Statistics](https://i.imgur.com/C9ZtqID.png)

Order history can be checked in given section.

<b> Admin Panel <b>
  
  Orders are accepted via django admin panel, where their status is changed and qr code for delivery gets scanned by delivery driver.
  [Order information in Django-Admin](https://i.imgur.com/XKrxkFb.png)
  
  Scanned QR code:
  [Scanned Delivery QR code](https://i.imgur.com/2fZPx0w.png)
  
  Admin pannel also allows for adding new products, restaurants, categories, food images.
  
 
