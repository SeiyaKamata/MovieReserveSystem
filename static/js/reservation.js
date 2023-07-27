const toastLiveExample = document.getElementById("liveToast");
const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastLiveExample);
toastBootstrap.show();

function deleteReservation(reservation) {
  href = reservation.childNodes.item(1).value
  text = reservation.childNodes.item(3).value
  modalText = document.getElementById("modal-text");
  deleteButton = document.getElementById("delete-button");
  deleteButton.href = href;
}
