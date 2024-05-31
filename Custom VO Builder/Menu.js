function createMenu()
{
    var ui = SpreadsheetApp.getUi();
    ui.createMenu('Custom VO Builder')
        .addItem('Load States', 'loadStates')
        .addItem('Load Dialogue Events', 'loadDialogueEvents')
        .addToUi();
}