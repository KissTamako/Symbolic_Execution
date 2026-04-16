(set-logic ALL)
; Frontier Constraint ID: 578c96baa0974c19
; Generated at: 2026-04-16 14:42:45
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 595)) (False)
(assert (not (= x 595)))

; Query: ((== x 596)) (False)
(assert (not (not (= x 596))))

(check-sat)
(get-model)
