(set-logic ALL)
; Constraint ID: 7f2e0922c4c87336
; Generated at: 2026-04-16 10:43:23
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59467)) (False)
(assert (not (= x 59467)))

; Query: ((== x 59468)) (False)
(assert (not (not (= x 59468))))

(check-sat)
(get-model)
