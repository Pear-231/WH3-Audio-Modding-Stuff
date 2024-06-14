function createMenu()
{
  Logger.log(`Running: createMenu()`);

  var ui = SpreadsheetApp.getUi();
  ui.createMenu('Audio Editor')
      .addItem('Show Instructions', 'showInstructions')
      .addItem('Load States', 'loadStates')
      .addItem('Load Dialogue Events', 'loadDialogueEvents')
      .addItem('Download Sheet as Audio Project', 'downloadAudioProject')
      .addToUi();
}

function showInstructions()
{
  Logger.log(`Running: showInstructions()`);

  var html = HtmlService.createHtmlOutputFromFile('Instructions')
      .setTitle('Instructions')
      .setWidth(300);
  SpreadsheetApp.getUi().showSidebar(html);
}

function downloadAudioProject()
{
  Logger.log(`Running: downloadAudioProject()`);

  var json = sheetToJson();
  
  if (json === null)
    return

  var jsonString = JSON.stringify(json, null, 2);
  var encodedJson = encodeURIComponent(jsonString);

  var htmlContent = `
    <html>
      <head>
        <style>
          .download-button {
            display: inline-block;
            background-color: #007BFF; /* Blue background */
            border: none;
            color: white;
            text-align: center;
            text-decoration: none;
            font-size: 16px;
            cursor: pointer;
            padding: 12px 24px;
            transition-duration: 0.4s;
            border-radius: 8px;
          }
          .download-button:hover {
            background-color: #0056b3; /* Darker blue */
          }
        </style>
      </head>
      <body>
        <a href="data:application/json;charset=utf-8,${encodedJson}" download="dialogue_data.json">
          <button class="download-button">Download Audio Project</button>
        </a>
      </body>
    </html>
  `;

  var htmlOutput = HtmlService.createHtmlOutput(htmlContent)
      .setWidth(250)
      .setHeight(100);

  SpreadsheetApp.getUi().showModalDialog(htmlOutput, " ");
}