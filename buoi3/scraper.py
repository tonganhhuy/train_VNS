import os
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, insert
import time
from dotenv import load_dotenv
import csv
import re

current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, '.env')
load_dotenv(dotenv_path=env_path)

DB_USER = os.getenv("DB_USER") or "root"
DB_PASSWORD = os.getenv("DB_PASSWORD") or "" 
DB_HOST = os.getenv("DB_HOST") or "localhost"
DB_PORT = os.getenv("DB_PORT") or "3306"
DB_NAME = os.getenv("DB_NAME") or "scraper_db"

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
engine = create_engine(DATABASE_URL, echo=False)
metadata = MetaData()

movies_table = Table(
    'movies', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(500), nullable=False),
    Column('genre', String(255)),
    Column('country', String(255)),
    Column('duration', String(255)),
    Column('release_year', Integer)
)
metadata.create_all(engine)

def scrape_movie_details(movie_url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        response = requests.get(movie_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title_tag = soup.find('h1') 
        title = title_tag.get_text(strip=True) if title_tag else "Unknown"

        movie_data = {
            'title': title,
            'genre': 'Đang cập nhật',
            'country': 'Đang cập nhật',
            'duration': 'Đang cập nhật',
            'release_year': 0
        }

        page_text = soup.get_text(separator=" ", strip=True)
        

        stop_words = r"(Thời lượng:|Số tập:|Tình trạng:|Ngôn ngữ:|Năm sản xuất:|Quốc gia:|Thể loại:|Diễn viên:|Đạo diễn:|$)"
        
        def get_val(keyword):
            pattern = rf"{keyword}\s*(.*?)(?={stop_words})"
            match = re.search(pattern, page_text, re.IGNORECASE)
            return match.group(1).strip() if match else ""

        duration = get_val(r"Thời lượng:")
        if duration: movie_data['duration'] = duration
            
        year_str = get_val(r"Năm sản xuất:")
        year_match = re.search(r'\d{4}', year_str)
        if year_match: movie_data['release_year'] = int(year_match.group())
            
        country = get_val(r"Quốc gia:")
        genre = get_val(r"Thể loại:")
        if genre:
            genre = genre.replace("·", "").replace("-", ",").strip()
            if genre.startswith(","): genre = genre[1:].strip()
            movie_data['genre'] = genre

        if country:
            if "·" in country:
                parts = country.split("·")
                movie_data['country'] = parts[0].strip()
                if movie_data['genre'] == 'Đang cập nhật' or not movie_data['genre']:
                    movie_data['genre'] = ", ".join([p.strip() for p in parts[1:]])
            else:
                movie_data['country'] = country
        if not movie_data['genre']: movie_data['genre'] = 'Đang cập nhật'

        return movie_data
    except Exception as e:
        print(f"  [!] Lỗi khi cào {movie_url}: {e}")
        return None

def crawl_movies_with_limit(base_list_url, target_limit):
    scraped_movies = []
    current_page = 1
    print(f"[*] Bắt đầu cào dữ liệu. Mục tiêu: {target_limit} phim.")

    while len(scraped_movies) < target_limit:
        page_url = f"{base_list_url}?page={current_page}" 
        try:
            res = requests.get(page_url, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(res.text, 'html.parser')
            
            movie_links = []
            for a_tag in soup.select('.item a'): 
                link = a_tag.get('href')
                if link and link not in movie_links:
                    if not link.startswith('http'): link = "https://motchillzl.id" + link
                    movie_links.append(link)
            
            if not movie_links: break

            for link in movie_links:
                if len(scraped_movies) >= target_limit: break
                print(f"  -> Đang cào ({len(scraped_movies)+1}/{target_limit}): {link}")
                details = scrape_movie_details(link)
                if details: scraped_movies.append(details)
                time.sleep(1) 
            current_page += 1
        except Exception as e:
            print(f"[!] Lỗi phân trang: {e}")
            break
    return scraped_movies

if __name__ == "__main__":
    LIST_URL = "https://motchillzl.id/phim-moi" 
    TARGET_COUNT = 500 
    movies_data = crawl_movies_with_limit(LIST_URL, TARGET_COUNT)
    
    if movies_data:
        csv_filename = "du_lieu_phim.csv"
        csv_filepath = os.path.join(current_dir, csv_filename)
        
        with open(csv_filepath, mode='w', newline='', encoding='utf-8-sig') as csv_file:
            fieldnames = ['title', 'genre', 'country', 'duration', 'release_year']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            writer.writerows(movies_data)
        
        print(f"\n[+] ĐÃ LƯU THÀNH CÔNG VÀO FILE: {csv_filename}")

        try:
            with engine.begin() as conn:
                conn.execute(movies_table.delete()) 
                conn.execute(insert(movies_table), movies_data)
            print("[+] ĐÃ LƯU THÀNH CÔNG VÀO DATABASE MYSQL!")
        except Exception as db_error:
            print(f"[-] Lỗi khi lưu vào Database: {db_error}")