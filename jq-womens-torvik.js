(function() {
    // headers according to table structure 2026-03-17
    const headers = "rank,team,conf,games,record,adjoe,adjde,barthag,efgp,efgdp,tor,tord,orb,drb,ftr,ftrd,2pp,2ppd,3pp,3ppd,3pr,3prd,adjt,wab".split(",");

    let csvContent = headers.join(",") + "\n";

    $("tbody tr.seedrow").each(function() {
        let rowData = [];

        $(this).find("td").each(function() {
            let $td = $(this);

            // Clone the cell to manipulate it without breaking the UI
            let $clone = $td.clone();

            // Remove the <span class="lowrow"> which contains the sub-ranks/notes
            $clone.find(".lowrow").remove();

            // Get text, trim it, and remove any weird non-breaking spaces
            let text = $clone.text().trim().replace(/\u00a0/g, " ");

            // Handle commas in text (like "1,000") by wrapping in quotes
            if (text.includes(",")) {
                text = `"${text}"`;
            }

            rowData.push(text);
        });

        csvContent += rowData.join(",") + "\n";
    });

    console.log(csvContent);
    copy(csvContent);
    console.log("CSV data has been copied to your clipboard!");
})();