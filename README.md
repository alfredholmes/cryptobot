# CryptoBot
A bot to manage nicehash orders

### Features (still in development)
+ Order Floating
  + Orders will fall to the lowest price and rise upto a limit if the order market changes
+ Automatic ordering and order refils based on https://shapeshift.io prices
+ Order and Pool monitoring
  + If an order is not meeting expectations and this is statistically significant then the order will either be cancelled or profitable bounds changed
  
### Running instructions
```
pip install requests
git clone https://github.com/alfredholmes/cryptobot.git
cd cryptobot
python bot.py
```
 
