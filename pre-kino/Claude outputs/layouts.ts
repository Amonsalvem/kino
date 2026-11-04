// ============================================================================
// Composition system.
//
// The problem this solves, measured on a real deck: 30 of 31 slides opened
// `kicker > head` and closed on `foot`, inside one 1000px column with one left
// margin. Eleven were byte-identical in structure. A deck with one rhythm reads
// as machine-made however good its prose is.
//
// So composition is DERIVED — first from the slide's role in the argument, then
// from the SHAPE OF ITS CONTENT, because that is what produced the eleven
// identical slides: same type, same number of paragraphs, therefore same frame.
// Two paragraphs do not have to stack; the second can sit in a side rail.
//
// `slide.layout` overrides when a slide earns a different shape.
// Pure: no DOM, no globals — unit-testable.
// ============================================================================
import type { Slide } from "./types.js";

/** The shapes a slide can take. Each maps to a grid span and an anchor in CSS. */
export type Layout =
  | "portada" // the cover: thesis anchored low-left
  | "columna" // the workhorse: a reading column, left-anchored
  | "partido" // head and content side by side instead of stacked
  | "nota" // main paragraph in the measure, the rest in a margin rail
  | "sangre" // edge to edge: the drawing is the slide
  | "cifra" // one number fills the frame; the label is small beside it
  | "diptico" // two panels of equal weight, no centred column
  | "matriz" // a table or a bar chart: wide, head in a rail above
  | "lista" // enumerated items flowing in two columns
  | "cierre" // the decision: anchored low-right, nothing else on the slide
  | "indice" // the source list: dense, full width, small type
  | "respiro"; // a pause: one assertion, no chrome

export const LAYOUTS: readonly Layout[] = [
  "portada",
  "columna",
  "partido",
  "nota",
  "sangre",
  "cifra",
  "diptico",
  "matriz",
  "lista",
  "cierre",
  "indice",
  "respiro",
] as const;

const isLayout = (v: unknown): v is Layout =>
  typeof v === "string" && (LAYOUTS as readonly string[]).includes(v);

/** A slide whose content is a drawing rather than prose. */
function esLienzo(sl: Slide): boolean {
  return sl.type === "diagrama" || typeof (sl as { lienzo?: string }).lienzo === "string";
}

/**
 * Pick the shape for one slide.
 *
 * For prose the decision is made by how many paragraphs the slide carries, not
 * by its position: one paragraph reads beside its assertion, two split into a
 * measure plus a margin note, three or more want a plain column. That is what
 * stops a run of statements from sharing a frame — the variation comes from the
 * material instead of from a counter.
 *
 * `indice` still enters, but only to decide which SIDE a rail falls on, so the
 * choice stays stable across re-renders and language switches.
 */
export function layoutFor(sl: Slide, indice: number): Layout {
  if (isLayout((sl as { layout?: unknown }).layout)) {
    return (sl as { layout: Layout }).layout;
  }
  if (sl.type === "cover") return "portada";
  if (esLienzo(sl)) return "sangre";
  if (sl.type === "quote") return "respiro";
  if (sl.type === "comparison") return "diptico";
  if (sl.type === "table" || sl.type === "bars" || sl.type === "timeline") return "matriz";
  if (sl.type === "recommendations" || sl.type === "datagap") return "lista";
  if (sl.type === "cta") return "cierre";
  if (sl.type === "sources") return "indice";

  // A single headline number deserves the frame; two or three want the column.
  if (sl.type === "stat") return (sl.stats ?? []).length === 1 ? "cifra" : "columna";

  if (sl.type === "statement") {
    const n = (sl.body ?? []).length;
    if (n === 1) return "partido";
    if (n === 2) return "nota";
    return "columna";
  }

  // Unknown types alternate rather than all collapsing into one shape.
  return indice % 2 === 0 ? "columna" : "partido";
}

/** Layouts that suppress the kicker rule and the evidence footer chrome. */
export function sinCromo(l: Layout): boolean {
  return l === "respiro" || l === "portada";
}

/** Which layouts carry a side rail that can be mirrored. */
function tieneRail(l: Layout): boolean {
  return l === "nota" || l === "partido";
}

/**
 * Which side a rail falls on.
 *
 * Counted among the slides that SHARE the shape, not by deck position: three
 * `nota` slides that happen to land on odd indices would otherwise all mirror
 * the same way and the alternation would do nothing. Pure function of the deck,
 * so it is stable across re-renders and language switches.
 */
export function ladoRail(slides: Slide[], indice: number): "der" | "izq" {
  const mio = layoutFor(slides[indice] as Slide, indice);
  let previos = 0;
  for (let i = 0; i < indice; i++) {
    if (layoutFor(slides[i] as Slide, i) === mio) previos++;
  }
  return previos % 2 === 0 ? "der" : "izq";
}

/** Class list for the slide section. */
export function claseLamina(l: Layout): string {
  return `slide lay-${l}`;
}

/** Class list for the inner wrapper. `lado` comes from `ladoRail`. */
export function claseInterior(l: Layout, extra?: string, lado?: "der" | "izq"): string {
  const rail = tieneRail(l) && lado ? `rail-${lado}` : "";
  return ["slide-inner", `in-${l}`, rail, extra].filter(Boolean).join(" ");
}

/**
 * How uniform is a deck's composition? Returns the share of slides that carry
 * the most common shape. The deck this system was built for scored 0.94 before;
 * the self-audit passes it below 0.45.
 */
export function uniformidad(slides: Slide[]): number {
  if (!slides.length) return 0;
  const cuenta = new Map<Layout, number>();
  slides.forEach((sl, i) => {
    const l = layoutFor(sl, i);
    cuenta.set(l, (cuenta.get(l) ?? 0) + 1);
  });
  return Math.max(...cuenta.values()) / slides.length;
}
