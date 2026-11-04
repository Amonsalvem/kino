// ============================================================================
// Motion system.
//
// Three curves, and each one means something. They are not decoration and they
// are not interchangeable: a deck where everything moves the same way is the
// motion equivalent of one column and one margin.
//
//   crecer  what appears — fast in, settles
//   decaer  what expires — slower, so caducar reads differently from ser revocado
//   latir   what is alive — the only thing that moves on its own
//
// The curves come from the Kino brand layer (`--kino-crecer` / `--kino-decaer` /
// `--kino-latir`); this module names them and decides which applies, so the
// choice is testable and not buried in a stylesheet.
// ============================================================================

export type Curva = "crecer" | "decaer" | "latir";

/** What kind of change is happening to an element. */
export type Cambio =
  | "entra" // enters the frame
  | "vence" // a validity window running out
  | "revoca" // taken away by a person
  | "vive" // a confirmed, live state
  | "sale"; // leaves the frame

export interface Movimiento {
  curva: Curva;
  /** CSS custom property holding the duration+easing pair. */
  prop: string;
  /** True when the motion repeats rather than playing once. */
  continuo: boolean;
}

const M: Record<Curva, Omit<Movimiento, "curva">> = {
  crecer: { prop: "--kino-crecer", continuo: false },
  decaer: { prop: "--kino-decaer", continuo: false },
  latir: { prop: "--kino-latir", continuo: true },
};

/**
 * Which curve a change moves on.
 *
 * `vence` and `revoca` both remove something, and they deliberately differ:
 * expiry decays slowly, revocation is an act and cuts fast. Showing them with
 * the same motion would flatten a distinction the product depends on.
 */
export function curvaDe(c: Cambio): Movimiento {
  const curva: Curva =
    c === "vive" ? "latir" : c === "vence" ? "decaer" : c === "revoca" ? "crecer" : c === "sale" ? "decaer" : "crecer";
  return { curva, ...M[curva] };
}

/**
 * Stagger, in milliseconds, for the nth element of a slide.
 *
 * The eye reads kicker → assertion → content → evidence, so the entry follows
 * that order. It flattens after the fourth element: past that the delay stops
 * guiding and starts making the audience wait.
 */
export function retardo(n: number, paso = 55, tope = 4): number {
  if (n <= 0) return 0;
  return Math.min(n, tope) * paso;
}

/** Everything collapses to a single frame when the viewer asked for less motion. */
export function respetaReduccion(reduce: boolean, ms: number): number {
  return reduce ? 0 : ms;
}
