# LinkedIn Job Scraper

A Python Selenium scraper to extract LinkedIn job postings, including title, company, location, date, job description, and link. Results are saved to an Excel file.

---

## Features

* Scrape LinkedIn jobs without login.
* Extract job title, company, location, date, description, and link.
* Auto-scroll to load all jobs on the page.
* Random delays to prevent LinkedIn blocking.
* Save results to Excel (`.xlsx`).
* Configurable search parameters via `settings.json`.

## Project Structure

```text
linkedin_scraper/
│
├── README.md
├── requirements.txt
├── .gitignore
├── main.py
├── src/
│ ├── scraper.py
│ ├── storage.py
│ └── utils.py
├── config/
│ └── settings.json
└── data/
└── linkedin_jobs.xlsx
```

## Installation

 1. Clone the repository:

```bash
git clone https://github.com/yourusername/linkedin_scraper.git
cd linkedin_scraper
```



 2. Create a virtual environment (optional but recommended):

```python
python -m venv venv
# Linux/Mac
source venv/bin/activate
# Windows
venv\Scripts\activate
```


 3. Install dependencies:

```python
pip install -r requirements.txt
```

## Configuration
Edit `config/settings.json` to customize:
```json
{
  "linkedin_url": "https://www.linkedin.com/jobs/search?keywords=Senior%20Backend%20Engineer&location=United%20States",
  "scroll_pause_time": 2,
  "max_scrolls": 20,
  "delay_range": [2, 5],
  "job_limit": 10,
  "output_file": "data/linkedin_jobs.xlsx"
}
```
- linkedin_url - Linkedin job search URL.
- scroll_pause_time - Pause time after each scroll.
- max_scrolls - Maximum scroll attempts.
- delay_range - random delay range between requests.
- job_limit - Maximum number of jobs to scrape.
-output_file - Path to save Excel output.

## Usage
Run the scraper :
```bash
python main.py
```

## Notes
- Ensure Chrome Driver matches your installed Chrome version.
- The script may break if LinkedIn updates their page structure.
- Use reponsibly and avoid scraping too frequently.