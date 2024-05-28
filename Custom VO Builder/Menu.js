function onOpen() 
{
  var ui = SpreadsheetApp.getUi();
  ui.createMenu('Custom VO Builder')
      .addItem('Load Vanilla Data', 'loadVanillaData')
      .addItem('Load Modded States', 'loadModdedStates')
      .addItem('Unload All Data', 'removeAllNamedRanges')
      .addToUi();
}