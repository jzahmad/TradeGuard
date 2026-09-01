const loginForm =
    document.getElementById("loginForm");

if (loginForm) {
    loginForm.addEventListener(
        "submit",
        function (event) {

            event.preventDefault();

            window.location.href =
                "dashboard.html";
        }
    );
}


const registerForm =
    document.getElementById("registerForm");

if (registerForm) {
    registerForm.addEventListener(
        "submit",
        function (event) {

            event.preventDefault();

            alert(
                "Account created successfully."
            );

            window.location.href =
                "login.html";
        }
    );
}



const buyQuantity =
    document.getElementById("buyQuantity");

const buyTotal =
    document.getElementById("buyTotal");

const buyButton =
    document.getElementById("buyButton");

const MOCK_BUY_PRICE = 210;


function updateBuyTotal() {

    if (!buyQuantity || !buyTotal) {
        return;
    }

    const quantity =
        Number(buyQuantity.value) || 0;

    const total =
        quantity * MOCK_BUY_PRICE;

    buyTotal.textContent =
        "$" +
        total.toLocaleString(
            "en-US",
            {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }
        );
}


if (buyQuantity) {

    buyQuantity.addEventListener(
        "input",
        updateBuyTotal
    );

    updateBuyTotal();
}


if (buyButton) {

    buyButton.addEventListener(
        "click",
        function () {

            const quantity =
                Number(buyQuantity.value);

            if (
                !Number.isInteger(quantity) ||
                quantity <= 0
            ) {
                alert(
                    "Enter a valid quantity."
                );

                return;
            }

            const confirmed =
                confirm(
                    `Submit BUY order for ${quantity} shares of AAPL?`
                );

            if (!confirmed) {
                return;
            }

            alert(
                "Buy order submitted. Status: Pending"
            );

            window.location.href =
                "orders.html";
        }
    );
}



const sellTicker =
    document.getElementById("sellTicker");

const sellTickerDisplay =
    document.getElementById(
        "sellTickerDisplay"
    );

const sellPrice =
    document.getElementById("sellPrice");

const sellQuantity =
    document.getElementById(
        "sellQuantity"
    );

const sellTotal =
    document.getElementById("sellTotal");

const availableShares =
    document.getElementById(
        "availableShares"
    );

const sellButton =
    document.getElementById(
        "sellButton"
    );


function updateSellValues() {

    if (
        !sellTicker ||
        !sellQuantity ||
        !sellPrice ||
        !sellTotal
    ) {
        return;
    }

    const selected =
        sellTicker.options[
            sellTicker.selectedIndex
        ];

    const ticker =
        selected.value;

    const price =
        Number(
            selected.dataset.price
        );

    const maxShares =
        Number(
            selected.dataset.max
        );

    const quantity =
        Number(sellQuantity.value) || 0;


    if (sellTickerDisplay) {
        sellTickerDisplay.textContent =
            ticker;
    }


    sellPrice.textContent =
        "$" +
        price.toFixed(2);


    sellTotal.textContent =
        "$" +
        (
            price * quantity
        ).toLocaleString(
            "en-US",
            {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }
        );


    sellQuantity.max =
        maxShares;


    if (availableShares) {
        availableShares.textContent =
            `${maxShares} shares available`;
    }
}


if (
    sellTicker &&
    sellQuantity
) {

    sellTicker.addEventListener(
        "change",
        updateSellValues
    );

    sellQuantity.addEventListener(
        "input",
        updateSellValues
    );

    updateSellValues();
}


if (sellButton) {

    sellButton.addEventListener(
        "click",
        function () {

            const selected =
                sellTicker.options[
                    sellTicker.selectedIndex
                ];

            const maxShares =
                Number(
                    selected.dataset.max
                );

            const quantity =
                Number(
                    sellQuantity.value
                );

            const ticker =
                selected.value;


            if (
                !Number.isInteger(quantity) ||
                quantity <= 0
            ) {
                alert(
                    "Enter a valid quantity."
                );

                return;
            }


            if (quantity > maxShares) {

                alert(
                    `You only own ${maxShares} shares of ${ticker}.`
                );

                return;
            }


            const confirmed =
                confirm(
                    `Submit SELL order for ${quantity} shares of ${ticker}?`
                );

            if (!confirmed) {
                return;
            }


            alert(
                "Sell order submitted. Status: Pending"
            );


            window.location.href =
                "orders.html";
        }
    );
}



const cancelButtons =
    document.querySelectorAll(
        ".cancel-btn"
    );


cancelButtons.forEach(
    function (button) {

        button.addEventListener(
            "click",
            function () {

                const confirmed =
                    confirm(
                        "Are you sure you want to cancel this pending order?"
                    );


                if (!confirmed) {
                    return;
                }


                const row =
                    button.closest("tr");


                const statusCell =
                    row.querySelector(
                        ".status-cell"
                    );


                if (statusCell) {

                    statusCell.innerHTML =
                        `
                        <span class="status cancelled">
                            CANCELLED
                        </span>
                        `;
                }


                button.remove();
            }
        );
    }
);