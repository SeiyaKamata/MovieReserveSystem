// URLを取得
let url = new URL(window.location.href);

// URLSearchParamsオブジェクトを取得
let params = url.searchParams;

// getメソッド
schedule_id = params.get("schedule_id");
document.getElementById("input-schedule").value = schedule_id;

seats = new Set();

function toggleSeatColor(seat) {
  seat.classList.toggle("selected");

  if (!seats.has(seat.id)) {
    seats.add(seat.id); // Setに要素を追加
  } else {
    seats.delete(seat.id); // Setから要素を削除
  }

  document.getElementById("input-seat").value = Array.from(seats).join(',');
}
