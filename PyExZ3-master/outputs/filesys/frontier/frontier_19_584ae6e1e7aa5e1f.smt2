(set-logic ALL)
; Frontier Constraint ID: 584ae6e1e7aa5e1f
; Generated at: 2026-04-17 02:53:43
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 2539)) (False)
(assert (not (= x 2539)))

; Query: ((== x 2540)) (False)
(assert (not (not (= x 2540))))

(check-sat)
(get-model)
