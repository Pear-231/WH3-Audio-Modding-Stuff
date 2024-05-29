function getBnkFromDialogueEvent(dialogueEvent) 
{
  Logger.log(`Running: getBnkFromDialogueEvent()`);

  if (dialogueEvent.includes("battle_vo_conversation"))
      return "battle_vo_conversational";

  else if (dialogueEvent.includes("battle_vo_order"))
      return "battle_vo_orders";

  else if (dialogueEvent.includes("campaign_vo_cs") || dialogueEvent.includes("Campaign_CS"))
      return "campaign_vo_conversational";

  else if (dialogueEvent.includes("campaign_vo") || dialogueEvent === "gotrek_felix_arrival" || dialogueEvent === "gotrek_felix_departure")
      return "campaign_vo";

  else if (dialogueEvent.includes("frontend_vo"))
      return "frontend_vo";

  else if (dialogueEvent === "Battle_Individual_Melee_Weapon_Hit")
      return "battle_individual_melee";
}

function clearDataValidationsOnRow(sheet, row)
{
  Logger.log(`Running: clearDataValidationsOnRow()`);

  sheet.getRange(row, 2, 1, sheet.getMaxColumns() - 1).clearDataValidations();
}

function clearDataOnRow(sheet, row)
{
  Logger.log(`Running: clearDataOnRow()`);

  sheet.getRange(row, 2, 1, sheet.getMaxColumns() - 1).clear();
}

function getPreviousDialogueEventRow(sheet, row, column)
{  
  Logger.log(`Running: previousDialogueEventRow()`);

  var range = sheet.getRange(1, column, row, 1);
  var values = range.getValues();
  
  for (var i = row - 1; i >= 0; i--) {
    var cellValue = values[i][0];
    if (cellValue !== undefined && cellValue !== "" && cellValue !== "State Path" && cellValue !== "Sounds")
      return i + 1;
  }
}

function createDictionaryFromSheet(sheetName)
{
  Logger.log(`Running: createDictionaryFromSheet()`);
  Logger.log(`Creating dictionary from sheet: ${sheetName}`);

  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName);
  var lastColumn = sheet.getLastColumn();
  var lastRow = sheet.getLastRow();
  var dictionary = {};
  
  // Loop through each non-empty column
  for (var col = 1; col <= lastColumn; col++) {
    var key = sheet.getRange(2, col).getValue(); // Get the value in row 2 of the current column as key

    if (key) {
      dictionary[key] = [];
      var numRows = lastRow - 2;

      // Check if there are values below row 2
      if (numRows > 0) {
        var values = sheet.getRange(3, col, numRows, 1).getValues(); // Get values below row 2 in the current column

        for (var i = 0; i < values.length; i++) {
          if (values[i][0] !== "")
            dictionary[key].push(values[i][0]); // Add non-empty value to the list for the current key
        }
      }
    }
  }
  
  Logger.log(dictionary); // Output the dictionary to the Logs

  return dictionary;
}

function mergeDictionaries(vanillaStates, moddedStates)
{  
  Logger.log(`Running: mergeDictionaries()`);

  if (Object.keys(moddedStates).length === 0)
    return vanillaStates;

  if (Object.keys(vanillaStates).length === 0)
    return moddedStates;

  var allStates = {};

  for (var key in moddedStates)
  {
    if (vanillaStates.hasOwnProperty(key))
      allStates[key] = moddedStates[key].concat(vanillaStates[key]);
    
    else
      allStates[key] = moddedStates[key];
  }

  // Include remaining keys from vanillaStates that are not in moddedStates
  for (var key in vanillaStates)
  {
    if (!moddedStates.hasOwnProperty(key))
      allStates[key] = vanillaStates[key];
  }

  Logger.log(allStates); // Output the merged dictionary to the Logs

  return allStates;
}

function getColumnRangeByValue(sheetName, searchValue, headersRow, useEmptyCells)
{
  Logger.log(`Running: getColumnRangeByValue()`);

  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName);
  var lastColumn = sheet.getLastColumn();
  var headers = sheet.getRange(headersRow, 1, 1, lastColumn).getValues()[0];
  var columnIndex = headers.indexOf(searchValue) + 1;
  
  if (columnIndex > 0)
  {
    var range = sheet.getRange(1, columnIndex, 1, 1);
    var column = range.getA1Notation().match(/([A-Z]+)/)[0]
    Logger.log(range.getA1Notation().match(/([A-Z]+)/)[0]);
    
    if (useEmptyCells)
    {
      var searchValueRange = sheet.getRange(`${column}${headersRow + 1}:${column}`)
      return searchValueRange;
    }

    else
    {
      var lastRow = sheet.getLastRow();
      var columnValues = sheet.getRange(1, columnIndex, lastRow, 1).getValues();
      
      // Iterate backwards to find the last non-empty row
      for (var i = columnValues.length - 1; i >= 0; i--)
        if (columnValues[i][0] !== "") 
        {
          lastNonEmptyRow = i + 1; 
          var searchValueRange = sheet.getRange(`${column}${headersRow + 1}:${column}${lastNonEmptyRow}`)
          return searchValueRange;
        }
    }
  }

  else
  {
    Logger.log(`Could not find '${searchValue}' in headers.`);
    return null;
  }
}
