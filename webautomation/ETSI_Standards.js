const { Builder, By, Key, until } = require('selenium-webdriver');
const chrome = require('selenium-webdriver/chrome');
const fs = require('fs');
const assert = require('assert');
const readlineSync = require('readline-sync');
const path = require('path');
const { time } = require('console');

async function exampleAutomation() {
    const downloadPath = 'D:\\ETSI-Standards';

    // Set up Chrome options
    const chromeOptions = new chrome.Options();
    chromeOptions.setUserPreferences({
        'download.default_directory': downloadPath,
        'profile.default_content_settings.popups': 0, // Disable pop-ups
        'download.prompt_for_download': false, // Disable download prompt
        'safebrowsing.enabled': false, // Disable safebrowsing
        'printing.enabled': false, // Disable printing
        "plugins.always_open_pdf_externally": true, // Automatically open PDFs
        "--remote-debugging-port=9222": true,
        "--no-sandbox": true,
    });
    // Uncomment the next line if you want to run Chrome headlessly
    //chromeOptions.addArguments('--headless');


    // Create a new WebDriver instance
    const driver = await new Builder()
        .forBrowser('chrome')
        .setChromeOptions(chromeOptions)
        .build();

    try {
        // Navigate to the website
        const url = process.argv[2];
        if(!url) {
            console.error('No URL Provided. Usage: node scriptName.js <URL>');
            return;
        }

        await driver.get(url);
       
        // Wait for the element to be located and click it <a href="https://www.etsi.org/deliver/etsi_ts\100900_100999\100902\07.04.00_60\ts_100902v070400p.pdf" target="_blank"><img alt="Download Pdf Document available" border="0" src="images/PDA_Pdf.gif" id="DownloadPdf" name="DownloadPdf"></a>
        const link = await driver.wait(until.elementLocated(By.xpath('/html/body/table[4]/tbody/tr[2]/td[1]/table/tbody/tr[1]/td/a')), 25000).click();
        // Optionally, wait for some condition post-click, such as a new page to be loaded or a download to start
        // Example: await driver.wait(until.titleIs('Expected Page Title'), 10000);

        console.log('Action completed.');
    } finally {
        // Close the browser after a delay to observe the result
        setTimeout(() => {
            driver.quit();
        }, 25000); // Adjust delay as needed to observe the result before closing
    }
}

exampleAutomation().catch(console.error);
