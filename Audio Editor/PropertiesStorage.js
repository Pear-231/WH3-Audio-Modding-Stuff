function storeDialogueEvents()
{
    Logger.log(`Running: storeDialogueEvents()`);

    var sheetName = "Dialogue Events Data Validation";
    var column = "A";
    var headerRow = 1;

    var result = getColumnValues(sheetName, column, headerRow);
    var dialogueEvents = result.list;

    setSavedValue("dialogueEvents", dialogueEvents)
    Logger.log(`${getSavedValue("dialogueEvents")}`);
}

function storeDialogueEventStateGroups()
{
    Logger.log(`Running: storeDialogueEventStateGroups()`);

    var dialogueEventStateGroups = {}

    var sheetName = "Dialogue Events";
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName);
    var dataRange = sheet.getDataRange();
    var lastColumn = dataRange.getLastColumn();
    var headerRow = 2; 

    for (var column = 1; column <= lastColumn; column++)
    {
        var columnLetter = columnToLetter(column)
        var result = getColumnValues(sheetName, columnLetter, headerRow);
        var dialogueEvent = result.header
        var stateGroups = result.list
        dialogueEventStateGroups[dialogueEvent] = stateGroups
    }

    setSavedValue("dialogueEventStateGroups", dialogueEventStateGroups)

    var savedValue = getSavedValue("dialogueEventStateGroups")
    for (var key in savedValue) {
        Logger.log(`${key}: ${savedValue[key]}`);
    }
}

function setSavedValue(SavedValueName, valueToStore)
{
    Logger.log(`Running: setSavedValue()`);

    var userProperties = PropertiesService.getUserProperties();
    userProperties.setProperty(SavedValueName, JSON.stringify(valueToStore));
}

function getSavedValue(SavedValueName)
{
    Logger.log(`Running: getSavedValue()`);

    var userProperties = PropertiesService.getUserProperties();
    var SavedValueJson = userProperties.getProperty(SavedValueName);
    var SavedValue = JSON.parse(SavedValueJson)

    return SavedValue;
}