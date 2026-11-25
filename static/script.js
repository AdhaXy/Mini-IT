// Minor form helpers: add and remove property rows.
const list = document.getElementById("property-list");
const template = document.getElementById("row-template");
const addButton = document.getElementById("add-row");
const maxRows = Number(list.dataset.max);

function renumberRows() {
  list.querySelectorAll(".property-row").forEach((row, index) => {
    row.querySelector(".row-number").textContent = "Property " + (index + 1);
  });
  addButton.disabled = list.children.length >= maxRows;
}

addButton.addEventListener("click", () => {
  if (list.children.length >= maxRows) return;
  list.appendChild(template.content.cloneNode(true));
  renumberRows();
});

list.addEventListener("click", (event) => {
  if (!event.target.classList.contains("remove-row")) return;
  if (list.children.length === 1) return; // keep at least one row
  event.target.closest(".property-row").remove();
  renumberRows();
});

renumberRows();
