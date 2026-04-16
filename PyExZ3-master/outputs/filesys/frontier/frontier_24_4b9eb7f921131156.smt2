(set-logic ALL)
; Frontier Constraint ID: 4b9eb7f921131156
; Generated at: 2026-04-16 14:36:25
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 373)) (False)
(assert (not (not (= x 373))))

(check-sat)
(get-model)
