(set-logic ALL)
; Constraint ID: ceaa237e7e3469f1
; Generated at: 2026-04-16 11:40:22
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60169)) (False)
(assert (not (= x 60169)))

; Query: ((== x 60170)) (False)
(assert (not (not (= x 60170))))

(check-sat)
(get-model)
