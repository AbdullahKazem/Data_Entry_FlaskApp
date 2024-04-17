function disableButton(){
    var productButton = document.getElementById("products").disabled = true;
}
function movetohome(){
    window.location.href="input";
}

function movetoproducts(){
    window.location.href="products";
}

function movetoRFID(){
  window.location.href="RFID";
}

function movetologin(){
  window.location.href="login";
}

// validate form function is created to ensure that user select a value
function validateForm() {
  var lineSelectedValue = document.getElementById("machinename").value;
  var productSelectedValue = document.getElementById("productname").value;
  if (lineSelectedValue === "" || productSelectedValue === "") {
    alert("Please select an option");
    return false; // Prevent form submission
  }
  return true; // Allow form submission
}

function getData() {
  // Get the values from the textboxes
  alert("Data Was Submited Successfully");
}

/* in add function if user click add button the form appear if press add agian the form 
disappear so every tim user press add button first time form appear next disappear*/

var x=0;
function add(page){
    if(page == 'products'){
      var addForm = document.getElementById('addproduct');
    }else{
      var addForm = document.getElementById('addcode');
    }
    
    if (x % 2 == 0) {
        addForm.style.display = "inline-block";
        x=0;
    }else{
        addForm.style.display = "none";
    }
    x++;
    console.log(x)
}

var originalData = [];
function edit(page){
    var tablecells = document.querySelectorAll('#responsive-table td:not(.exclude)');
    var button = document.createElement("button");
    button.textContent = "Apply";
    button.id="Apply_Button";
    button.className = "b";
    button.style.width = "150px";
    button.style.height = "35px";
    button.style.display="inline-block";
    button.style.position="relative";
    button.style.margin = "10px 0px 0px 10px";
    button.type="button";
    console.log(tablecells);
    if(tablecells.length != 0){
      document.getElementById("Apply").appendChild(button);
    }

    button.addEventListener("click", function() {
      var editedData = [];
      var count = 0;
      //get edited data
      // console.log("kazem");
      tablecells.forEach(function(cell) {
        var input = cell.querySelector('input');
        editedData.push(input.value);
        cell.classList.remove('edit-mode');
      });

      var table = document.getElementById("responsive-table");
      var productsId = []
      for( var i=1; i<table.rows.length;i++){
        var check = table.rows[i].cells[0];
        var checkbox = check.querySelector('input[type="checkbox"]');
        console.log(checkbox.value)
        productsId.push(checkbox.value);
      }
      // console.log(productsId);
      for (var i=1; i<table.rows.length; i++){
        for(var j=1; j<table.rows[i].cells.length; j++){
          table.rows[i].cells[j].textContent = editedData[count];
          console.log(table.rows[i].cells[j].textContent);
          count++;
        }
      } 
      var buttonToRemove = document.getElementById('Apply_Button');
      if (buttonToRemove ) {
        buttonToRemove.remove();
      }
      // buttonToRemove.remove();
      originalData = [...editedData];
      var xhr = new XMLHttpRequest();
      if(page == 'products'){ 
        xhr.open("POST", "/Best/products/edit_data", true)
        xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xhr.send(JSON.stringify({origin: originalData, productId: productsId}))
      }
      else{
        xhr.open("POST", "/Best/RFID/edit_data", true)
        xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xhr.send(JSON.stringify({origin: originalData, productId: productsId}))
      }
    });

    tablecells.forEach(function(cell) {
      toggleCells(cell);
    });
  }

function toggleCells(cell){
  var content = cell.textContent;
  
  if (!cell.classList.contains('edit-mode')) {
  // Replace the content with input fields in edit mode
    var input = document.createElement('input');
    input.style.width = "100%";
    input.style.fontSize = "large";
    input.type = 'text';
    input.value = content;
    originalData.push(content);
    cell.innerHTML = '';
    cell.appendChild(input);
    cell.classList.add('edit-mode');
  } else {
  //Replace the input fields with the original content when exiting edit mode
    var input = cell.querySelector('input');
    var inputValue = input.value;
    cell.innerHTML = originalData.shift();
    cell.classList.remove('edit-mode');
    var buttonToRemove = document.getElementById('Apply_Button');
    if (buttonToRemove) {
      buttonToRemove.remove();
    }
  } 
}


function remove(){
    var checkboxes = document.querySelectorAll('.responsive-table input[type="checkbox"]');

    var checkboxValues = [];
    checkboxes.forEach(function(checkbox) {
        if (checkbox.checked) {
            checkboxValues.push(checkbox.value);
        }
    });

    console.log(checkboxValues);
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/BlueSkies/delete", true)
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({checkedList: checkboxValues}))

}