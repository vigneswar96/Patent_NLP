const { Builder, By, Key, until } = require('selenium-webdriver');
const chrome = require('selenium-webdriver/chrome');
const fs = require('fs');
const assert = require('assert');
const readlineSync = require('readline-sync');
const path = require('path');

// This is a code that works on Google Patents. 
async function exampleAutomation() {
    const downloadPath = 'E:\\Walsh_work\\Google_patent_Downloads\\1)Patent_pdf';
    const textPath = 'E:\\Walsh_work\\Google_patent_Downloads\\2)Patent_Text_json';
    // Set up Chrome options
    const chromeOptions = new chrome.Options();
    chromeOptions.setUserPreferences({
        'download.default_directory': downloadPath, 
        'profile.default_content_settings.popups': 0, //    Disable pop-ups
        'download.prompt_for_download': false,//    Disable download prompt
        'safebrowsing.enabled': false,//   Disable safebrowsing
        'printing.enabled':false, //Disable printing
        "plugins.always_open_pdf_externally": true,
        "--remote-debugging-port=9222": true,
        "--no-sandbox": true,
    });
    //chromeOptions.addArguments('--headless');  // This is commented out because we want to see the browser window
    // Create a new WebDriver instance
    const driver = await new Builder()
        .forBrowser('chrome')
        .setChromeOptions(chromeOptions)
        .build();
    try {
        // Navigate to the website
        await driver.get('https://patents.google.com/');
        const args = process.argv.slice(2);// what is argv.slice(2) doing here?  It is reading the command line arguments passed to the script.
        const patentNumber = args[0];// Read the argument from the command line 
        console.log('Patent number:', patentNumber);
        const searchInput = By.xpath('//*[@id="searchInput"]'); 
        await driver.wait(until.elementLocated(searchInput), 10000);
        await driver.findElement(searchInput).sendKeys(patentNumber, Key.RETURN); 
        await driver.wait(until.elementLocated(By.xpath('//*[@id="wrapper"]')), 5000); 
        const grabpatent = await driver.findElement(By.xpath('//*[@id="wrapper"]')).getText();
        const jsonContent = JSON.stringify(grabpatent, null, 2);
        const textFilePath = path.join(textPath, `${patentNumber}_patenttext.json`);
        await new Promise(resolve => setTimeout(resolve, 5000));
        fs.writeFileSync(textFilePath, jsonContent, 'utf8');
        await driver.wait(until.elementLocated(By.xpath('//*[@id="wrapper"]/div[1]/div[2]/section/header/div/a')), 10000);    
        await driver.findElement(By.xpath('//*[@id="wrapper"]/div[1]/div[2]/section/header/div/a')).click();
        await new Promise(resolve => setTimeout(resolve, 20000)); // Wait for 20 seconds            
        } finally {
            // Perform cleanup operations
            await driver.quit();
        }
};
exampleAutomation()