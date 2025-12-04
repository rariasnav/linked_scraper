import json
import urllib.parse
import os
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

CONFIG_PATH = "config/settings.json"


# -------------------------------
# Helpers
# -------------------------------
def load_settings():
    if not os.path.exists(CONFIG_PATH):
        return {}
    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except:
        return {}


def save_settings(data):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f, indent=4)


def parse_delay(text):
    try:
        parts = [float(x.strip()) for x in text.split(",")]
        return parts if len(parts) == 2 else [2, 5]
    except:
        return [2, 5]


def generate_linkedin_url(keyword, location, work_types, date_posted, salary):
    base = "https://www.linkedin.com/jobs/search/"
    keyword = urllib.parse.quote(keyword)
    location = urllib.parse.quote(location)

    # Date posted
    date_map = {
        "last 24 hours": "r86400",
        "a week": "r604800",
        "a month": "r2592000"
    }
    f_TPR = f"&f_TPR={date_map.get(date_posted.lower(), '')}" if date_posted.lower(
    ) != "any time" else ""

    # Work types
    f_WT_map = {"Remote": "2", "Hybrid": "3", "On-site": "1"}
    selected = [f_WT_map[w] for w in work_types if w in f_WT_map]
    f_WT = f"&f_WT={','.join(selected)}" if selected else ""

    # Salary
    salary_map = {"$40,000+": "1", "$60,000+": "2",
                  "$80,000+": "3", "$100,000+": "4", "$120,000+": "5"}
    f_SB2 = f"&f_SB2={salary_map.get(salary)}" if salary in salary_map else ""

    return f"{base}?keywords={keyword}&location={location}&geoId=103644278{f_SB2}{f_TPR}{f_WT}"


# -------------------------------
# GUI App
# -------------------------------
class LinkedInGUI(App):
    WORK_TYPES = ["Remote", "Hybrid", "On-site"]

    def build(self):
        self.title = "LinkedIn Scraper"
        self.settings = load_settings()
        layout = GridLayout(cols=2, spacing=10, padding=20)

        # Helper to create label + input
        def add_row(label_text, widget):
            layout.add_widget(Label(text=label_text))
            layout.add_widget(widget)

        # Keyword & Location
        self.keyword = TextInput(text=self.settings.get(
            "keyword", "Senior Backend Engineer"), multiline=False)
        add_row("Keyword:", self.keyword)

        self.location = TextInput(text=self.settings.get(
            "location", "United States"), multiline=False)
        add_row("Location:", self.location)

        # Work Type (checkboxes)
        add_row("Work Type:", self._create_work_type_box())

        # Date Posted
        self.date_posted = Spinner(
            text=self.settings.get("date_posted", "last 24 hours"),
            values=["Any Time", "last 24 hours", "a week", "a month"]
        )
        add_row("Date Posted:", self.date_posted)

        # Salary
        self.salary_spinner = Spinner(
            text=self.settings.get("salary", "$60,000+"),
            values=["All Range", "$40,000+", "$60,000+",
                    "$80,000+", "$100,000+", "$120,000+"]
        )
        add_row("Salary:", self.salary_spinner)

        # Numeric fields
        self.job_limit = TextInput(text=str(self.settings.get(
            "job_limit", 20)), multiline=False, input_filter="int")
        add_row("Job Limit:", self.job_limit)

        self.scroll_pause = TextInput(
            text=str(self.settings.get("scroll_pause_time", 2)), multiline=False)
        add_row("Scroll Pause Time:", self.scroll_pause)

        self.max_scrolls = TextInput(text=str(self.settings.get(
            "max_scrolls", 20)), multiline=False, input_filter="int")
        add_row("Max Scrolls:", self.max_scrolls)

        self.delay_range = TextInput(
            text=",".join(map(str, self.settings.get("delay_range", [2, 5]))), multiline=False
        )
        add_row("Delay Range (min,max):", self.delay_range)

        self.output = TextInput(text=self.settings.get(
            "output_file", "data/linkedin_jobs.xlsx"), multiline=False)
        add_row("Output File:", self.output)

        # Apply button
        add_row("", self._create_apply_button())

        return layout

    def _create_work_type_box(self):
        self.work_checkboxes = {}
        box = BoxLayout(orientation="horizontal", spacing=10)
        selected = self.settings.get("work_type", ["Remote"])
        for wt in self.WORK_TYPES:
            box.add_widget(Label(text=wt))
            cb = CheckBox(active=wt in selected)
            self.work_checkboxes[wt] = cb
            box.add_widget(cb)
        return box

    def _create_apply_button(self):
        btn = Button(text="Apply")
        btn.bind(on_press=self.apply_settings)
        return btn

    def apply_settings(self, _):
        work_types = [wt for wt, cb in self.work_checkboxes.items()
                      if cb.active]

        data = {
            "keyword": self.keyword.text,
            "location": self.location.text,
            "work_type": work_types,
            "date_posted": self.date_posted.text,
            "salary": self.salary_spinner.text,
            "job_limit": int(self.job_limit.text or 20),
            "scroll_pause_time": float(self.scroll_pause.text or 2),
            "max_scrolls": int(self.max_scrolls.text or 20),
            "delay_range": parse_delay(self.delay_range.text),
            "output_file": self.output.text,
            "linkedin_url": generate_linkedin_url(
                self.keyword.text, self.location.text, work_types, self.date_posted.text, self.salary_spinner.text
            )
        }

        save_settings(data)
        print("\nSettings Saved!")
        print("LinkedIn URL:", data["linkedin_url"])


if __name__ == "__main__":
    LinkedInGUI().run()
