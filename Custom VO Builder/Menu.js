function onOpen() 
{
  Logger.log(`Running: onOpen()`);

  var ui = SpreadsheetApp.getUi();
  ui.createMenu('Custom VO Builder')
      .addItem('Load Dialogue Events', 'loadDialogueEvents')
      .addItem('Load States', 'loadStates')
      .addToUi();
}