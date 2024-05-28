function getBnkFromDialogueEvent(dialogueEvent) 
{
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

// Clear content and data validations
function cleanRow(sheet, row)
{
    for (var i = 2; i <= 12; i++) // Start from column B (2) and end at column L (12)
        sheet.getRange(row, i).clear().clearDataValidations();
}
function removeValidationFromRange(rangeToClear)
{
  rangeToClear.clearDataValidations();
}

function createNamedRanges(sheetName, headersRow) 
{
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName);
  var lastColumn = sheet.getLastColumn();
  var headerRange = sheet.getRange(headersRow, 1, 1, lastColumn);
  var headers = headerRange.getValues()[0];

  // Filter out empty or whitespace-only headers
  headers = headers.filter(
    function(header) 
    {
      return header && header.toString().trim() !== "";
    }
  );

  Logger.log("Filtered Headers: " + headers.join(", "));

  for (var i = 0; i < headers.length; i++) 
  {
    var header = headers[i];
    Logger.log("Processing header: " + header);
    var columnValues = [];
    var values = sheet.getRange(headersRow + 1, i + 1, sheet.getLastRow() - headersRow, 1).getValues();

    for (var j = 0; j < values.length; j++) 
    {
      if (values[j][0] !== "") 
        columnValues.push(values[j][0]);
    }

    // Only create a named range if there are non-empty cells
    if (columnValues.length > 0) 
    {
      // Define range for non-empty cells starting from row 2
      var range = sheet.getRange(headersRow + 1, i + 1, columnValues.length, 1);
      
      // Create or update named range
      var namedRange = sheet.getParent().getNamedRanges().filter(
        function(namedRange) 
        {
          return namedRange.getName() === header;
        }
      );

      if (namedRange.length == 0) 
      {
        Logger.log("Creating new named range: " + header);
        sheet.getParent().setNamedRange(header, range);
      } 
      
      else 
      {
        Logger.log("Updating existing named range: " + header);
        namedRange[0].remove();
        sheet.getParent().setNamedRange(header, range);
      }
    } 

    else 
      Logger.log("No data found in column " + (i + 1) + " for header " + header);
  }
}

function removeAllNamedRanges() 
{
  var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  var namedRanges = spreadsheet.getNamedRanges();
  
  for (var i = 0; i < namedRanges.length; i++)
    namedRanges[i].remove();
}