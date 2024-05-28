function handleDropDownValidation(e) 
{
  var sheet = e.source.getActiveSheet();
  var sheetName = sheet.getName()
  var cell = e.range;
  var cellValue = e.value;
  var row = cell.getRow();
  var column = cell.getColumn()

  if (sheetName === "Battle VO" || (sheetName === "Campaign VO") || (sheetName === "Conversational Battle VO") || (sheetName === "Conversational Campaign VO") || (sheetName === "Frontend VO"))
  {
    Logger.log(`Sheet: ${sheetName}`);

    if (column === 1 && row >= 2) 
    {
      Logger.log(`Column: ${sheetName}, Row: ${row}`);
      var rangeToClear = sheet.getRange('B:L');
      removeValidationFromRange(rangeToClear)

      if (cellValue !== "" && cellValue !== "Sounds" && cellValue !== "State Path")
        populateStateGroups(sheet, row)

      else if (cellValue === "State Path") 
        createStatePathDropDowns(sheet, row)
    }
  }
}

function populateStateGroups(sheet, row)
{
  cleanRow(sheet, row)
  sheet.getRange(row, 2).setFormula('=TRANSPOSE(INDIRECT(A' + row + '))');
}

function createStatePathDropDowns(sheet, row)
{
  var targetRow = populateStatesDataValidation(sheet, row);
  var lastColumn = sheet.getLastColumn();
  var dataValidationSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('States Data Validation');
  
  for (var i = 2; i <= lastColumn; i++) 
  {
    var targetCell = sheet.getRange(row, i);
    var cellCheck = sheet.getRange(targetRow, i);

    if (cellCheck.getValue() !== "") 
    {
      targetCell.clear().clearDataValidations(); 
      var columnIndex = i - 2; // Calculate the index for data validation range
      var validationRange = dataValidationSheet.getRange(1, columnIndex + 1, dataValidationSheet.getLastRow(), 1); // Get the corresponding validation range for the current column
      var rule = SpreadsheetApp.newDataValidation().requireValueInRange(validationRange).setAllowInvalid(false).build(); // Build data validation rule
      targetCell.setDataValidation(rule); // Apply data validation rule to the cell
    }
  }
}

function populateStatesDataValidation(sheet, row) 
{
  var dataValidationSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('States Data Validation');

  dataValidationSheet.getRange('A1:L1').clear(); // Clear existing data
  
  var conditionMet = false;
  for (var i = 0; ; i++) 
  {
      var checkColumn = String.fromCharCode(65 + i % 26); // Get the column letter of the source cell
      var column = String.fromCharCode(65 + i); // Get column letter (A-L)

      while (row >= 1) 
      {
        var sourceCell = sheet.getRange(checkColumn + row);
        var cellValue = sourceCell.getValue();

        if (cellValue !== undefined && cellValue !== "" && cellValue !== "State Path" && cellValue !== "Sounds") 
        {
          conditionMet = true;
          break;
        }

        row--;
      }

      if (conditionMet) 
        break;
  }

  for (var g = 0; g < 12; g++) // Start from column A (0) and end at column L (12)
  {
    var column = String.fromCharCode(65 + g); // Get column letter (A-L)
    var sourceColumn = String.fromCharCode(65 + (g + 1)); // Get the column letter of the source cell
    
    var formula = "=INDIRECT('" + sheet.getName() + "'!" + sourceColumn + row + ")";
    dataValidationSheet.getRange(column + '1').setFormula(formula);
  }

  return row;
}

function populateDialogueEventValidation() 
{
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Dialogue Events Data Validation");
  var lastRow = sheet.getLastRow();
  var dialogueEvents = sheet.getRange("A2:A" + lastRow).getValues();
  var results = [];

  for (var i = 0; i < dialogueEvents.length; i++) 
  {
    var dialogueEvent = dialogueEvents[i][0];
    var result = getBnkFromDialogueEvent(dialogueEvent);
    results.push([result]);
  }

  var outputRange = sheet.getRange(2, 2, results.length, 1); // Start from B2, 1 column wide
  outputRange.setValues(results);
}

function loadModdedStates()
{
  createNamedRanges("Vanilla & Modded States", 1);
}

function loadVanillaData() 
{
  createNamedRanges("Vanilla States", 2);
  createNamedRanges("Dialogue Events", 2);
  populateDialogueEventValidation()
}