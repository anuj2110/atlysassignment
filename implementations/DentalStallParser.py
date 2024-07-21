from helpers.parser import Parser
import requests
from bs4 import BeautifulSoup
import httpx
import asyncio
import time
from helpers.StorageInterface import StorageInterface
from helpers.MessagingInteface import MessagingInteface
from fastapi import BackgroundTasks
import os
import aiohttp
from entities.JsonEntity import JsonEntity


class DentalStallParser(Parser):
    def __init__(self, url: str):
        self.url = url

    async def download_image(self, session, url, file_path):
        async with session.get(url) as resp:
            with open(file_path, 'wb') as f:
                while True:
                    chunk = await resp.content.read(1024)
                    if not chunk:
                        break
                    f.write(chunk)

    async def download_images(self, urls, file_paths, notifier):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for url, file_path in zip(urls, file_paths):
                tasks.append(self.download_image(session, url, file_path))
            await asyncio.gather(*tasks)
        notifier.send_message("Images downloaded successfully")

    async def parse_single(self, page_no, result, url_file_paths):
        max_retries = 3
        wait_time = 3

        for attempt in range(max_retries):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"{self.url}{page_no}") as response:
                        response.raise_for_status()
                        soup = BeautifulSoup(await response.text(), "html.parser")
                        products = soup.find_all(
                            "div", class_="product-inner clearfix")
                        for product in products:
                            url = product.find("div", class_="mf-product-thumbnail").find("img",
                                                                                          class_="attachment-woocommerce_thumbnail size-woocommerce_thumbnail").get("data-lazy-src")
                            file_path = f"data/images/{url.split('/')[-1]}"
                            product_title = product.find(
                                "div", class_="mf-product-details").find("h2", class_="woo-loop-product__title").text
                            product_price = float(product.find("div", class_="mf-product-price-box").find(
                                "span", class_="woocommerce-Price-amount amount").find("bdi").text[1:])

                            data = JsonEntity(
                                prodcut_title=product_title, product_price=product_price, path_to_image=file_path)
                            result.append(data.model_dump())
                            url_file_paths[0].append(url)
                            url_file_paths[1].append(file_path)
                break
            except (aiohttp.ClientError, ValueError) as e:
                print(f"Error parsing page {page_no}: {e}")
                if attempt < max_retries - 1:
                    print(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)

    async def parse(self, num_pages, storer: StorageInterface, notifier: MessagingInteface, background_tasks: BackgroundTasks):
        print(os.environ.get("BASE_DIR"))
        data = []
        url_file_paths = [[], []]
        start = time.time()
        async with httpx.AsyncClient() as client:
            tasks = [self.parse_single(num, data, url_file_paths)
                     for num in range(1, num_pages+1)]
            await asyncio.gather(*tasks, return_exceptions=True)
        storer.save(data)
        notifier.send_message(
            "Scrapped the web pages from 1-{num_pages} pages, downloading images in background. Will notify when done.")
        background_tasks.add_task(
            self.download_images, url_file_paths[0], url_file_paths[1],notifier)
        end = time.time()
        print(f"Time taken: {end - start} seconds")
