document.getElementById('hotel_stay').addEventListener('change', function() {
    let hotelDetails = document.getElementById('hotel_details');
    let otherAddress = document.getElementById('other_address').querySelector('input');
    if (this.checked) {
        hotelDetails.style.display = 'block';
        otherAddress.required = false;
        otherAddress.disabled = true;
    } else {
        hotelDetails.style.display = 'none';
        otherAddress.required = true;
        otherAddress.disabled = false;
    }
});



// valid phone number
document.addEventListener("DOMContentLoaded", function () {
    const phoneInput = document.getElementById("phone");
    const errorMessage = document.querySelector(".error-message");

    phoneInput.addEventListener("input", function () {
        const phonePattern = /^[6-9]\d{9}$/; // Valid Indian number pattern
        if (!phonePattern.test(phoneInput.value)) {
            errorMessage.style.display = "block";
        } else {
            errorMessage.style.display = "none";
        }
    });
});


// for the food order quantity
document.getElementById('quantity').addEventListener('input', function() {
    let quantity = parseInt(this.value);
    let price = parseFloat(document.getElementById('food_price').value);
    let totalPrice = quantity * price;
    document.getElementById('total_price').innerText = totalPrice.toFixed(2);
});