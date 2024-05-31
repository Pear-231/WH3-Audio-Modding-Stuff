function onOpen() 
{
  Logger.log(`Running: onOpen()`);

  createMenu()
}

function onSelectionChange(e)
{
  showSidebar() 
}

function showSidebar()
{
  var html = HtmlService.createHtmlOutputFromFile('sideBarTest')
      .setTitle('Custom Sidebar')
      .setWidth(300);
  SpreadsheetApp.getUi().showSidebar(html);
}