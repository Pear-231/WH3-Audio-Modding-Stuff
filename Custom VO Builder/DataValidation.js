function loadStates()
{
  Logger.log(`Running: loadStates()`);

  populateStatesDataValidation()
}

function loadDialogueEvents() 
{
  Logger.log(`Running: loadDialogueEvents()`);

  populateDialogueEventsValidation()
}

function handleDropDownValidation(e) 
{
  Logger.log(`Running: handleDropDownValidation()`);

  var sheet = e.source.getActiveSheet();
  var sheetName = sheet.getName()

  if (sheetName === "Battle VO" || (sheetName === "Campaign VO") || (sheetName === "Conversational Battle VO") || (sheetName === "Conversational Campaign VO") || (sheetName === "Frontend VO"))
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
        clearDataValidationsOnRow(sheet, row)

      if (cellValue !== undefined && cellValue !== "")
      {
        if (cellValue !== "Sounds" && cellValue !== "State Path")
          populateStateGroups(sheet, row, column)

        else if (cellValue === "State Path")
          {
            clearDataValidationsOnRow(sheet, row)
            createStatePathDropDowns(sheet, row, column)
          }
      }
    }

    createSoundsOnlyDropDown(e)
  }
}

function populateStateGroups(sheet, row, column)
{
  Logger.log(`Running: populateStateGroups()`);

  clearDataValidationsOnRow(sheet, row)
  
  // Get the named range value from the cell in column A
  var namedRangeName = sheet.getRange(row, column).getValue();
  var namedRange = SpreadsheetApp.getActiveSpreadsheet().getRangeByName(namedRangeName);

  if (namedRange)
  {
    // Retrieve the values from the named range
    var rangeValues = namedRange.getValues();

    // Flatten the values into a single array
    var flattenedValues = rangeValues.flat();

    // Resize the target range to fit all the values
    sheet.getRange(row, 2, 1, flattenedValues.length).setValues([flattenedValues]);
  }
}

function createStatePathDropDowns(sheet, row, column)
{
  Logger.log(`Running: createStatePathDropDowns()`);

  var previousDialogueEventRow = getPreviousDialogueEventRow(sheet, row, column);
  Logger.log(`previousDialogueEventRow: ${previousDialogueEventRow}`);

  var dialogueEvent = sheet.getRange(previousDialogueEventRow, column).getValue();
  Logger.log(`dialogueEvent: ${dialogueEvent}`);

  var dialogueEventsSheet = "Dialogue Events";
  var headersRow = 2
  var dialogueEventRange = getColumnRangeByValue(dialogueEventsSheet, dialogueEvent, headersRow, false);
  var dialogueEventRangeAddress = dialogueEventRange.getA1Notation();
  Logger.log(`dialogueEventRangeAddress: ${dialogueEventRangeAddress}`);

  var dialogueEventSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(dialogueEventsSheet);
  var fullDialogueEventRange = dialogueEventSheet.getRange(dialogueEventRangeAddress);
  var dialogueEventValues = fullDialogueEventRange.getValues();
  Logger.log(`dialogueEventValues: ${dialogueEventValues}`);

  var flattenedValues = dialogueEventValues.flat();
  var flattenedValuesLength = flattenedValues.length;
  Logger.log(`flattenedValuesLength: ${flattenedValuesLength}`);

  var validationRules = []; // Create an array to store the validation rules

  // Create the drop downs and collect validation rules
  for (var i = 0; i < flattenedValuesLength; i++) 
  {
    var targetCell = sheet.getRange(row, i + 1 + column); // Adjusting column index by adding 'column'
    var stateGroup = flattenedValues[i];
    Logger.log(`stateGroup: ${stateGroup}`);
    
    var statesSheet = "States Data Validation";
    var headersRow = 1
    var stateGroupRange = getColumnRangeByValue(statesSheet, stateGroup, headersRow, true);
    var stateGroupRangeAddress = stateGroupRange.getA1Notation();
    Logger.log(`stateGroupRangeAddress: ${stateGroupRangeAddress}`);

    var statesSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(statesSheet);
    var fullStateGroupRange = statesSheet.getRange(stateGroupRangeAddress);

    var rule = SpreadsheetApp.newDataValidation().requireValueInRange(fullStateGroupRange).setAllowInvalid(false).build(); // Build data validation rule
    validationRules.push({ cell: targetCell, rule: rule }); // Store the validation rule and the corresponding target cell
  }

  // Apply all collected validation rules at once
  for (var j = 0; j < validationRules.length; j++)
    validationRules[j].cell.setDataValidation(validationRules[j].rule);
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