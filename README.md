# FastScraper:Scraping Data at speed

This is FastScraper, a scraping tool build to scrape data from websites. It is been produced as an assignment for Atlys team take home assignment. The project uses Python,FastAPI and asynchronous programming to make the project.\

## Steps to run the project
1. First of all clone the repository
	 `git clone https://github.com/anuj2110/atlysassignment`

2. Make sure to create a .env file with the variables given in the email
3. After completing above steps, just run
		`docker-compose up --build`



## Routes
1. /scrape-simple -> Uses simple logging to show the results of scrapping. It is a GET request
2. /scrape-email -> Sends email when done with scraping processes. It is a GET request, but need to send a body with fields
	`
	{
		"recipient_emails":["email1","email2"]
	}`

## Additional Information
1. It will show 0 results, if the results are already scrapped

## Future Improvements
As with every software, this one can also be optimized further, some of my observations
1. Better caching policies
2. Using MongoDb or noSQL DBs in general will be super benificial.
3. Image downloading can be offloaded and be stored in some blob storages like s3 etc.

