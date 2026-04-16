(set-logic ALL)
; Constraint ID: 7db21d41c5f4fb9e
; Generated at: 2026-04-16 11:14:00
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59848)) (False)
(assert (not (= x 59848)))

; Query: ((== x 59849)) (False)
(assert (not (not (= x 59849))))

(check-sat)
(get-model)
