const pupeteer = require("puppeteer");
const puppeteerExtra = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
const { writeFile } = require('fs');


(async () => {
    const browser = await pupeteer.launch({ headless: false });
    const page = await browser.newPage();
    await page.goto("https://ppubs.uspto.gov/pubwebapp/");

    await page.evaluate(() => {
        document.querySelector("#search-content > div > div > div.leftPane.ui-resizable > div.searchTop > div > div > trix-editor");
    })
    //await page.click('a[href="/login"]');
    await page.waitForSelector('#search-content > div > div > div.leftPane.ui-resizable > div.searchTop > div > div > trix-editor');
    await page.type('#search-content > div > div > div.leftPane.ui-resizable > div.searchTop > div > div > trix-editor','20130089108', { delay: 200 });
    await page.click('#search-btn-search');

    await new Promise(resolve => setTimeout(resolve, 5000)); // Wait for 5 seconds

    const grabpatent = await page.evaluate(() => {
        const patent = document.querySelector("#documentViewer-content > div.container.widgetToolbar-horizontal-top > div.textViewer > div > div.realdocument > div.docMetadata > div > div") ; 
        return patent ? patent.innerText : 'not found';
    })
    console.log(grabpatent);

    

    //document.querySelector("#slickgrid_400612-title-row-0-cell-9 > button")

})();

