function loadStates()
{
  Logger.log(`Running: loadStates()`);
  populateStatesDataValidation()
}

function loadDialogueEvents() 
{
  Logger.log(`Running: loadDialogueEvents()`);
  storeDialogueEvents()
  storeDialogueEventStateGroups()
  populateDialogueEventsValidation() 
}

function handleDropDownValidation(e) 
{
  Logger.log(`Running: handleDropDownValidation()`);

  var sheet = e.source.getActiveSheet();
  var sheetName = sheet.getName()

  if (sheetName === "Battle VO Builder" || sheetName === "Campaign VO Builder" || sheetName === "Conversational Battle VO Builder" || sheetName === "Conversational Campaign VO Builder" || sheetName === "Frontend VO Builder")
  {
    var cell = e.range;
    var column = cell.getColumn()
    var row = cell.getRow();

    if (column === 1 && row >= 2)  
    {
      var cellValue = e.value;
      var previousCellValue = e.oldValue;
      Logger.log(`cellValue: ${cellValue}`);
      Logger.log(`previousCellValue: ${previousCellValue}`);

      if (previousCellValue == "State Path")
        sheet.getRange(row, 2, 1, sheet.getMaxColumns() - 1).clearDataValidations();
      
      if (cellValue !== undefined && cellValue !== "")
      {
        var dialogueEvents = getSavedValue("dialogueEvents")

        if (dialogueEvents.includes(cellValue))
        {
          sheet.getRange(row, 1, 3, sheet.getMaxColumns() - 1).clearDataValidations();
          sheet.getRange(row, 2, 3, sheet.getMaxColumns() - 1).clearContent();

          var statePathCell = sheet.getRange(row + 1, column);
          statePathCell.setValue("State Path");
    
          var soundsCell = sheet.getRange(row + 2, column);
          soundsCell.setValue("Sounds");
          
          var stateGroups = populateStateGroups(sheet, row, column)
          createStatePathDropDowns(sheet, row + 1, column);

          sheet.getRange(row, 2, 1, stateGroups.length).setValues([stateGroups]);
        }

        else if (cellValue === "State Path")
        {
          sheet.getRange(row, 1, 2, sheet.getMaxColumns() - 1).clearDataValidations();
          sheet.getRange(row, 2, 2, sheet.getMaxColumns() - 1).clearContent();

          var soundsCell = sheet.getRange(row + 1, column);
          soundsCell.setValue("Sounds");

          createStatePathDropDowns(sheet, row, column);
        }
      }
    }

    applyDataValidationToEmptyCells(sheet)
  }
}

function populateStateGroups(sheet, row, column)
{
  Logger.log(`Running: populateStateGroups()`);

  var dialogueEvent = sheet.getRange(row, column).getValue();
  Logger.log(`dialogueEvent: ${dialogueEvent}`);

  var dialogueEventStateGroups = getSavedValue("dialogueEventStateGroups")
  var flattenedValues = dialogueEventStateGroups[dialogueEvent].flat();

  return flattenedValues;
}

function createStatePathDropDowns(sheet, row, column)
{
  Logger.log(`Running: createStatePathDropDowns()`);

  var previousDialogueEventRow = getPreviousDialogueEventRow(sheet, row, column);
  Logger.log(`previousDialogueEventRow: ${previousDialogueEventRow}`);

  var dialogueEvent = sheet.getRange(previousDialogueEventRow, column).getValue();
  Logger.log(`dialogueEvent: ${dialogueEvent}`);

  var dialogueEventStateGroups = getSavedValue("dialogueEventStateGroups")
  var stateGroups = dialogueEventStateGroups[dialogueEvent]

  var flattenedValues = stateGroups.flat();
  var flattenedValuesLength = flattenedValues.length;

  var dropDownsValidation = [];

  for (var i = 0; i < flattenedValuesLength; i++) 
  {
    var targetCell = sheet.getRange(row, i + 1 + column);
    var stateGroup = flattenedValues[i];
    Logger.log(`stateGroup: ${stateGroup}`);
    
    var statesSheet = "States Data Validation";
    var headersRow = 1
    var stateGroupRange = getColumnRangeByValue(statesSheet, stateGroup, headersRow, true);
    var stateGroupRangeAddress = stateGroupRange.getA1Notation();
    Logger.log(`stateGroupRangeAddress: ${stateGroupRangeAddress}`);

    var statesSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(statesSheet);
    var fullStateGroupRange = statesSheet.getRange(stateGroupRangeAddress);

    var rule = SpreadsheetApp.newDataValidation().requireValueInRange(fullStateGroupRange).setAllowInvalid(false).build();
    dropDownsValidation.push({ cell: targetCell, rule: rule });
  }

  for (var j = 0; j < dropDownsValidation.length; j++)
    dropDownsValidation[j].cell.setDataValidation(dropDownsValidation[j].rule);
}

