import requests
import logging
import config

async def create(id: str, size: int, quantity: int, price: int, full_price: int) -> str:
    ref = id
    while True:
        offer_url=requests.post("https://api.monobank.ua/personal/checkout/order",
            json={   
                "order_ref": ref,
                "amount": full_price,
                "count": quantity,
                "products": [
                    {
                        "name": f"Кастомна подушка Розмір: {size} см",
                        "cnt": quantity,
                        "price": price,
                        "product_img_src": f"{config.FTP}/data/preview_pils/{id}.png"
                    }
                ],
                "dlv_method_list": [
                    "np_brnm",
                    "courier",
                    "np_box"
                ],
                "payment_method_list": [
                    "card"
                ],
                "callback_url": f"https://t.me/{config.BOT_USERNAME}?start=paid{config.PAID_TOKEN}{id}",
                "return_url": f"https://t.me/{config.BOT_USERNAME}"
            },
            headers={'X-Token':'mQn21CdkRQZUhhK3gomr6wg'}
        ).json()

        if 'result' not in offer_url:
            ref+="d"
            continue
        
        break
    
    return offer_url['result']['redirect_url']