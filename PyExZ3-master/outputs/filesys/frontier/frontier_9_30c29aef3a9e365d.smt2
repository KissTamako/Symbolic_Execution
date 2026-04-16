(set-logic ALL)
; Frontier Constraint ID: 30c29aef3a9e365d
; Generated at: 2026-04-16 15:56:50
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1624)) (False)
(assert (not (= x 1624)))

; Query: ((== x 1625)) (False)
(assert (not (not (= x 1625))))

(check-sat)
(get-model)
