(() => {
  "use strict";
  let selected = null;
  const $ = (id) => document.getElementById(id),
    norm = (s) =>
      s
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .toLowerCase();
  function render() {
    const q = norm($("library-search").value);
    const list = BIBLIOTECA.filter((x) =>
      norm(x.title + " " + x.text).includes(q),
    );
    $("library-list").replaceChildren(
      ...list.map((x) => {
        const b = document.createElement("button");
        b.className = "btn";
        b.textContent = x.title;
        b.addEventListener("click", () => {
          selected = x;
          $("library-title").textContent = x.title;
          $("library-text").value = x.text;
          $("library-copy").disabled = false;
          $("library-download").disabled = false;
          $("library-status").textContent = "Coleção aberta para revisão.";
        });
        return b;
      }),
    );
    if (!list.length)
      $("library-list").textContent =
        "Nenhuma coleção encontrada. Experimente outra palavra.";
    $("library-count").textContent = list.length + " coleções";
  }
  $("library-search").addEventListener("input", render);
  $("library-copy").addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText($("library-text").value);
      $("library-status").textContent = "Copiado";
    } catch {
      $("library-status").textContent =
        "Selecione o texto e use Ctrl+C para copiar.";
    }
  });
  $("library-download").addEventListener("click", () => {
    const u = URL.createObjectURL(
        new Blob([$("library-text").value], {
          type: "text/plain;charset=utf-8",
        }),
      ),
      a = document.createElement("a");
    a.href = u;
    a.download = "referencia-" + selected.id + ".txt";
    a.click();
    setTimeout(() => URL.revokeObjectURL(u), 1000);
    $("library-status").textContent = "Arquivo gerado";
  });
  render();
})();
