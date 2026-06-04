from database import SessionLocal
import models

def seed_assets():
    db = SessionLocal()
    default_assets = [
        {"symbol": "BTC", "name": "Bitcoin", "price": 70000},
        {"symbol": "ETH", "name": "Ethereum", "price": 2070},
        {"symbol": "SOL", "name": "Solana", "price": 87},
        {"symbol": "DOGE", "name": "DogeCoin", "price": 30},
        {"symbol": "BNB",  "name": "Binance Coin", "price": 700}

    ]
    for asset in default_assets:
        existing = db.query(models.Asset).filter(models.Asset.symbol == asset["symbol"]).first()

        if not existing:
            new_asset = models.Asset(
                symbol = asset["symbol"],
                name  = asset["name"],
                price = asset["price"]
            )
            db.add(new_asset)
            db.commit()

    db.close()




