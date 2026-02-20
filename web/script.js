document.getElementById("printForm").addEventListener("submit", async function(e){
    e.preventDefault();

    let formData = new FormData(this);

    let res = await fetch("/upload", {
        method: "POST",
        body: formData
    });

    let data = await res.json();
    document.getElementById("amount").innerHTML =
        "Amount: ₹" + data.amount + " | Go to machine & press print";
});
