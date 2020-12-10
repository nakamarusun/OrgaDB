// A custom form can be made without the createNewForm() function.
// This is because the script only detects the first and second form item
// as `event comment` and `event rating` respectively.
// After that, additional items can be added, but will not be sent to the REST endpoint.

function createNewForm() {
  
  // This is the main function that the user should run :)
  // These variables marked by the stars are variables that you should be able to change.
  // Below it, is not meant to be changed.
  // *********************
  var eventId = "<EVENT-ID>"; // VERY IMPORTANT. Get the event id from the database
  var fileName = "<GOOGLE-FILE-NAME>";
  var formTitle = "<FORM-TITLE>";
  var description = "<FORM-DESCRIPTION>";
  // *********************
  
  // Create form
  var form = FormApp.create(fileName);
  form.setTitle(formTitle);
  // Store the event id on the first line of the description
  form.setDescription(description + "\n" + eventId);
  
  // Here, we can add all the form answers
  // Comment about the event
  form.addParagraphTextItem()
  .setRequired(true)
  .setTitle("What do you think of the event?")
  .setHelpText("Please write what you think of this event. This will help us improve in the future :)");
  
  // Rating about the event
  form.addScaleItem()
  .setRequired(true)
  .setTitle("Rate the event.")
  .setHelpText("Select a number that you think represent your experience wih our event. 0 is the lowest, 10 is the highest.")
  .setBounds(1, 10)
  .setLabels("Hate it!", "Love it!");
  
  // Register the trigger
  registerFormSend(form);

  return form;
}

function registerFormSend(form) {
  
  // Registers the forms so that when the user submits,
  // function onFormSend will be executed.
  ScriptApp.newTrigger('onFormSend')
  .forForm(form)
  .onFormSubmit()
  .create();
}

function registerForm(id) {
  
  // Can be inputted with URL or ID
  if (id.startsWith("http") || id.startsWith("www") || id.startsWith("docs")) {
    return registerFormSend(FormApp.openByUrl(id));
  }
  return registerFormSend(FormApp.openById(id));
}

function onFormSend(e) {
  
  // Sends all the feedback data to a REST API on the destination point.
  // ********************
  var endPoint = "<REST-API-ENDPOINT>";
  var passphrase = "<AES-PASSPHRASE>";
  // ********************
  
  // Get current active form
  var form = e.source;
  
  // Gets the current event object response sent by the user
  var formResponse = e.response;
  
  // Get the responses
  var itemResponses = formResponse.getItemResponses();
  
  // Event ID
  desc = form.getDescription().trimRight().split(/[ \n\t]+/);
  
  // Insert essential data needed by the database
  var content = {
    'comment': itemResponses[0].getResponse(),
    'rating': itemResponses[1].getResponse(),
    'event_id': desc[desc.length - 1]
  };
  
  // Insert extra data from the form
  if (itemResponses.length > 2) {
    for (var i = 2; i < itemResponses.length; i++) {
      content[itemResponses[i].getItem().getTitle()] = itemResponses[i].getResponse();
    }
  }
  
  // Encrypts the content with AES
  var cipher = new cCryptoGS.Cipher(passphrase, 'aes');
  var encrypted = cipher.encrypt(JSON.stringify(content));
  
  // This will be added as a prefix to the encrypted data.
  // This will serve for just a marker so that the server won't even try
  // to decrypt garbage data.
  var prefix = "dbe";
  // HTTP fetch options
  var options = {
    'method' : 'post',
    'payload' : prefix + encrypted
  };
  
  // Send it to the endpoint
  UrlFetchApp.fetch(endPoint, options);
}