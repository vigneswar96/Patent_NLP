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


let btn1, btn2;

// Wait for 10 seconds before assigning values to btn1 and btn2
await new Promise(resolve => {
    setTimeout(() => {
        //btn1 = document.querySelector("#documentViewer-content > div.container.widgetToolbar-horizontal-top > div.widgetToolbar > div.widgetToolbar-buttonWrapper > button.button.icon.icon-text");
        btn1 = document.querySelector("#documentViewer-content > div.container.widgetToolbar-horizontal-top > div.widgetToolbar > div > button.button.icon.icon-text > span.icon");
        btn2 = document.querySelector("#documentViewer-content > div.container.widgetToolbar-horizontal-top > div.widgetToolbar > div.widgetToolbar-buttonWrapper > button.button.icon.icon-print");
        resolve();
    }, 10000);
});

// Wait for an additional 5 seconds (if needed)
await new Promise(resolve => setTimeout(resolve, 5000));

// Now you can safely click btn1 and btn2
await page.click(btn1); 
await page.click(btn2);
    


})();

//document.querySelector("#documentViewer-content > div.container.widgetToolbar-horizontal-top > div.widgetToolbar > div > button.button.icon.icon-text")
//document.querySelector("#documentViewer-content > div.container.widgetToolbar-horizontal-top > div.widgetToolbar > div > button.button.icon.icon-text")