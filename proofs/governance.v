(* PROJECT AEGIS: Formal Verification of Governance Logic *)
(* Sprint 21: Machine-Checked Proof of Safety *)

Require Import Bool.

(* 1. Define Types *)
Inductive Tier :=
  | Green
  | Yellow
  | Red.

Inductive AssetCrit :=
  | Low
  | Critical.

(* 2. Define State Variables *)
Record State := mkState {
  action_tier : Tier;
  target_crit : AssetCrit;
  twin_test_passed : bool;
  human_approval : bool
}.

(* 3. Define the O-SAFE Policy Function *)
(* Returns true if authorized, false otherwise *)
Definition is_authorized (s : State) : bool :=
  match s.(action_tier), s.(target_crit) with
  | Green, _ => true
  | Yellow, _ => true
  | Red, Low => true
  | Red, Critical => s.(twin_test_passed) || s.(human_approval)
  end.

(* 4. THE THEOREM (The Iron Rule) *)
(* "It is impossible to authorize a Red action on a Critical asset 
    if both Twin Test and Human Approval are missing." *)
Theorem iron_rule_safety : 
  forall s : State,
  s.(action_tier) = Red ->
  s.(target_crit) = Critical ->
  s.(twin_test_passed) = false ->
  s.(human_approval) = false ->
  is_authorized s = false.

Proof.
  intros s Htier Hcrit Htwin Hhuman.
  unfold is_authorized.
  rewrite Htier.
  rewrite Hcrit.
  rewrite Htwin.
  rewrite Hhuman.
  (* The expression becomes 'false || false' which is false *)
  simpl.
  reflexivity.
Qed.

(* Success: The proof is complete. *)
