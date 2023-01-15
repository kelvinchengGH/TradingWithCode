/*
A few requirements for configuring the table:
1. The table must have id="sortable", i.e. <table id="sortable">
2. The table needs to have a table header, and the table header must have
   onclick="sortBy(n)", where n is the column number starting with 0
   i.e. <th onclick="sortBy(0)">Title of First Column</th>
*/

cPrev = -1; // global var saves the previous c, used to
            // determine if the same column is clicked again

function compareRows( row1, row2 ) {
    x1 = row1[c];
    x2 = row2[c];
    if (x1 === x2) {
        return 0;
    } else {
        return (parseFloat(x1) < parseFloat(x2)) ? -1 : 1;
    }
}

function compareRows2 ( a, b, c ) {
    if (a[c] == b[c]) {
        return 0;
    } else {
        return (a[c] < b[c]) ? -1 : 1;
    }
}


function sortBy(c) {

    function compareRows( row1, row2 ) {
	x1 = row1[c];
	x2 = row2[c];
	if (x1 === x2) {
            return 0;
	}
	
	if ( !isNaN(x1) && !isNaN(x2) ) {
            return ( parseFloat(x1) < parseFloat(x2) ) ? -1 : 1;
	}
	else {
	    return (x1 < x2 ) ? -1 : 1;
	}
    }
    rows = document.getElementById("StockDataFrame").rows.length; // num of rows
    columns = document.getElementById("StockDataFrame").rows[0].cells.length; // num of columns
    arrTable = [...Array(rows)].map(e => Array(columns)); // create an empty 2d array

    for (ro=0; ro<rows; ro++) { // cycle through rows
        for (co=0; co<columns; co++) { // cycle through columns
            // assign the value in each row-column to a 2d array by row-column
            arrTable[ro][co] = document.getElementById("StockDataFrame").rows[ro].cells[co].innerHTML;
        }
    }

    th = arrTable.shift(); // remove the header row from the array, and save it
    
    if (c !== cPrev) { // different column is clicked, so sort by the new column
        arrTable.sort(
            // function (a, b) {
            //     if (a[c] == b[c]) {
            //         return 0;
            //     } else {
            //         return (a[c] < b[c]) ? -1 : 1;
            //     }
            // }
	    compareRows
        );
    } else { // if the same column is clicked then reverse the array
        arrTable.reverse();
    }
    
    cPrev = c; // save in previous c

    arrTable.unshift(th); // put the header back in to the array

    // cycle through rows-columns placing values from the array back into the html table
    for (ro=0; ro<rows; ro++) {
        for (co=0; co<columns; co++) {
            document.getElementById("StockDataFrame").rows[ro].cells[co].innerHTML = arrTable[ro][co];
        }
    }
}


