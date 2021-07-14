/* Set values + misc */
$(document).ready(function () {
  $("#one").load("../test.json", function () {
    alert("Load test");
  });
});
////../test.html ====> ajax link
{
  /* <p id="one"></p> add to price class name in html page */
}

var promoCode;
var promoPrice;
var fadeTime = 300;

/* Assign actions */
$(".quantity input").change(function () {
  updateQuantity(this);
});

$(".remove button").click(function () {
  removeItem(this);
});

$(document).ready(function () {
  updateSumItems();
});

$(".promo-code-cta").click(function () {
  /////////test ajax////////////
  if ($(".basket-module").val() !== " ") {
    $.ajax({
      type: "GET",
      url: "http://127.0.0.1:8000/cart/coupon/valid/", ///////enter url/////
      data: {
        coupon_code: $("#promo-code").val(),
          basket_total: $("#basket-total").val(),
      },
      success: function (dataResult) {
        //var dataResult = JSON.parse(dataResult);
          console.log(dataResult)
        //if (dataResult.statusCode == 200) {
          if (dataResult['status'] == 200) {
          console.log(dataResult['value'])
          var after_apply = $('#basket-total').val() - dataResult['price'];
          console.log('basket-total tag: ', $('#basket-total').val())
          console.log(after_apply)
          $("#basket-total").val(after_apply);
          // $('#apply').hide();
          // $('#edit').show();
          // $('#message').html("Promocode applied successfully !");
          alert("کد صحیح است");
        } else if (dataResult['status'] == 201) {
            alert(dataResult['error'])
          //alert("کد اشتباه است 201 erorr");
          // $('#message').html("Invalid promocode !");
        }
      },
    });
  } else {
    alert("کد اشتباه است ajax");
    // $('#message').html("Promocode can not be blank .Enter a Valid Promocode !");
  }

  // $("#edit").click(function(){
  // 	$('#coupon_code').val("");
  // 	$('#apply').show();
  // 	$('#edit').hide();
  // 	location.reload();
});


/////////test ajax////////////
// promoCode = $("#promo-code").val();

// if (promoCode == "10off" || promoCode == "10OFF") {
//   //If promoPrice has no value, set it as 10 for the 10OFF promocode
//   if (!promoPrice) {
//     promoPrice = 10000000;
//   } else if (promoCode) {
//     promoPrice = promoPrice * 1;
//   }
// } else if (promoCode != "") {
//   alert("کد اشتباه است");
//   promoPrice = 0;
// }
//If there is a promoPrice that has been set (it means there is a valid promoCode input) show promo
//   if (promoPrice) {
//     $(".summary-promo").removeClass("hide");
//     $(".promo-value").text(promoPrice.toFixed(0));
//     recalculateCart(true);
//   }
// });

/* Recalculate cart */
function recalculateCart(onlyTotal) {
  var subtotal = 0;

  /* Sum up row totals */
  $(".basket-product").each(function () {
    subtotal += parseFloat($(this).children(".subtotal").text());
  });

  /* Calculate totals */
  var total = subtotal;

  // If there is a valid promoCode, and subtotal < 10 subtract from total
  var promoPrice = parseFloat($(".promo-value").text());
  if (promoPrice) {
    if (subtotal >= 10) {
      total -= promoPrice;
    } else {
      alert("");
      $(".summary-promo").addClass("hide");
    }
  }

  /*If switch for update only total, update only total display*/
  if (onlyTotal) {
    /* Update total display */
    $(".total-value").fadeOut(fadeTime, function () {
      $("#basket-total").html(total.toFixed(0));
      $(".total-value").fadeIn(fadeTime);
    });
  } else {
    /* Update summary display. */
    $(".final-value").fadeOut(fadeTime, function () {
      $("#basket-subtotal").html(subtotal.toFixed(0));
      $("#basket-total").html(total.toFixed(0));
      if (total == 0) {
        $(".checkout-cta").fadeOut(fadeTime);
      } else {
        $(".checkout-cta").fadeIn(fadeTime);
      }
      $(".final-value").fadeIn(fadeTime);
    });
  }
}

/* Update quantity */
function updateQuantity(quantityInput) {
  /* Calculate line price */
  var productRow = $(quantityInput).parent().parent();
  var price = parseFloat(productRow.children(".price").text()) * 1000000;
  console.log('price: ', price)
  var quantity = $(quantityInput).val();
  var linePrice = price * quantity;

  /* Update line price display and recalc cart totals */
  productRow.children(".subtotal").each(function () {
    $(this).fadeOut(fadeTime, function () {
      $(this).text(linePrice.toFixed(0));
      recalculateCart();
      $(this).fadeIn(fadeTime);
    });
  });

  // productRow.find(".item-quantity").text(quantity);
  // updateSumItems();
}

function updateSumItems() {
  var sumItems = 0;
  $(".quantity input").each(function () {
    sumItems += parseInt($(this).val());
  });
  $(".total-items").text(sumItems);
}

/* Remove item from cart */
function removeItem(removeButton) {
  /* Remove row from DOM and recalc cart total */
  var productRow = $(removeButton).parent().parent();
  productRow.slideUp(fadeTime, function () {
    productRow.remove();
    recalculateCart();
    updateSumItems();
  });
}
anime({
  targets: ".show",
  translateX: 270,
  delay: anime.stagger(100), // increase delay by 100ms for each elements.
});