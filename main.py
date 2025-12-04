import json
from selenium import webdriver
from src.scraper import scrape_jobs
from src.storage import save_to_excel


def main():
    # Load config
    with open("config/settings.json", "r") as f:
        config = json.load(f)

    driver = webdriver.Chrome()
    driver.get(config["linkedin_url"])

    data = scrape_jobs(
        driver,
        limit=config.get("job_limit"),
        delay_range=config.get("delay_range", (2, 5))
    )

    save_to_excel(data, filename=config.get(
        "output_file", "data/linkedin_jobs.xlsx"))
    driver.quit()


if __name__ == "__main__":
    main()
