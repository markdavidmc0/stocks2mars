# stocks2mars
Social media trading bot based on comments from influencers.

## Prototype (current)
Scrape Elon Musk's Twitter feed, looking for crypto investment suggestions or comments.

1) Async check for latest Tweet, predict if crypto was mentioned alongwith sentiment score. 
2) Async save Tweet, prediction and score to Google Sheet.
3) Unit and integration tests using Python unittest. Include @integration and @unit flags where appropriate. Use Python mock built-in for unit tests.
4) CI/CD using Github actions:
    - runs unit test on feature push.
    - runs unit and integration tests on merge as gatekeeper.
    - deploy single docker contaniner scraper/analyser that uses multiprocessing.
    - PROD environment only.

*Note: Social media platform and user account to scrape from must be moduler so that other options can be plugged in in future. 

## MVP (31 March 2021)
Same as Prototype, but including but the following changes:

1) Add async POST to API with Tweet, prediction and confidence metrics.
2) Create Django app with list page endpoint and Postgres backend with single view of the data collected in 1).
3) Move Google Sheet integration from scraper and make that a sync job with API/database.
4) Add STG environment to CI/CD pipeline. Each environment should have its own database.

## First Major Release (31 May 2021)
Fully functional trading app that keeps track of influencer comments and user trades and actually makes trades independently in certain circumstances. 

Backend: Docker, Django, GCS, Google Sheets, Kubernetes, Postgres.
Frontend: Bootstrap, Django templates, DRF.

### Walkthrough
1) Build corpus of cryptos (cron job daily update) which saves to DB. This includes market volume, ranking and current crypto price.
2) Check influencer feed every few minutes, if not same as cached latest feed item then save to DB and add feed item text to queue.
3) Read messages from queue, predict crypto match. If medium confidence, send email alert and save to DB. If high confidence, send alert and make finance trade (if between 12pm and 6am) and save result to DB. A check needs to be made against the last price data point for this stock in comparison to now to see if trade is viable.
4) Async monitor stock price after trade, calculate % increase metric based on ranking/market volume/price and sell when that trigger is met. 

### App Views
1) Cryto index - list page (searchable).
2) Twitter query - list page.
3) Alerts query - list page.
4) Trades query - list page (success/fail status updates inc.).
5) Stock watch dash page. This has near real-time price for each traded stock. Basic trade options are included here (buy/sell).

### Limitations
1) The first major release will support Twitter and Cryptos only. Although, some design effort must ensure that other options can be plugged in for both social media platform and types of trade (on LSE for example).
2) Only the Binance API will be supported initially due to ease of use and familiarity.

