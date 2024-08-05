const { Builder, By, Key, until } = require('selenium-webdriver');
const webdriver = require('selenium-webdriver');
const firefox = require('selenium-webdriver/firefox');
const fs = require('fs');
const assert = require('assert');
const readlineSync = require('readline-sync');
const path = require('path');

// This is a code that works on Google Patents. 

async function exampleAutomation() {
    const textPath = 'E:\\Walsh_work\\Google_patent_Downloads\\Patent_Text_json';
    const downloadPath = 'E:\\Walsh_work\\Google_patent_Downloads\\Patent_pdf';
    // Set up Chrome options
    const firefoxOptions = new firefox.Options();
    const firefoxProfile = new firefox.Profile();
    firefoxOptions.useGeckoDriver;


    const driver = await new Builder()
        .forBrowser('firefox')
        .setFirefoxOptions(firefoxOptions)
        .build();
    //firefoxOptions.addArguments('--headless');  // This is commented out because we want to see the browser window
    // Create a new WebDriver instance

    try {
        // Navigate to the website
        await driver.get('https://patents.google.com/');
        const args = process.argv.slice(2);// what is argv.slice(2) doing here?  It is reading the command line arguments passed to the script.
        const patentNumber  = args[0]; // Read the argument from the command line 
        console.log('Patent number:', patentNumber);
        const searchInput = By.xpath('//*[@id="searchInput"]'); 
        await driver.wait(until.elementLocated(searchInput), 10000);
        await driver.findElement(searchInput).sendKeys(patentNumber, Key.RETURN); 
        await driver.wait(until.elementLocated(By.xpath('//*[@id="wrapper"]')), 5000); 
        const grabpatent = await driver.findElement(By.xpath('//*[@id="wrapper"]')).getText();
        const jsonContent = JSON.stringify(grabpatent, null, 2);
        const textFilePath = path.join(textPath, `${patentNumber}_patenttext.json`);
        fs.writeFileSync(textFilePath, jsonContent, 'utf8');
        //await driver.wait(until.elementLocated(By.xpath('//*[@id="wrapper"]/div[1]/div[2]/section/header/div/a')), 10000);    
        //await driver.findElement(By.xpath('//*[@id="wrapper"]/div[1]/div[2]/section/header/div/a')).click(); 
        //const windowHandles = await driver.getAllWindowHandles();
        //await driver.switchTo().window(Array.from(windowHandles)[1]);
        //await driver.wait(until.elementLocated(By.xpath('//*[@id="download"]')), 10000);
        //await driver.findElement(By.xpath('//*[@id="download"]')).click();
        await new Promise(resolve => setTimeout(resolve, 20000)); // Wait for 20 seconds            
        } finally {
            // Perform cleanup operations
            await driver.quit();
        }
};
exampleAutomation()