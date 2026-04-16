(set-logic ALL)
; Constraint ID: 4bc91b652b1f2273
; Generated at: 2026-04-16 11:52:16
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60511)) (False)
(assert (not (= x 60511)))

; Query: ((== x 60512)) (False)
(assert (not (not (= x 60512))))

(check-sat)
(get-model)
