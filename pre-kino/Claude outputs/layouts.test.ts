// ============================================================================
// Composition and motion: the pure parts.
// ============================================================================
import { describe, it, expect } from "vitest";
import { layoutFor, uniformidad, claseInterior, claseLamina, sinCromo, ladoRail } from "../src/layouts.js";
import { curvaDe, retardo, respetaReduccion } from "../src/motion.js";
import type { Slide } from "../src/types.js";

const sl = (o: Partial<Slide>): Slide => ({ type: "statement", ...o }) as Slide;

describe("layoutFor", () => {
  it("gives the cover its own shape", () => {
    expect(layoutFor(sl({ type: "cover" }), 0)).toBe("portada");
  });

  it("varies prose by how much of it there is, not by a counter", () => {
    const uno = sl({ type: "statement", body: [{ en: "a", es: "a" }] });
    const dos = sl({ type: "statement", body: [{ en: "a", es: "a" }, { en: "b", es: "b" }] });
    const tres = sl({ type: "statement", body: [{ en: "a", es: "a" }, { en: "b", es: "b" }, { en: "c", es: "c" }] });
    expect(layoutFor(uno, 4)).toBe("partido");
    expect(layoutFor(dos, 4)).toBe("nota");
    expect(layoutFor(tres, 4)).toBe("columna");
  });

  it("mirrors the rail among slides that share the shape, not by deck position", () => {
    const dos = (): Slide => sl({ type: "statement", body: [{ en: "a", es: "a" }, { en: "b", es: "b" }] });
    // Las tres `nota` caen en índices impares: alternar por posición no haría nada.
    const cubierta: Slide[] = [sl({ type: "cover" }), dos(), sl({ type: "quote" }), dos(), sl({ type: "quote" }), dos()];
    expect(ladoRail(cubierta, 1)).toBe("der");
    expect(ladoRail(cubierta, 3)).toBe("izq");
    expect(ladoRail(cubierta, 5)).toBe("der");
  });

  it("gives tables, lists, the decision and the sources their own frames", () => {
    expect(layoutFor(sl({ type: "table" }), 1)).toBe("matriz");
    expect(layoutFor(sl({ type: "bars" }), 1)).toBe("matriz");
    expect(layoutFor(sl({ type: "recommendations" }), 1)).toBe("lista");
    expect(layoutFor(sl({ type: "datagap" }), 1)).toBe("lista");
    expect(layoutFor(sl({ type: "cta" }), 1)).toBe("cierre");
    expect(layoutFor(sl({ type: "sources" }), 1)).toBe("indice");
  });

  it("is stable for the same slide at the same position", () => {
    const s = sl({ type: "statement" });
    expect(layoutFor(s, 7)).toBe(layoutFor(s, 7));
  });

  it("lets one headline number fill the frame but keeps three in a column", () => {
    expect(layoutFor(sl({ type: "stat", stats: [{ num: "711", lbl: "x" }] }), 1)).toBe("cifra");
    expect(
      layoutFor(sl({ type: "stat", stats: [{ num: "1", lbl: "a" }, { num: "2", lbl: "b" }, { num: "3", lbl: "c" }] }), 1),
    ).toBe("columna");
  });

  it("gives a drawing the full bleed, by type or by carrying a canvas", () => {
    expect(layoutFor(sl({ type: "diagrama" }), 2)).toBe("sangre");
    expect(layoutFor(sl({ type: "statement", lienzo: "actual-3" }), 2)).toBe("sangre");
  });

  it("treats a quote as a pause and a comparison as two equal panels", () => {
    expect(layoutFor(sl({ type: "quote" }), 3)).toBe("respiro");
    expect(layoutFor(sl({ type: "comparison" }), 3)).toBe("diptico");
  });

  it("honours an explicit override and ignores an invalid one", () => {
    expect(layoutFor(sl({ type: "statement", layout: "sangre" }), 0)).toBe("sangre");
    expect(layoutFor(sl({ type: "statement", layout: "inventado" }), 0)).toBe("columna");
  });
});

describe("uniformidad", () => {
  it("scores a single-shape deck at 1 and an empty one at 0", () => {
    const iguales = Array.from({ length: 10 }, () => sl({ type: "statement" }));
    expect(uniformidad(iguales)).toBe(1);
    expect(uniformidad([])).toBe(0);
  });

  it("drops below the audit threshold once shapes vary", () => {
    const mezcla: Slide[] = [
      sl({ type: "cover" }),
      sl({ type: "statement", body: [{ en: "a", es: "a" }] }),
      sl({ type: "statement", body: [{ en: "a", es: "a" }, { en: "b", es: "b" }] }),
      sl({ type: "quote" }),
      sl({ type: "comparison" }),
      sl({ type: "diagrama" }),
      sl({ type: "stat", stats: [{ num: "1", lbl: "a" }] }),
    ];
    expect(uniformidad(mezcla)).toBeLessThanOrEqual(0.55);
  });
});

describe("clases", () => {
  it("names the section and the inner wrapper", () => {
    expect(claseLamina("cifra")).toBe("slide lay-cifra");
    expect(claseInterior("respiro")).toBe("slide-inner in-respiro");
    expect(claseInterior("portada", "cover")).toBe("slide-inner in-portada cover");
    expect(claseInterior("nota", undefined, "der")).toBe("slide-inner in-nota rail-der");
    expect(claseInterior("columna", undefined, "der")).toBe("slide-inner in-columna");
  });

  it("marks the shapes that drop the chrome", () => {
    expect(sinCromo("respiro")).toBe(true);
    expect(sinCromo("columna")).toBe(false);
  });
});

describe("motion", () => {
  it("separates expiring from being revoked", () => {
    // Caducar y ser revocado no son lo mismo, y no pueden moverse igual.
    expect(curvaDe("vence").curva).toBe("decaer");
    expect(curvaDe("revoca").curva).toBe("crecer");
  });

  it("makes only a live state move on its own", () => {
    expect(curvaDe("vive").continuo).toBe(true);
    expect(curvaDe("entra").continuo).toBe(false);
  });

  it("staggers the reading order and then stops making people wait", () => {
    expect(retardo(0)).toBe(0);
    expect(retardo(2)).toBe(110);
    expect(retardo(9)).toBe(retardo(4));
  });

  it("collapses to one frame when the viewer asked for less motion", () => {
    expect(respetaReduccion(true, 900)).toBe(0);
    expect(respetaReduccion(false, 900)).toBe(900);
  });
});
