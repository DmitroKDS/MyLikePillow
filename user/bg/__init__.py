from bg.img import pil_effect, thumbnail

import asyncio

import logging

from rembg import remove

from PIL import Image


async def remove_img(img: Image.Image, img_path: str) -> dict:
    logging.info(f'Removing background {img_path}')

    no_bg_img = await asyncio.to_thread(remove, img.convert("RGB"))

    no_bg_img = await asyncio.to_thread(lambda: no_bg_img.crop(no_bg_img.getbbox()))

    no_bg_img = await asyncio.to_thread(lambda: thumbnail.init(no_bg_img, (4000, 4000)))
    
    no_bg_img = no_bg_img.convert("RGBA")

    logging.info(f'Background removed {img_path}')


    img_name = img_path.split('/')[-1]
    no_bg_img_path = f"data/no_bg/{img_name}"

    logging.info(f'No bg image saved {no_bg_img_path}')


    pil_effect_img = await asyncio.to_thread( pil_effect.add, no_bg_img )
    pil_effect_img_path = f"data/pil_effect/{img_name}"

    logging.info(f'Pil effect image saved {no_bg_img_path}')


    return {
        no_bg_img_path: no_bg_img,
        pil_effect_img_path: pil_effect_img
    }