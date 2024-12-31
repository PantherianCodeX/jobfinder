from crewai.tools import BaseTool
from typing import Type, List
from pydantic import BaseModel, Field
import requests
from bs4 import BeautifulSoup


class JobScraperInput(BaseModel):
    """Input schema for JobScraper."""
    platform_url: str = Field(
        default="https://www.freelancer.com/jobs",
        description="The URL of the freelance job platform to scrape."
    )


class JobScraper(BaseTool):
    name: str = "job_scraper"
    description: str = (
        "Scrapes freelance platforms for job postings and returns a list of job information, including title, description, budget, and links."
    )
    args_schema: Type[BaseModel] = JobScraperInput

    def _run(self, platform_url: str) -> List[dict]:
        """
        Scrapes the specified freelance platform URL for job postings.
        Args:
            platform_url (str): The URL of the freelance job platform to scrape.
        Returns:
            List[dict]: A list of job postings, each represented as a dictionary.
        """
        try:
            response = requests.get(platform_url)
            response.raise_for_status()  # Raise an error for bad HTTP responses
        except requests.RequestException as e:
            return [{"error": f"Failed to fetch job postings: {e}"}]

        soup = BeautifulSoup(response.text, "html.parser")
        job_cards = soup.find_all("div", class_="JobSearchCard-item")  # Update class name as needed

        jobs = []
        for card in job_cards:
            try:
                title = card.find("a", class_="JobSearchCard-primary-heading-link").text.strip()
                link = card.find("a", class_="JobSearchCard-primary-heading-link")["href"]
                description = card.find("p", class_="JobSearchCard-primary-description").text.strip()
                budget = card.find("div", class_="JobSearchCard-secondary-price").text.strip()

                jobs.append({
                    "title": title,
                    "link": f"https://www.freelancer.com{link}",
                    "description": description,
                    "budget": budget
                })
            except AttributeError:
                # Skip incomplete job cards
                continue

        return jobs