function populateDialogueEventsValidation() 
{
  Logger.log(`Running: populateDialogueEventsValidation()`);

  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Dialogue Events Data Validation");
  var parentBnkColumn = sheet.getRange("B2:B" + sheet.getLastRow());
  parentBnkColumn.clear();

  var lastRow = sheet.getLastRow();
  var dialogueEvents = sheet.getRange("A2:A" + lastRow).getValues();
  var results = [];

  for (var i = 0; i < dialogueEvents.length; i++) 
  {
    var dialogueEvent = dialogueEvents[i][0];
    var result = getBnkFromDialogueEvent(dialogueEvent);
    Logger.log(`dialogueEvent: ${dialogueEvent}`);
    results.push([result]);
  }

  var outputRange = sheet.getRange(2, 2, results.length, 1); // Start from B2, 1 column wide
  outputRange.setValues(results);
}

function populateStatesDataValidation()
{
  Logger.log(`Running: populateStatesDataValidation()`);

  var vanillaStates = createDictionaryFromSheet("Vanilla States");
  var moddedStates = createDictionaryFromSheet("Modded States");
  var allStates = mergeDictionaries(vanillaStates, moddedStates);

  var sheetName = "States Data Validation";
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName);

  // Clear existing data in the sheet
  sheet.clear();

  // Set column headers
  var headers = Object.keys(allStates);
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);

  // Determine the number of rows needed
  var numRows = Math.max.apply(null,
    headers.map(
      function(header)
      {
        return allStates[header].length;
      }
    )
  );

  // Prepare data to be pasted all at once
  var data = [];
  for (var i = 0; i < numRows; i++)
  {
    var rowData = [];
    headers.forEach(
      function(header)
      {
        rowData.push(allStates[header][i] || ""); // Fill empty cells with empty string
      }
    );
    data.push(rowData);
  }

  // Set the data in the sheet
  if (data.length > 0)
    sheet.getRange(2, 1, data.length, headers.length).setValues(data);
}

function applyDataValidationToEmptyCells(sheet)
{
  Logger.log(`Running: applyDataValidationToEmptyCells()`);

  var sheetName = sheet.getName();
  var applicationRange = sheet.getRange('A2:A');
  var validationSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Dialogue Events Data Validation");
  var validationRange;

  if (sheetName === "Battle VO Builder")
    validationRange = validationSheet.getRange("H2:H");

  else if (sheetName === "Campaign VO Builder")
    validationRange = validationSheet.getRange("I2:I");

  else if (sheetName === "Conversational Battle VO Builder")
    validationRange = validationSheet.getRange("G2:G");

  else if (sheetName === "Conversational Campaign VO Builder")
    validationRange = validationSheet.getRange("F2:F");

  else if (sheetName === "Frontend VO Builder")
    validationRange = validationSheet.getRange("J2:J");

  else
    return;

  var values = applicationRange.getValues();
  var dataValidations = applicationRange.getDataValidations();
  
  var rangesToValidate = [];

  for (var i = 0; i < values.length; i++)
  {
    if (values[i][0] === "" && !dataValidations[i][0])
      rangesToValidate.push(applicationRange.getCell(i + 1, 1));
  }

  var rule = SpreadsheetApp.newDataValidation().requireValueInRange(validationRange).setAllowInvalid(false).build();
  rangesToValidate.forEach(
    function(cell)
    {
      cell.setDataValidation(rule);
    }
  );
}