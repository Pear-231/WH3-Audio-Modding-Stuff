function sheetToJson()
{
    Logger.log(`Running: sheetToJson()`);

    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    var sheetName = sheet.getName();
    
    if (!(sheetName === "Battle VO Builder" || sheetName === "Campaign VO Builder" || sheetName === "Conversational Battle VO Builder" || sheetName === "Conversational Campaign VO Builder" || sheetName === "Frontend VO Builder"))
      return null;

    var data = sheet.getDataRange().getValues();
  
    var json = {
      Settings: {
        BnkName: sheetName,
        Language: "english(uk)"
      },
      DialogueEvents: []
    };
  
    var currentEvent = null;
    var currentDecisionTree = null;
  
    for (var i = 1; i < data.length; i++)
    { 
        // Start from index 1 to skip the header row
        var row = data[i];
        var firstCell = row[0].trim(); // Trim to remove any leading/trailing spaces
    
        if (!firstCell.startsWith("State Path") && !firstCell.startsWith("Sounds"))
        {
            // Start a new dialogue event
            if (currentEvent)
            {
                // Push the previous event before starting a new one
                if (currentDecisionTree)
                {
                    currentEvent.DecisionTree.push(currentDecisionTree);
                    currentDecisionTree = null;
                }
                json.DialogueEvents.push(currentEvent);
            }

            currentEvent = {
                DialogueEvent: firstCell,
                DecisionTree: []
            };
        }

        else if (firstCell.startsWith("State Path"))
        {
            // Start a new state path within the current dialogue event
            if (currentDecisionTree)
            {
                // Push the previous decision tree before starting a new one
                currentEvent.DecisionTree.push(currentDecisionTree);
            }
            
            var statePath = row.slice(1).filter(cell => cell.trim()).join('.');
            currentDecisionTree = {
            StatePath: statePath,
            Sounds: []
            };
        } 

        else if (firstCell.startsWith("Sounds"))
        {
            // Add sounds to the current decision tree
            for (var j = 1; j < row.length; j++)
            {
                if (row[j] && row[j].trim())
                {
                    var soundPath = row[j].trim();

                    // Remove double quotes from the beginning and end of the string
                    if (soundPath.startsWith('"') && soundPath.endsWith('"'))
                    soundPath = soundPath.substring(1, soundPath.length - 1);

                    currentDecisionTree.Sounds.push(soundPath);
                }
            }
        }
    }
  
    // Push the last decision tree and event
    if (currentDecisionTree)
      currentEvent.DecisionTree.push(currentDecisionTree);
    
    if (currentEvent)
      json.DialogueEvents.push(currentEvent);
  
    Logger.log(JSON.stringify(json, null, 2));

    return json;
}